"""
Model initialization module for clipx.
"""

from clipx.models.u2net.model import U2Net, ClipxError
from clipx.models.cascadepsp import CascadePSPModel
from clipx.models.auto import AutoModel

# Define a map of model names to model classes
MODEL_MAP = {
    'u2net': U2Net,
    'cascadepsp': CascadePSPModel,
    'auto': AutoModel,
}


def get_model(model_name):
    """
    Get model instance by name.

    Args:
        model_name: Name of the model to get

    Returns:
        Model instance

    Raises:
        ClipxError: If the model name is unknown
    """
    model_name = model_name.lower()
    if model_name not in MODEL_MAP:
        raise ClipxError(f"Unknown model: {model_name}. Available models: {', '.join(MODEL_MAP.keys())}")

    return MODEL_MAP[model_name]()