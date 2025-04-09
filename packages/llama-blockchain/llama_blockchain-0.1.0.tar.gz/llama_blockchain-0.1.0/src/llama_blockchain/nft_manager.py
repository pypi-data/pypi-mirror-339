"""
NFT Manager Module.

This module provides the NFTManager class for interacting with
non-fungible tokens (NFTs) on the blockchain, including ERC-721 and ERC-1155.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..contract_validator import ContractValidator
from ..exceptions.blockchain_exceptions import BlockchainError

logger = logging.getLogger(__name__)


class NFTManager:
    """
    Manages interactions with non-fungible tokens (NFTs).

    This class provides methods for NFT transfers, approvals, metadata retrieval,
    and other operations related to NFT standards like ERC-721 and ERC-1155.

    Attributes:
        contract_validator: ContractValidator instance for blockchain interactions.
    """

    def __init__(self, contract_validator: ContractValidator):
        """
        Initialize the NFTManager.

        Args:
            contract_validator: ContractValidator instance for blockchain interactions.
        """
        self.contract_validator = contract_validator
        logger.info("NFTManager initialized")

    def get_owner(self, nft_contract: str, token_id: int) -> str:
        """
        Get the owner of an NFT.

        Args:
            nft_contract: Name or address of the NFT contract.
            token_id: ID of the token to check.

        Returns:
            Address of the token owner.

        Raises:
            BlockchainError: If owner retrieval fails.
        """
        try:
            logger.info(f"Getting owner of token ID {token_id} in contract {nft_contract}")

            result = self.contract_validator.call_function(nft_contract, "ownerOf", token_id)

            return result.get("result", "")

        except Exception as e:
            logger.error(f"Failed to get NFT owner: {str(e)}")
            raise BlockchainError(f"Failed to get NFT owner: {str(e)}") from e

    def get_token_balance(
        self, nft_contract: str, account: str, token_id: Optional[int] = None
    ) -> int:
        """
        Get the NFT balance of an account.

        Args:
            nft_contract: Name or address of the NFT contract.
            account: Address to check balance for.
            token_id: Optional token ID for ERC-1155 tokens.

        Returns:
            Token balance.

        Raises:
            BlockchainError: If balance retrieval fails.
        """
        try:
            if token_id is not None:
                # ERC-1155 balance check
                logger.info(f"Getting ERC-1155 balance for token ID {token_id}, account {account}")

                result = self.contract_validator.call_function(
                    nft_contract, "balanceOf", account, token_id
                )
            else:
                # ERC-721 balance check
                logger.info(f"Getting ERC-721 balance for account {account}")

                result = self.contract_validator.call_function(nft_contract, "balanceOf", account)

            return result.get("result", 0)

        except Exception as e:
            logger.error(f"Failed to get NFT balance: {str(e)}")
            raise BlockchainError(f"Failed to get NFT balance: {str(e)}") from e

    def transfer(
        self,
        nft_contract: str,
        to_address: str,
        token_id: int,
        amount: int = 1,
        is_erc1155: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Transfer an NFT to a recipient.

        Args:
            nft_contract: Name or address of the NFT contract.
            to_address: Recipient address.
            token_id: ID of the token to transfer.
            amount: Amount of tokens to transfer (for ERC-1155).
            is_erc1155: Whether the contract is ERC-1155.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing transaction details.

        Raises:
            BlockchainError: If transfer fails.
        """
        try:
            if is_erc1155:
                logger.info(f"Transferring ERC-1155 token ID {token_id} to {to_address}")

                # Get the sender address
                from_address = kwargs.get("from", self.contract_validator.default_account)
                if not from_address:
                    raise BlockchainError("No sender address provided or default account set")

                # ERC-1155 transfer
                result = self.contract_validator.call_function(
                    nft_contract,
                    "safeTransferFrom",
                    from_address,
                    to_address,
                    token_id,
                    amount,
                    b"",
                    transaction=True,
                    **kwargs,
                )
            else:
                logger.info(f"Transferring ERC-721 token ID {token_id} to {to_address}")

                # Get the sender address
                from_address = kwargs.get("from", self.contract_validator.default_account)
                if not from_address:
                    raise BlockchainError("No sender address provided or default account set")

                # ERC-721 transfer
                result = self.contract_validator.call_function(
                    nft_contract,
                    "safeTransferFrom",
                    from_address,
                    to_address,
                    token_id,
                    transaction=True,
                    **kwargs,
                )

            return result

        except Exception as e:
            logger.error(f"NFT transfer failed: {str(e)}")
            raise BlockchainError(f"Failed to transfer NFT: {str(e)}") from e

    def approve(
        self, nft_contract: str, to_address: str, token_id: int, **kwargs
    ) -> Dict[str, Any]:
        """
        Approve an address to transfer a specific NFT.

        Args:
            nft_contract: Name or address of the NFT contract.
            to_address: Address to approve.
            token_id: ID of the token to approve.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing transaction details.

        Raises:
            BlockchainError: If approval fails.
        """
        try:
            logger.info(f"Approving {to_address} for token ID {token_id}")

            result = self.contract_validator.call_function(
                nft_contract, "approve", to_address, token_id, transaction=True, **kwargs
            )

            return result

        except Exception as e:
            logger.error(f"NFT approval failed: {str(e)}")
            raise BlockchainError(f"Failed to approve NFT transfer: {str(e)}") from e

    def get_approved(self, nft_contract: str, token_id: int) -> str:
        """
        Get the approved address for a specific NFT.

        Args:
            nft_contract: Name or address of the NFT contract.
            token_id: ID of the token to check.

        Returns:
            Address approved for the token.

        Raises:
            BlockchainError: If retrieval fails.
        """
        try:
            logger.info(f"Getting approved address for token ID {token_id}")

            result = self.contract_validator.call_function(nft_contract, "getApproved", token_id)

            return result.get("result", "")

        except Exception as e:
            logger.error(f"Failed to get approved address: {str(e)}")
            raise BlockchainError(f"Failed to get approved address: {str(e)}") from e

    def set_approval_for_all(
        self, nft_contract: str, operator: str, approved: bool, **kwargs
    ) -> Dict[str, Any]:
        """
        Set or revoke approval for an operator to manage all NFTs.

        Args:
            nft_contract: Name or address of the NFT contract.
            operator: Address to grant/revoke operator status.
            approved: Whether to approve or revoke.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing transaction details.

        Raises:
            BlockchainError: If approval setting fails.
        """
        try:
            logger.info(f"Setting approval for all tokens to {operator}: {approved}")

            result = self.contract_validator.call_function(
                nft_contract, "setApprovalForAll", operator, approved, transaction=True, **kwargs
            )

            return result

        except Exception as e:
            logger.error(f"Setting approval for all failed: {str(e)}")
            raise BlockchainError(f"Failed to set approval for all: {str(e)}") from e

    def is_approved_for_all(self, nft_contract: str, owner: str, operator: str) -> bool:
        """
        Check if an operator is approved for all of an owner's NFTs.

        Args:
            nft_contract: Name or address of the NFT contract.
            owner: Address of the token owner.
            operator: Address of the operator to check.

        Returns:
            Boolean indicating approval status.

        """
        try:
            result = self.contract_validator.call_function(
                nft_contract, "isApprovedForAll", owner, operator
            )

            return result.get("result", False)

        except Exception as e:
            logger.error(f"Failed to check approval for all: {str(e)}")
            raise BlockchainError(f"Failed to check approval for all: {str(e)}") from e
