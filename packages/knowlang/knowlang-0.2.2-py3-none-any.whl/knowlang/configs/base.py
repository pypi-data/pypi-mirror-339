from pydantic_settings import SettingsConfigDict
from pathlib import Path
from typing import Optional
from pydantic import ValidationInfo
from knowlang.core.types import ModelProvider 
import os

def generate_model_config(env_dir : Path = Path('settings'), env_file: Path = '.env', env_prefix : str = '') -> SettingsConfigDict:
    return SettingsConfigDict(
        env_file=str(env_dir / env_file),
        env_prefix=env_prefix,
        env_file_encoding='utf-8',
        env_nested_delimiter='__'
    )

def _validate_api_key(v: Optional[str], info: ValidationInfo) -> Optional[str]:
    """Validate API key is present when required"""
    if info.data['model_provider'] in [
        ModelProvider.OPENAI, 
        ModelProvider.ANTHROPIC,
        ModelProvider.VOYAGE
    ]:
        if not v:
            raise ValueError(f"API key required for {info.data['model_provider']}")
        elif info.data['model_provider'] == ModelProvider.ANTHROPIC:
            os.environ["ANTHROPIC_API_KEY"] = v
        elif info.data['model_provider'] == ModelProvider.OPENAI:
            os.environ["OPENAI_API_KEY"] = v
        elif info.data['model_provider'] == ModelProvider.VOYAGE:
            os.environ["VOYAGE_API_KEY"] = v
            
    return v