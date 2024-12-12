"""
Stitch multiple images horizontally or vertically
"""

import os

from PIL import Image
from PIL import ImageFile
from PIL import UnidentifiedImageError


def __get_final_dimensions(
    images: list[ImageFile.ImageFile], is_vertical: bool
) -> tuple:
    width_idx = 0 if is_vertical else 1
    height_idx = 1 if is_vertical else 0
    width = 0
    height = 0

    for image in images:
        if image.size[width_idx] > width:
            width = image.size[width_idx]
    for image in images:
        height += int(width / image.size[width_idx] * image.size[height_idx])

    if is_vertical:
        return width, height
    else:
        return height, width


def __stitch_images(
    images: list[ImageFile.ImageFile], width: int, height: int, is_vertical: bool
) -> Image.Image:
    final = Image.new("RGB", (width, height), color=(0, 0, 0))
    pos = 0
    if is_vertical:
        for image in images:
            temp = image.resize((width, int(width / image.size[0] * image.size[1])))
            final.paste(temp, (0, pos))
            pos += int(width / image.size[0] * image.size[1])
    else:
        for image in images:
            temp = image.resize((int(height / image.size[1] * image.size[0]), height))
            final.paste(temp, (pos, 0))
            pos += int(height / image.size[1] * image.size[0])
    return final


def process(
    src_images: list[str],
    dst_dir: str,
    dst_image: str,
    is_vertical: bool,
    is_jpg: bool = False,
    quality: int = 100,
) -> str:
    # preliminary checks
    if not os.path.isdir(dst_dir):
        return "Destination directory does not exist"
    if os.path.isfile(os.path.join(dst_dir, dst_image)):
        return "Destination file already exists"

    # loading images
    try:
        images = [Image.open(src_image) for src_image in src_images]
    except UnidentifiedImageError:
        return "Given file does not look like an image"
    except FileNotFoundError:
        return "Given file does not exist in the given directory"

    # stitching images
    width, height = __get_final_dimensions(images, is_vertical)
    final_image = __stitch_images(images, width, height, is_vertical)

    # writing final image
    if is_jpg:
        final_image.save(
            os.path.join(dst_dir, dst_image) + ".jpg", format="JPEG", quality=quality
        )
    else:
        final_image.save(
            os.path.join(dst_dir, dst_image) + ".png", format="PNG", quality=quality
        )
    return "Image generated successfully"
