"""
Command line parser for clipx with improved validation logic.
"""

import os
import sys
import click
import logging
from pathlib import Path

from clipx.utils import ClipxError, is_image_file
from clipx.commands.input import add_input_options
from clipx.commands.output import add_output_options
from clipx.commands.model import add_model_options
from clipx.commands.mask import add_mask_options
from clipx.models import get_model

# Configure logging
logger = logging.getLogger(__name__)


def validate_input_path(input_path):
    """
    Validate that the input path exists and is a valid image or directory.

    Args:
        input_path: Path to check

    Raises:
        ClipxError: If validation fails
    """
    # Check if path exists
    if not os.path.exists(input_path):
        raise ClipxError(f"Input path does not exist: {input_path}")

    # If it's a directory, check if it contains at least one image
    if os.path.isdir(input_path):
        has_images = any(is_image_file(os.path.join(input_path, f))
                         for f in os.listdir(input_path)
                         if os.path.isfile(os.path.join(input_path, f)))
        if not has_images:
            raise ClipxError(f"No image files found in directory: {input_path}")
    # If it's a file, check if it's an image
    elif not is_image_file(input_path):
        raise ClipxError(f"Input file is not a recognized image format: {input_path}")


def validate_model(model_name):
    """
    Validate the model name and check if model needs to be downloaded.

    Args:
        model_name: Name of the model to check

    Raises:
        ClipxError: If validation fails
    """
    try:
        # Try to get the model - this will raise ClipxError if model is unknown
        model = get_model(model_name)

        # For U2Net, check if model file exists or can be downloaded
        if model_name.lower() == 'u2net':
            from clipx.models.u2net.download import download_u2net_model
            try:
                # This will download the model if it doesn't exist
                download_u2net_model()
                logger.info(f"U2Net model is ready to use")
            except Exception as e:
                raise ClipxError(f"Failed to download U2Net model: {e}")

        # For CascadePSP, check if model file exists or can be downloaded
        elif model_name.lower() == 'cascadepsp':
            from clipx.models.cascadepsp.download import download_and_or_check_model_file
            try:
                model_folder = os.path.expanduser("~/.clipx/cascadepsp")
                os.makedirs(model_folder, exist_ok=True)
                model_path = os.path.join(model_folder, "model")
                download_and_or_check_model_file(model_path)
                logger.info(f"CascadePSP model is ready to use")
            except Exception as e:
                raise ClipxError(f"Failed to download CascadePSP model: {e}")

        # For auto model, we need both models
        elif model_name.lower() == 'auto':
            # Check U2Net
            from clipx.models.u2net.download import download_u2net_model
            try:
                download_u2net_model()
                logger.info(f"U2Net model is ready to use")
            except Exception as e:
                raise ClipxError(f"Failed to download U2Net model: {e}")

            # Check CascadePSP
            from clipx.models.cascadepsp.download import download_and_or_check_model_file
            try:
                model_folder = os.path.expanduser("~/.clipx/cascadepsp")
                os.makedirs(model_folder, exist_ok=True)
                model_path = os.path.join(model_folder, "model")
                download_and_or_check_model_file(model_path)
                logger.info(f"CascadePSP model is ready to use")
            except Exception as e:
                raise ClipxError(f"Failed to download CascadePSP model: {e}")

    except Exception as e:
        raise ClipxError(f"Model validation error: {e}")


def validate_mask_path(mask_path):
    """
    Validate that the mask path exists and is a valid image.

    Args:
        mask_path: Path to check

    Raises:
        ClipxError: If validation fails
    """
    if mask_path is None:
        return

    if not os.path.exists(mask_path):
        raise ClipxError(f"Mask file does not exist: {mask_path}")

    if not os.path.isfile(mask_path) or not is_image_file(mask_path):
        raise ClipxError(f"Mask file is not a recognized image format: {mask_path}")


def create_cli_parser():
    """
    Create CLI parser with all options and validation logic.
    """
    def version_callback(ctx, param, value):
        """
        Callback for version option - fast implementation.
        """
        if not value or ctx.resilient_parsing:
            return value

        # Import version only when needed to speed up CLI
        from clipx import __version__
        click.echo(f"clipx version {__version__}")
        ctx.exit()

    def help_callback(ctx, param, value):
        """
        Callback for help option - fast implementation.
        """
        if not value or ctx.resilient_parsing:
            return value

        click.echo(ctx.get_help())
        ctx.exit()

    # 关键修改：添加 standalone_mode=False 参数
    @click.command(standalone_mode=False)
    @click.option('-v', '--version', is_flag=True,
                  help='Show version information.',
                  callback=version_callback,
                  is_eager=True,
                  expose_value=False)
    @click.option('-h', '--help', is_flag=True,
                  help='Show this help message.',
                  callback=help_callback,
                  is_eager=True,
                  expose_value=False)
    @add_input_options
    @add_output_options
    @add_model_options
    @add_mask_options
    def clipx_command(**kwargs):
        """
        clipx - Image background removal tool.

        Example usage:
          clipx -i input.jpg -o output.png
          clipx -m u2net -i input.jpg -o output.png
          clipx -m u2net -i input.jpg -o mask.png -k
        """
        try:
            # Step 1: Check if parameters are correctly parsed
            for key, value in kwargs.items():
                if key == 'input' and value is None:
                    raise ClipxError("Input image or folder is required")

            # Log parsed arguments
            logger.debug(f"Parsed arguments: {kwargs}")

            # Step 2: Validate the input file/folder
            input_path = kwargs.get('input')
            logger.info(f"Validating input path: {input_path}")
            validate_input_path(input_path)

            # Step 3: Validate mask file if provided
            mask_path = kwargs.get('use_mask')
            if mask_path:
                logger.info(f"Validating mask path: {mask_path}")
                validate_mask_path(mask_path)

            # Step 4: Validate the model and check if it needs to be downloaded
            model_name = kwargs.get('model', 'auto')
            logger.info(f"Validating model: {model_name}")
            validate_model(model_name)

            # All checks passed, return the validated options
            return kwargs

        except ClipxError as e:
            # Provide friendly error messages for expected errors
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
        except Exception as e:
            # For unexpected errors, provide a more generic message
            click.echo(f"An unexpected error occurred: {e}", err=True)
            logger.exception("Unexpected error in command processing")
            sys.exit(1)

    return clipx_command