"""
Blockchain Verifier Module.

This module provides the BlockchainVerifier class, which orchestrates interactions
with various blockchain components including contract validation, data provenance
tracking, and zero-knowledge proof generation.
"""

import logging
from typing import Any, Dict, List, Optional

from .contract_validator import ContractValidator
from .blockchain_exceptions import BlockchainError
from .dao_manager import DAOManager
from .nft_manager import NFTManager
from .ranking_manager import RankingManager
from .token_manager import TokenManager
from .provenance_tracker import ProvenanceTracker
from .zk_prover import ZKProver

logger = logging.getLogger(__name__)


class BlockchainVerifier:
    """
    Orchestrates interactions with blockchain components for verification, provenance tracking,
    and management of blockchain assets.

    The BlockchainVerifier serves as the central coordinator for all blockchain-related
    operations, providing a unified interface for the various specialized components.

    Attributes:
        contract_validator (ContractValidator): Component for validating smart contracts.
        provenance_tracker (ProvenanceTracker): Component for tracking data provenance.
        zk_prover (ZKProver): Component for generating and verifying zero-knowledge proofs.
        dao_manager (DAOManager): Component for interacting with decentralized autonomous organizations.
        nft_manager (NFTManager): Component for managing non-fungible tokens.
        ranking_manager (RankingManager): Component for decentralized ranking systems.
        token_manager (TokenManager): Component for managing fungible tokens.
    """

    def __init__(
        self,
        ethereum_rpc_url: Optional[str] = None,
        use_zk_proofs: bool = False,
        provenance_mode: str = "on-chain",
        chain_id: Optional[int] = None,
        default_account: Optional[str] = None,
        private_key_env_var: Optional[str] = None,
        contract_addresses: Optional[Dict[str, str]] = None,
        abi_directory: Optional[str] = None,
    ):
        """
        Initialize the BlockchainVerifier with its component parts.

        Args:
            ethereum_rpc_url: URL for the Ethereum node to connect to.
            use_zk_proofs: Whether to enable zero-knowledge proofs functionality.
            provenance_mode: Mode for provenance tracking ('on-chain' or 'in-memory').
            chain_id: ID of the blockchain network to connect to.
            default_account: Default Ethereum account address to use for transactions.
            private_key_env_var: Name of environment variable containing the private key.
            contract_addresses: Dictionary mapping contract names to their addresses.
            abi_directory: Directory path containing contract ABI files.

        Raises:
            BlockchainError: If there are issues initializing blockchain components.
        """
        try:
            logger.info("Initializing BlockchainVerifier")

            # Initialize core components
            self.contract_validator = ContractValidator(
                ethereum_rpc_url=ethereum_rpc_url,
                chain_id=chain_id,
                default_account=default_account,
                private_key_env_var=private_key_env_var,
                contract_addresses=contract_addresses or {},
                abi_directory=abi_directory,
            )

            self.provenance_tracker = ProvenanceTracker(
                mode=provenance_mode, contract_validator=self.contract_validator
            )

            self.zk_prover = ZKProver(enabled=use_zk_proofs)

            # Initialize manager components
            self.dao_manager = DAOManager(contract_validator=self.contract_validator)
            self.nft_manager = NFTManager(contract_validator=self.contract_validator)
            self.ranking_manager = RankingManager(contract_validator=self.contract_validator)
            self.token_manager = TokenManager(contract_validator=self.contract_validator)

            logger.info("BlockchainVerifier initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize BlockchainVerifier: {str(e)}")
            raise BlockchainError(f"Failed to initialize blockchain components: {str(e)}") from e

    def verify_data(
        self,
        data: Any,
        verification_type: str = "hash",
        contract_name: Optional[str] = None,
        generate_proof: bool = False,
    ) -> Dict[str, Any]:
        """
        Verify data using the appropriate verification method.

        Args:
            data: The data to verify.
            verification_type: Type of verification to perform ('hash', 'signature', 'merkle', etc.).
            contract_name: Optional name of contract to use for verification.
            generate_proof: Whether to generate a zero-knowledge proof.

        Returns:
            Dictionary containing verification results.

        Raises:
            BlockchainError: If verification fails.
        """
        try:
            logger.info(f"Verifying data using {verification_type} method")

            # Track data provenance
            provenance_id = self.provenance_tracker.track(
                data=data,
                action="verify",
                metadata={"verification_type": verification_type},
            )

            # Perform contract verification if needed
            verification_result = {}
            if contract_name:
                verification_result = self.contract_validator.verify_data(
                    data=data,
                    verification_type=verification_type,
                    contract_name=contract_name,
                )

            # Generate ZK proof if requested
            proof = None
            if generate_proof:
                proof = self.zk_prover.generate_proof(
                    data=data, verification_type=verification_type
                )

            result = {
                "verified": (
                    True if not contract_name else verification_result.get("verified", False)
                ),
                "provenance_id": provenance_id,
                "timestamp": self.provenance_tracker.get_timestamp(),
            }

            if proof:
                result["proof"] = proof

            logger.info("Data verification completed successfully")
            return result

        except Exception as e:
            logger.error(f"Data verification failed: {str(e)}")
            raise BlockchainError(f"Failed to verify data: {str(e)}") from e

    def submit_transaction(
        self, contract_name: str, function_name: str, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Submit a transaction to a smart contract.

        Args:
            contract_name: Name of the contract to interact with.
            function_name: Name of the function to call.
            *args: Positional arguments for the contract function.
            **kwargs: Keyword arguments including transaction parameters.

        Returns:
            Dictionary containing transaction results.

        Raises:
            BlockchainError: If the transaction fails.
        """
        try:
            logger.info(f"Submitting transaction to {contract_name}.{function_name}")

            # Track transaction provenance
            provenance_id = self.provenance_tracker.track(
                data={
                    "contract_name": contract_name,
                    "function_name": function_name,
                    "args": args,
                    "kwargs": {k: v for k, v in kwargs.items() if k != "private_key"},
                },
                action="transaction",
                metadata={"type": "contract_interaction"},
            )

            # Submit the transaction
            tx_result = self.contract_validator.call_function(
                contract_name=contract_name,
                function_name=function_name,
                *args,
                **kwargs,
            )

            result = {
                "success": True,
                "provenance_id": provenance_id,
                "transaction_hash": tx_result.get("transaction_hash"),
                "result": tx_result.get("result"),
            }

            logger.info("Transaction submitted successfully")
            return result

        except Exception as e:
            logger.error(f"Transaction failed: {str(e)}")
            raise BlockchainError(f"Failed to submit transaction: {str(e)}") from e

    def get_provenance_history(
        self,
        data_id: Optional[str] = None,
        action_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve provenance history for data or actions.

        Args:
            data_id: Optional ID of data to retrieve history for.
            action_type: Optional type of action to filter by.
            limit: Maximum number of records to return.

        Returns:
            List of provenance records.
        """
        logger.info("Retrieving provenance history")
        return self.provenance_tracker.get_history(
            data_id=data_id, action_type=action_type, limit=limit
        )

    def generate_zk_proof(self, data: Any, proof_type: str) -> Dict[str, Any]:
        """
        Generate a zero-knowledge proof for the given data.

        Args:
            data: Data to generate proof for.
            proof_type: Type of proof to generate.

        Returns:
            Dictionary containing the generated proof.

        Raises:
            BlockchainError: If proof generation fails.
        """
        try:
            logger.info(f"Generating {proof_type} zero-knowledge proof")

            # Track the proof generation in provenance
            self.provenance_tracker.track(
                data=data, action="generate_proof", metadata={"proof_type": proof_type}
            )

            # Generate the proof
            proof = self.zk_prover.generate_proof(data=data, proof_type=proof_type)

            logger.info("Zero-knowledge proof generated successfully")
            return proof

        except Exception as e:
            logger.error(f"Proof generation failed: {str(e)}")
            raise BlockchainError(f"Failed to generate zero-knowledge proof: {str(e)}") from e

    def verify_zk_proof(self, proof: Dict[str, Any], data: Any) -> bool:
        """
        Verify a zero-knowledge proof against the given data.

        Args:
            proof: The proof to verify.
            data: The data the proof was generated for.

        Returns:
            Boolean indicating whether the proof is valid.

        Raises:
            BlockchainError: If proof verification fails.
        """
        try:
            logger.info("Verifying zero-knowledge proof")

            # Track the verification in provenance
            self.provenance_tracker.track(
                data=data, action="verify_proof", metadata={"proof": proof}
            )

            # Verify the proof
            is_valid = self.zk_prover.verify_proof(proof=proof, data=data)

            logger.info(f"Proof verification result: {is_valid}")
            return is_valid

        except Exception as e:
            logger.error(f"Proof verification failed: {str(e)}")
            raise BlockchainError(f"Failed to verify zero-knowledge proof: {str(e)}") from e
