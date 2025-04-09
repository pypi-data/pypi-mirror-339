"""
Configuration management for Sven client.

This module handles loading configuration from various sources:
1. .sven.yml file in the current directory
2. .sven.yml file in the user's home directory
3. Environment variables
4. Command line arguments
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field


class KnowledgeConfig(BaseModel):
    """Configuration for knowledge base."""

    name: str = Field(..., description="The name of the knowledge base")
    url: str | None = Field(None, description="The URL of the knowledge base")
    path: str | None = Field(None, description="The path to the knowledge base")

    class Config:
        validate_assignment = True

    def __init__(self, **data):
        super().__init__(**data)
        self._validate_url_path_exclusivity()

    def _validate_url_path_exclusivity(self):
        if self.url is not None and self.path is not None:
            raise ValueError("Only one of 'url' or 'path' can be specified, not both")

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in ("url", "path"):
            self._validate_url_path_exclusivity()


class SvenConfig(BaseModel):
    """Configuration manager for Sven client."""

    api_url: str = Field(default="http://localhost:8007")
    api_key: str = Field(default="")

    knowledge: List[KnowledgeConfig] = Field(default=[])

    sven_dir: Path = Field(default=Path.home() / ".sven")
    config_dir: Path = Field(default=Path.home())
    config_file: Path = Field(default=Path.home() / ".sven.yml")

    def get_knowledge_base(self, name: str) -> Optional[KnowledgeConfig]:
        """Get a knowledge base by name."""
        for knowledge_base in self.knowledge:
            if knowledge_base.name == name:
                return knowledge_base
        return None

    def save(self):
        """Save the configuration to the .sven.yml file."""
        with open(self.config_file, "w") as f:
            config = self.model_dump()
            # Filter out config_dir, sven_dir, and config_file
            config.pop("config_dir")
            config.pop("sven_dir")
            config.pop("config_file")
            yaml.dump(config, f)


def load() -> Dict[str, Union[str, int]]:
    """
    Load configuration from various sources with following precedence:
    1. .sven.yml in current directory (highest precedence)
    2. .sven.yml in user's home directory

    Returns:
        Dict containing merged configuration
    """
    # Start with empty config
    config = {}

    # Load from user's home directory .sven.yml
    home_config = Path.home() / ".sven.yml"
    if home_config.exists():
        config = _load_from_file(home_config)
        config["config_dir"] = Path.home()
        config["sven_dir"] = Path.home() / ".sven"
        config["config_file"] = home_config

    # Load from current directory .sven.yml (highest precedence)
    local_config = Path.cwd() / ".sven.yml"
    if local_config.exists():
        config = _load_from_file(local_config)
        config["config_dir"] = Path.cwd()
        config["sven_dir"] = Path.cwd() / ".sven"
        config["config_file"] = local_config

    return SvenConfig.model_validate(config)


def _load_from_file(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        config_path: Path to the configuration file
    """
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config from {config_path}: {str(e)}")

    return {}


# Create a singleton instance
settings = load()
