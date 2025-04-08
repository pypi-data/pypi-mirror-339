import numpy as np
from lazylinop.wip.butterfly import dft_square_dyadic_ks_values, fuse
from lazylinop.wip.butterfly import ksm


def dft(p: int, n_factors: int, backend: str = 'numpy',
        strategy: str = 'l2r', dtype: str = 'complex64'):
    r"""
    Return a :class:`LazyLinOp` `L` corresponding to
    the Discrete-Fourier-Transform.

    Shape of ``L`` is $\left(2^m,~2^m\right)$.

    Args:
        p: ``int``
            Size of the DFT is a power of two $2^p$.
        n_factors: ``int``
            Number of factors ``n_factors <= m``.
            If ``n_factors = m``, return the square-dyadic decomposition.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        strategy: ``str``, optional
            It could be:

            - ``'l2r'`` fuse from left to right.
            - ``balanced`` fuse from left to right and right to left ($p>3$).

              - Case ``p = 6`` and ``n_factors = 2``:
                step 0: 0 1 2 3 4 5
                step 1: 01 2 3 45
                step 2: 012 345
              - Case ``p = 7`` and ``n_factors = 2``:
                step 0: 0 1 2 3 4 5 6
                step 1: 01 2 3 4 56
                step 2: 012 3 456
                step 3: 0123 456
              - Case ``p = 7`` and ``n_factors = 3``:
                step 0: 0 1 2 3 4 5 6
                step 1: 01 2 3 4 56
                step 2: 012 3 456
            - ``'memory'`` find the two consecutive ``ks_values`` that
              minimize the memory of the fused ``ks_values``.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the DFT.
    """
    if n_factors > p or n_factors < 1:
        raise ValueError("n_factors must be positive and less or equal to p.")
    if dtype != 'complex64' and dtype != 'complex128':
        raise Exception("dtype must be either 'complex64' or 'complex128'.")

    ks_values = dft_square_dyadic_ks_values(p, dtype=dtype)
    if p == n_factors:
        # Nothing to fuse.
        return ksm(ks_values, backend=backend)
    else:
        tmp = [None] * (p // 2 + p % 2)
        m, target = p, p
        if strategy == 'l2r':
            # Fuse from left to right (in-place modification of ks_values).
            while True:
                for i in range(0, m - m % 2 - 1, 2):
                    if target > n_factors:
                        ks_values[i // 2] = fuse(ks_values[i], ks_values[i + 1],
                                                 backend=backend)
                        target -= 1
                if target == n_factors:
                    break
                if m % 2 == 1:
                    ks_values[m // 2 + m % 2 - 1] = ks_values[m - 1]
                    # target -= 1
                if target == n_factors:
                    break
                m = m // 2 + m % 2
                target = m
            return ksm(ks_values[:n_factors], backend=backend)
        elif strategy == 'balanced':
            if p <= 3:
                raise Exception("strategy 'balanced' does not work when p <= 3.")
            # Fuse from left to right and from right to left.
            step = 0
            idx = [str(i) for i in range(p)]
            print(f"step={step}", idx)
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    idx[lpos + 1] = idx[lpos] + idx[lpos + 1]
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    idx[rpos - 1] = idx[rpos - 1] + idx[rpos]
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m / 2:
                    lpos, rpos = n_left, m - 1 - n_right
                print(f"step={step}", idx[n_left:(p - n_right)])
                step += 1
                if target == n_factors:
                    break
            # if n_left != n_right:
            #     raise Exception("Cannot fuse from left to right and right to left" +
            #                     " for the given values of p and n_factors.")
            m, target = p, p
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    ks_values[lpos + 1] = fuse(ks_values[lpos], ks_values[lpos + 1],
                                               backend=backend)
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    ks_values[rpos - 1] = fuse(ks_values[rpos - 1], ks_values[rpos],
                                               backend=backend)
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m // 2:
                    lpos, rpos = n_left, m - 1 - n_right
                if target == n_factors:
                    break
            return ksm(ks_values[n_left:(n_left + n_factors)], backend=backend)
        elif strategy == 'memory':
            step = 0
            idx = [str(i) for i in range(p)]
            print(f"step={step}", idx)
            n_fuses = 0
            while True:
                # Build memory list.
                memory = np.full(p - n_fuses - 1, 0)
                for i in range(p - n_fuses - 1):
                    a1, b1, c1, d1 = ks_values[i].shape
                    a2, b2, c2, d2 = ks_values[i + 1].shape
                    memory[i] = a1 * ((b1 * d1) // d2) * ((a2 * c2) // a1) * d2
                # Find argmin.
                argmin = np.argmin(memory)
                # Fuse argmin and argmin + 1.
                ks_values[argmin] = fuse(ks_values[argmin], ks_values[argmin + 1],
                                         backend=backend)
                idx[argmin] = idx[argmin] + idx[argmin + 1]
                n_fuses += 1
                # Delete argmin + 1.
                ks_values.pop(argmin + 1)
                idx.pop(argmin + 1)
                target -= 1
                print(f"step={step}", idx)
                step += 1
                if target == n_factors:
                    break
            return ksm(ks_values, backend=backend)
        else:
            raise Exception("strategy must be either 'l2r', 'balanced' or 'memory'.")
