# clipx/models/u2net/model.py
"""
U2Net model implementation.
"""

import os
import numpy as np
import torch
from PIL import Image
import onnxruntime as ort

from clipx.models.base import BaseModel
from clipx.models.u2net.download import download_u2net_model

class ClipxError(Exception):
    """Base exception class for clipx errors"""
    pass

class U2Net(BaseModel):
    """
    U2Net model for background removal.
    """

    def __init__(self):
        """
        Initialize the U2Net model.
        """
        super().__init__()
        self.name = "u2net"
        self.session = None
        self.model_path = None

    def load(self, device='cpu'):
        """
        Load the U2Net model.

        Args:
            device: Device to load the model on ('cpu' or 'cuda')

        Returns:
            self: The model instance
        """
        print(f"Loading U2Net model on {device}")

        # Download model if not exists
        try:
            self.model_path = download_u2net_model()
        except Exception as e:
            raise ClipxError(f"Failed to download U2Net model: {e}")

        # Create ONNX session
        providers = ['CPUExecutionProvider']
        if device == 'cuda' and 'CUDAExecutionProvider' in ort.get_available_providers():
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']

        try:
            sess_options = ort.SessionOptions()
            self.session = ort.InferenceSession(
                self.model_path,
                sess_options=sess_options,
                providers=providers
            )
        except Exception as e:
            raise ClipxError(f"Failed to create ONNX session: {e}")

        print(f"U2Net model loaded successfully from {self.model_path}")
        return self

    def _normalize(self, img, size=(320, 320)):
        """
        Normalize the input image for U2Net.

        Args:
            img: PIL Image
            size: Size to resize to

        Returns:
            dict: Normalized input for ONNX session
        """
        try:
            # Convert to RGB and resize
            im = img.convert("RGB").resize(size, Image.LANCZOS)

            # Convert to numpy array and normalize
            im_ary = np.array(im)
            im_ary = im_ary / np.max(im_ary)

            # Apply mean and std normalization
            tmpImg = np.zeros((im_ary.shape[0], im_ary.shape[1], 3))
            tmpImg[:, :, 0] = (im_ary[:, :, 0] - 0.485) / 0.229
            tmpImg[:, :, 1] = (im_ary[:, :, 1] - 0.456) / 0.224
            tmpImg[:, :, 2] = (im_ary[:, :, 2] - 0.406) / 0.225

            # Transpose to channel-first format
            tmpImg = tmpImg.transpose((2, 0, 1))

            # Add batch dimension
            return {
                self.session.get_inputs()[0].name: np.expand_dims(tmpImg, 0).astype(np.float32)
            }
        except Exception as e:
            raise ClipxError(f"Failed to normalize image: {e}")

    def process(self, img, mask=None, fast=False):
        """
        Process the input image with U2Net.

        Args:
            img: PIL Image to process
            mask: Optional existing mask (not used for U2Net)
            fast: Whether to use fast mode (not used for U2Net)

        Returns:
            PIL Image: The resulting mask
        """
        if self.session is None:
            raise ClipxError("Model not loaded. Call load() first.")

        print("Processing image with U2Net")

        # If mask is provided, just return it
        if mask is not None:
            print("Using provided mask, skipping U2Net inference")
            return mask

        try:
            # Get normalized input
            input_data = self._normalize(img)

            # Run inference
            print("Running U2Net inference")
            ort_outs = self.session.run(None, input_data)

            # Post-process the result
            pred = ort_outs[0][:, 0, :, :]

            # Normalize prediction to range [0, 1]
            ma = np.max(pred)
            mi = np.min(pred)
            pred = (pred - mi) / (ma - mi)
            pred = np.squeeze(pred)

            # Convert to PIL Image and resize to match input
            mask = Image.fromarray((pred * 255).astype("uint8"), mode="L")
            mask = mask.resize(img.size, Image.LANCZOS)

            print("U2Net processing completed")
            return mask
        except Exception as e:
            raise ClipxError(f"Error processing image with U2Net: {e}")