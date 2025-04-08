

from clipx.models.base import BaseModel
from clipx.models.u2net.model import U2Net
from clipx.models.cascadepsp import CascadePSPModel


class AutoModel(BaseModel):
    """
    Auto model that first uses U2Net to generate a mask,
    then refines it with CascadePSP.
    """

    def __init__(self):
        """
        Initialize the Auto model.
        """
        super().__init__()
        self.u2net = U2Net()
        self.cascadepsp = CascadePSPModel()
        self.device = 'cpu'

    def load(self, device='cpu'):
        """
        Load both U2Net and CascadePSP models.

        Args:
            device: Device to load models on ('cpu' or 'cuda')

        Returns:
            self: The model instance
        """
        print(f"Loading Auto model (U2Net + CascadePSP) on {device}")
        self.device = device
        self.u2net.load(device)
        self.cascadepsp.load(device)
        return self

    def process(self, image, mask=None, fast=False, **kwargs):
        """
        Process the image using both U2Net and CascadePSP.

        Args:
            image: PIL Image to process
            mask: Optional existing mask
            fast: Whether to use fast mode for CascadePSP
            **kwargs: Additional parameters

        Returns:
            PIL Image: The resulting refined mask
        """
        print("Processing with Auto model (U2Net + CascadePSP)")

        # If mask is provided, skip U2Net
        if mask is None:
            print("Generating mask with U2Net")
            mask = self.u2net.process(image)

        # Refine mask with CascadePSP
        print("Refining mask with CascadePSP")
        refined_mask = self.cascadepsp.process(image, mask, fast=fast)

        return refined_mask