"""Configuration handling for the registry."""

import importlib.resources
import json
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from langgate.core.logging import get_logger
from langgate.core.utils.config_utils import resolve_path

logger = get_logger(__name__)


class RegistryConfig:
    """Configuration handler for the registry."""

    def __init__(
        self,
        models_data_path: Path | None = None,
        config_path: Path | None = None,
        env_file_path: Path | None = None,
    ):
        """
        Args:
            models_data_path: Path to the models data JSON file
            config_path: Path to the main configuration YAML file
            env_file_path: Path to a `.env` file for environment variables
        """
        # Set up default paths
        cwd = Path.cwd()
        # Get package resource paths
        registry_resources = importlib.resources.files("langgate.registry")
        core_resources = importlib.resources.files("langgate.core")
        default_models_path = Path(
            str(registry_resources.joinpath("data", "default_models.json"))
        )
        default_config_path = Path(
            str(core_resources.joinpath("data", "default_config.yaml"))
        )

        # Define default paths with priorities
        # Models data: args > env > cwd > package_dir
        cwd_models_path = cwd / "langgate_models.json"

        # Config: args > env > cwd > package_dir
        cwd_config_path = cwd / "langgate_config.yaml"

        # Env file: args > env > cwd
        cwd_env_path = cwd / ".env"

        # Resolve paths using priority order
        self.models_data_path = resolve_path(
            "LANGGATE_MODELS",
            models_data_path,
            cwd_models_path if cwd_models_path.exists() else default_models_path,
            "models_data_path",
        )

        self.config_path = resolve_path(
            "LANGGATE_CONFIG",
            config_path,
            cwd_config_path if cwd_config_path.exists() else default_config_path,
            "config_path",
        )

        self.env_file_path = resolve_path(
            "LANGGATE_ENV_FILE", env_file_path, cwd_env_path, "env_file_path"
        )

        # Load environment variables from .env file if it exists
        if self.env_file_path.exists():
            load_dotenv(self.env_file_path)
            logger.debug("loaded_env_file", path=str(self.env_file_path))

        # Initialize data structures
        self.models_data: dict[str, dict[str, Any]] = {}
        self.global_config: dict[str, Any] = {}
        self.service_config: dict[str, dict[str, Any]] = {}
        self.model_mappings: dict[str, dict[str, Any]] = {}

        # Load configuration
        self._load_config()

    def _resolve_path(
        self, env_var: str, arg_path: Path | None, default_path: Path, path_desc: str
    ) -> Path:
        """Resolve a file path based on priority: args > env > default.

        Args:
            env_var: Environment variable name to check
            arg_path: Path provided in constructor args
            default_path: Default path to use if others not provided
            path_desc: Description for logging

        Returns:
            Resolved Path object
        """
        # Priority: args > env > default
        resolved_path = arg_path or Path(os.getenv(env_var, str(default_path)))

        # Log the resolved path and its existence
        exists = resolved_path.exists()
        logger.debug(
            f"resolved_{path_desc}",
            path=str(resolved_path),
            exists=exists,
            source="args" if arg_path else ("env" if os.getenv(env_var) else "default"),
        )

        return resolved_path

    def _load_config(self) -> None:
        """Load configuration from files."""
        try:
            # Load model data
            self._load_model_data()

            # Load main configuration
            self._load_main_config()

        except Exception:
            logger.exception(
                "failed_to_load_config",
                models_data_path=str(self.models_data_path),
                config_path=str(self.config_path),
            )
            raise

    def _load_model_data(self) -> None:
        """Load model data from JSON file."""
        try:
            with open(self.models_data_path) as f:
                self.models_data = json.load(f)
            logger.info(
                "loaded_model_data",
                models_data_path=str(self.models_data_path),
                model_count=len(self.models_data),
            )
        except FileNotFoundError:
            logger.warning(
                "model_data_file_not_found",
                models_data_path=str(self.models_data_path),
            )
            self.models_data = {}

    def _load_main_config(self) -> None:
        """Load main configuration from YAML file."""
        try:
            with open(self.config_path) as f:
                config: dict[str, Any] = yaml.safe_load(f)
            logger.info(
                "loaded_config",
                config_path=str(self.config_path),
            )

            # Extract global defaults
            self.global_config = {
                "default_params": config.get("default_params", {}),
            }

            # Extract service provider config
            self.service_config = config.get("services", {})

            # Process model mappings
            self._process_model_mappings(config.get("models", []))

        except FileNotFoundError:
            logger.warning(
                "config_file_not_found",
                config_path=str(self.config_path),
            )
            self.global_config = {"default_params": {}}
            self.service_config = {}
            self.model_mappings = {}

    def _process_model_mappings(self, models_config: list[dict[str, Any]]) -> None:
        """Process model mappings from configuration.

        Args:
            models_config: List of model configurations from the YAML file
        """
        self.model_mappings = {}

        for model_config in models_config:
            model_id: str = model_config["id"]
            service: dict[str, Any] = model_config["service"]
            service_provider: str = service["provider"]
            service_model_id: str = service["model_id"]

            # Store mapping info
            self.model_mappings[model_id] = {
                "service_provider": service_provider,
                "service_model_id": service_model_id,
                "override_params": model_config.get("override_params", {}),
                "remove_params": model_config.get("remove_params", []),
                "rename_params": model_config.get("rename_params", {}),
                "name": model_config.get("name"),
                "description": model_config.get("description"),
            }
