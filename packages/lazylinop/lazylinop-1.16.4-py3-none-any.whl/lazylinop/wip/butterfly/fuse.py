import numpy as np
from lazylinop.wip.butterfly import ksm
from lazylinop.signal import fft


def dft_square_dyadic_ks_values(p: int, dense: bool=False,
                                dtype: str='complex64'):
    r"""
    Return a list of ``ks_values`` that corresponds
    to the ``F @ P.T`` matrix decomposition into ``p`` factors,
    where ``F`` is the DFT matrix and ``P`` the bit-reversal permutation matrix.
    The size $2^p$ of the DFT is a power of $2$.

    Args:
        p: ``int``
            DFT of size $2^p$.
        dense: ``bool``, optional
            If ``dense=True`` compute and return
            2d representation of the factors.
            Default value is ``False``.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        List of 4d ``np.ndarray`` corresponding to ``ks_values``.
        If ``dense=True`` it also returns a list of
        2d ``np.ndarray`` corresponding to the ``p`` factors.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import dft_square_dyadic_ks_values
        >>> from lazylinop.wip.butterfly import ksm
        >>> from lazylinop.signal import fft
        >>> from lazylinop.basicops import bitrev
        >>> p = 10
        >>> N = 2 ** p
        >>> ks_values = dft_square_dyadic_ks_values(p)
        >>> x = np.random.randn(N)
        >>> L = ksm(ks_values, backend='scipy')
        >>> P = bitrev(N)
        >>> np.allclose(fft(N) @ x, L @ P @ x)
        True
    """
    inv_sqrt2 = 1.0 / np.sqrt(2.0)
    N = 2 ** p
    if dense:
        factors = [None] * p
    ks_values = [None] * p
    for n in range(p):
        if n == (p - 1):
            f2 = (fft(2) @ np.eye(2)).astype(dtype)
            if dense:
                factors[n] = np.kron(np.eye(N // 2, dtype=dtype), f2)
            a = N // 2
            b, c = 2, 2
            d = 1
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            for i in range(a):
                ks_values[n][i, :, :, 0] = f2
        else:
            s = N // 2 ** (p - n)
            t = N // 2 ** (n + 1)
            w = np.exp(2.0j * np.pi / (2 * t))
            omega = (w ** (-np.arange(t))).astype(dtype)
            if dense:
                diag_omega = np.diag(omega)
                factors[n] = np.kron(
                    np.eye(s, dtype=dtype) * inv_sqrt2,
                    np.vstack((
                        np.hstack((np.eye(t, dtype=dtype), diag_omega)),
                        np.hstack((np.eye(t, dtype=dtype), -diag_omega)))))
            a = s
            b, c = 2, 2
            d = t
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            # Map between 2d and 4d representations.
            # col = i * c * d + k * d + l
            # row = i * b * d + j * d + l
            # Loop over the a blocks.
            for i in range(a):
                for u in range(t):
                    for v in range(4):
                        if v == 0:
                            # Identity.
                            sub_col = u
                            sub_row = u
                            tmp = inv_sqrt2
                        elif v == 1:
                            # diag(omega).
                            sub_col = u + t
                            sub_row = u
                            tmp = omega[u] * inv_sqrt2
                        elif v == 2:
                            # Identity.
                            sub_col = u
                            sub_row = u + t
                            tmp = inv_sqrt2
                        else:
                            # -diag(omega)
                            sub_col = u + t
                            sub_row = u + t
                            tmp = -omega[u] * inv_sqrt2
                        j = sub_row // d
                        k = sub_col // d
                        l = sub_col - k * d
                        ks_values[n][i, j, k, l] = tmp
    if dense:
        return ks_values, factors
    else:
        return ks_values


def fuse(ks_values1: np.ndarray, ks_values2: np.ndarray,
         backend: str = 'numpy'):
    r"""
    Fuse two ``ks_values`` of shape $\left(a_1,~b_1,~c_1,~d_1\right)$
    and $\left(a_2,~b_2,~c_2,~d_2\right)$.
    The shape of the resulting ``ks_values`` is
    $\left(a_1,~\frac{b_1d_1}{d_2},~\frac{a_2c_2}{a_1},~d_2\right)$.

    Args:
        ks_values1: ``np.ndarray``
            First ``ks_values`` of shape $\left(a_1,~b_1,~c_1,~d_1\right)$.
        ks_values2: ``np.ndarray``
            Second ``ks_values`` of shape $\left(a_2,~b_2,~c_2,~d_2\right)$.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            Use ``backend`` to fuse the two ``ks_values``.
            See :py:func:`ksm` for more details.

    Returns:
        The resulting ``ks_values`` is a ``np.ndarray``
        of shape $\left(a_1,~\frac{b_1d_1}{d_2},~\frac{a_2c_2}{a_1},~d_2\right)$.

    .. seealso::
        - :py:func:`ksm`.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.butterfly import ksm, fuse
        >>> a1, b1, c1, d1 = 2, 2, 2, 4
        >>> a2, b2, c2, d2 = 4, 2, 2, 2
        >>> v1 = np.random.randn(a1, b1, c1, d1)
        >>> v2 = np.random.randn(a2, b2, c2, d2)
        >>> v = fuse(v1, v2)
        >>> v.shape
        (2, 4, 4, 2)
        >>> L = ksm(v)
        >>> L1 = ksm(v1)
        >>> L2 = ksm(v2)
        >>> x = np.random.randn(L.shape[1])
        >>> np.allclose(L @ x, L1 @ L2 @ x)
        True
    """
    a1, b1, c1, d1 = ks_values1.shape
    a2, b2, c2, d2 = ks_values2.shape
    a, b, c, d = a1, (b1 * d1) // d2, (a2 * c2) // a1, d2
    dtype = (ks_values1[0, 0, 0, :1] * ks_values2[0, 0, 0, :1]).dtype
    ks_values = np.zeros((a, b, c, d), dtype=dtype)
    # Define two ksm from the two ks_values.
    L1 = ksm(ks_values1, backend=backend)
    L2 = ksm(ks_values2, backend=backend)
    in2 = L2.shape[1]
    # Compute dense representation of L1 @ L2.
    x = np.zeros(in2, dtype=dtype)
    for col in range(in2):
        x[col] = 1.0
        y = L1 @ (L2 @ x)
        x[col] = 0.0
        # Map between 2d and 4d representations.
        # col = i * c * d + k * d + l
        # row = i * b * d + j * d + l
        # Find i, k and l from col value.
        i = col // (c * d)
        k = (col - i * c * d) // d
        l = col - i * c * d - k * d
        # Inside the current block.
        # Find i, j and l from row value.
        row = np.arange(i * c * d, (i + 1) * c * d, 1)
        j = (row - i * b * d) // d
        ll = row - i * b * d - j * d
        idx = np.where(l == ll)[0]
        ks_values[i, j[idx], k, ll[idx]] = y[row[idx]]
        # for row in range(i * c * d, (i + 1) * c * d, 1):
        # # for row in range(y.shape[0]):
        #     # Find i, j and l from row value.
        #     # Check if the indices are coherents.
        #     j = (row - i * b * d) // d
        #     # if i == row // (b * d) and l == row - i * b * d - j * d:
        #     if l == row - i * b * d - j * d:
        #         ks_values[i, j, k, l] = y[row]
    return ks_values
