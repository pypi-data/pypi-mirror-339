"""
DAO Manager Module.

This module provides the DAOManager class for interacting with
decentralized autonomous organizations (DAOs) on the blockchain.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..contract_validator import ContractValidator
from ..exceptions.blockchain_exceptions import BlockchainError

logger = logging.getLogger(__name__)


class DAOManager:
    """
    Manages interactions with decentralized autonomous organizations (DAOs).

    This class provides methods for DAO proposal creation, voting, and execution,
    as well as governance token management and delegation.

    Attributes:
        contract_validator: ContractValidator instance for blockchain interactions.
    """

    def __init__(self, contract_validator: ContractValidator):
        """
        Initialize the DAOManager.

        Args:
            contract_validator: ContractValidator instance for blockchain interactions.
        """
        self.contract_validator = contract_validator
        logger.info("DAOManager initialized")

    def create_proposal(
        self,
        dao_contract: str,
        title: str,
        description: str,
        targets: List[str],
        values: List[int],
        signatures: List[str],
        calldatas: List[str],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Create a new proposal in a DAO.

        Args:
            dao_contract: Name or address of the DAO governance contract.
            title: Title of the proposal.
            description: Description of the proposal.
            targets: List of contract addresses that will be called.
            values: List of ETH values to send with each call.
            signatures: List of function signatures to call.
            calldatas: List of encoded function parameters.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing proposal creation details.

        Raises:
            BlockchainError: If proposal creation fails.
        """
        try:
            logger.info(f"Creating DAO proposal: {title}")
            formatted_description = f"{title}\n\n{description}"

            result = self.contract_validator.call_function(
                dao_contract,  # Positional
                "propose",  # Positional
                targets,  # Positional
                values,  # Positional
                signatures,  # Positional
                calldatas,  # Positional
                formatted_description,  # Positional
                transaction=True,  # Keyword
                **kwargs,
            )

            return result

        except Exception as e:
            logger.error(f"DAO proposal creation failed: {str(e)}")
            raise BlockchainError(f"Failed to create DAO proposal: {str(e)}") from e

    def vote(
        self,
        dao_contract: str,
        proposal_id: int,
        support: int,
        reason: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Vote on a DAO proposal.

        Args:
            dao_contract: Name or address of the DAO governance contract.
            proposal_id: ID of the proposal to vote on.
            support: Vote type (0=against, 1=for, 2=abstain).
            reason: Optional explanation for the vote.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing voting details.

        Raises:
            BlockchainError: If voting fails.
        """
        try:
            logger.info(f"Voting on DAO proposal {proposal_id} with support={support}")

            if reason:
                # Vote with reason
                result = self.contract_validator.call_function(
                    dao_contract,  # Positional
                    "castVoteWithReason",  # Positional
                    proposal_id,  # Positional
                    support,  # Positional
                    reason,  # Positional
                    transaction=True,  # Keyword
                    **kwargs,
                )
            else:
                # Simple vote
                result = self.contract_validator.call_function(
                    dao_contract,  # Positional
                    "castVote",  # Positional
                    proposal_id,  # Positional
                    support,  # Positional
                    transaction=True,  # Keyword
                    **kwargs,
                )

            return result

        except Exception as e:
            logger.error(f"DAO voting failed: {str(e)}")
            raise BlockchainError(f"Failed to vote on DAO proposal: {str(e)}") from e

    def delegate(self, governance_token: str, delegate_address: str, **kwargs) -> Dict[str, Any]:
        """
        Delegate voting power to an address.

        Args:
            governance_token: Name or address of the governance token contract.
            delegate_address: Address to delegate voting power to.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing delegation details.

        Raises:
            BlockchainError: If delegation fails.
        """
        try:
            logger.info(f"Delegating voting power to {delegate_address}")

            result = self.contract_validator.call_function(
                governance_token,  # Positional
                "delegate",  # Positional
                delegate_address,  # Positional
                transaction=True,  # Keyword
                **kwargs,
            )

            return result

        except Exception as e:
            logger.error(f"Delegation failed: {str(e)}")
            raise BlockchainError(f"Failed to delegate voting power: {str(e)}") from e

    def get_voting_power(
        self, governance_token: str, account: str, block_number: Optional[int] = None
    ) -> int:
        """
        Get the voting power of an address.

        Args:
            governance_token: Name or address of the governance token contract.
            account: Address to check voting power for.
            block_number: Optional block number to check historical voting power.

        Returns:
            Voting power amount.

        Raises:
            BlockchainError: If voting power retrieval fails.
        """
        try:
            logger.info(f"Getting voting power for {account}")

            if block_number:
                # Get historical voting power
                result = self.contract_validator.call_function(
                    governance_token,  # Positional
                    "getPastVotes",  # Positional
                    account,  # Positional
                    block_number,  # Positional
                )
            else:
                # Get current voting power
                result = self.contract_validator.call_function(
                    governance_token, "getVotes", account  # Positional  # Positional  # Positional
                )

            return result.get("result", 0)

        except Exception as e:
            logger.error(f"Failed to get voting power: {str(e)}")
            raise BlockchainError(f"Failed to get voting power: {str(e)}") from e

    def get_proposal(self, dao_contract: str, proposal_id: int) -> Dict[str, Any]:
        """
        Get details of a DAO proposal.

        Args:
            dao_contract: Name or address of the DAO governance contract.
            proposal_id: ID of the proposal to get details for.

        Returns:
            Dictionary containing proposal details.

        Raises:
            BlockchainError: If proposal retrieval fails.
        """
        try:
            logger.info(f"Getting proposal details for proposal ID {proposal_id}")

            # Proposal state (0=Pending, 1=Active, 2=Canceled, 3=Defeated, 4=Succeeded, 5=Queued, 6=Expired, 7=Executed)
            state_result = self.contract_validator.call_function(
                dao_contract, "state", proposal_id  # Positional  # Positional  # Positional
            )

            # Get proposal details
            # Different DAOs have different proposal structure, this is a simplified example
            proposal_result = self.contract_validator.call_function(
                dao_contract, "proposals", proposal_id  # Positional  # Positional  # Positional
            )

            # Get proposal votes
            votes_result = self.contract_validator.call_function(
                dao_contract, "proposalVotes", proposal_id  # Positional  # Positional  # Positional
            )

            # Map state code to descriptive string
            state_map = {
                0: "Pending",
                1: "Active",
                2: "Canceled",
                3: "Defeated",
                4: "Succeeded",
                5: "Queued",
                6: "Expired",
                7: "Executed",
            }

            state_code = state_result.get("result", 0)

            # Extract proposal details based on return structure
            # This may vary between different DAO implementations
            proposal_data = proposal_result.get("result", {})
            votes_data = votes_result.get("result", {})

            if isinstance(proposal_data, tuple):
                # Handle tuple return type
                return {
                    "id": proposal_id,
                    "state": state_map.get(state_code, "Unknown"),
                    "state_code": state_code,
                    "proposer": proposal_data[0] if len(proposal_data) > 0 else "",
                    "description": proposal_data[4] if len(proposal_data) > 4 else "",
                    "votes_for": votes_data[0] if len(votes_data) > 0 else 0,
                    "votes_against": votes_data[1] if len(votes_data) > 1 else 0,
                    "votes_abstain": votes_data[2] if len(votes_data) > 2 else 0,
                }
            else:
                # Handle dictionary return type or other formats
                return {
                    "id": proposal_id,
                    "state": state_map.get(state_code, "Unknown"),
                    "state_code": state_code,
                    "proposer": proposal_data.get("proposer", ""),
                    "description": proposal_data.get("description", ""),
                    "votes_for": votes_data.get("for", 0),
                    "votes_against": votes_data.get("against", 0),
                    "votes_abstain": votes_data.get("abstain", 0),
                }

        except Exception as e:
            logger.error(f"Failed to get proposal details: {str(e)}")
            raise BlockchainError(f"Failed to get proposal details: {str(e)}") from e

    def execute_proposal(
        self,
        dao_contract: str,
        proposal_id: int,
        targets: List[str],
        values: List[int],
        signatures: List[str],
        calldatas: List[str],
        description_hash: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute a successful DAO proposal.

        Args:
            dao_contract: Name or address of the DAO governance contract.
            proposal_id: ID of the proposal to execute.
            targets: List of contract addresses that will be called.
            values: List of ETH values to send with each call.
            signatures: List of function signatures to call.
            calldatas: List of encoded function parameters.
            description_hash: Hash of the proposal description.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing execution details.

        Raises:
            BlockchainError: If execution fails.
        """
        try:
            logger.info(f"Executing DAO proposal {proposal_id}")

            result = self.contract_validator.call_function(
                dao_contract,  # Positional
                "execute",  # Positional
                targets,  # Positional
                values,  # Positional
                signatures,  # Positional
                calldatas,  # Positional
                description_hash,  # Positional
                transaction=True,  # Keyword
                **kwargs,
            )

            return result

        except Exception as e:
            logger.error(f"Proposal execution failed: {str(e)}")
            raise BlockchainError(f"Failed to execute proposal: {str(e)}") from e

    def queue_proposal(
        self,
        dao_contract: str,
        proposal_id: int,
        targets: List[str],
        values: List[int],
        signatures: List[str],
        calldatas: List[str],
        description_hash: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Queue a successful DAO proposal for execution.

        Args:
            dao_contract: Name or address of the DAO governance contract.
            proposal_id: ID of the proposal to queue.
            targets: List of contract addresses that will be called.
            values: List of ETH values to send with each call.
            signatures: List of function signatures to call.
            calldatas: List of encoded function parameters.
            description_hash: Hash of the proposal description.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing queuing details.

        Raises:
            BlockchainError: If queuing fails.
        """
        try:
            logger.info(f"Queueing DAO proposal {proposal_id}")

            result = self.contract_validator.call_function(
                dao_contract,  # Positional
                "queue",  # Positional
                targets,  # Positional
                values,  # Positional
                signatures,  # Positional
                calldatas,  # Positional
                description_hash,  # Positional
                transaction=True,  # Keyword
                **kwargs,
            )

            return result

        except Exception as e:
            logger.error(f"Proposal queuing failed: {str(e)}")
            raise BlockchainError(f"Failed to queue proposal: {str(e)}") from e

    def cancel_proposal(self, dao_contract: str, proposal_id: int, **kwargs) -> Dict[str, Any]:
        """
        Cancel a DAO proposal.

        Args:
            dao_contract: Name or address of the DAO governance contract.
            proposal_id: ID of the proposal to cancel.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing cancellation details.

        Raises:
            BlockchainError: If cancellation fails.
        """
        try:
            logger.info(f"Canceling DAO proposal {proposal_id}")

            result = self.contract_validator.call_function(
                dao_contract,  # Positional
                "cancel",  # Positional
                proposal_id,  # Positional
                transaction=True,  # Keyword
                **kwargs,
            )

            return result

        except Exception as e:
            logger.error(f"Proposal cancellation failed: {str(e)}")
            raise BlockchainError(f"Failed to cancel proposal: {str(e)}") from e

    def get_proposal_count(self, dao_contract: str) -> int:
        """
        Get the total number of proposals in a DAO.

        Args:
            dao_contract: Name or address of the DAO governance contract.

        Returns:
            Total number of proposals.

        Raises:
            BlockchainError: If count retrieval fails.
        """
        try:
            logger.info(f"Getting proposal count for {dao_contract}")

            result = self.contract_validator.call_function(
                contract_name=dao_contract, function_name="proposalCount"
            )

            return result.get("result", 0)

        except Exception as e:
            logger.error(f"Failed to get proposal count: {str(e)}")
            raise BlockchainError(f"Failed to get proposal count: {str(e)}") from e
