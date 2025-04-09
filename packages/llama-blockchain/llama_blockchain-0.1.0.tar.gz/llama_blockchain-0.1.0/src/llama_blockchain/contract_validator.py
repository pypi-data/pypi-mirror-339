"""
Contract Validator Module.

This module provides the ContractValidator class for interacting with blockchain
smart contracts, including validation, function calls, and transaction submission.
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

try:
    from eth_account import Account
    from eth_account.signers.local import LocalAccount
    from web3 import Web3
    from web3.exceptions import ContractLogicError, InvalidAddress
    from web3.middleware import geth_poa_middleware

    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False

from .exceptions.blockchain_exceptions import ContractValidationError, TransactionError

logger = logging.getLogger(__name__)


class ContractValidator:
    """
    Handles interaction with blockchain smart contracts, including validation,
    function calls, and transaction submission.

    This class provides a centralized interface for all contract interactions,
    handling web3 connectivity, transaction signing, and error handling.

    Attributes:
        web3: Web3 instance for connecting to Ethereum.
        chain_id: ID of the connected blockchain network.
        contracts: Dictionary of loaded contract instances.
        default_account: Default account address for transactions.
        signer_account: Account instance for signing transactions.
    """

    def __init__(
        self,
        ethereum_rpc_url: Optional[str] = None,
        chain_id: Optional[int] = None,
        default_account: Optional[str] = None,
        private_key_env_var: Optional[str] = None,
        contract_addresses: Optional[Dict[str, str]] = None,
        abi_directory: Optional[str] = None,
        simulation_mode: bool = False,
    ):
        """
        Initialize the ContractValidator for blockchain interactions.

        Args:
            ethereum_rpc_url: URL for the Ethereum node to connect to.
            chain_id: ID of the blockchain network to connect to.
            default_account: Default Ethereum account address to use for transactions.
            private_key_env_var: Name of environment variable containing the private key.
            contract_addresses: Dictionary mapping contract names to their addresses.
            abi_directory: Directory path containing contract ABI files.
            simulation_mode: Whether to run in simulation mode without blockchain connection.

        Raises:
            ContractValidationError: If web3 is not available or connection fails.
        """
        self.simulation_mode = simulation_mode
        self.contracts = {}
        self.default_account = default_account
        self.signer_account = None
        self.chain_id = chain_id

        # Initialize web3 connection if not in simulation mode
        if not simulation_mode:
            if not WEB3_AVAILABLE:
                logger.warning(
                    "Web3.py is not available. Running in limited functionality mode. "
                    "Install web3.py to enable full Ethereum connectivity."
                )
                return

            if not ethereum_rpc_url:
                ethereum_rpc_url = os.environ.get("ETHEREUM_RPC_URL")

            if not ethereum_rpc_url:
                logger.warning(
                    "No Ethereum RPC URL provided. Running in limited functionality mode. "
                    "Set ETHEREUM_RPC_URL environment variable to enable full functionality."
                )
                return

            try:
                logger.info(f"Connecting to Ethereum node at {ethereum_rpc_url}")
                self.web3 = Web3(Web3.HTTPProvider(ethereum_rpc_url))

                # Handle POA chains like BSC, Polygon, etc.
                self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

                if not self.web3.is_connected():
                    logger.warning("Failed to connect to Ethereum node")
                    return

                logger.info("Successfully connected to Ethereum node")

                # Set up the chain ID
                if not chain_id:
                    self.chain_id = self.web3.eth.chain_id
                    logger.info(f"Using chain ID from node: {self.chain_id}")

                # Set up the default account
                if not default_account:
                    if self.web3.eth.accounts:
                        self.default_account = self.web3.eth.accounts[0]
                        logger.info(f"Using default account from node: {self.default_account}")

                # Set up the signer account if private key is available
                if private_key_env_var:
                    private_key = os.environ.get(private_key_env_var)
                    if private_key:
                        self.signer_account = Account.from_key(private_key)
                        if not default_account:
                            self.default_account = self.signer_account.address
                        logger.info("Loaded signer account from private key")

                # Load contract ABIs and addresses
                if contract_addresses and abi_directory:
                    self._load_contracts(contract_addresses, abi_directory)

            except Exception as e:
                logger.error(f"Error initializing Web3 connection: {str(e)}")
                raise ContractValidationError(
                    f"Failed to initialize Ethereum connection: {str(e)}"
                ) from e
        else:
            logger.info("Running in simulation mode - no blockchain connection required")

    def _load_contracts(self, contract_addresses: Dict[str, str], abi_directory: str) -> None:
        """
        Load contract ABIs and create contract instances.

        Args:
            contract_addresses: Dictionary mapping contract names to addresses.
            abi_directory: Directory containing ABI JSON files.

        Raises:
            ContractValidationError: If contract loading fails.
        """
        if not WEB3_AVAILABLE or self.simulation_mode:
            logger.info("Skipping contract loading in simulation mode or without web3")
            return

        try:
            logger.info(f"Loading contracts from {abi_directory}")
            abi_dir = Path(abi_directory)

            for contract_name, address in contract_addresses.items():
                abi_file = abi_dir / f"{contract_name}.json"

                if not abi_file.exists():
                    logger.warning(f"ABI file not found for contract: {contract_name}")
                    continue

                with open(abi_file, "r") as f:
                    abi = json.load(f)

                # Create the contract instance
                if Web3.is_address(address):
                    contract = self.web3.eth.contract(
                        address=Web3.to_checksum_address(address), abi=abi
                    )
                    self.contracts[contract_name] = contract
                    logger.info(f"Loaded contract {contract_name} at {address}")
                else:
                    logger.warning(f"Invalid address for contract {contract_name}: {address}")

        except Exception as e:
            logger.error(f"Error loading contracts: {str(e)}")
            raise ContractValidationError(f"Failed to load contract ABIs: {str(e)}") from e

    def add_contract(self, name: str, address: str, abi: Union[str, List, Dict]) -> None:
        """
        Add a contract to the validator.

        Args:
            name: Name to identify the contract.
            address: Ethereum address of the contract.
            abi: Contract ABI as string, list, or dict.

        Raises:
            ContractValidationError: If the contract cannot be added.
        """
        if self.simulation_mode or not WEB3_AVAILABLE:
            logger.info(f"Added contract {name} in simulation mode")
            self.contracts[name] = {"address": address, "abi": abi}
            return

        try:
            if isinstance(abi, str):
                abi = json.loads(abi)

            contract = self.web3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)

            self.contracts[name] = contract
            logger.info(f"Added contract {name} at {address}")

        except Exception as e:
            logger.error(f"Failed to add contract {name}: {str(e)}")
            raise ContractValidationError(f"Failed to add contract {name}: {str(e)}") from e

    def call_function(
        self, contract_name: str, function_name: str, *args, transaction: bool = False, **kwargs
    ) -> Dict[str, Any]:
        """
        Call a function on a smart contract.

        Args:
            contract_name: Name of the contract to call.
            function_name: Name of the function to call.
            *args: Positional arguments for the contract function.
            transaction: Whether this is a state-changing transaction.
            **kwargs: Additional keyword arguments including transaction parameters.

        Returns:
            Dictionary containing the result or transaction details.

        Raises:
            ContractValidationError: If the function call fails.
        """
        if self.simulation_mode:
            logger.info(f"Simulating function call: {contract_name}.{function_name}")
            return self._simulate_function_call(contract_name, function_name, *args, **kwargs)

        if not WEB3_AVAILABLE:
            logger.error("Web3.py is required for contract function calls")
            raise ContractValidationError("Web3.py is required for contract function calls")

        if contract_name not in self.contracts:
            logger.error(f"Contract {contract_name} not found")
            raise ContractValidationError(f"Contract {contract_name} not found")

        try:
            logger.info(f"Calling function: {contract_name}.{function_name}")
            contract = self.contracts[contract_name]

            # Extract transaction parameters
            tx_params = {}
            for key in ["from", "gas", "gasPrice", "value", "nonce"]:
                if key in kwargs:
                    tx_params[key] = kwargs.pop(key)

            # Set default 'from' address if not provided
            if "from" not in tx_params and self.default_account:
                tx_params["from"] = self.default_account

            # Check if this is a read or write operation
            if not transaction:
                # Read operation (call)
                logger.debug(f"Performing read call to {function_name} with args: {args}")
                function = getattr(contract.functions, function_name)
                result = function(*args, **kwargs).call(tx_params)
                return {"success": True, "result": result}
            else:
                # Write operation (transaction)
                return self._submit_transaction(contract, function_name, args, kwargs, tx_params)

        except ContractLogicError as e:
            logger.error(f"Contract logic error in {function_name}: {str(e)}")
            raise ContractValidationError(f"Contract logic error: {str(e)}") from e
        except Exception as e:
            logger.error(f"Error calling {function_name}: {str(e)}")
            raise ContractValidationError(
                f"Failed to call function {function_name}: {str(e)}"
            ) from e

    def _submit_transaction(
        self,
        contract,
        function_name: str,
        args: Tuple,
        kwargs: Dict[str, Any],
        tx_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Submit a transaction to a smart contract.

        Args:
            contract: Web3 contract instance.
            function_name: Name of the function to call.
            args: Positional arguments for the function.
            kwargs: Keyword arguments for the function.
            tx_params: Transaction parameters.

        Returns:
            Dictionary containing transaction details.

        Raises:
            TransactionError: If the transaction fails.
        """
        try:
            logger.info(f"Submitting transaction to {function_name}")
            function = getattr(contract.functions, function_name)
            function_call = function(*args, **kwargs)

            # Get the private key for signing, if available
            private_key = kwargs.pop("private_key", None)

            # Use the signer account if available and no specific private key was provided
            if not private_key and self.signer_account:
                private_key = self.signer_account._private_key

            # If we have a private key, sign the transaction and send it
            if private_key:
                logger.debug("Signing transaction with private key")

                # Ensure we have all needed transaction parameters
                if "gas" not in tx_params:
                    tx_params["gas"] = self.web3.eth.estimate_gas(
                        {
                            **tx_params,
                            "to": contract.address,
                            "data": function_call._encode_transaction_data(),
                        }
                    )

                if "gasPrice" not in tx_params:
                    tx_params["gasPrice"] = self.web3.eth.gas_price

                if "nonce" not in tx_params and "from" in tx_params:
                    tx_params["nonce"] = self.web3.eth.get_transaction_count(tx_params["from"])

                # Add chain ID if available
                if self.chain_id:
                    tx_params["chainId"] = self.chain_id

                # Build and sign the transaction
                unsigned_tx = function_call.build_transaction(tx_params)
                signed_tx = self.web3.eth.account.sign_transaction(
                    unsigned_tx, private_key=private_key
                )

                # Send the signed transaction
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

                return {
                    "success": receipt.status == 1,
                    "transaction_hash": tx_hash.hex(),
                    "receipt": dict(receipt),
                    "block_number": receipt.blockNumber,
                }
            else:
                # No private key, use the node's account (requires unlocked account)
                logger.debug("Submitting transaction using node's account")
                tx_hash = function_call.transact(tx_params)
                receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

                return {
                    "success": receipt.status == 1,
                    "transaction_hash": tx_hash.hex(),
                    "receipt": dict(receipt),
                    "block_number": receipt.blockNumber,
                }

        except Exception as e:
            logger.error(f"Transaction error in {function_name}: {str(e)}")
            raise TransactionError(f"Failed to submit transaction: {str(e)}") from e

    def _simulate_function_call(
        self, contract_name: str, function_name: str, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Simulate a function call without connecting to blockchain.

        Args:
            contract_name: Name of the contract.
            function_name: Name of the function to call.
        """
        # Simulation logic would go here
        logger.info(f"Simulating call to {contract_name}.{function_name}")
        return {"simulation_result": "ok", "args": args, "kwargs": kwargs}  # Placeholder
