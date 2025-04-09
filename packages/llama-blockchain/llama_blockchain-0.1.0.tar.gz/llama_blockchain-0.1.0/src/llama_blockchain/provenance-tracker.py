"""
Provenance Tracker Module.

This module provides the ProvenanceTracker class for tracking and verifying
the provenance of data, both on-chain and in-memory.
"""

import copy
import hashlib
import json
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

from .contract_validator import ContractValidator
from .exceptions.blockchain_exceptions import ProvenanceError

logger = logging.getLogger(__name__)


class ProvenanceTracker:
    """
    Tracks and verifies the provenance of data, both on-chain and in-memory.

    This class provides methods for recording data operations, tracking data lineage,
    and verifying data integrity through provenance records.

    Attributes:
        mode: Mode of operation ('on-chain' or 'in-memory').
        contract_validator: ContractValidator instance for blockchain interactions.
        records: In-memory storage of provenance records when not using blockchain.
    """

    def __init__(
        self,
        mode: str = "in-memory",
        contract_validator: Optional[ContractValidator] = None,
        provenance_contract_name: Optional[str] = None,
    ):
        """
        Initialize the ProvenanceTracker.

        Args:
            mode: Mode of operation ('on-chain' or 'in-memory').
            contract_validator: ContractValidator instance for blockchain interactions.
            provenance_contract_name: Name of the contract to use for on-chain provenance.

        Raises:
            ProvenanceError: If initialization fails.
        """
        valid_modes = ["on-chain", "in-memory"]
        if mode not in valid_modes:
            raise ProvenanceError(f"Invalid mode: {mode}. Must be one of {valid_modes}")

        self.mode = mode
        self.contract_validator = contract_validator
        self.provenance_contract_name = provenance_contract_name
        self.records = []

        # Validate dependencies for on-chain mode
        if mode == "on-chain" and (not contract_validator or not provenance_contract_name):
            logger.warning(
                "On-chain mode requires contract_validator and provenance_contract_name. "
                "Falling back to in-memory mode."
            )
            self.mode = "in-memory"

        logger.info(f"ProvenanceTracker initialized in {self.mode} mode")

    def track(self, data: Any, action: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Track a data operation by recording its provenance.

        Args:
            data: The data being operated on.
            action: The type of action being performed on the data.
            metadata: Additional information about the operation.

        Returns:
            String identifier for the provenance record.

        Raises:
            ProvenanceError: If tracking fails.
        """
        try:
            # Generate a unique ID for this provenance record
            provenance_id = str(uuid.uuid4())

            # Create timestamp for the record
            timestamp = int(time.time())

            # Create a serializable copy of the data
            if isinstance(data, dict):
                # Shallow copy is sufficient for serialization
                data_copy = copy.copy(data)
            else:
                # For non-dict data, just use as is
                data_copy = data

            # Generate a hash of the data for integrity verification
            data_hash = self._hash_data(data_copy)

            # Create the provenance record
            record = {
                "id": provenance_id,
                "timestamp": timestamp,
                "action": action,
                "data_hash": data_hash,
                "metadata": metadata or {},
            }

            # Store the record according to the selected mode
            if (
                self.mode == "on-chain"
                and self.contract_validator
                and self.provenance_contract_name
            ):
                logger.info(f"Storing provenance record on-chain: {provenance_id}")
                self._store_on_chain(record)
            else:
                logger.info(f"Storing provenance record in-memory: {provenance_id}")
                self.records.append(record)

            return provenance_id

        except Exception as e:
            logger.error(f"Failed to track provenance: {str(e)}")
            raise ProvenanceError(f"Failed to track provenance: {str(e)}") from e

    def _hash_data(self, data: Any) -> str:
        """
        Generate a hash of the provided data.

        Args:
            data: The data to hash.

        Returns:
            String hash of the data.
        """
        try:
            # Convert the data to a JSON string
            if isinstance(data, (dict, list, tuple)):
                # Sort keys for consistent hashing
                data_str = json.dumps(data, sort_keys=True)
            else:
                data_str = str(data)

            # Generate a SHA-256 hash
            return hashlib.sha256(data_str.encode()).hexdigest()

        except Exception as e:
            logger.error(f"Failed to hash data: {str(e)}")
            # Return a placeholder hash in case of error
            return hashlib.sha256(str(time.time()).encode()).hexdigest()

    def _store_on_chain(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store a provenance record on the blockchain.

        Args:
            record: The provenance record to store.

        Returns:
            Dictionary containing transaction details.

        Raises:
            ProvenanceError: If storage fails.
        """
        try:
            logger.info(f"Attempting to store provenance record on-chain: {record['id']}")
            result = self.contract_validator.call_function(
                self.provenance_contract_name,
                "storeProvenanceRecord",
                record["id"],
                record["timestamp"],
                record["action"],
                record["data_hash"],
                json.dumps(record["metadata"]),
                transaction=True,
            )

            logger.info(f"Provenance record stored on-chain: {record['id']}")
            return result

        except Exception as e:
            logger.error(f"Failed to store provenance on-chain: {str(e)}")
            # Fall back to in-memory storage in case of error
            logger.info(f"Falling back to in-memory storage for: {record['id']}")
            self.records.append(record)
            return {"success": False, "error": str(e)}

    def verify(self, provenance_id: str, data: Any) -> Dict[str, Any]:
        """
        Verify that data matches a previously recorded provenance record.

        Args:
            provenance_id: ID of the provenance record to verify against.
            data: The data to verify.

        Returns:
            Dictionary containing verification results.

        Raises:
            ProvenanceError: If verification fails.
        """
        try:
            logger.info(f"Verifying data against provenance record: {provenance_id}")

            # Generate a hash of the current data
            current_hash = self._hash_data(data)

            # Get the provenance record
            record = self.get_record(provenance_id)

            if not record:
                return {
                    "verified": False,
                    "error": f"No provenance record found with ID: {provenance_id}",
                }

            # Compare the hashes
            if record["data_hash"] == current_hash:
                logger.info(f"Data verified successfully: {provenance_id}")
                return {
                    "verified": True,
                    "timestamp": record["timestamp"],
                    "action": record["action"],
                    "metadata": record["metadata"],
                }
            else:
                logger.warning(f"Data verification failed: {provenance_id}")
                return {
                    "verified": False,
                    "error": "Data hash does not match the provenance record",
                    "expected_hash": record["data_hash"],
                    "actual_hash": current_hash,
                }

        except Exception as e:
            logger.error(f"Verification error: {str(e)}")
            raise ProvenanceError(f"Failed to verify data: {str(e)}") from e

    def get_record(self, provenance_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a provenance record by ID.

        Args:
            provenance_id: ID of the record to retrieve.

        Returns:
            The provenance record dictionary, or None if not found.

        Raises:
            ProvenanceError: If retrieval fails.
        """
        try:
            logger.info(f"Retrieving provenance record: {provenance_id}")

            # Retrieve the record according to the selected mode
            if (
                self.mode == "on-chain"
                and self.contract_validator
                and self.provenance_contract_name
            ):
                logger.info(f"Retrieving record from blockchain: {provenance_id}")
                result = self.contract_validator.call_function(
                    self.provenance_contract_name, "getProvenanceRecord", provenance_id
                )

                if result.get("success", False) and result.get("result"):
                    # Parse the contract result into a record
                    contract_result = result["result"]

                    # Structure depends on the contract implementation
                    # This is a common approach with indexed returns
                    if isinstance(contract_result, tuple) and len(contract_result) >= 5:
                        return {
                            "id": provenance_id,
                            "timestamp": contract_result[0],
                            "action": contract_result[1],
                            "data_hash": contract_result[2],
                            "metadata": (
                                json.loads(contract_result[3]) if contract_result[3] else {}
                            ),
                        }
                    else:
                        logger.warning(f"Unexpected contract result format: {contract_result}")
                        return None
                else:
                    logger.warning(f"No record found on-chain: {provenance_id}")
                    return None
            else:
                # Search in-memory records
                for record in self.records:
                    if record["id"] == provenance_id:
                        return record

                logger.warning(f"No record found in-memory: {provenance_id}")
                return None

        except Exception as e:
            logger.error(f"Failed to retrieve provenance record: {str(e)}")
            raise ProvenanceError(f"Failed to retrieve provenance record: {str(e)}") from e

    def get_history(
        self, data_id: Optional[str] = None, action_type: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve provenance history, optionally filtered by data ID or action type.

        Args:
            data_id: Optional ID of data to retrieve history for.
            action_type: Optional type of action to filter by.
            limit: Maximum number of records to return.

        Returns:
            List of provenance records.

        Raises:
            ProvenanceError: If history retrieval fails.
        """
        try:
            logger.info("Retrieving provenance history")

            if (
                self.mode == "on-chain"
                and self.contract_validator
                and self.provenance_contract_name
            ):
                # For on-chain mode, this would require more sophisticated querying
                # which is beyond the scope of this implementation
                logger.warning(
                    "Detailed history filtering is limited in on-chain mode. "
                    "Falling back to basic retrieval."
                )

                # This assumes the contract has a function to get the most recent records
                result = self.contract_validator.call_function(
                    self.provenance_contract_name, "getRecentRecords", limit
                )

                if result.get("success", False) and result.get("result"):
                    records = result["result"]
                    return [
                        {
                            "id": record[0],
                            "timestamp": record[1],
                            "action": record[2],
                            "data_hash": record[3],
                            "metadata": json.loads(record[4]) if record[4] else {},
                        }
                        for record in records
                    ]
                else:
                    return []
            else:
                # Filter in-memory records
                filtered_records = self.records

                if data_id:
                    # In a real implementation, we would need a way to associate
                    # records with specific data IDs
                    filtered_records = [
                        r
                        for r in filtered_records
                        if r.get("metadata", {}).get("data_id") == data_id
                    ]

                if action_type:
                    filtered_records = [
                        r for r in filtered_records if r.get("action") == action_type
                    ]

                # Sort by timestamp (newest first) and limit
                sorted_records = sorted(
                    filtered_records, key=lambda r: r.get("timestamp", 0), reverse=True
                )

                return sorted_records[:limit]

        except Exception as e:
            logger.error(f"Failed to retrieve provenance history: {str(e)}")
            raise ProvenanceError(f"Failed to retrieve provenance history: {str(e)}") from e

    def get_timestamp(self) -> int:
        """
        Get the current timestamp in seconds since the epoch.

        Returns:
            Current timestamp.
        """
        return int(time.time())
