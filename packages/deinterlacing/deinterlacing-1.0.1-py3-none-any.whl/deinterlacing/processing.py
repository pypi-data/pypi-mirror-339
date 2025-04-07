import warnings
from functools import partial
from math import inf
from typing import Literal

import numpy as np
from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass
from tqdm import tqdm

from deinterlacing.tools import (
    NDArrayLike,
    ParameterError,
    calculate_phase_offset,
    extract_image_block,
    index_image_blocks,
    pixel_alignment,
    wrap_cupy,
)

try:
    import cupy as cp
except ImportError:
    cp = np
else:
    from cupy.fft import fft as cupy_fft
    from cupy.fft import ifft as cupy_ifft


__all__ = [
    "DeinterlaceParameters",
    "deinterlace",
]


@dataclass(slots=True)
class DeinterlaceParameters:
    #: Number of frames included per FFT calculation.
    block_size: int | None = None
    #: Whether to apply subsampling
    subsample: Literal["mean", "median", "std", "sum", None] = None
    #: Number of frames to deinterlace individually before switching to batch-wise
    #: processing.
    unstable: int | None = None
    #: Subsearc
    subsearch: int | None = 15
    #: Align
    align: Literal["pixel", "subpixel"] = "pixel"
    #: use gpu
    use_gpu: bool = False
    #: images to validate against
    _images: NDArrayLike | None = Field(default=None, init_var=True)

    def __post_init__(self, _images: NDArrayLike | None = None) -> None:
        if _images is not None:
            self.validate_with_images(_images)

    @field_validator("block_size", "unstable", "subsearch", mode="after")
    @classmethod
    def _validate_positive_integer(cls, value: int | None, ctx: Field) -> int | None:
        """
        Validate that the given value is a positive integer or None.

        :param value: The value to validate, which can be an integer or None.
        :returns: The validated value, or None if the input was None.
        """
        if value is not None and value <= 0:
            raise ParameterError(parameter=ctx.field_name, value=value, limits=(0, inf))
        return value

    def validate_with_images(self, images: NDArrayLike) -> None:
        """
        Validate the parameters against the provided images..

        :param images: The images to validate against.
        :returns: None
        """
        # BLOCK SIZE
        if self.block_size is None:
            self.block_size = images.shape[0]
        if self.block_size <= images.shape[0]:
            raise ParameterError(
                parameter="block_size",
                value=self.block_size,
                limits=(1, images.shape[0]),
            )

        # SUBSEARCH
        if self.subsearch is None:
            min_dim = min(images.shape[1:])  # Get the minimum spatial dimension
            self.subsearch = min_dim // 16
        if self.subsearch < min(images.shape[1:]):
            raise ParameterError(
                parameter="subsearch",
                value=self.subsearch,
                limits=(1, min(images.shape[1:]) - 1),
            )

        # UNSTABLE
        if self.unstable is not None and self.unstable > images.shape[0]:
            raise ParameterError(
                parameter="unstable",
                value=self.unstable,
                limits=(0, images.shape[0]),
            )

        # USE GPU
        if self.use_gpu and cp == np:
            msg = "CuPy is not available. GPU acceleration cannot be used."
            raise ValueError(msg)


def deinterlace(
    images: NDArrayLike,
    parameters: DeinterlaceParameters | None = None,
) -> None:
    """
    Deinterlace images collected using resonance-scanning microscopes such that the
    forward and backward-scanned lines are properly aligned. A fourier-approach is
    utilized: the fourier transform of the two sets of lines is computed to calculate
    the cross-power spectral density. Taking the inverse fourier transform of the
    cross-power spectral density yields a matrix whose peak corresponds to the
    sub-pixel offset between the two sets of lines. This translative offset was then
    discretized and used to shift the backward-scanned lines.

    Unfortunately, the fast-fourier transform methods that underlie the implementation
    of the deinterlacing algorithm have poor spatial complexity
    (i.e., large memory constraints). This weakness is particularly problematic when
    using GPU-parallelization. To mitigate these issues, deinterlacing can be performed
    batch-wise while maintaining numerically identical results (see `block_size`).

    To improve performance, the deinterlacing algorithm can be applied to a subsample
    of the images while maintaining efficacy. Specifically, setting the `subsample`
    parameter will apply the deinterlacing algorithm to the the standard deviation of
    each pixel across a block of images. This approach is better suited to images with
    limited signal-to-noise or sparse activity than simply operating on every n-th
    frame.

    Finally, it is often the case that the auto-alignment algorithms used in microscopy
    software are unstable until a sufficient number of frames have been collected.
    Therefore, the `unstable` parameter can be used to specify the number of frames
    that should be deinterlaced individually before switching to batch-wise processing.

    .. note::
        This function operates in-place.

    .. warning::
        The number of frames included in each fourier transform must be several times
        smaller than the maximum number of frames that fit within your GPU's VRAM
        (`CuPy <https://cupy.dev>`_) or RAM (`NumPy <https://numpy.org>`_). This
        function will not automatically revert to the NumPy implementation if there is
        not sufficient VRAM. Instead, an out of memory error will be raised.
    """
    parameters = parameters or DeinterlaceParameters()
    parameters.validate_with_images(images)

    # Set implementations for offset calculation and alignment
    if parameters.use_gpu:  # If cp != np then cupy is available
        func_handle = partial(
            calculate_phase_offset,
            fft_implementation=cupy_fft,
            ifft_implementation=cupy_ifft,
        )
        _calculate_phase_offset_ = wrap_cupy(func_handle, "images")
    else:
        _calculate_phase_offset_ = calculate_phase_offset
    if parameters.align == "pixel":
        align = pixel_alignment
    elif parameters.align == "subpixel":
        align = pixel_alignment
        warnings.warn("Subpixel alignment is not implemented yet.", stacklevel=2)
    else:
        align = pixel_alignment
        # TODO: finalize this

    # now iterate
    num_blocks, blocks = index_image_blocks(
        images, parameters.block_size, parameters.unstable
    )
    pbar = tqdm(total=num_blocks, desc="Deinterlacing Images", colour="blue")
    for start, stop in blocks:
        # Extract images to calculate phase offset from
        block_images = extract_image_block(images, start, stop, parameters.subsample)
        # Calculate Offset
        phase_offset = _calculate_phase_offset_(block_images, parameters.subsearch)
        # In-Place Alignment
        align(images, start, stop, phase_offset)
        pbar.update(1)
    pbar.close()
