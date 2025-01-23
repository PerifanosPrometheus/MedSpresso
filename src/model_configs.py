"""
Configuration loader for supported models in MedSpresso.
"""
from pathlib import Path
import yaml

def load_model_configs() -> dict:
    """Load model configurations from YAML file."""
    config_path = Path(__file__).parent.parent / "configs" / "models.yaml"
    try:
        with open(config_path) as f:
            configs = yaml.safe_load(f)
        return configs.get("models", {})
    except FileNotFoundError:
        print(f"Warning: Model config file not found at {config_path}")
        return {}

MODEL_CONFIGS = load_model_configs()

def get_model_config(model_name: str) -> dict:
    """Get configuration for a specific model."""
    return MODEL_CONFIGS.get(model_name, {})

def get_template(model_name: str) -> str:
    """Get chat template for a specific model."""
    return get_model_config(model_name).get("template", "{prompt}")

def list_supported_models() -> list:
    """Get list of all supported models."""
    return list(MODEL_CONFIGS.keys()) 