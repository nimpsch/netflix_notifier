import os
from typing import Dict
import yaml
from dotenv import load_dotenv

from config.provider_model import Provider
from config.provider_name import ProviderName

load_dotenv()


class ProviderFactory:
    _providers_config: Dict[str, Dict]

    @staticmethod
    def load_providers(file_path="config/providers.yml"):
        with open(file_path, "r") as file:
            ProviderFactory._providers_config = yaml.safe_load(file)["providers"]

    @staticmethod
    def get_provider(name: ProviderName) -> Provider:
        if not hasattr(ProviderFactory, "_providers_config"):
            raise RuntimeError("Providers configuration not loaded. Call 'load_providers' first.")

        provider_config = ProviderFactory._providers_config.get(name.value)
        if not provider_config:
            raise ValueError(f"Provider '{name}' not found in configuration.")

        username = os.getenv(f"{name.name}_USERNAME")
        password = os.getenv(f"{name.name}_PASSWORD")

        if not username or not password:
            raise ValueError(f"Credentials for '{name}' not found in environment variables.")

        # Create and return the Provider instance
        return Provider(
            name=name.value,
            imap_server=provider_config["imap_server"],
            smtp_server=provider_config["smtp_server"],
            imap_port=provider_config["imap_port"],
            smtp_port=provider_config["smtp_port"],
            username=username,
            password=password
        )
