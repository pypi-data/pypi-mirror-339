import os
import numpy as np

from typing import List
from tkinter import filedialog as fd
from tifffile import imread, imwrite

from .utils import check_crop_img, crop_with_padding
from .blurring import gaussian_blur
from .downscaling import binning_img, binning_label
from .upscaling import upsample_img, upsample_labels
from tqdm import tqdm



def downsample_batch(input_folder_path: str, input_folder_name: str, downsampling_factor: int, keep_dims: bool = False, mode: str = "sum"):
    """Downsamples a batch of images by a given factor. The last two dimensions of the array are binned.
    Creates new folders outside input_folder to store the results.
    :param input_folder_path: path to folder containing an "images" folder and a "labels" folder. Images inside both folders should have the same name.
    :param downsampling_factor: factor used to bin dimensions
    :para keep_dims: whether to keep the original dimensions or just blur the image (defaults to False)
    :param mode: can be either sum, max or mean, defaults to sum if not specified or not valid mode
    """

    if keep_dims:
        new_dataset_path = os.path.join(os.path.dirname(os.path.dirname(input_folder_path)), "Processed", f"{input_folder_name}_downsampled_{downsampling_factor}_mode_{mode}_same_dims")
    else:
        new_dataset_path = os.path.join(os.path.dirname(os.path.dirname(input_folder_path)), "Processed", f"{input_folder_name}_downsampled_{downsampling_factor}_mode_{mode}_diff_dims")

    new_images_path = os.path.join(new_dataset_path, "Images")
    new_labels_path = os.path.join(new_dataset_path, "Labels")

    if not os.path.exists(new_dataset_path):
        os.mkdir(new_dataset_path)
        os.mkdir(new_images_path)
        os.mkdir(new_labels_path)

    for img_name in os.listdir(os.path.join(input_folder_path, "Images")):
        img = imread(os.path.join(input_folder_path, "Images", img_name)).astype(np.float32)
        img = check_crop_img(img, downsampling_factor)
        lbl = imread(os.path.join(input_folder_path, "Labels", img_name)).astype(np.float32)
        lbl = check_crop_img(lbl, downsampling_factor)
        imwrite(os.path.join(new_images_path, img_name), binning_img(img, downsampling_factor, keep_dims=keep_dims, mode=mode))
        if keep_dims:
            imwrite(os.path.join(new_labels_path, img_name), lbl.astype(np.uint16))
        else:
            imwrite(os.path.join(new_labels_path, img_name), binning_label(lbl, downsampling_factor).astype(np.uint16))


def upsample_batch(input_folder_path: str, input_folder_name: str, magnification: int, keep_dims: bool = False):
    """Upsamples a batch of images by the magnification param using Catmull-rom interpolation and labels using Nearest-neighbor.
    Creates new folders outside input_folder to store the results.
    :param input_folder_path: path to folder containing an "images" folder and a "labels" folder. Images inside both folders should have the same name.
    :param magnification: upscaling factor
    :para keep_dims: whether to keep the original dimensions or just blur the image (defaults to False)
    """

    if keep_dims:
        new_dataset_path = os.path.join(os.path.dirname(os.path.dirname(input_folder_path)), "Processed", f"{input_folder_name}_upsampled_{magnification}_same_dims")
    else:
        new_dataset_path = os.path.join(os.path.dirname(os.path.dirname(input_folder_path)), "Processed", f"{input_folder_name}_upsampled_{magnification}_diff_dims")

    new_images_path = os.path.join(new_dataset_path, "Images")
    new_labels_path = os.path.join(new_dataset_path, "Labels")

    if not os.path.exists(new_dataset_path):
        os.mkdir(new_dataset_path)
        os.mkdir(new_images_path)
        os.mkdir(new_labels_path)

    for img_name in os.listdir(os.path.join(input_folder_path, "Images")):
        img = imread(os.path.join(input_folder_path, "Images", img_name)).astype(np.float32)
        lbl = imread(os.path.join(input_folder_path, "Labels", img_name)).astype(np.float32)
        imwrite(os.path.join(new_images_path, img_name), upsample_img(img, magnification, keep_dims=keep_dims))
        imwrite(os.path.join(new_labels_path, img_name), upsample_labels(lbl, magnification, keep_dims=keep_dims).astype(np.uint16))


def blur_batch(input_folder_path: str, input_folder_name: str, gaussian_sigma: float):
    """Applies Gaussian blur to a batch of images.
    Creates new folders outside input_folder to store the results.
    :param input_folder_path: path to folder containing an "images" folder and a "labels" folder. Images inside both folders should have the same name.
    :param gaussians: list of standard deviations
    """

    new_dataset_path = os.path.join(os.path.dirname(os.path.dirname(input_folder_path)), "Processed", f"{input_folder_name}_blurred_{gaussian_sigma}")
    new_images_path = os.path.join(new_dataset_path, "Images")
    new_labels_path = os.path.join(new_dataset_path, "Labels")

    if not os.path.exists(new_dataset_path):
        os.mkdir(new_dataset_path)
        os.mkdir(new_images_path)
        os.mkdir(new_labels_path)

    for img_name in os.listdir(os.path.join(input_folder_path, "Images")):
        img = imread(os.path.join(input_folder_path, "Images", img_name)).astype(np.float32)
        lbl = imread(os.path.join(input_folder_path, "Labels", img_name)).astype(np.float32)
        imwrite(os.path.join(new_images_path, img_name), gaussian_blur(img, gaussian_sigma))
        imwrite(os.path.join(new_labels_path, img_name), lbl.astype(np.uint16))


def process_batch(input_folder_path: str, input_folder_name: str, downsampling_factors: List[int], magnifications: List[int], gaussians: List[float], modes: List[str] = ["sum", "mean"]):
    """Performs all downstream preprocessing on a single dataset"""

    for mag in magnifications:
        upsample_batch(
            input_folder_path,
            input_folder_name,
            mag
            )
        upsample_batch(
            input_folder_path,
            input_folder_name,
            mag,
            keep_dims=True
            )

    for mode in modes:
        for dsf in downsampling_factors:
            downsample_batch(
                input_folder_path,
                input_folder_name,
                dsf,
                keep_dims=True,
                mode=mode
                )
            downsample_batch(
                input_folder_path,
                input_folder_name,
                dsf,
                keep_dims=False,
                mode=mode
                )

    for gau in gaussians:
        blur_batch(
            input_folder_path,
            input_folder_name,
            gau
        )


def process_all_datasets(datasets_path: str, downsampling_factor: List[int], magnification: List[int], gaussians: List[float], modes: List[str] = ["sum", "mean"]):
    """Performs all downstream preprocessing on all datasets in a folder"""

    if datasets_path is None:
        datasets_path = fd.askdirectory()

    if not os.path.exists(os.path.join(os.path.dirname(datasets_path), "Processed")):
        os.mkdir(os.path.join(os.path.dirname(datasets_path), "Processed"))

    for fld in os.listdir(datasets_path):
        if os.path.isdir(os.path.join(datasets_path, fld)):
            process_batch(
                os.path.join(datasets_path, fld),
                fld,
                downsampling_factor,
                magnification,
                gaussians,
                modes
                )

# Core Processing Functions
def rescale_image(image: np.ndarray, factor: int, mode: str) -> np.ndarray:
    """Rescale image using specified method"""
    if mode == "down":
        return binning_img(image, factor, keep_dims=False, mode="mean")
    elif mode == "up":
        return upsample_img(image, factor, keep_dims=False)
    else:
        raise ValueError(f"Invalid scale mode: {mode}. Use 'up' or 'down'")


#  Processing Pipeline
def rescale_and_crop_image(INPUT_DIR, OUTPUT_DIR, SCALE_FACTOR, SCALE_MODE, TARGET_SHAPE, SAVE_SCALED):
    # Create output directories
    os.makedirs(os.path.join(OUTPUT_DIR, "scaled"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "final"), exist_ok=True)
    # Get image list
    images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.tif')]

    for filename in images:
        # Load image
        img_path = os.path.join(INPUT_DIR, filename)
        image = np.squeeze(imread(img_path))

        # Rescale
        scaled = rescale_image(image, SCALE_FACTOR, SCALE_MODE)

        # Save intermediate
        if SAVE_SCALED:
            imwrite(os.path.join(OUTPUT_DIR, "scaled", f"scaled_{SCALE_MODE}_{SCALE_FACTOR}_{filename}"), scaled)

        # Crop/Pad
        final_image = crop_with_padding(scaled, TARGET_SHAPE)

        # Save result
        imwrite(os.path.join(OUTPUT_DIR, "final", f"processed_{SCALE_MODE}_{SCALE_FACTOR}_{filename}"), final_image)


def rescale_and_crop(INPUT_DIR, OUTPUT_DIR, SCALE_FACTOR, TARGET_SHAPE, SAVE_SCALED):
    for s in tqdm(SCALE_FACTOR, desc="Rescaling and cropping"):
        SCALE_MODE = "down" if s<1 else "up"
        if s < 1:
            SCALE_MODE = "down"
            s = np.floor(1/s)
        else:
            SCALE_MODE = "up"
        print(s)
        rescale_and_crop_image(INPUT_DIR, OUTPUT_DIR, np.int8(s), SCALE_MODE, TARGET_SHAPE, SAVE_SCALED)