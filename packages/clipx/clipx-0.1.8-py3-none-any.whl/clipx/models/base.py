"""
Base model class for all models.
"""


class BaseModel:
    """
    Base class for all models.
    """

    def __init__(self):
        """
        Initialize the base model.
        """
        self.name = "base"

    def load(self, device='cpu'):
        """
        Load the model.

        Args:
            device: Device to load the model on ('cpu' or 'cuda')

        Returns:
            self: The model instance
        """
        raise NotImplementedError("Subclasses must implement load()")

    def process(self, img, mask=None, fast=False):
        """
        Process the input image.

        Args:
            img: PIL Image to process
            mask: Optional existing mask
            fast: Whether to use fast mode

        Returns:
            PIL Image: The result
        """
        raise NotImplementedError("Subclasses must implement process()")