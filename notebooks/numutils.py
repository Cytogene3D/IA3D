
import numpy as np


def _logbins_numba(lo, hi, ratio=0, N=0, prepend_zero=False):
    """Make bins with edges evenly spaced in log-space.

    Parameters
    ----------
    lo, hi : int
        The span of the bins.
    ratio : float
        The target ratio between the upper and the lower edge of each bin.
        Either ratio or N must be specified.
    N : int
        The target number of bins. The resulting number of bins is not guaranteed.
        Either ratio or N must be specified.

    """
    lo = int(lo)
    hi = int(hi)
    if ratio != 0:
        if N != 0:
            raise ValueError("Please specify N or ratio")
        N = np.log(hi / lo) / np.log(ratio)
    elif N == 0:
        raise ValueError("Please specify N or ratio")
    data10 = 10 ** np.linspace(np.log10(lo), np.log10(hi), int(N))
    data10 = np.rint(data10)
    data10_int = np.sort(np.unique(data10)).astype(np.int_)
    assert data10_int[0] == lo
    assert data10_int[-1] == hi
    if prepend_zero:
        data10_int = np.concatenate((np.array([0]), data10_int))
    return data10_int


def observed_over_expected(
    matrix, mask=np.empty(shape=(0), dtype=np.bool_), dist_bin_edge_ratio=1.03
):
    """
    Normalize the contact matrix for distance-dependent contact decay.
    The diagonals of the matrix, corresponding to contacts between loci pairs
    with a fixed distance, are grouped into exponentially growing bins of
    distances; the diagonals from each bin are normalized by their average value.

    Parameters
    ----------
    matrix : np.ndarray
        A 2D symmetric matrix of contact frequencies.
    mask : np.ndarray
        A 1D or 2D mask of valid data.
        If 1D, it is interpreted as a mask of "good" bins.
        If 2D, it is interpreted as a mask of "good" pixels.
    dist_bin_edge_ratio : float
        The ratio of the largest and the shortest distance in each distance bin.

    Returns
    -------
    OE : np.ndarray
        The diagonal-normalized matrix of contact frequencies.
    dist_bins : np.ndarray
        The edges of the distance bins used to calculate average
        distance-dependent contact frequency.
    sum_pixels : np.ndarray
        The sum of contact frequencies in each distance bin.
    n_pixels : np.ndarray
        The total number of valid pixels in each distance bin.

    """
    N = matrix.shape[0]

    mask2d = np.empty(shape=(0, 0), dtype=np.bool_)
    if mask.ndim == 1:
        if mask.size > 0:
            mask2d = mask.reshape((1, -1)) * mask.reshape((-1, 1))
    elif mask.ndim == 2:
        # Numba expects mask to be a 1d array, so we need to hint
        # that it is now a 2d array
        mask2d = mask.reshape((int(np.sqrt(mask.size)), int(np.sqrt(mask.size))))
    else:
        raise ValueError("The mask must be either 1D or 2D.")

    data = np.copy(matrix).astype(np.float64)

    has_mask = mask2d.size > 0
    dist_bins = _logbins_numba(1, N, dist_bin_edge_ratio)
    dist_bins = np.concatenate((np.array([0]), dist_bins))
    n_pixels_arr = np.zeros_like(dist_bins[1:])
    sum_pixels_arr = np.zeros_like(dist_bins[1:], dtype=np.float64)

    bin_idx, n_pixels, sum_pixels = 0, 0, 0

    for bin_idx, lo, hi in zip(
        range(len(dist_bins) - 1), dist_bins[:-1], dist_bins[1:]
    ):
        sum_pixels = 0
        n_pixels = 0
        for offset in range(lo, hi):
            for j in range(0, N - offset):
                if not has_mask or mask2d[offset + j, j]:
                    sum_pixels += data[offset + j, j]
                    n_pixels += 1

        n_pixels_arr[bin_idx] = n_pixels
        sum_pixels_arr[bin_idx] = sum_pixels

        if n_pixels == 0:
            continue
        mean_pixel = sum_pixels / n_pixels
        if mean_pixel == 0:
            continue

        for offset in range(lo, hi):
            for j in range(0, N - offset):
                if not has_mask or mask2d[offset + j, j]:

                    data[offset + j, j] /= mean_pixel
                    if offset > 0:
                        data[j, offset + j] /= mean_pixel

    return data, dist_bins, sum_pixels_arr, n_pixels_arr


def adaptive_coarsegrain(ar, countar, cutoff=5, max_levels=8, min_shape=8):
    """
    Adaptively coarsegrain a Hi-C matrix based on local neighborhood pooling
    of counts.

    Parameters
    ----------
    ar : array_like, shape (n, n)
        A square Hi-C matrix to coarsegrain. Usually this would be a balanced
        matrix.

    countar : array_like, shape (n, n)
        The raw count matrix for the same area. Has to be the same shape as the
        Hi-C matrix.

    cutoff : float, optional
        A minimum number of raw counts per pixel required to stop 2x2 pooling.
        Larger cutoff values would lead to a more coarse-grained, but smoother
        map. 3 is a good default value for display purposes, could be lowered
        to 1 or 2 to make the map less pixelated. Setting it to 1 will only
        ensure there are no zeros in the map.

    max_levels : int, optional
        How many levels of coarsening to perform. It is safe to keep this
        number large as very coarsened map will have large counts and no
        substitutions would be made at coarser levels.
    min_shape : int, optional
        Stop coarsegraining when coarsegrained array shape is less than that.

    Returns
    -------
    Smoothed array, shape (n, n)

    Notes
    -----
    The algorithm works as follows:

    First, it pads an array with NaNs to the nearest power of two. Second, it
    coarsens the array in powers of two until the size is less than minshape.

    Third, it starts with the most coarsened array, and goes one level up.
    It looks at all 4 pixels that make each pixel in the second-to-last
    coarsened array. If the raw counts for any valid (non-NaN) pixel are less
    than ``cutoff``, it replaces the values of the valid (4 or less) pixels
    with the NaN-aware average. It is then applied to the next
    (less coarsened) level until it reaches the original resolution.

    In the resulting matrix, there are guaranteed to be no zeros, unless very
    large zero-only areas were provided such that zeros were produced
    ``max_levels`` times when coarsening.

    Examples
    --------
    >>> c = cooler.Cooler("/path/to/some/cooler/at/about/2000bp/resolution")

    >>> # sample region of about 6000x6000
    >>> mat = c.matrix(balance=True).fetch("chr1:10000000-22000000")
    >>> mat_raw = c.matrix(balance=False).fetch("chr1:10000000-22000000")
    >>> mat_cg = adaptive_coarsegrain(mat, mat_raw)

    >>> plt.figure(figsize=(16,7))
    >>> ax = plt.subplot(121)
    >>> plt.imshow(np.log(mat), vmax=-3)
    >>> plt.colorbar()
    >>> plt.subplot(122, sharex=ax, sharey=ax)
    >>> plt.imshow(np.log(mat_cg), vmax=-3)
    >>> plt.colorbar()

    """

    def _coarsen(ar, operation=np.sum):
        """Coarsegrains an array by a factor of 2"""
        M = ar.shape[0] // 2
        newar = np.reshape(ar, (M, 2, M, 2))
        cg = operation(newar, axis=1)
        cg = operation(cg, axis=2)
        return cg

    def _expand(ar, counts=None):
        """
        Performs an inverse of nancoarsen
        """
        N = ar.shape[0] * 2
        newar = np.zeros((N, N))
        newar[::2, ::2] = ar
        newar[1::2, ::2] = ar
        newar[::2, 1::2] = ar
        newar[1::2, 1::2] = ar
        return newar

    # defining arrays, making sure they are floats
    ar = np.asarray(ar, float)
    countar = np.asarray(countar, float)

    # TODO: change this to the nearest shape correctly counting the smallest
    # shape the algorithm will reach
    Norig = ar.shape[0]
    Nlog = np.log2(Norig)
    if not np.allclose(Nlog, np.rint(Nlog)):
        newN = int(2 ** np.ceil(Nlog))  # next power-of-two sized matrix
        newar = np.empty((newN, newN), dtype=float)  # fitting things in there
        newar[:] = np.nan
        newcountar = np.zeros((newN, newN), dtype=float)
        newar[:Norig, :Norig] = ar
        newcountar[:Norig, :Norig] = countar
        ar = newar
        countar = newcountar

    armask = np.isfinite(ar)  # mask of "valid" elements
    countar[~armask] = 0
    ar[~armask] = 0

    assert np.isfinite(countar).all()
    assert countar.shape == ar.shape

    # We will be working with three arrays.
    ar_cg = [ar]  # actual Hi-C data
    countar_cg = [countar]  # counts contributing to Hi-C data (raw Hi-C reads)
    armask_cg = [armask]  # mask of "valid" pixels of the heatmap

    # 1. Forward pass: coarsegrain all 3 arrays
    for i in range(max_levels):
        if countar_cg[-1].shape[0] > min_shape:
            countar_cg.append(_coarsen(countar_cg[-1]))
            armask_cg.append(_coarsen(armask_cg[-1]))
            ar_cg.append(_coarsen(ar_cg[-1]))

    # Get the most coarsegrained array
    ar_cur = ar_cg.pop()
    countar_cur = countar_cg.pop()
    armask_cur = armask_cg.pop()

    # 2. Reverse pass: replace values starting with most coarsegrained array
    # We have 4 pixels that were coarsegrained to one pixel.
    # Let V be the array of values (ar), and C be the array of counts of
    # valid pixels. Then the coarsegrained values and valid pixel counts
    # are:
    # V_{cg} = V_{0,0} + V_{0,1} + V_{1,0} + V_{1,1}
    # C_{cg} = C_{0,0} + C_{0,1} + C_{1,0} + C_{1,1}
    # The average value at the coarser level is V_{cg} / C_{cg}
    # The average value at the finer level is V_{0,0} / C_{0,0}, etc.
    #
    # We would replace 4 values with the average if counts for either of the
    # 4 values are less than cutoff. To this end, we perform nanmin of raw
    # Hi-C counts in each 4 pixels
    # Because if counts are 0 due to this pixel being invalid - it's fine.
    # But if they are 0 in a valid pixel - we replace this pixel.
    # If we decide to replace the current 2x2 square with coarsegrained
    # values, we need to make it produce the same average value
    # To this end, we would replace V_{0,0} with V_{cg} * C_{0,0} / C_{cg} and
    # so on.
    for i in range(len(countar_cg)):
        ar_next = ar_cg.pop()
        countar_next = countar_cg.pop()
        armask_next = armask_cg.pop()

        # obtain current "average" value by dividing sum by the # of valid pixels
        val_cur = ar_cur / armask_cur
        # expand it so that it is the same shape as the previous level
        val_exp = _expand(val_cur)
        # create array of substitutions: multiply average value by counts
        addar_exp = val_exp * armask_next

        # make a copy of the raw Hi-C array at current level
        countar_next_mask = np.array(countar_next)
        countar_next_mask[armask_next == 0] = np.nan  # fill nans
        countar_exp = _expand(_coarsen(countar_next, operation=np.nanmin))

        curmask = countar_exp < cutoff  # replacement mask
        ar_next[curmask] = addar_exp[curmask]  # procedure of replacement
        ar_next[armask_next == 0] = 0  # now setting zeros at invalid pixels

        # prepare for the next level
        ar_cur = ar_next
        countar_cur = countar_next
        armask_cur = armask_next

    ar_next[armask_next == 0] = np.nan
    ar_next = ar_next[:Norig, :Norig]

    return ar_next
