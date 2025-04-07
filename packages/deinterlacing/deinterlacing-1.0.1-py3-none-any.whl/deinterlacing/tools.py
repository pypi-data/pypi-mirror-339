import inspect
from collections.abc import Callable, Generator
from functools import wraps
from itertools import chain
from typing import Any, Literal, Protocol, TypeAlias

import numpy as np
from boltons.iterutils import chunk_ranges
from numpy.fft import fft as numpy_fft
from numpy.fft import ifft as numpy_ifft

try:
    import cupy as cp
except ImportError:
    cp = np
else:
    pass

__all__ = [
    "calculate_phase_offset",
    "extract_image_block",
    "index_image_blocks",
    "pixel_alignment",
    "subpixel_alignment",
]

#: Type alias for numpy array-like data structures.
NDArrayLike: TypeAlias = np.ndarray | cp.ndarray

#: Type alias for a generator of image blocks
ImageBlockGenerator: TypeAlias = Generator[tuple[int, int], None, None]


class FFTImplementation(Protocol):
    """
    A protocol for FFT/iFFT implementations that can be called with a numpy or cupy
    array. These functions should accept an array and an optional axis parameter, and
    return the transformed array of the same type (numpy or cupy). The axis parameters
    will be called as a keyword-argument, so the position of the axis argument in the
    implementation signature does not matter.
    """

    def __call__(self, a: NDArrayLike, axis: int, *args, **kwargs) -> NDArrayLike: ...


class ParameterError(ValueError):
    """Custom exception for parameter validation errors in deinterlacing."""

    def __init__(self, parameter: str, value: Any, limits: tuple[Any, Any]) -> None:
        self.value = value
        self.limits = limits
        message = (
            f"Parameter '{parameter}' with value {value} is "
            f"not within the appropriate bounds {limits}."
        )
        super().__init__(message)


def calculate_phase_offset(
    images: NDArrayLike,
    subsearch: int | None = None,
    fft_implementation: FFTImplementation = numpy_fft,
    ifft_implementation: FFTImplementation = numpy_ifft,
) -> int:
    """
    Calculate the phase offset between forward and backward scanned lines in resonance
    scanning microscopy images using the cross-power spectral density method. This
    function computes the Fourier transform of the forward and backward scanned lines,
    calculates the cross-power spectral density, and finds the peak in the inverse
    Fourier transform to determine the sub-pixel offset. The result is the integer
    number of pixels by which the backward scanned lines should be shifted to align
    with the forward scanned lines.

    :param images: (frames, y-pixels, x-pixels)
    :param subsearch: The number of pixels to search through
    :param fft_implementation: The FFT implementation to use
    :param ifft_implementation: The ifft implementation to use
    :returns: The integer phase offset (in pixels) to align the backward scanned lines
    """
    # offset
    OFFSET = 1e-5  # noqa: N806

    forward = fft_implementation(images[..., 1::2, :], axis=-1)
    forward /= np.abs(forward) + OFFSET

    backward = fft_implementation(images[..., ::2, :], axis=-1)
    np.conj(backward, out=backward)
    backward /= np.abs(backward) + OFFSET
    backward = backward[:, : forward.shape[-2], ...]

    # inverse
    comp_conj = ifft_implementation(forward * backward, axis=-1)
    comp_conj = np.real(comp_conj)
    comp_conj = comp_conj.mean(axis=1).mean(axis=0)
    comp_conj = np.fft.fftshift(comp_conj)

    # search only subspace to save computation time and avoid any artifacts from edge
    # of image. extremely important!
    peak = np.argmax(
        comp_conj[-subsearch + images.shape[-2] // 2 : images.shape[-1] // 2]
        + subsearch
        + 1
    )

    # If the image is very sparse, the peak here could be determined by the statistics
    # of PMT noise, which is unrelated to scanning artifacts. To avoid this, we can
    # check if the second highest peak is significantly lower than the zeroth peak in
    # the case that the calculated phase offset is 0

    if peak == subsearch:
        # argpart is log(n) complexity, so it is faster than sorting the entire array
        pk0, pk1 = np.argpartition(
            -comp_conj[-subsearch + images.shape[-2] // 2 : images.shape[-1] // 2]
            + subsearch
            + 1,
            2,
        )[:2]
        # If peak is +/- 1 from the first peak, it is likely not genuine
        if (new_peak := pk1) - pk0 != 1:
            peak = new_peak
    return -(peak - subsearch)


def extract_image_block(
    images: NDArrayLike,
    start: int,
    stop: int,
    subsample: Literal["mean", "median", "std", "sum", None],
) -> NDArrayLike:
    image_block = images[start:stop, ...]
    if subsample == "mean":
        return image_block.mean(axis=0).astype(images.dtype)
    if subsample == "median":
        return np.median(image_block, axis=0).astype(images.dtype)
    if subsample == "std":
        return image_block.std(axis=0, ddof=1).astype(images.dtype)
    if subsample == "sum":
        return image_block.sum(axis=0).astype(images.dtype)
    return image_block


def index_image_blocks(
    images: NDArrayLike,
    block_size: int,
    unstable: int | None = None,
) -> tuple[int, ImageBlockGenerator]:
    """
    Index the image blocks for batch processing during deinterlacing. This function
    returns the number of blocks and a generator yielding tuples of start and end
    indices for each block of images to be processed. It takes into account the
    `unstable` parameter, which specifies how many frames should be processed
    individually before switching to batch-wise processing.

    :param images:
    :param block_size:
    :param unstable:
    :returns: The number of blocks and a generator yielding tuples of
        (start_index, end_index) for each block.
    """
    if unstable:
        stable_frames = images.shape[0] - unstable
        num_blocks = (
            unstable
            + stable_frames // block_size
            + bool(stable_frames % block_size) * 1
        )
        blocks = chain(
            chunk_ranges(unstable, 1),
            chunk_ranges(stable_frames, block_size, input_offset=unstable),
        )
    else:
        num_blocks = (
            images.shape[0] // block_size + bool(images.shape[0] % block_size) * 1
        )
        blocks = chunk_ranges(images.shape[0], block_size)

    return num_blocks, blocks


def pixel_alignment(
    images: NDArrayLike, start: int, stop: int, phase_offset: int
) -> None:
    if phase_offset > 0:
        images[start:stop, 1::2, phase_offset:] = images[
            start:stop, 1::2, :-phase_offset
        ]
    elif phase_offset < 0:
        images[start:stop, 1::2, :phase_offset] = images[
            start:stop, 1::2, -phase_offset:
        ]


def subpixel_alignment(
    images: NDArrayLike, start: int, stop: int, phase_offset: int
) -> None:
    _ = images
    _ = start
    _ = stop
    _ = phase_offset
    msg = "Not Implemented Yet"
    raise NotImplementedError(msg)
    # TODO: Implement subpixel alignment


def wrap_cupy(
    function: Callable[[cp.ndarray], cp.ndarray], *parameter: str
) -> Callable[[np.ndarray], np.ndarray]:
    """
    Convenience decorator that wraps a CuPy function such that incoming numpy arrays
    are converted to cupy arrays and swapped back on return.

    :param function: any CuPy function that accepts a CuPy array
    :param parameter: name/s of the parameter to be converted
    :returns: wrapped function
    """

    @wraps(function)
    def decorator(*args, **kwargs) -> Callable[[np.ndarray], np.ndarray]:
        sig = inspect.signature(function)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        bound_args.arguments = {**bound_args.kwargs, **bound_args.arguments}
        for param in parameter:
            # noinspection PyUnresolvedReferences
            bound_args.arguments[param] = cp.asarray(bound_args.arguments[param])
        return function(**bound_args.arguments).get()

    # noinspection PyTypeChecker
    return decorator
