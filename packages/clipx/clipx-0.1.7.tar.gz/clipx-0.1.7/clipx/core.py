"""
Core processing module for clipx.
"""

import os
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Clipx:
    """
    Main class for image processing with U2Net and CascadePSP.
    """

    def __init__(self, device='cpu'):
        """
        Initialize the processing pipeline.

        Args:
            device: Device to use for processing ('cpu' or 'cuda')
        """
        self.device = device
        self.u2net = None
        self.cascadepsp = None
        logger.info(f"Initializing Clipx on {device}")

    def load_u2net(self):
        """
        Load the U2Net model.
        """
        if self.u2net is None:
            from clipx.models.u2net import U2Net
            logger.info("Loading U2Net model")
            self.u2net = U2Net().load(device=self.device)
        return self.u2net

    def load_cascadepsp(self):
        """
        Load the CascadePSP model.
        """
        if self.cascadepsp is None:
            from clipx.models.cascadepsp import CascadePSPModel
            logger.info("Loading CascadePSP model")
            self.cascadepsp = CascadePSPModel().load(device=self.device)
        return self.cascadepsp

    def process(self, input_path, output_path, model='combined', threshold=130, fast_mode=False):
        """
        Process an image using the selected model(s).

        Args:
            input_path: Path to input image
            output_path: Path to save the output image
            model: Model to use ('u2net', 'cascadepsp', or 'combined')
            threshold: Threshold for binary mask generation (0-255)
            fast_mode: Whether to use fast mode for CascadePSP

        Returns:
            Path to the output image
        """
        logger.info(f"Processing image: {input_path} with model: {model}")

        # Load input image
        try:
            img = Image.open(input_path).convert("RGB")
            logger.info(f"Image loaded: {img.size[0]}x{img.size[1]}")
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            raise ValueError(f"Failed to load image: {e}")

        # Process based on selected model
        if model == 'u2net':
            return self._process_u2net(img, output_path, threshold)
        elif model == 'cascadepsp':
            return self._process_cascadepsp(img, output_path, threshold, fast_mode)
        elif model == 'combined':
            return self._process_combined(img, output_path, threshold, fast_mode)
        else:
            raise ValueError(f"Unknown model: {model}")

    def _process_u2net(self, img, output_path, threshold):
        """
        Process with U2Net only.
        """
        # Load model
        u2net = self.load_u2net()

        # Generate mask and remove background
        logger.info("Generating binary mask with U2Net")
        binary_mask = u2net.get_binary_mask(img, threshold)

        # Save result
        if output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Remove background
            logger.info("Removing background with binary mask")
            result = Image.composite(img.convert("RGBA"),
                                    Image.new("RGBA", img.size, (0, 0, 0, 0)),
                                    binary_mask)
            result.save(output_path)
        else:
            # Save mask directly
            binary_mask.save(output_path)

        logger.info(f"Output saved to: {output_path}")
        return output_path

    def _process_cascadepsp(self, img, output_path, threshold, fast_mode):
        """
        Process with CascadePSP only.

        Note: CascadePSP requires a binary mask as input, so we need to generate
        a mask first using a simple thresholding method.
        """
        # Load model
        cascadepsp = self.load_cascadepsp()

        # Generate a simple mask (grayscale conversion and thresholding)
        logger.info("Generating simple mask for CascadePSP input")
        gray = img.convert("L")
        simple_mask = gray.point(lambda p: 255 if p > threshold else 0)

        # Refine mask with CascadePSP
        logger.info(f"Refining mask with CascadePSP (fast mode: {fast_mode})")
        refined_mask_np = cascadepsp.process(
            image=img,
            mask=simple_mask,
            fast=fast_mode
        )
        refined_mask = Image.fromarray(refined_mask_np)

        # Save result
        if output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Remove background
            logger.info("Removing background with refined mask")
            result = Image.composite(img.convert("RGBA"),
                                    Image.new("RGBA", img.size, (0, 0, 0, 0)),
                                    refined_mask)
            result.save(output_path)
        else:
            # Save mask directly
            refined_mask.save(output_path)

        logger.info(f"Output saved to: {output_path}")
        return output_path

    def _process_combined(self, img, output_path, threshold, fast_mode):
        """
        Process with combined U2Net and CascadePSP.
        """
        # Load models
        u2net = self.load_u2net()
        cascadepsp = self.load_cascadepsp()

        # Generate mask with U2Net
        logger.info("Generating binary mask with U2Net")
        binary_mask = u2net.get_binary_mask(img, threshold)

        # Refine mask with CascadePSP
        logger.info(f"Refining mask with CascadePSP (fast mode: {fast_mode})")
        refined_mask_np = cascadepsp.process(
            image=img,
            mask=binary_mask,
            fast=fast_mode
        )
        refined_mask = Image.fromarray(refined_mask_np)

        # Save result
        if output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Remove background
            logger.info("Removing background with refined mask")
            result = Image.composite(img.convert("RGBA"),
                                    Image.new("RGBA", img.size, (0, 0, 0, 0)),
                                    refined_mask)
            result.save(output_path)
        else:
            # Save mask directly
            refined_mask.save(output_path)

        logger.info(f"Output saved to: {output_path}")
        return output_path