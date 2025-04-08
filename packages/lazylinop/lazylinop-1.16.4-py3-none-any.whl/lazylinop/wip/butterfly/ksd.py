# -*- coding: utf-8 -*-

from lazylinop import aslazylinop, islazylinop, LazyLinOp
from lazylinop.basicops import eye
from lazylinop.wip.butterfly.GB_factorization import GBfactorize
from lazylinop.wip.butterfly.GB_operators import twiddle_to_dense
from lazylinop.wip.butterfly.GB_param_generate import DebflyGen
from lazylinop.wip.butterfly.ksm import ksm, _find_hyper_parameters
from lazylinop.wip.butterfly.ksm import ksm, _context
from lazylinop.wip.butterfly import Chain
try:
    import pycuda.driver as cuda
    import pycuda._driver as _cuda
except:
    cuda, _cuda = None, None
try:
    import pyopencl as cl
except:
    cl = None
from scipy.sparse import csr_matrix
import numpy as np
try:
    import torch
except ModuleNotFoundError:
    # "Fake" torch
    class Torch():
        def __init__(self):
            self._Tensor = type(None)

        @property
        def Tensor(self):
            return self._Tensor

    torch = Torch()


def bitrev_perm(N):
    r"""
    Bitreversal permutation.

    Args:
        N: ``int``
            The size of the permutation, it must be a power of two.
            P dimensions will be N x N.

    Returns:
        A ``scipy.sparse.csr_matrix`` defining the bit-reversal permutation.

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/wiki/Bit-reversal_permutation>`_.
    """
    if np.log2(N) > np.log2(np.floor(N)):
        raise ValueError('N must be a power of two')
    row_inds = np.arange(0, N, dtype='int')
    col_inds = bitrev(row_inds)
    ones = np.ones((N), dtype='float')
    return csr_matrix((ones, (row_inds, col_inds)), shape=(N, N))


def bitrev(inds):
    r"""
    Bitreversal permutation.

    Args:
        inds: ``list[int]``
            The list of indices to bit-reverse.

    Returns:
        The bit-reversal permutation of inds.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly.ksd import bitrev
        >>> bitrev(np.arange(4))
        array([0, 2, 1, 3])

    .. seealso::
        `Wikipedia <https://en.wikipedia.org/wiki/Bit-reversal_permutation>`_.
    """
    n = len(inds)
    if n == 1:
        return inds
    else:
        even = bitrev(inds[np.arange(0, n, 2, dtype='int')])
        odd = bitrev(inds[np.arange(1, n, 2, dtype='int')])
        return np.hstack((even, odd))


def _balanced_permutation(k):
    if k == 1:
        return [1]
    elif k == 2:
        return [1, 2]
    if k % 2 == 0:
        left_perm = _balanced_permutation((k // 2) - 1)
        right_perm = [
            i + (k + 1) // 2 for i in _balanced_permutation(k // 2)]
        return [k // 2] + left_perm + right_perm
    elif k % 2 == 1:
        left_perm = _balanced_permutation(k // 2)
        right_perm = [
            i + (k + 1) // 2 for i in _balanced_permutation(k // 2)]
        return [k // 2 + 1] + left_perm + right_perm


def ksd(matrix: np.ndarray,
        chain: Chain,
        ortho: bool = True,
        order: str = 'l2r',
        svd_backend: str = 'numpy',
        **kwargs):
    r"""
    Returns a :class:`.LazyLinOp`
    corresponding to the (often called "butterfly") factorization of
    ``matrix`` into Kronecker-sparse factors with sparsity patterns
    determined by chainable instance ``chain`` of :py:class:`Chain`..

    ``L = ksd(...)`` returns a :class:`.LazyLinOp`
    corresponding to the factorization of ``matrix`` where
    ``L = ksm(...) @ ksm(...) @ ... @ ksm(...)``.

    .. note::

        ``L.ks_values`` returns the ``ks_values`` of the factorization
        (see :py:func:`ksm` for more details).

    To factorize the DFT matrix, please consider the following example:

    .. code-block:: python3

        M = 16
        # Build DFT matrix using lazylinop.signal.fft function.
        from lazylinop.signal import fft
        V = fft(M).toarray()
        # Use square-dyadic decomposition.
        chain = Chain(V.shape, 'square dyadic')
        # Multiply the DFT matrix with the bit-reversal permutation matrix.
        from lazylinop.basicops import bitrev
        P = bitrev(M)
        L = ksd(V @ P.T, chain=chain, backend='scipy')

    We can draw the square-dyadic decomposition:

    .. image:: _static/dft_16x16_square_dyadic.svg

    Args:
        matrix: ``np.ndarray``
            Matrix to factorize.
        chain: ``Chain``
            Chainable instance of the ``Chain`` class.
            See :class:`.Chain` documentation for more details.
        ortho: ``bool``, optional
            Whether to use orthonormalisation or not during
            the algorithm, see :ref:`[1] <ksd>` for more details.
            Default is ``True``.
        order: ``str``, optional
            Determines in which order partial factorizations
            are performed, see :ref:`[1] <ksd>` for more details.

            - ``'l2r'`` Left-to-right decomposition (default).
            - ``'balanced'``
        svd_backend: ``str``, optional
            Use NumPy ``'numpy'`` (default) or PyTorch ``'pytorch'``
            to compute SVD and QR decompositions needed during the
            factorization process. Use ``'scipy'`` to compute partial SVD.
            The performances between ``'scipy'`` backend and the others
            depend on the size of ``matrix``.

    Kwargs:
        Additional arguments ``backend``,
        ``params`` (one per pattern) to pass to :func:`ksm`.

    Returns:
        ``L`` is a :class:`.LazyLinOp`
        that corresponds to the product of ``n_patterns``
        :class:`.LazyLinOp` each one returned by :func:`ksm`.

    .. seealso::
        - :class:`.Chain`,
        - :func:`ksm`.

    .. _ksd:

        **References:**

        [1] Butterfly Factorization with Error Guarantees.
        Léon Zheng, Quoc-Tung Le, Elisa Riccietti, and Rémi Gribonval
        https://hal.science/hal-04763712v1/document

    Examples:
        >>> import numpy as np
        >>> from lazylinop import aslazylinop
        >>> from lazylinop.wip.butterfly import bitrev_perm, Chain, ksd
        >>> from lazylinop.signal import fft
        >>> N = 2 ** 8
        >>> M = N
        >>> n_factors = 2
        >>> V = fft(M).toarray()
        >>> chain = Chain(V.shape, 'smallest monotone', n_factors)
        >>> # Use bit reversal permutations matrix.
        >>> P = bitrev_perm(N)
        >>> F = ksd(V @ P.T, chain)
        >>> F = F @ P
        >>> approx = F.toarray()
        >>> error = np.linalg.norm(V - approx) / np.linalg.norm(V)
        >>> np.allclose(error, 0.0)
        True
    """

    # Rank of sub-blocks (1 is default), used by the underlying SVD.
    rank = chain._rank  # 1 # ???

    if chain.n_patterns < 2:
        raise ValueError("n_patterns must be > 1.")

    shape = matrix.shape

    if 'backend' not in kwargs.keys():
        kwargs['backend'] = 'numpy'
    if 'params' not in kwargs.keys():
        kwargs['params'] = [(None, None)] * chain.n_patterns
    else:
        if not isinstance(kwargs['params'], list):
            raise Exception("params must be a list of tuple.")
        n_factors = len(kwargs['params'])
        if n_factors != chain.n_patterns:
            raise Exception("Length of kwargs['params'] must be" +
                            " equal to chain.n_patterns.")
        for i in range(n_factors):
            if not isinstance(kwargs['params'][i], tuple):
                raise Exception("params must be a list of tuple.")

    nrows, ncols = shape[0], shape[1]
    if nrows <= rank or ncols <= rank:
        raise Exception("Number of rows and number of columns must" +
                        " be greater than the rank value.")
    if isinstance(matrix, np.ndarray) and (svd_backend != 'numpy' and
                                           svd_backend != 'scipy'):
        raise Exception("Because svd_backend='numpy' or 'scipy'" +
                        " matrix must be a NumPy array.")
    if type(matrix).__name__ == 'Torch' and svd_backend != 'pytorch':
        raise Exception("Because ``svd_backend='pytorch'`` matrix" +
                        " must be a PyTorch tensor.")

    matrix = matrix.reshape(1, 1, nrows, ncols)

    # Set architecture for butterfly factorization.
    if chain._chain_type == "custom":
        min_param = chain.ks_patterns
    elif chain._chain_type == "square dyadic":
        min_param = chain.ks_patterns
    elif chain._chain_type == "random":
        context, context_idx = _context(kwargs['backend'])
        if context is None:
            min_param = chain.ks_patterns
        else:
            # Get maximum shared memory before to determine hyper-parameters.
            if cuda is not None and \
               _cuda is not None and isinstance(context, cuda.Context):
                smem = context.get_device().get_attribute(
                    _cuda.device_attribute.MAX_SHARED_MEMORY_PER_BLOCK
                )
                max_block_dim = (
                    context.get_device().get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_X),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_Y),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_BLOCK_DIM_Z))
                max_grid_dim = (
                    context.get_device().get_attribute(cuda.device_attribute.MAX_GRID_DIM_X),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_GRID_DIM_Y),
                    context.get_device().get_attribute(cuda.device_attribute.MAX_GRID_DIM_Z))
            elif cl is not None:
                smem = context.devices[0].get_info(
                    cl.device_info.LOCAL_MEM_SIZE)
                max_block_dim = None
                max_grid_dim = None
            else:
                smem = 49152
                max_block_dim = None
                max_grid_dim = None
            # Find a chain such that hyper-parameters are
            # found for all the factors.
            new_chain = chain
            for t in range(10000):
                tmp = new_chain.ks_patterns
                # print('r', tmp)
                failed = False
                for i in range(new_chain.n_patterns):
                    a, b, c, d = tmp[i]
                    # Check if we find hyper-parameters for the current factor.
                    hp = _find_hyper_parameters(a, b, c, d, 1,
                                                smem, matrix.dtype.itemsize,
                                                max_block_dim=max_block_dim,
                                                max_grid_dim=max_grid_dim)
                    if hp == [0] * 6:
                        # print('failed', a, b, c, d)
                        failed = True
                        break
                    rhp = _find_hyper_parameters(a, c, b, d, 1,
                                                 smem, matrix.dtype.itemsize,
                                                 max_block_dim=max_block_dim,
                                                 max_grid_dim=max_grid_dim)
                    if rhp == [0] * 6:
                        # print('rfailed', a, b, c, d)
                        failed = True
                        break
                if not failed:
                    min_param = new_chain.ks_patterns
                    break
                else:
                    new_chain = Chain(chain.shape,
                                      chain_type='random',
                                      n_patterns=chain.n_patterns)
            del context
    elif chain._chain_type == "smallest monotone":
        min_param = chain.ks_patterns
    elif chain._chain_type == "dft":
        min_param = chain.ks_patterns
    else:
        pass

    # Permutation.
    if order == "l2r":
        perm = [i for i in range(chain.n_patterns - 1)]
    elif order == "balanced":
        perm = [i - 1 for i in _balanced_permutation(chain.n_patterns - 1)]
    else:
        raise NotImplementedError("order must be either 'l2r' or 'balanced'")

    # FIXME: p, q compatibility
    if hasattr(chain, '_abcdpq'):
        min_param = chain._abcdpq
    else:
        tmp = []
        for i in range(len(min_param)):
            tmp.append((min_param[i][0], min_param[i][1],
                        min_param[i][2], min_param[i][3], 1, 1))
        min_param = tmp

    # Run factorization and return a list of factors.
    factor_list = GBfactorize(matrix, min_param,
                              perm, ortho,
                              backend=svd_backend)

    for i, f in enumerate(factor_list):
        # See GB_operators.twiddle_to_dense().
        a, d, b, c = f.factor.shape
        if isinstance(f.factor, torch.Tensor):
            factor_list[i] = (f.factor).permute(0, 2, 1, 3).permute(0, 1, 3, 2)
        elif isinstance(f.factor, np.ndarray):
            factor_list[i] = np.swapaxes(
                np.swapaxes((f.factor), 2, 1), 3, 2)
        else:
            pass

    L = ksm(factor_list,
            params=kwargs['params'], backend=kwargs['backend'])

    return L
