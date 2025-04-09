"""
Key Manager Utility Module.

This module provides utilities for managing cryptographic keys
for blockchain interactions.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    import eth_account
    from eth_account import Account
    from web3 import Web3

    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False

logger = logging.getLogger(__name__)


class KeyManager:
    """
    Manages cryptographic keys for blockchain interactions.

    This class provides methods for loading, storing, and managing private keys,
    with a focus on secure key handling practices.

    Attributes:
        accounts: Dictionary mapping account addresses to Account instances.
    """

    def __init__(self):
        """Initialize the KeyManager."""
        self.accounts = {}
        logger.info("KeyManager initialized")

    def load_key_from_env(
        self, env_var_name: str, password_env_var: Optional[str] = None
    ) -> Optional[str]:
        """
        Load a private key from an environment variable.

        Args:
            env_var_name: Name of the environment variable containing the key.
            password_env_var: Optional name of environment variable with password.

        Returns:
            Account address or None if loading fails.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for key management")
            return None

        try:
            logger.info(f"Loading private key from environment variable {env_var_name}")

            # Get the private key from environment variable
            private_key = os.environ.get(env_var_name)
            if not private_key:
                logger.warning(f"Environment variable {env_var_name} not set or empty")
                return None

            # Check if key is encrypted and needs a password
            if private_key.startswith("{") and password_env_var:
                # Key might be a JSON keystore
                keystore_json = json.loads(private_key)
                password = os.environ.get(password_env_var)

                if not password:
                    logger.warning(f"Password environment variable {password_env_var} not set")
                    return None

                # Decrypt the keystore
                account = Account.from_key(
                    eth_account.account.decode_keyfile_json(keystore_json, password.encode())
                )
            else:
                # Direct private key
                account = Account.from_key(private_key)

            # Store the account
            address = account.address
            self.accounts[address] = account

            logger.info(f"Successfully loaded account {address}")
            return address

        except Exception as e:
            logger.error(f"Failed to load private key: {str(e)}")
            return None

    def load_key_from_file(
        self,
        file_path: str,
        password: Optional[str] = None,
        password_file: Optional[str] = None,
    ) -> Optional[str]:
        """
        Load a private key from a file.

        Args:
            file_path: Path to the key file.
            password: Optional password for encrypted keys.
            password_file: Optional path to a file containing the password.

        Returns:
            Account address or None if loading fails.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for key management")
            return None

        try:
            logger.info(f"Loading private key from file {file_path}")
            file_path = Path(file_path)

            if not file_path.exists():
                logger.error(f"Key file not found: {file_path}")
                return None

            # Read the file content
            with open(file_path, "r") as f:
                file_content = f.read().strip()

            # Check if it's a JSON keystore
            if file_content.startswith("{"):
                keystore_json = json.loads(file_content)

                # Get password if needed
                if password is None and password_file:
                    with open(password_file, "r") as f:
                        password = f.read().strip()

                if password is None:
                    logger.error("Password required for encrypted keystore")
                    return None

                # Decrypt the keystore
                account = Account.from_key(
                    eth_account.account.decode_keyfile_json(keystore_json, password.encode())
                )
            else:
                # Direct private key
                account = Account.from_key(file_content)

            # Store the account
            address = account.address
            self.accounts[address] = account

            logger.info(f"Successfully loaded account {address}")
            return address

        except Exception as e:
            logger.error(f"Failed to load private key from file: {str(e)}")
            return None

    def generate_account(self) -> str:
        """
        Generate a new Ethereum account.

        Returns:
            Address of the new account.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for key management")
            return None

        try:
            logger.info("Generating new Ethereum account")

            # Generate a new private key and account
            account = Account.create()

            # Store the account
            address = account.address
            self.accounts[address] = account

            logger.info(f"Generated new account {address}")
            return address

        except Exception as e:
            logger.error(f"Failed to generate account: {str(e)}")
            return None

    def export_account(
        self,
        address: str,
        file_path: Optional[str] = None,
        password: Optional[str] = None,
        encrypt: bool = True,
    ) -> Optional[Union[str, Dict]]:
        """
        Export an account to a file or return as a string/dictionary.

        Args:
            address: Address of the account to export.
            file_path: Optional path to save the exported key.
            password: Optional password for encryption.
            encrypt: Whether to encrypt the private key.

        Returns:
            Private key, keystore JSON, or None if export fails.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for key management")
            return None

        try:
            logger.info(f"Exporting account {address}")

            # Get the account
            account = self.accounts.get(address)
            if not account:
                logger.error(f"Account {address} not found")
                return None

            if encrypt and password:
                # Create an encrypted keystore
                keystore = account.encrypt(password)
                export_data = json.dumps(keystore)
            else:
                # Export the raw private key (as a hex string)
                export_data = account._private_key.hex()

            # Save to file if a path is provided
            if file_path:
                with open(file_path, "w") as f:
                    f.write(export_data)
                logger.info(f"Exported account to {file_path}")

            return export_data

        except Exception as e:
            logger.error(f"Failed to export account: {str(e)}")
            return None

    def sign_transaction(self, address: str, transaction: Dict[str, Any]) -> Optional[str]:
        """
        Sign a transaction with the private key of an account.

        Args:
            address: Address of the account to sign with.
            transaction: Transaction dictionary to sign.

        Returns:
            Signed transaction hex string or None if signing fails.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for transaction signing")
            return None

        try:
            logger.info(f"Signing transaction with account {address}")

            # Get the account
            account = self.accounts.get(address)
            if not account:
                logger.error(f"Account {address} not found")
                return None

            # Sign the transaction
            signed_tx = account.sign_transaction(transaction)

            # Return the raw transaction
            return signed_tx.rawTransaction.hex()

        except Exception as e:
            logger.error(f"Failed to sign transaction: {str(e)}")
            return None

    def sign_message(self, address: str, message: str) -> Optional[Dict[str, str]]:
        """
        Sign a message with the private key of an account.

        Args:
            address: Address of the account to sign with.
            message: Message to sign.

        Returns:
            Dictionary with signature details or None if signing fails.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for message signing")
            return None

        try:
            logger.info(f"Signing message with account {address}")

            # Get the account
            account = self.accounts.get(address)
            if not account:
                logger.error(f"Account {address} not found")
                return None

            # Sign the message
            message_hash = eth_account.messages.encode_defunct(text=message)
            signed_message = account.sign_message(message_hash)

            # Return the signature details
            return {
                "message": message,
                "messageHash": signed_message.messageHash.hex(),
                "signature": signed_message.signature.hex(),
                "r": signed_message.r,
                "s": signed_message.s,
                "v": signed_message.v,
            }

        except Exception as e:
            logger.error(f"Failed to sign message: {str(e)}")
            return None

    def get_private_key(self, address: str) -> Optional[str]:
        """
        Get the private key for an account.

        Warning: Use with caution! Private keys should be handled securely.

        Args:
            address: Address of the account.

        Returns:
            Private key as a hex string or None if not found.
        """
        if not WEB3_AVAILABLE:
            logger.error("web3.py is required for key management")
            return None

        try:
            # Get the account
            account = self.accounts.get(address)
            if not account:
                logger.error(f"Account {address} not found")
                return None

            # Return the private key
            return account._private_key.hex()

        except Exception as e:
            logger.error(f"Failed to get private key: {str(e)}")
            return None
