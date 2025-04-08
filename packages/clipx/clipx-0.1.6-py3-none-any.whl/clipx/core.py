"""
Core processing logic for clipx.
"""

import os
import torch
from pathlib import Path
import sys

from clipx.models import get_model, ClipxError
from clipx.commands import get_output_path
from clipx.utils import (
    load_image,
    load_mask,
    save_image,
    apply_mask_to_image,
    is_image_file
)


def process_single_image(input_path, output_path=None, model_name='auto', use_mask=None,
                         only_mask=False, fast=False):
    """
    Process a single image with the specified model.

    Args:
        input_path: Path to input image
        output_path: Path to output image or None to use default
        model_name: Name of model to use
        use_mask: Path to existing mask or None
        only_mask: Whether to output only the mask
        fast: Whether to use fast mode for CascadePSP
    """
    try:
        # Generate output path if not provided
        if output_path is None:
            output_path = get_output_path(input_path)

        # Choose device (use CUDA if available)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {device}")

        # Load input image
        print(f"Loading input image: {input_path}")
        input_image = load_image(input_path)

        # Load mask if provided
        mask = None
        if use_mask:
            print(f"Loading mask: {use_mask}")
            mask = load_mask(use_mask)

        print(f"Initializing model: {model_name}")
        # Get the appropriate model
        model = get_model(model_name).load(device)

        # Process with model
        print(f"Processing image with {model_name} model")

        # Model processing
        result_mask = model.process(input_image, mask, fast=fast)

        # Save result
        if only_mask:
            print(f"Saving mask to: {output_path}")
            save_image(result_mask, output_path)
            print(f"Mask saved to {output_path}")
        else:
            # Apply refined mask to image
            print("Applying mask to image")
            result_image = apply_mask_to_image(input_image, result_mask)
            print(f"Saving result to: {output_path}")
            save_image(result_image, output_path)
            print(f"Image with removed background saved to {output_path}")

        return True  # 添加返回值表示处理成功
    except ClipxError as e:
        print(f"Error: {e}")
        return False  # 添加返回值表示处理失败
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False  # 添加返回值表示处理失败


def process_command(options):
    """
    Process command line options.

    Args:
        options: Dictionary of command line options

    Returns:
        bool: True if processing succeeded, False otherwise
    """
    try:
        input_path = options.get('input')
        output_path = options.get('output')
        model_name = options.get('model', 'auto')
        use_mask = options.get('use_mask')
        only_mask = options.get('only_mask', False)
        fast = options.get('fast', False)

        print(f"Processing command with options: {options}")

        # Process directory or single file
        if os.path.isdir(input_path):
            result = process_directory(
                input_path,
                output_path,
                model_name,
                use_mask,
                only_mask,
                fast
            )
        else:
            result = process_single_image(
                input_path,
                output_path,
                model_name,
                use_mask,
                only_mask,
                fast
            )

        return result
    except ClipxError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def process_directory(input_dir, output_dir=None, model_name='auto', use_mask=None,
                      only_mask=False, fast=False):
    """
    Process all images in a directory.

    Args:
        input_dir: Directory containing input images
        output_dir: Directory for output images or None to use input_dir
        model_name: Name of model to use
        use_mask: Path to existing mask directory or None
        only_mask: Whether to output only masks
        fast: Whether to use fast mode for CascadePSP
    """
    try:
        input_dir = Path(input_dir)
        print(f"Processing directory: {input_dir}")

        # Use input directory as output if not specified
        if output_dir is None:
            output_dir = input_dir
        else:
            output_dir = Path(output_dir)
            os.makedirs(output_dir, exist_ok=True)

        print(f"Output directory: {output_dir}")

        # Get all image files in the directory
        image_files = [f for f in input_dir.iterdir() if f.is_file() and is_image_file(str(f))]

        if not image_files:
            print(f"No image files found in {input_dir}")
            return

        # Process each image
        print(f"Found {len(image_files)} images to process")
        for img_path in image_files:
            rel_path = img_path.relative_to(input_dir)
            out_path = output_dir / rel_path

            # If use_mask is a directory, look for corresponding mask
            mask_path = None
            if use_mask and os.path.isdir(use_mask):
                mask_file = Path(use_mask) / rel_path
                if mask_file.exists():
                    mask_path = str(mask_file)
            elif use_mask:
                mask_path = use_mask

            try:
                process_single_image(
                    str(img_path),
                    str(out_path),
                    model_name,
                    mask_path,
                    only_mask,
                    fast
                )
            except ClipxError as e:
                print(f"Error processing {img_path}: {e}")
                print("Continuing with next image...")
                continue
    except ClipxError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
