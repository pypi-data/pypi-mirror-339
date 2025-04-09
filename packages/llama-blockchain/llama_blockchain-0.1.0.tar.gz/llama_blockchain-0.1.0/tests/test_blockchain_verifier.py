"""
Test module for BlockchainVerifier.

This module contains tests for the BlockchainVerifier class and its components.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from llama_blockchain.blockchain_verifier import BlockchainVerifier
from llama_blockchain.contract_validator import ContractValidator
from llama_blockchain.exceptions.blockchain_exceptions import BlockchainError


class TestBlockchainVerifier(unittest.TestCase):
    """Test cases for the BlockchainVerifier class."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock the ContractValidator to avoid actual blockchain interactions
        self.contract_validator_patcher = patch(
            "llama_blockchain.blockchain_verifier.ContractValidator"
        )
        self.mock_contract_validator_class = self.contract_validator_patcher.start()
        self.mock_contract_validator = MagicMock(spec=ContractValidator)
        self.mock_contract_validator_class.return_value = self.mock_contract_validator

        # Mock additional components
        self.provenance_tracker_patcher = patch(
            "llama_blockchain.blockchain_verifier.ProvenanceTracker"
        )
        self.mock_provenance_tracker_class = self.provenance_tracker_patcher.start()
        self.mock_provenance_tracker = MagicMock()
        self.mock_provenance_tracker_class.return_value = self.mock_provenance_tracker

        self.zk_prover_patcher = patch("llama_blockchain.blockchain_verifier.ZKProver")
        self.mock_zk_prover_class = self.zk_prover_patcher.start()
        self.mock_zk_prover = MagicMock()
        self.mock_zk_prover_class.return_value = self.mock_zk_prover

        # Mock manager components
        self.dao_manager_patcher = patch("llama_blockchain.blockchain_verifier.DAOManager")
        self.mock_dao_manager_class = self.dao_manager_patcher.start()
        self.mock_dao_manager = MagicMock()
        self.mock_dao_manager_class.return_value = self.mock_dao_manager

        self.nft_manager_patcher = patch("llama_blockchain.blockchain_verifier.NFTManager")
        self.mock_nft_manager_class = self.nft_manager_patcher.start()
        self.mock_nft_manager = MagicMock()
        self.mock_nft_manager_class.return_value = self.mock_nft_manager

        self.ranking_manager_patcher = patch("llama_blockchain.blockchain_verifier.RankingManager")
        self.mock_ranking_manager_class = self.ranking_manager_patcher.start()
        self.mock_ranking_manager = MagicMock()
        self.mock_ranking_manager_class.return_value = self.mock_ranking_manager

        self.token_manager_patcher = patch("llama_blockchain.blockchain_verifier.TokenManager")
        self.mock_token_manager_class = self.token_manager_patcher.start()
        self.mock_token_manager = MagicMock()
        self.mock_token_manager_class.return_value = self.mock_token_manager

        # Create the BlockchainVerifier instance
        self.verifier = BlockchainVerifier(
            ethereum_rpc_url="https://mainnet.infura.io/v3/your-api-key",
            use_zk_proofs=True,
            provenance_mode="in-memory",
        )

    def tearDown(self):
        """Tear down test fixtures."""
        self.contract_validator_patcher.stop()
        self.provenance_tracker_patcher.stop()
        self.zk_prover_patcher.stop()
        self.dao_manager_patcher.stop()
        self.nft_manager_patcher.stop()
        self.ranking_manager_patcher.stop()
        self.token_manager_patcher.stop()

    def test_initialization(self):
        """Test BlockchainVerifier initialization."""
        # Verify that components were initialized
        self.mock_contract_validator_class.assert_called_once()
        self.mock_provenance_tracker_class.assert_called_once()
        self.mock_zk_prover_class.assert_called_once()
        self.mock_dao_manager_class.assert_called_once()
        self.mock_nft_manager_class.assert_called_once()
        self.mock_ranking_manager_class.assert_called_once()
        self.mock_token_manager_class.assert_called_once()

        # Verify that component attributes are set
        self.assertEqual(self.verifier.contract_validator, self.mock_contract_validator)
        self.assertEqual(self.verifier.provenance_tracker, self.mock_provenance_tracker)
        self.assertEqual(self.verifier.zk_prover, self.mock_zk_prover)
        self.assertEqual(self.verifier.dao_manager, self.mock_dao_manager)
        self.assertEqual(self.verifier.nft_manager, self.mock_nft_manager)
        self.assertEqual(self.verifier.ranking_manager, self.mock_ranking_manager)
        self.assertEqual(self.verifier.token_manager, self.mock_token_manager)

    def test_initialization_error(self):
        """Test BlockchainVerifier initialization with error."""
        # Mock the ContractValidator to raise an exception
        self.mock_contract_validator_class.side_effect = Exception("Mocked initialization error")

        # Verify that the error is propagated
        with self.assertRaises(BlockchainError):
            BlockchainVerifier(ethereum_rpc_url="https://mainnet.infura.io/v3/your-api-key")

    def test_verify_data(self):
        """Test verifying data."""
        # Mock provenance tracker responses
        self.mock_provenance_tracker.track.return_value = "mock-provenance-id"
        self.mock_provenance_tracker.get_timestamp.return_value = 12345

        # Test data verification without contract
        test_data = {"test": "value"}
        result = self.verifier.verify_data(test_data)

        # Verify provenance tracking was called
        self.mock_provenance_tracker.track.assert_called_once_with(
            data=test_data, action="verify", metadata={"verification_type": "hash"}
        )

        # Verify result structure
        self.assertTrue(result["verified"])
        self.assertEqual(result["provenance_id"], "mock-provenance-id")
        self.assertEqual(result["timestamp"], 12345)

        # Test with contract verification
        self.mock_contract_validator.verify_data.return_value = {"verified": True}

        result = self.verifier.verify_data(test_data, contract_name="TestContract")

        # Verify contract validation was called
        self.mock_contract_validator.verify_data.assert_called_once_with(
            data=test_data, verification_type="hash", contract_name="TestContract"
        )

        # Verify result structure
        self.assertTrue(result["verified"])

        # Test with proof generation
        self.mock_zk_prover.generate_proof.return_value = {"proof": "mock-proof"}

        result = self.verifier.verify_data(test_data, generate_proof=True)

        # Verify proof generation was called
        self.mock_zk_prover.generate_proof.assert_called_once_with(
            data=test_data, verification_type="hash"
        )

        # Verify result structure
        self.assertEqual(result["proof"], {"proof": "mock-proof"})

    def test_verify_data_error(self):
        """Test verifying data with error."""
        # Mock provenance tracker to raise an exception
        self.mock_provenance_tracker.track.side_effect = Exception("Mocked verification error")

        # Verify that the error is propagated
        with self.assertRaises(BlockchainError):
            self.verifier.verify_data({"test": "value"})

    def test_submit_transaction(self):
        """Test submitting a transaction."""
        # Mock provenance tracker responses
        self.mock_provenance_tracker.track.return_value = "mock-provenance-id"

        # Mock contract validator response
        self.mock_contract_validator.call_function.return_value = {
            "transaction_hash": "0x1234",
            "result": "success",
        }

        # Test transaction submission
        result = self.verifier.submit_transaction(
            contract_name="TestContract", function_name="testFunction", arg1="value1", arg2="value2"
        )

        # Verify provenance tracking was called
        self.mock_provenance_tracker.track.assert_called_once()

        # Verify contract function call was made
        self.mock_contract_validator.call_function.assert_called_once_with(
            contract_name="TestContract", function_name="testFunction", arg1="value1", arg2="value2"
        )

        # Verify result structure
        self.assertTrue(result["success"])
        self.assertEqual(result["provenance_id"], "mock-provenance-id")
        self.assertEqual(result["transaction_hash"], "0x1234")
        self.assertEqual(result["result"], "success")

    def test_submit_transaction_error(self):
        """Test error handling in the submit_transaction method."""
        # Setup the verifier with a mock web3 provider
        verifier = BlockchainVerifier(network="test", private_key="0x1234")

        # Mock the transaction failure
        verifier._web3_provider.eth.send_raw_transaction.side_effect = Exception(
            "Transaction failed"
        )

        # Call the method with test data
        with self.assertRaises(BlockchainVerificationError):
            verifier.submit_transaction(
                data="test data", contract_address="0x5678", method_name="storeHash"
            )
