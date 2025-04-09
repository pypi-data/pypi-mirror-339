"""
Blockchain Exceptions Module.

This module defines custom exception classes for blockchain-related errors.
"""


class BlockchainError(Exception):
    """Base exception for blockchain-related errors."""

    pass


class ContractValidationError(BlockchainError):
    """Exception raised for errors in contract validation or interaction."""

    pass


class ProvenanceError(BlockchainError):
    """Exception raised for errors in data provenance tracking."""

    pass


class ZKProofError(BlockchainError):
    """Exception raised for errors in zero-knowledge proof generation or verification."""

    pass


class TransactionError(BlockchainError):
    """Exception raised for errors in blockchain transaction submission or execution."""

    pass
