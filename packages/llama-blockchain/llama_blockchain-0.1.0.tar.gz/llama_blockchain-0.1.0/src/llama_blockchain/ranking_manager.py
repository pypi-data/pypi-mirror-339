"""
Ranking Manager Module.

This module provides the RankingManager class for interacting with
decentralized ranking systems and reputation protocols on the blockchain.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from ..contract_validator import ContractValidator
from ..exceptions.blockchain_exceptions import BlockchainError

logger = logging.getLogger(__name__)


class RankingManager:
    """
    Manages interactions with decentralized ranking and reputation systems.

    This class provides methods for submitting, retrieving, and aggregating
    blockchain-based rankings and reputation scores.

    Attributes:
        contract_validator: ContractValidator instance for blockchain interactions.
    """

    def __init__(self, contract_validator: ContractValidator):
        """
        Initialize the RankingManager.

        Args:
            contract_validator: ContractValidator instance for blockchain interactions.
        """
        self.contract_validator = contract_validator
        logger.info("RankingManager initialized")

    def submit_ranking(
        self,
        ranking_contract: str,
        entity_id: str,
        score: int,
        category: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Submit a ranking score for an entity.

        Args:
            ranking_contract: Name or address of the ranking contract.
            entity_id: ID of the entity being ranked.
            score: Numerical score or rating.
            category: Optional category for the ranking.
            metadata: Optional additional information about the ranking.
            **kwargs: Additional transaction parameters.

        Returns:
            Dictionary containing submission details.

        Raises:
            BlockchainError: If submission fails.
        """
        try:
            logger.info(f"Submitting ranking score {score} for entity {entity_id}")

            # Convert metadata to string if provided
            metadata_str = ""
            if metadata:
                import json

                metadata_str = json.dumps(metadata)

            if category:
                # Submit ranking with category
                result = self.contract_validator.call_function(
                    ranking_contract,
                    "submitRanking",
                    entity_id,
                    score,
                    category,
                    metadata_str,
                    transaction=True,
                    **kwargs,
                )
            else:
                # Submit ranking without category
                result = self.contract_validator.call_function(
                    ranking_contract,
                    "submitRanking",
                    entity_id,
                    score,
                    metadata_str,
                    transaction=True,
                    **kwargs,
                )

            return result

        except Exception as e:
            logger.error(f"Ranking submission failed: {str(e)}")
            raise BlockchainError(f"Failed to submit ranking: {str(e)}") from e
