import os
import sys
import numpy as np
from PIL import Image


class ClipxError(Exception):
    """Base exception class for clipx errors"""
    pass


def is_image_file(filename):
    """
    Check if file is an image based on extension
    """
    valid_extensions = ['.jpg', '.jpeg', '.png']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


def load_image(image_path):
    """
    Load image from path
    """
    print(f"Loading image from {image_path}")
    try:
        img = Image.open(image_path).convert('RGB')
        print(f"Image loaded successfully: size={img.size}, mode={img.mode}")
        return img
    except Exception as e:
        raise ClipxError(f"Error loading image {image_path}: {e}")


def load_mask(mask_path):
    """
    Load mask image from path
    """
    if mask_path is None:
        return None

    print(f"Loading mask from {mask_path}")
    try:
        mask = Image.open(mask_path)
        # Convert to grayscale if not already
        if mask.mode != 'L':
            mask = mask.convert('L')
            print(f"Converted mask to grayscale")
        print(f"Mask loaded successfully: size={mask.size}, mode={mask.mode}")
        return mask
    except Exception as e:
        raise ClipxError(f"Error loading mask {mask_path}: {e}")


def save_image(image, output_path):
    """
    Save image to path
    """
    print(f"Saving image to {output_path}")

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Convert numpy array to PIL Image if needed
    if isinstance(image, np.ndarray):
        print(f"Converting numpy array shape={image.shape} to PIL Image")
        if len(image.shape) == 2:  # Grayscale
            pil_image = Image.fromarray(image)
        elif len(image.shape) == 3 and image.shape[2] == 3:  # RGB
            pil_image = Image.fromarray(image)
        elif len(image.shape) == 3 and image.shape[2] == 4:  # RGBA
            pil_image = Image.fromarray(image)
        else:
            raise ClipxError(f"Unsupported image shape: {image.shape}")
    else:
        pil_image = image
        print(f"Using provided PIL Image: size={pil_image.size}, mode={pil_image.mode}")

    # Save the image
    try:
        pil_image.save(output_path)
        print(f"Image saved successfully to {output_path}")
    except Exception as e:
        raise ClipxError(f"Error saving image to {output_path}: {e}")


def apply_mask_to_image(image, mask):
    """
    Apply mask to image to create transparent background

    Args:
        image: PIL Image or numpy array (RGB)
        mask: PIL Image or numpy array (grayscale)

    Returns:
        PIL Image with alpha channel
    """
    print("Applying mask to image")

    try:
        # Convert to PIL Images if needed
        if isinstance(image, np.ndarray):
            print("Converting image from numpy array to PIL Image")
            image = Image.fromarray(image)

        if isinstance(mask, np.ndarray):
            print("Converting mask from numpy array to PIL Image")
            mask = Image.fromarray(mask)

        # Convert image to RGBA if it's not already
        if image.mode != 'RGBA':
            print(f"Converting image from {image.mode} to RGBA")
            image = image.convert('RGBA')

        # Ensure mask is in correct mode
        if mask.mode != 'L':
            print(f"Converting mask from {mask.mode} to grayscale")
            mask = mask.convert('L')

        # Resize mask to match image if needed
        if image.size != mask.size:
            print(f"Resizing mask from {mask.size} to {image.size}")
            mask = mask.resize(image.size, Image.LANCZOS)

        # Apply mask as alpha channel
        print("Applying mask as alpha channel")
        image.putalpha(mask)

        print("Mask applied successfully")
        return image
    except Exception as e:
        raise ClipxError(f"Error applying mask to image: {e}")