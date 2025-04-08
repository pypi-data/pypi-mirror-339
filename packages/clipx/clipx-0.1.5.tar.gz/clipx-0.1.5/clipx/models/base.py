"""
Base class for all models in clipx.
"""

from abc import ABC, abstractmethod
import os
import numpy as np
from PIL import Image


class BaseModel(ABC):
    """
    Base class for all models in clipx.
    """

    @abstractmethod
    def load(self, device='cpu'):
        """
        Load model to specified device.

        Args:
            device: Device to load model on ('cpu' or 'cuda')

        Returns:
            self: Returns self for method chaining
        """
        pass

    @abstractmethod
    def process(self, image, mask=None, **kwargs):
        """
        Process the image with the model.

        Args:
            image: Input image (PIL Image or numpy array)
            mask: Optional mask image (PIL Image or numpy array)
            **kwargs: Additional model-specific parameters

        Returns:
            Processed image or mask
        """
        pass

    def prepare_image(self, image):
        """
        Convert image to numpy array if it's a PIL Image.

        Args:
            image: Input image (PIL Image or numpy array)

        Returns:
            numpy.ndarray: Image as numpy array
        """
        if isinstance(image, Image.Image):
            return np.array(image)
        return image

    def prepare_mask(self, mask):
        """
        Convert mask to numpy array if it's a PIL Image.

        Args:
            mask: Input mask (PIL Image or numpy array)

        Returns:
            numpy.ndarray or None: Mask as numpy array or None
        """
        if mask is None:
            return None
        if isinstance(mask, Image.Image):
            return np.array(mask)
        return mask