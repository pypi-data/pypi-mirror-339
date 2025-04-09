"""
Settings Module.

This module provides configuration settings for the llama_blockchain package,
allowing for customization of blockchain connectivity, logging, and other parameters.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Logging configuration
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Blockchain configuration
DEFAULT_ETH_RPC_URL = "http://localhost:8545"
DEFAULT_CHAIN_ID = 1  # Ethereum Mainnet

# Contract data directories
DEFAULT_ABI_DIRECTORY = "abi"
DEFAULT_CONTRACT_CONFIG_FILE = "contracts.json"

# Other defaults
DEFAULT_TIMEOUT = 120  # Seconds
DEFAULT_GAS_LIMIT_MULTIPLIER = 1.1  # 10% safety margin
DEFAULT_SIMULATION_MODE = False


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a file or environment variables.

    Args:
        config_file: Optional path to a JSON configuration file.

    Returns:
        Dictionary containing configuration settings.
    """
    # Start with default configuration
    config = {
        "logging": {
            "level": os.environ.get("LLAMA_BLOCKCHAIN_LOG_LEVEL", DEFAULT_LOG_LEVEL),
            "format": DEFAULT_LOG_FORMAT,
        },
        "blockchain": {
            "ethereum_rpc_url": os.environ.get("ETHEREUM_RPC_URL", DEFAULT_ETH_RPC_URL),
            "chain_id": int(os.environ.get("ETHEREUM_CHAIN_ID", DEFAULT_CHAIN_ID)),
            "default_account": os.environ.get("ETHEREUM_DEFAULT_ACCOUNT"),
            "private_key_env_var": os.environ.get("ETHEREUM_PRIVATE_KEY_ENV_VAR"),
            "simulation_mode": os.environ.get(
                "LLAMA_BLOCKCHAIN_SIMULATION", DEFAULT_SIMULATION_MODE
            ),
        },
        "contracts": {
            "abi_directory": os.environ.get("LLAMA_BLOCKCHAIN_ABI_DIR", DEFAULT_ABI_DIRECTORY),
            "addresses": {},
        },
        "transaction": {
            "timeout": int(os.environ.get("LLAMA_BLOCKCHAIN_TX_TIMEOUT", DEFAULT_TIMEOUT)),
            "gas_limit_multiplier": float(
                os.environ.get("LLAMA_BLOCKCHAIN_GAS_MULTIPLIER", DEFAULT_GAS_LIMIT_MULTIPLIER)
            ),
        },
        "provenance": {
            "mode": os.environ.get("LLAMA_BLOCKCHAIN_PROVENANCE_MODE", "in-memory"),
            "contract_name": os.environ.get("LLAMA_BLOCKCHAIN_PROVENANCE_CONTRACT"),
        },
        "zk_proofs": {
            "enabled": os.environ.get("LLAMA_BLOCKCHAIN_ZK_ENABLED", "false").lower() == "true"
        },
    }

    # Load from configuration file if provided
    if config_file:
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, "r") as f:
                    file_config = json.load(f)

                # Merge configurations (simple recursive update)
                _merge_configs(config, file_config)
        except Exception as e:
            logging.warning(f"Failed to load configuration from {config_file}: {str(e)}")

    # Load contract addresses from separate file if it exists
    contract_config_file = os.environ.get(
        "LLAMA_BLOCKCHAIN_CONTRACT_CONFIG", DEFAULT_CONTRACT_CONFIG_FILE
    )
    try:
        contract_config_path = Path(contract_config_file)
        if contract_config_path.exists():
            with open(contract_config_path, "r") as f:
                contract_config = json.load(f)

            # Update contract addresses
            if "addresses" in contract_config:
                config["contracts"]["addresses"].update(contract_config["addresses"])
    except Exception as e:
        logging.warning(
            f"Failed to load contract configuration from {contract_config_file}: {str(e)}"
        )

    return config


def _merge_configs(base_config: Dict[str, Any], overlay_config: Dict[str, Any]) -> None:
    """
    Recursively merge overlay_config into base_config.

    Args:
        base_config: Base configuration dictionary to update.
        overlay_config: Overlay configuration to merge into base.
    """
    for key, value in overlay_config.items():
        if key in base_config and isinstance(base_config[key], dict) and isinstance(value, dict):
            # Recursively merge dictionaries
            _merge_configs(base_config[key], value)
        else:
            # Replace or add values
            base_config[key] = value


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Configure logging based on configuration.

    Args:
        config: Configuration dictionary.
    """
    log_config = config.get("logging", {})
    log_level = log_config.get("level", DEFAULT_LOG_LEVEL)
    log_format = log_config.get("format", DEFAULT_LOG_FORMAT)

    # Convert string log level to logging constant
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    level = level_map.get(log_level.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(level=level, format=log_format)

    # Configure package logger
    logger = logging.getLogger("llama_blockchain")
    logger.setLevel(level)

    # Create console handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)

    logger.info(f"Logging configured with level: {log_level}")
