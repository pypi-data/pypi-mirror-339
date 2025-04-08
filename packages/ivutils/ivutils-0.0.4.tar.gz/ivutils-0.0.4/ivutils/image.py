from typing import Tuple, Dict, Set

import csv
import os
import glob
import fnmatch
from PIL import Image
import inspect


def batch_image_grid(in_pattern: str, out_file_format: str, grid_size: Tuple[int, int], src_dirs: list[str]= None, src_dir_pattern: str = None, wrap_last_img: bool = False):
    """
    Create a grid of images from multiple directories.

    Args:
    - in_pattern (str): Pattern to match input image files. Supports "glob" format string
    - out_file_format (str): Format string for output file names.
    - grid_size (Tuple[int, int]): Number of rows and columns in the grid.
    - src_dirs (list[str], optional): List of source directories. Defaults to None.
    - src_dir_pattern (str, optional): Pattern to match source directories. Defaults to None. If this is provided, the function overrides "src_dirs" with the result.
    - wrap_last_img (bool, optional): Whether to wrap the last image in the grid. Defaults to False.
    """

    def files_in_dir_gen(dir_idx: int):
        directory = src_dirs[dir_idx]
        for f in os.listdir(directory):
            if in_pattern in f:
                yield os.path.join(directory, f)

    def load_image_to_buffer(img_path: str, buffer: Image):
        with Image.open(img_path) as new_img:
            # Resize the new image to match the size of the reusable object
            new_img = new_img.resize((img_width, img_height))
            # Update the pixels of the reusable object
            img_buffer.paste(new_img)

    def get_image_details(dir_path: str):
        img_filename = None
        for f in os.listdir(dir_path):
            if in_pattern in f:
                img_filename = os.path.join(dir_path, f)
                break

        width, height, mode = None, None, None
        if img_filename is not None:
            with Image.open(img_filename) as img:
                width, height, mode = img.width, img.height, img.mode

        return width, height, mode

    # Use src_dir_pattern to override src_dirs if present
    if src_dir_pattern:
        src_dirs = [d for d in glob.glob(src_dir_pattern) if os.path.isdir(d)]

    if not src_dirs or len(src_dirs) == 0:
        return

    num_rows, num_cols = grid_size

    img_width, img_height, img_mode = get_image_details(src_dirs[0])
    black_img  = Image.new(img_mode, (num_cols * img_width, num_rows * img_height), (0,0,0))
    grid_image = Image.new(img_mode, (num_cols * img_width, num_rows * img_height))
    img_buffer = Image.new(img_mode, (img_width, img_height))

    dir_idx = 0
    img_files_gen = files_in_dir_gen(dir_idx)

    batch_id = 0
    while inspect.getgeneratorstate(img_files_gen) != inspect.GEN_CLOSED:

        for row in range(num_rows):
            col = 0
            end_of_dir_files = False
            try:
                for col in range(num_cols):
                    img_file = next(img_files_gen)
                    print(f"processing: {img_file}")
                    load_image_to_buffer(img_file, img_buffer)
                    grid_image.paste(img_buffer, (col * img_width, row * img_height))

            except StopIteration:
                print(f"done processing ")
                end_of_dir_files = True
                if wrap_last_img:
                    for i in range(num_cols - col):
                        grid_image.paste(img_buffer, ((col + i) * img_width, row * img_height))

            if end_of_dir_files:
                dir_idx += 1
                if dir_idx >= len(src_dirs):
                    break
                else:
                    img_files_gen = files_in_dir_gen(dir_idx)

        out_batch_file = out_file_format.format(**{"batch_id": batch_id})
        batch_id += 1
        grid_image.save(out_batch_file)
        grid_image.paste(black_img, (0, 0))
    return


def get_image_from_grid(
                        img_target: Image,
                        target_index: int,
                        grid_size: tuple,
                        img_batch_filename: str = None,
                        img_batch: Image = None) -> Image:
    """
    Extracts an image from a grid of images and pastes it onto a target image.

    Args:
    - img_batch_filename (str): The filename of the batch image. (Mutually exclusive with img_batch)
    - img_batch (Image): The batch image containing the grid of images. (Mutually exclusive with img_batch_filename)
    - img_target (Image): The target image where the extracted image will be pasted.
    - target_index (int): The index of the image to extract from the grid.
    - grid_size (tuple): The size of the grid (m, n) in the batch image.

    Returns:
    - The target image with the extracted image pasted onto it.

    Raises:
    - ValueError: If both img_batch_filename and img_batch are provided, or if neither is provided.
    - ValueError: If target_index is out of range of grid_size.
    """

    # Validate that exactly one of img_batch_filename and img_batch is provided
    if (img_batch_filename is None) == (img_batch is None):
        raise ValueError("Must provide exactly one of img_batch_filename and img_batch")

    # Load the batch image if a filename is provided
    if img_batch_filename is not None:
        img_batch = Image.open(img_batch_filename)

    # Validate that target_index is within the range of grid_size
    grid_m, grid_n = grid_size
    if target_index < 0 or target_index >= grid_m * grid_n:
        raise ValueError("target_index is out of range of grid_size")

    # Calculate the position of the image to extract from the grid
    img_x = (target_index % grid_n) * (img_batch.width // grid_n)
    img_y = (target_index // grid_n) * (img_batch.height // grid_m)

    # Crop the image from the grid
    img_extracted = img_batch.crop(
        (img_x, img_y, img_x + (img_batch.width // grid_n), img_y + (img_batch.height // grid_m)))

    # Paste the extracted image onto the target image
    # Paste at position (0, 0) since target image is the same size as the extracted image
    img_target.paste(img_extracted, (0, 0))

    return img_target


def preprocess_image(image_path, resize_dim=(640, 480)):
    """Preprocesses an image to a target size (16:9) while handling different aspect ratios.

    Args:
        image_path: Path to the image.
        resize_dim: Tuple (width, height) for the target size (default: 640x480).

    Returns:
        A PIL Image object, or None if an error occurred.
    """
    try:
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
        return None  # Return None on error
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    ow, oh = image.size
    aspect_ratio = ow / oh
    target_ratio = resize_dim[0] / resize_dim[1]

    if aspect_ratio > target_ratio:  # Landscape
        new_h = int(oh * (resize_dim[0] / ow))
        image = image.resize((resize_dim[0], new_h), Image.BICUBIC)
        padding = (0, (resize_dim[1] - new_h) // 2, 0, resize_dim[1] - new_h - (resize_dim[1] - new_h) // 2)
        # Create a new image with the target size and black background color
        new_image = Image.new("RGB", resize_dim, (0, 0, 0))
        # Paste the resized image onto the new image with padding
        new_image.paste(image, (0, (resize_dim[1] - new_h) // 2))
        image = new_image  # Update the image reference to the new padded image

    elif aspect_ratio < target_ratio:  # Portrait
        new_w = int(ow * (resize_dim[1] / oh))
        image = image.resize((new_w, resize_dim[1]), Image.BICUBIC)
        padding = ((resize_dim[0] - new_w) // 2, 0, resize_dim[0] - new_w - (resize_dim[0] - new_w) // 2, 0)
        new_image = Image.new("RGB", resize_dim, (0, 0, 0))
        new_image.paste(image, ((resize_dim[0] - new_w) // 2, 0))
        image = new_image  # Update the image reference

    else:  # Already 16:9
        image = image.resize(resize_dim, Image.BICUBIC)

    return image  # Return the processed image


def resize_images(src_dir: str, out_file_format: str, search_ext: Set[str], trg_size: Tuple[int, int] = (320, 240), mappings_file: str = None):

    def callback(src_filename: str, trg_filename: str):
        img = preprocess_image(image_path=src_filename, resize_dim=trg_size)
        if img is not None:
            img.save(trg_filename)

    file_mappings = __iterate_files_recursive(src_dir, out_file_format, callback, search_ext)
    if mappings_file:
        with open(mappings_file, mode='w', newline='') as file:
            csv.writer(file).writerows(file_mappings)


def __iterate_files_recursive(root_dir: str, out_file_format: str, callback: callable, search_ext: Set[str]):
    """
    Iterates over all files in a directory and its subdirectories.

    :param root_dir:
    :param out_file_format:
    :param callback:
    :param search_ext:
    :return:
    """
    file_map = []
    out_file = ""
    try:
        seq_id = 0
        for cur_dir, _, files in os.walk(root_dir):
            rel_dir = os.path.relpath(cur_dir, root_dir)
            for file in files:
                _, file_ext = os.path.splitext(file)
                if file_ext in search_ext:
                    out_file = out_file_format.format(seq_id=seq_id)
                    seq_id += 1
                    file_map.append([os.path.join(rel_dir, file), out_file])
                    callback(os.path.join(cur_dir, file), out_file)

    except FileNotFoundError as ex:
        print(f"Error: {out_file} : {ex}")
    except OSError as ex:
        print(f"Error accessing directory '{root_dir}': {ex}")

    return file_map
