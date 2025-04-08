"""Generate assay images."""

import math
import random

from PIL import Image, ImageDraw, ImageFilter
from PIL.Image import Image as PilImage  # to satisfy type checking

from .assays import AssayParams, Assay, AllAssays

# Image parameters.
BORDER_WIDTH = 16
WELL_SIZE = 64
BLACK = 0
WHITE = 255
BLUR_RADIUS = 4


def images_generate(params: AssayParams, assays: AllAssays) -> dict[str, PilImage]:
    """Generate image files.

    Parameters:
        params: assay generation parameters
        assays: generated assays

    Returns:
        A dictionary of assay IDs and generated images.
    """
    max_reading = _find_max_reading(assays, params.plate_size)
    scaling = float(math.ceil(max_reading + 1))
    return {a.ident: _make_image(params, a, scaling) for a in assays.items}


def _find_max_reading(assays: AllAssays, p_size: int) -> float:
    """Find maximum assay reading value.

    Parameters:
        assays: generated assays
        p_size: plate size

    Returns:
        Largest reading value across all assays.
    """
    result = 0.0
    for a in assays.items:
        for x in range(p_size):
            for y in range(p_size):
                result = max(result, a.readings[x, y])
    return result


def _make_image(params: AssayParams, assay: Assay, scaling: float) -> PilImage:
    """Generate a single image.

    Parameters:
        params: assay parameters
        assay: assay to generate image for
        scaling: color scaling factor

    Returns:
       Image.
    """
    # Create blank image.
    p_size = params.plate_size
    img_noise = params.image_noise
    img_size = (p_size * WELL_SIZE) + ((p_size + 1) * BORDER_WIDTH)
    img = Image.new("L", (img_size, img_size), color=BLACK)

    # Fill with pristine reading values.
    spacing = WELL_SIZE + BORDER_WIDTH
    draw = ImageDraw.Draw(img)
    for ix, x in enumerate(range(BORDER_WIDTH, img_size, spacing)):
        for iy, y in enumerate(range(BORDER_WIDTH, img_size, spacing)):
            color = math.floor(WHITE * assay.readings[ix, iy] / scaling)
            draw.rectangle((x, y, x + WELL_SIZE, y + WELL_SIZE), color)

    # Add uniform noise (not provided by pillow).
    for x in range(img_size):
        for y in range(img_size):
            noise = random.randint(-img_noise, img_noise)
            old_val = img.getpixel((x, y))
            assert isinstance(old_val, int)  # for type checking
            val = max(BLACK, min(WHITE, old_val + noise))
            img.putpixel((x, y), val)

    # Blur.
    img = img.filter(ImageFilter.GaussianBlur(BLUR_RADIUS))

    return img
