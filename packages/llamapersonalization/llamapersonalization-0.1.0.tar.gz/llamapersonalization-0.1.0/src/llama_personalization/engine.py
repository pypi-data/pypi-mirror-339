"""
llama_personalization
====================

A privacy-focused personalization engine for language models that uses federated learning,
differential privacy, secure enclaves, and homomorphic encryption.

This package provides tools for personalizing language models while preserving user privacy
through multiple layers of privacy-preserving techniques.
"""

import base64
import hashlib
import hmac
import json
import logging
import os
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("llama_personalization")

# ============================
# Configuration Management
# ============================


class ConfigError(Exception):
    """Exception raised for configuration errors."""

    pass


@dataclass
class PrivacyConfig:
    """Privacy configuration settings."""

    epsilon: float = field(default=1.0)  # Differential privacy epsilon parameter
    delta: float = field(default=1e-5)  # Differential privacy delta parameter
    clip_norm: float = field(default=1.0)  # Gradient clipping norm for DP-SGD
    noise_multiplier: float = field(default=1.1)  # Noise multiplier for DP-SGD
    secure_aggregation: bool = field(default=True)  # Whether to use secure aggregation
    min_clients: int = field(default=5)  # Minimum number of clients for aggregation
    he_precision_bits: int = field(default=16)  # Precision bits for homomorphic encryption

    @classmethod
    def from_env(cls) -> "PrivacyConfig":
        """
        Load privacy configuration from environment variables.

        Returns:
            PrivacyConfig: Configuration with values from environment or defaults.
        """
        return cls(
            epsilon=float(os.environ.get("LLAMA_PRIVACY_EPSILON", 1.0)),
            delta=float(os.environ.get("LLAMA_PRIVACY_DELTA", 1e-5)),
            clip_norm=float(os.environ.get("LLAMA_PRIVACY_CLIP_NORM", 1.0)),
            noise_multiplier=float(os.environ.get("LLAMA_PRIVACY_NOISE_MULTIPLIER", 1.1)),
            secure_aggregation=os.environ.get("LLAMA_PRIVACY_SECURE_AGGREGATION", "true").lower()
            == "true",
            min_clients=int(os.environ.get("LLAMA_PRIVACY_MIN_CLIENTS", 5)),
            he_precision_bits=int(os.environ.get("LLAMA_PRIVACY_HE_PRECISION_BITS", 16)),
        )


@dataclass
class FederatedConfig:
    """Federated learning configuration settings."""

    rounds: int = field(default=10)  # Number of federated learning rounds
    local_epochs: int = field(default=1)  # Number of local training epochs
    batch_size: int = field(default=16)  # Batch size for local training
    learning_rate: float = field(default=0.001)  # Learning rate for local training
    client_fraction: float = field(default=0.1)  # Fraction of clients to select per round
    min_clients_per_round: int = field(default=3)  # Minimum clients per round
    max_clients_per_round: int = field(default=10)  # Maximum clients per round

    @classmethod
    def from_env(cls) -> "FederatedConfig":
        """
        Load federated learning configuration from environment variables.

        Returns:
            FederatedConfig: Configuration with values from environment or defaults.
        """
        return cls(
            rounds=int(os.environ.get("LLAMA_FEDERATED_ROUNDS", 10)),
            local_epochs=int(os.environ.get("LLAMA_FEDERATED_LOCAL_EPOCHS", 1)),
            batch_size=int(os.environ.get("LLAMA_FEDERATED_BATCH_SIZE", 16)),
            learning_rate=float(os.environ.get("LLAMA_FEDERATED_LEARNING_RATE", 0.001)),
            client_fraction=float(os.environ.get("LLAMA_FEDERATED_CLIENT_FRACTION", 0.1)),
            min_clients_per_round=int(os.environ.get("LLAMA_FEDERATED_MIN_CLIENTS", 3)),
            max_clients_per_round=int(os.environ.get("LLAMA_FEDERATED_MAX_CLIENTS", 10)),
        )


@dataclass
class ModelConfig:
    """Language model configuration settings."""

    model_name: str = field(default="mlx-base")
    adapter_dim: int = field(default=8)  # LoRA adapter dimension
    adapter_alpha: float = field(default=16.0)  # LoRA alpha scaling parameter
    dropout: float = field(default=0.05)  # Dropout rate for adapters

    @classmethod
    def from_env(cls) -> "ModelConfig":
        """
        Load model configuration from environment variables.

        Returns:
            ModelConfig: Configuration with values from environment or defaults.
        """
        return cls(
            model_name=os.environ.get("LLAMA_MODEL_NAME", "mlx-base"),
            adapter_dim=int(os.environ.get("LLAMA_ADAPTER_DIM", 8)),
            adapter_alpha=float(os.environ.get("LLAMA_ADAPTER_ALPHA", 16.0)),
            dropout=float(os.environ.get("LLAMA_ADAPTER_DROPOUT", 0.05)),
        )


@dataclass
class SecurityConfig:
    """Security-related configuration settings."""

    secure_enclave_simulation: bool = field(default=True)  # Whether to simulate secure enclaves
    salt: str = field(default="")  # Salt for secure operations
    key_rotation_days: int = field(default=30)  # Key rotation period in days

    @classmethod
    def from_env(cls) -> "SecurityConfig":
        """
        Load security configuration from environment variables.

        Returns:
            SecurityConfig: Configuration with values from environment or defaults.
        """
        # Generate a random salt if not provided
        default_salt = base64.b64encode(os.urandom(16)).decode("utf-8")

        return cls(
            secure_enclave_simulation=os.environ.get(
                "LLAMA_SECURE_ENCLAVE_SIMULATION", "true"
            ).lower()
            == "true",
            salt=os.environ.get("LLAMA_SECURITY_SALT", default_salt),
            key_rotation_days=int(os.environ.get("LLAMA_KEY_ROTATION_DAYS", 30)),
        )


@dataclass
class Config:
    """Main configuration class that aggregates all config components."""

    privacy: PrivacyConfig = field(default_factory=PrivacyConfig)
    federated: FederatedConfig = field(default_factory=FederatedConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    storage_path: str = field(default="./data")
    log_level: str = field(default="INFO")

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.

        Returns:
            Config: Configuration with values from environment or defaults.
        """
        # Set up logging based on environment
        log_level = os.environ.get("LLAMA_LOG_LEVEL", "INFO")
        logging.getLogger("llama_personalization").setLevel(getattr(logging, log_level))

        return cls(
            privacy=PrivacyConfig.from_env(),
            federated=FederatedConfig.from_env(),
            model=ModelConfig.from_env(),
            security=SecurityConfig.from_env(),
            storage_path=os.environ.get("LLAMA_STORAGE_PATH", "./data"),
            log_level=log_level,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of configuration.
        """
        return {
            "privacy": {
                "epsilon": self.privacy.epsilon,
                "delta": self.privacy.delta,
                "clip_norm": self.privacy.clip_norm,
                "noise_multiplier": self.privacy.noise_multiplier,
                "secure_aggregation": self.privacy.secure_aggregation,
                "min_clients": self.privacy.min_clients,
                "he_precision_bits": self.privacy.he_precision_bits,
            },
            "federated": {
                "rounds": self.federated.rounds,
                "local_epochs": self.federated.local_epochs,
                "batch_size": self.federated.batch_size,
                "learning_rate": self.federated.learning_rate,
                "client_fraction": self.federated.client_fraction,
                "min_clients_per_round": self.federated.min_clients_per_round,
                "max_clients_per_round": self.federated.max_clients_per_round,
            },
            "model": {
                "model_name": self.model.model_name,
                "adapter_dim": self.model.adapter_dim,
                "adapter_alpha": self.model.adapter_alpha,
                "dropout": self.model.dropout,
            },
            "security": {
                "secure_enclave_simulation": self.security.secure_enclave_simulation,
                # We don't include the salt in the dictionary for security reasons
                "key_rotation_days": self.security.key_rotation_days,
            },
            "storage_path": self.storage_path,
            "log_level": self.log_level,
        }

    def save(self, path: str) -> None:
        """
        Save configuration to a JSON file.

        Args:
            path: Path to save the configuration file.
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

        logger.info(f"Configuration saved to {path}")

    @classmethod
    def load(cls, path: str) -> "Config":
        """
        Load configuration from a JSON file.

        Args:
            path: Path to the configuration file.

        Returns:
            Config: Loaded configuration.

        Raises:
            ConfigError: If the configuration file doesn't exist or is invalid.
        """
        try:
            with open(path, "r") as f:
                config_dict = json.load(f)

            privacy_config = PrivacyConfig(
                epsilon=config_dict["privacy"]["epsilon"],
                delta=config_dict["privacy"]["delta"],
                clip_norm=config_dict["privacy"]["clip_norm"],
                noise_multiplier=config_dict["privacy"]["noise_multiplier"],
                secure_aggregation=config_dict["privacy"]["secure_aggregation"],
                min_clients=config_dict["privacy"]["min_clients"],
                he_precision_bits=config_dict["privacy"]["he_precision_bits"],
            )

            federated_config = FederatedConfig(
                rounds=config_dict["federated"]["rounds"],
                local_epochs=config_dict["federated"]["local_epochs"],
                batch_size=config_dict["federated"]["batch_size"],
                learning_rate=config_dict["federated"]["learning_rate"],
                client_fraction=config_dict["federated"]["client_fraction"],
                min_clients_per_round=config_dict["federated"]["min_clients_per_round"],
                max_clients_per_round=config_dict["federated"]["max_clients_per_round"],
            )

            model_config = ModelConfig(
                model_name=config_dict["model"]["model_name"],
                adapter_dim=config_dict["model"]["adapter_dim"],
                adapter_alpha=config_dict["model"]["adapter_alpha"],
                dropout=config_dict["model"]["dropout"],
            )

            security_config = SecurityConfig(
                secure_enclave_simulation=config_dict["security"]["secure_enclave_simulation"],
                salt=os.environ.get(
                    "LLAMA_SECURITY_SALT", ""
                ),  # Always get salt from env for security
                key_rotation_days=config_dict["security"]["key_rotation_days"],
            )

            return cls(
                privacy=privacy_config,
                federated=federated_config,
                model=model_config,
                security=security_config,
                storage_path=config_dict["storage_path"],
                log_level=config_dict["log_level"],
            )
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise ConfigError(f"Failed to load configuration from {path}: {str(e)}")


# ============================
# Secure Enclave Simulation
# ============================


class SecureEnclaveSimulation:
    """
    A simulation of a secure enclave for privacy-preserving operations.

    This class simulates the behavior of a secure enclave (like Intel SGX or Apple's
    Secure Enclave) for protecting sensitive user data and operations.
    """

    def __init__(self, config: SecurityConfig):
        """
        Initialize the secure enclave simulation.

        Args:
            config: Security configuration.
        """
        self.config = config
        self._attestation_key = self._generate_attestation_key()
        self._data_store = {}  # Simulated secure storage
        self._encryption_key = self._derive_key("encryption")

    def _generate_attestation_key(self) -> bytes:
        """
        Generate a key for attesting that code is running in the secure enclave.

        Returns:
            bytes: Attestation key.
        """
        # In a real secure enclave, this would be a hardware-protected key
        seed = f"{self.config.salt}:attestation:{int(time.time() / (86400 * self.config.key_rotation_days))}"
        return hashlib.sha256(seed.encode()).digest()

    def _derive_key(self, purpose: str) -> bytes:
        """
        Derive a key for a specific purpose.

        Args:
            purpose: Purpose of the key.

        Returns:
            bytes: Derived key.
        """
        # In a real secure enclave, key derivation would use hardware-protected keys
        seed = f"{self.config.salt}:{purpose}:{int(time.time() / (86400 * self.config.key_rotation_days))}"
        return hashlib.sha256(seed.encode()).digest()

    def attest(self) -> str:
        """
        Generate an attestation that proves the code is running in the secure enclave.

        Returns:
            str: Base64-encoded attestation.
        """
        # Simplified attestation simulation
        timestamp = str(int(time.time()))
        signature = hmac.new(self._attestation_key, timestamp.encode(), hashlib.sha256).digest()
        return base64.b64encode(timestamp.encode() + b":" + signature).decode()

    def verify_attestation(self, attestation: str) -> bool:
        """
        Verify an attestation from another secure enclave.

        Args:
            attestation: Base64-encoded attestation.

        Returns:
            bool: True if the attestation is valid.
        """
        try:
            decoded = base64.b64decode(attestation)
            timestamp_bytes, signature = decoded.split(b":", 1)
            timestamp = timestamp_bytes.decode()

            # Check if attestation is expired (simplified)
            if int(time.time()) - int(timestamp) > 3600:  # 1 hour
                logger.warning("Attestation expired")
                return False

            expected_signature = hmac.new(
                self._attestation_key, timestamp.encode(), hashlib.sha256
            ).digest()

            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.warning(f"Failed to verify attestation: {e}")
            return False

    def store_data(self, key: str, data: Any) -> None:
        """
        Securely store data in the enclave.

        Args:
            key: Key to identify the data.
            data: Data to store.
        """
        # In a real secure enclave, this would be encrypted with a hardware-protected key
        serialized = json.dumps(data).encode()
        encrypted = self._encrypt(serialized)
        self._data_store[key] = encrypted

    def retrieve_data(self, key: str) -> Optional[Any]:
        """
        Retrieve data from the secure storage.

        Args:
            key: Key identifying the data.

        Returns:
            Optional[Any]: Retrieved data or None if the key doesn't exist.
        """
        if key not in self._data_store:
            return None

        encrypted = self._data_store[key]
        serialized = self._decrypt(encrypted)
        return json.loads(serialized.decode())

    def _encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data using the enclave's encryption key.

        Args:
            data: Data to encrypt.

        Returns:
            bytes: Encrypted data.
        """
        # This is a simplified encryption simulation
        # In a real enclave, this would use hardware-accelerated encryption
        nonce = os.urandom(16)

        # XOR encryption as a simple simulation
        # In a real implementation, use AES-GCM or similar
        key_repeated = self._encryption_key * (len(data) // len(self._encryption_key) + 1)
        key_repeated = key_repeated[: len(data)]

        encrypted = bytes(a ^ b for a, b in zip(data, key_repeated))
        return nonce + encrypted

    def _decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using the enclave's encryption key.

        Args:
            encrypted_data: Data to decrypt.

        Returns:
            bytes: Decrypted data.
        """
        # Extract nonce and ciphertext
        nonce, ciphertext = encrypted_data[:16], encrypted_data[16:]

        # XOR decryption (same as encryption for XOR)
        key_repeated = self._encryption_key * (len(ciphertext) // len(self._encryption_key) + 1)
        key_repeated = key_repeated[: len(ciphertext)]

        return bytes(a ^ b for a, b in zip(ciphertext, key_repeated))

    def secure_compute(self, function: Callable, *args, **kwargs) -> Any:
        """
        Perform a computation securely within the enclave.

        Args:
            function: Function to execute securely.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: Result of the secure computation.
        """
        # In a real secure enclave, this would ensure the computation stays within
        # the enclave's trusted execution environment
        try:
            result = function(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error in secure computation: {e}")
            raise


# ============================
# Differential Privacy Utilities
# ============================


class DifferentialPrivacy:
    """Utilities for applying differential privacy techniques."""

    @staticmethod
    def add_gaussian_noise(
        values: np.ndarray, l2_norm_clip: float, noise_multiplier: float
    ) -> np.ndarray:
        """
        Add calibrated Gaussian noise for differential privacy.

        Args:
            values: Values to add noise to.
            l2_norm_clip: L2 norm clipping threshold.
            noise_multiplier: Noise multiplier (determines privacy level).

        Returns:
            np.ndarray: Values with noise added.
        """
        # Flatten to simplify norm calculation
        original_shape = values.shape
        flattened = values.flatten()

        # Calculate L2 norm
        l2_norm = np.linalg.norm(flattened)

        # Scale values if norm exceeds clip threshold
        if l2_norm > l2_norm_clip:
            scale = l2_norm_clip / l2_norm
            flattened = flattened * scale

        # Add Gaussian noise
        stddev = l2_norm_clip * noise_multiplier
        noise = np.random.normal(0, stddev, flattened.shape)

        # Return values with noise added, reshaped to original shape
        return (flattened + noise).reshape(original_shape)

    @staticmethod
    def clip_gradients(
        gradients: Union[np.ndarray, List[np.ndarray]], l2_norm_clip: float
    ) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Clip gradients to a maximum L2 norm.

        Args:
            gradients: Gradients to clip, either a single array or a list of arrays.
            l2_norm_clip: L2 norm clipping threshold.

        Returns:
            Union[np.ndarray, List[np.ndarray]]: Clipped gradients.
        """
        if isinstance(gradients, list):
            # Handle list of arrays (per-layer gradients)
            flat_gradients = np.concatenate([g.flatten() for g in gradients])
            l2_norm = np.linalg.norm(flat_gradients)

            if l2_norm > l2_norm_clip:
                scale = l2_norm_clip / l2_norm
                return [g * scale for g in gradients]
            return gradients
        else:
            # Handle single array
            l2_norm = np.linalg.norm(gradients)

            if l2_norm > l2_norm_clip:
                scale = l2_norm_clip / l2_norm
                return gradients * scale
            return gradients

    @staticmethod
    def compute_epsilon(
        noise_multiplier: float, sample_rate: float, steps: int, delta: float
    ) -> float:
        """
        Compute the epsilon parameter for the given privacy parameters.

        Args:
            noise_multiplier: Noise multiplier used in DP-SGD.
            sample_rate: Sampling rate (batch size / dataset size).
            steps: Number of training steps.
            delta: Target delta parameter.

        Returns:
            float: The resulting epsilon parameter.
        """
        # This is a simplified calculation
        # In a real implementation, use a DP accountant like RDP accounting
        # This provides a loose upper bound
        c = np.sqrt(2 * np.log(1.25 / delta))
        return c * sample_rate * np.sqrt(steps) / noise_multiplier


# ============================
# Homomorphic Encryption Simulation
# ============================


class MLXHomomorphicEncryption:
    """
    Simulation of homomorphic encryption for MLX models.

    This class simulates homomorphic encryption operations for model weights
    and gradients, allowing computation on encrypted data.
    """

    def __init__(self, precision_bits: int = 16):
        """
        Initialize the homomorphic encryption simulation.

        Args:
            precision_bits: Number of bits used for fixed-point precision.
        """
        self.precision_bits = precision_bits
        self.scale = 2**precision_bits
        self._key = os.urandom(32)  # 256-bit key

    def _values_to_fixed_point(self, values: np.ndarray) -> np.ndarray:
        """
        Convert floating-point values to fixed-point representation.

        Args:
            values: Floating-point values.

        Returns:
            np.ndarray: Fixed-point integer representation.
        """
        return np.round(values * self.scale).astype(np.int64)

    def _fixed_point_to_values(self, fixed_point: np.ndarray) -> np.ndarray:
        """
        Convert fixed-point representation back to floating-point values.

        Args:
            fixed_point: Fixed-point integer representation.

        Returns:
            np.ndarray: Floating-point values.
        """
        return fixed_point.astype(np.float32) / self.scale

    def encrypt(self, values: np.ndarray) -> Dict[str, Any]:
        """
        Encrypt floating-point values.

        Args:
            values: Floating-point values to encrypt.

        Returns:
            Dict[str, Any]: Encrypted values and metadata.
        """
        # Convert to fixed-point
        fixed_point = self._values_to_fixed_point(values)

        # Simulate encryption with random masks
        # In a real HE system, this would use proper encryption
        mask = np.random.randint(-1000000, 1000000, size=fixed_point.shape, dtype=np.int64)
        encrypted = fixed_point + mask

        # Store the mask securely (in a real system, this would be derived from the key)
        h = hashlib.sha256(self._key + np.array2string(values).encode()).digest()
        mask_id = base64.b64encode(h).decode()

        # In a real implementation, the mask would be derived from the key and ciphertext
        # For simulation, we store the mask in a global dictionary
        if not hasattr(MLXHomomorphicEncryption, "_masks"):
            MLXHomomorphicEncryption._masks = {}
        MLXHomomorphicEncryption._masks[mask_id] = mask

        return {"encrypted_data": encrypted, "shape": values.shape, "mask_id": mask_id}

    def decrypt(self, encrypted: Dict[str, Any]) -> np.ndarray:
        """
        Decrypt encrypted values.

        Args:
            encrypted: Encrypted values and metadata.

        Returns:
            np.ndarray: Decrypted floating-point values.
        """
        # Extract encrypted data and mask
        encrypted_data = encrypted["encrypted_data"]
        mask_id = encrypted["mask_id"]

        # Get the mask (in a real system, this would be derived from the key)
        if not hasattr(MLXHomomorphicEncryption, "_masks"):
            raise ValueError("No masks found")

        mask = MLXHomomorphicEncryption._masks.get(mask_id)
        if mask is None:
            raise ValueError("Invalid mask ID")

        # Decrypt
        fixed_point = encrypted_data - mask

        # Convert back to floating-point
        return self._fixed_point_to_values(fixed_point)

    def add(self, encrypted1: Dict[str, Any], encrypted2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add two encrypted values homomorphically.

        Args:
            encrypted1: First encrypted values.
            encrypted2: Second encrypted values.

        Returns:
            Dict[str, Any]: Encrypted result of addition.
        """
        if encrypted1["shape"] != encrypted2["shape"]:
            raise ValueError("Shapes must match for homomorphic addition")

        # Homomorphic addition is just adding the ciphertexts
        result_data = encrypted1["encrypted_data"] + encrypted2["encrypted_data"]

        # Combine masks
        mask1 = MLXHomomorphicEncryption._masks.get(encrypted1["mask_id"])
        mask2 = MLXHomomorphicEncryption._masks.get(encrypted2["mask_id"])
        combined_mask = mask1 + mask2

        # Generate new mask ID
        h = hashlib.sha256((encrypted1["mask_id"] + encrypted2["mask_id"]).encode()).digest()
        new_mask_id = base64.b64encode(h).decode()

        # Store combined mask
        MLXHomomorphicEncryption._masks[new_mask_id] = combined_mask

        return {
            "encrypted_data": result_data,
            "shape": encrypted1["shape"],
            "mask_id": new_mask_id,
        }

    def multiply_scalar(self, encrypted: Dict[str, Any], scalar: float) -> Dict[str, Any]:
        """
        Multiply encrypted values by a scalar homomorphically.

        Args:
            encrypted: Encrypted values.
            scalar: Scalar to multiply by.

        Returns:
            Dict[str, Any]: Encrypted result of multiplication.
        """
        # Convert scalar to fixed-point
        scalar_fixed = int(round(scalar * self.scale))

        # Homomorphic multiplication by a scalar
        result_data = encrypted["encrypted_data"] * scalar_fixed // self.scale

        # Adjust mask
        mask = MLXHomomorphicEncryption._masks.get(encrypted["mask_id"])
        new_mask = mask * scalar_fixed // self.scale

        # Generate new mask ID
        h = hashlib.sha256((encrypted["mask_id"] + str(scalar)).encode()).digest()
        new_mask_id = base64.b64encode(h).decode()

        # Store new mask
        MLXHomomorphicEncryption._masks[new_mask_id] = new_mask

        return {
            "encrypted_data": result_data,
            "shape": encrypted["shape"],
            "mask_id": new_mask_id,
        }

    def mean(self, encrypted_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compute the mean of multiple encrypted values homomorphically.

        Args:
            encrypted_list: List of encrypted values.

        Returns:
            Dict[str, Any]: Encrypted result of the mean operation.
        """
        if not encrypted_list:
            raise ValueError("List of encrypted values cannot be empty")

        # Check that all shapes match
        shape = encrypted_list[0]["shape"]
        for enc in encrypted_list:
            if enc["shape"] != shape:
                raise ValueError("All shapes must match for homomorphic mean")

        # Sum all encrypted values
        result = encrypted_list[0].copy()
        for i in range(1, len(encrypted_list)):
            result = self.add(result, encrypted_list[i])

        # Divide by count
        return self.multiply_scalar(result, 1.0 / len(encrypted_list))


# ============================
# Core ML Private Interface Simulation
# ============================


class CoreMLPrivateInterface:
    """
    Simulation of Apple's Core ML private interface.

    This class simulates the privacy-preserving interfaces of Core ML,
    allowing secure model inference and private data handling.
    """

    def __init__(self, secure_enclave: SecureEnclaveSimulation):
        """
        Initialize the Core ML private interface simulation.

        Args:
            secure_enclave: Secure enclave simulation for secure operations.
        """
        self.secure_enclave = secure_enclave
        self.user_preferences = {}
        self.preference_history = {}
        self._init_mock_model()

    def _init_mock_model(self) -> None:
        """Initialize a mock model for simulation purposes."""
        # In a real implementation, this would interface with Core ML
        self.model_initialized = True
        logger.info("Mock Core ML model initialized")

    def predict_private(self, inputs: Any, user_id: str) -> Dict[str, Any]:
        """
        Make a prediction using the model while preserving privacy.

        Args:
            inputs: Model inputs.
            user_id: Identifier for the user.

        Returns:
            Dict[str, Any]: Model prediction and explanation.
        """
        # Ensure we have an enclave attestation
        attestation = self.secure_enclave.attest()

        # In a real implementation, this would happen within the secure enclave
        return self.secure_enclave.secure_compute(
            self._private_prediction, inputs, user_id, attestation
        )

    def _private_prediction(self, inputs: Any, user_id: str, attestation: str) -> Dict[str, Any]:
        """
        Perform a private prediction within the secure enclave.

        Args:
            inputs: Model inputs.
            user_id: Identifier for the user.
            attestation: Secure enclave attestation.

        Returns:
            Dict[str, Any]: Model prediction and explanation.
        """
        # Load user preferences from secure storage
        user_prefs = self.secure_enclave.retrieve_data(f"user_prefs:{user_id}") or {}

        # Mock prediction (in a real implementation, this would use Core ML)
        # The prediction would incorporate user preferences but keep them private
        prediction = {"result": "Personalized result based on private preferences"}

        # Generate explanation (for GDPR compliance)
        explanation = {
            "factors": ["User's topic interests", "Content relevance"],
            "preference_categories_used": list(user_prefs.keys()),
            # Don't reveal actual preference values for privacy
            "attestation": attestation,  # Proof that privacy was preserved
        }

        return {"prediction": prediction, "explanation": explanation}

    def update_preferences(self, user_id: str, preferences: Dict[str, Any]) -> None:
        """
        Update user preferences securely.

        Args:
            user_id: Identifier for the user.
            preferences: Updated preferences.
        """
        # Store preferences securely in the enclave
        current_prefs = self.secure_enclave.retrieve_data(f"user_prefs:{user_id}") or {}

        # Update with new preferences
        updated_prefs = {**current_prefs, **preferences}

        # Store in secure enclave
        self.secure_enclave.store_data(f"user_prefs:{user_id}", updated_prefs)

        # Also store history of preference updates for auditing
        history = self.secure_enclave.retrieve_data(f"pref_history:{user_id}") or []
        history.append(
            {
                "timestamp": time.time(),
                "categories_updated": list(preferences.keys()),
                # Don't store actual values in history for privacy
            }
        )
        self.secure_enclave.store_data(f"pref_history:{user_id}", history)

        logger.info(f"Updated preferences for user {user_id}")

    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        """
        Export all user data in compliance with GDPR.

        Args:
            user_id: Identifier for the user.

        Returns:
            Dict[str, Any]: All user data.
        """
        # This method allows users to exercise their right to data portability
        preferences = self.secure_enclave.retrieve_data(f"user_prefs:{user_id}") or {}
        history = self.secure_enclave.retrieve_data(f"pref_history:{user_id}") or []

        return {
            "user_id": user_id,
            "preferences": preferences,
            "preference_history": history,
            "last_export_time": time.time(),
        }

    def delete_user_data(self, user_id: str) -> bool:
        """
        Delete all user data in compliance with GDPR.

        Args:
            user_id: Identifier for the user.

        Returns:
            bool: True if data was deleted successfully.
        """
        # This method allows users to exercise their right to be forgotten
        try:
            # Delete all user data from secure storage
            self.secure_enclave.store_data(f"user_prefs:{user_id}", None)
            self.secure_enclave.store_data(f"pref_history:{user_id}", None)

            # Log deletion (without personal data)
            logger.info(f"Deleted all data for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete data for user {user_id}: {e}")
            return False


# ============================
# Model Adapter for MLX
# ============================


class LoRAAdapter:
    """
    Low-Rank Adaptation (LoRA) implementation for MLX language models.

    This class implements LoRA-style parameter-efficient fine-tuning
    for language models, allowing personalization with minimal parameters.
    """

    def __init__(
        self,
        base_model_name: str,
        adapter_dim: int = 8,
        alpha: float = 16.0,
        dropout: float = 0.05,
    ):
        """
        Initialize a LoRA adapter for an MLX model.

        Args:
            base_model_name: Name of the base model.
            adapter_dim: Dimension of low-rank adaptation matrices.
            alpha: Scaling factor for LoRA.
            dropout: Dropout probability for regularization.
        """
        self.base_model_name = base_model_name
        self.adapter_dim = adapter_dim
        self.alpha = alpha
        self.dropout = dropout
        self.scaling = alpha / adapter_dim

        # Initialize adapter parameters (A and B matrices)
        self.adapters = {}
        self._init_adapters()

    def _init_adapters(self) -> None:
        """Initialize adapter parameters for the model."""
        # In a real implementation, this would use actual model dimensions
        # For simulation, we use fixed dimensions

        # Simulate model architecture
        model_dims = {
            # Format: layer_name: input_dim, output_dim
            "attention_query": (768, 768),
            "attention_key": (768, 768),
            "attention_value": (768, 768),
            "attention_output": (768, 768),
            "ffn_intermediate": (768, 3072),
            "ffn_output": (3072, 768),
        }

        # Initialize A and B matrices for each layer
        for layer_name, (in_dim, out_dim) in model_dims.items():
            # Initialize with random values (scaled appropriately)
            # A is d×r and B is r×k where r is the adapter dimension
            a_matrix = np.random.normal(
                0, 1.0 / np.sqrt(self.adapter_dim), (in_dim, self.adapter_dim)
            )
            b_matrix = np.zeros((self.adapter_dim, out_dim))

            self.adapters[layer_name] = {"A": a_matrix, "B": b_matrix}

        logger.info(f"Initialized LoRA adapters with rank {self.adapter_dim}")

    def get_adapter_params(self) -> Dict[str, np.ndarray]:
        """
        Get all adapter parameters.

        Returns:
            Dict[str, np.ndarray]: Dictionary of all adapter parameters.
        """
        params = {}
        for layer_name, matrices in self.adapters.items():
            params[f"{layer_name}.A"] = matrices["A"]
            params[f"{layer_name}.B"] = matrices["B"]
        return params

    def set_adapter_params(self, params: Dict[str, np.ndarray]) -> None:
        """
        Set adapter parameters.

        Args:
            params: Dictionary of adapter parameters.
        """
        for param_name, param_value in params.items():
            layer_name, matrix_type = param_name.rsplit(".", 1)
            if layer_name in self.adapters and matrix_type in ["A", "B"]:
                self.adapters[layer_name][matrix_type] = param_value
            else:
                logger.warning(f"Ignoring unknown parameter: {param_name}")

    def forward(self, x: np.ndarray, layer_name: str) -> np.ndarray:
        """
        Apply the LoRA adapter to an input.

        Args:
            x: Input tensor.
            layer_name: Name of the layer.

        Returns:
            np.ndarray: Adapter output.
        """
        if layer_name not in self.adapters:
            logger.warning(f"No adapter for layer: {layer_name}")
            return np.zeros_like(x)

        adapter = self.adapters[layer_name]

        # Apply LoRA: x → x + scaling * (x @ A) @ B
        intermediate = np.matmul(x, adapter["A"])
        result = np.matmul(intermediate, adapter["B"])

        return result * self.scaling

    def save(self, path: str) -> None:
        """
        Save adapter parameters to a file.

        Args:
            path: Path to save the adapter parameters.
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Convert adapters to saveable format
        adapter_params = self.get_adapter_params()

        # Add metadata
        save_data = {
            "metadata": {
                "base_model_name": self.base_model_name,
                "adapter_dim": self.adapter_dim,
                "alpha": self.alpha,
                "dropout": self.dropout,
            },
            "adapters": {name: array.tolist() for name, array in adapter_params.items()},
        }

        # Save to file
        with open(path, "w") as f:
            json.dump(save_data, f)

        logger.info(f"Saved LoRA adapter to {path}")

    @classmethod
    def load(cls, path: str) -> "LoRAAdapter":
        """
        Load adapter parameters from a file.

        Args:
            path: Path to the saved adapter parameters.

        Returns:
            LoRAAdapter: Loaded adapter.
        """
        with open(path, "r") as f:
            data = json.load(f)

        # Extract metadata
        metadata = data["metadata"]

        # Create adapter
        adapter = cls(
            base_model_name=metadata["base_model_name"],
            adapter_dim=metadata["adapter_dim"],
            alpha=metadata["alpha"],
            dropout=metadata["dropout"],
        )

        # Load parameters
        for name, array_list in data["adapters"].items():
            param_array = np.array(array_list)
            layer_name, matrix_type = name.rsplit(".", 1)
            adapter.adapters[layer_name][matrix_type] = param_array

        logger.info(f"Loaded LoRA adapter from {path}")
        return adapter

    def apply_gradient(
        self, gradients: Dict[str, np.ndarray], learning_rate: float = 0.001
    ) -> None:
        """
        Apply gradients to update adapter parameters.

        Args:
            gradients: Gradients for each parameter.
            learning_rate: Learning rate for the update.
        """
        for param_name, gradient in gradients.items():
            if param_name in self.get_adapter_params():
                layer_name, matrix_type = param_name.rsplit(".", 1)
                self.adapters[layer_name][matrix_type] -= learning_rate * gradient

    def merge_with_base_model(self) -> Dict[str, np.ndarray]:
        """
        Merge adapter with base model weights.

        Returns:
            Dict[str, np.ndarray]: Updated model parameters.
        """
        # In a real implementation, this would load and update the actual model
        # For simulation, we return a mock representation
        mock_merged_model = {
            "model_type": self.base_model_name,
            "has_merged_adapters": True,
            "adapter_config": {"dim": self.adapter_dim, "alpha": self.alpha},
        }

        return mock_merged_model


# ============================
# Federated Learning Environment
# ============================


class FederatedLearningEnv:
    """
    Simulation environment for federated learning with privacy guarantees.

    This class orchestrates the federated learning process, including client
    selection, model distribution, and secure aggregation.
    """

    def __init__(self, config: Config):
        """
        Initialize the federated learning environment.

        Args:
            config: Configuration for the environment.
        """
        self.config = config
        self.clients = {}  # Maps client IDs to Agent instances
        self.global_model = None
        self.current_round = 0
        self.secure_enclave = SecureEnclaveSimulation(config.security)
        self.he = MLXHomomorphicEncryption(config.privacy.he_precision_bits)

        # Initialize the global model
        self._init_global_model()

    def _init_global_model(self) -> None:
        """Initialize the global model."""
        self.global_model = LoRAAdapter(
            base_model_name=self.config.model.model_name,
            adapter_dim=self.config.model.adapter_dim,
            alpha=self.config.model.adapter_alpha,
            dropout=self.config.model.dropout,
        )

        logger.info(f"Initialized global model: {self.config.model.model_name}")

    def register_client(self, client_id: str, agent: "Agent") -> None:
        """
        Register a client for federated learning.

        Args:
            client_id: Identifier for the client.
            agent: Client agent.
        """
        self.clients[client_id] = agent
        logger.info(f"Registered client: {client_id}")

    def select_clients(self) -> List[str]:
        """
        Select clients for the current round of federated learning.

        Returns:
            List[str]: Selected client IDs.
        """
        available_clients = list(self.clients.keys())

        # Determine number of clients to select
        num_to_select = max(
            min(
                int(len(available_clients) * self.config.federated.client_fraction),
                self.config.federated.max_clients_per_round,
            ),
            min(self.config.federated.min_clients_per_round, len(available_clients)),
        )

        # Randomly select clients
        selected_clients = random.sample(available_clients, num_to_select)

        logger.info(f"Selected {len(selected_clients)} clients for round {self.current_round}")
        return selected_clients

    def distribute_model(self, client_ids: List[str]) -> None:
        """
        Distribute the global model to selected clients.

        Args:
            client_ids: IDs of clients to receive the model.
        """
        model_params = self.global_model.get_adapter_params()

        for client_id in client_ids:
            if client_id in self.clients:
                self.clients[client_id].receive_model(model_params)
            else:
                logger.warning(f"Client {client_id} not found")

    def collect_updates(self, client_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Collect model updates from clients.

        Args:
            client_ids: IDs of clients to collect updates from.

        Returns:
            Dict[str, Dict[str, Any]]: Updates from each client.
        """
        updates = {}

        for client_id in client_ids:
            if client_id not in self.clients:
                logger.warning(f"Client {client_id} not found")
                continue

            # Get update from client
            client_update = self.clients[client_id].prepare_update()

            # Verify and process update
            if client_update is not None:
                # In a real implementation, would verify attestation
                updates[client_id] = client_update

        logger.info(f"Collected updates from {len(updates)} clients")
        return updates

    def secure_aggregate(self, updates: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """
        Securely aggregate client updates using secure aggregation protocol.

        Args:
            updates: Updates from clients.

        Returns:
            Dict[str, np.ndarray]: Aggregated update.
        """
        # Check if we have enough clients for secure aggregation
        if len(updates) < self.config.privacy.min_clients:
            logger.warning(
                f"Not enough clients for secure aggregation: {len(updates)} < "
                f"{self.config.privacy.min_clients}"
            )
            return None

        # Use the secure enclave for aggregation
        return self.secure_enclave.secure_compute(self._secure_aggregation_impl, updates)

    def _secure_aggregation_impl(self, updates: Dict[str, Dict[str, Any]]) -> Dict[str, np.ndarray]:
        """
        Implementation of secure aggregation within the secure enclave.

        Args:
            updates: Updates from clients.

        Returns:
            Dict[str, np.ndarray]: Aggregated update.
        """
        # Start with an empty aggregation
        aggregated = {}

        # For each parameter in the model
        for client_id, client_update in updates.items():
            for param_name, encrypted_param in client_update["encrypted_params"].items():
                if param_name not in aggregated:
                    # First client to contribute this parameter
                    aggregated[param_name] = encrypted_param
                else:
                    # Add to existing parameter
                    aggregated[param_name] = self.he.add(aggregated[param_name], encrypted_param)

        # Average the parameters
        num_clients = len(updates)
        for param_name in aggregated:
            aggregated[param_name] = self.he.multiply_scalar(
                aggregated[param_name], 1.0 / num_clients
            )

        # Decrypt the aggregated parameters
        decrypted = {
            param_name: self.he.decrypt(encrypted_param)
            for param_name, encrypted_param in aggregated.items()
        }

        return decrypted

    def update_global_model(self, aggregated_update: Dict[str, np.ndarray]) -> None:
        """
        Update the global model with aggregated client updates.

        Args:
            aggregated_update: Aggregated update from clients.
        """
        if aggregated_update is None:
            logger.warning("No update to apply to global model")
            return

        # Apply the update to the global model
        self.global_model.set_adapter_params(aggregated_update)

        # Save checkpoint of the global model
        os.makedirs(os.path.join(self.config.storage_path, "checkpoints"), exist_ok=True)
        self.global_model.save(
            os.path.join(
                self.config.storage_path,
                "checkpoints",
                f"global_model_round_{self.current_round}.json",
            )
        )

        logger.info(f"Updated global model at round {self.current_round}")

    def train_round(self) -> None:
        """Perform one round of federated learning."""
        self.current_round += 1
        logger.info(f"Starting federated round {self.current_round}")

        # Select clients
        selected_clients = self.select_clients()

        # Distribute model
        self.distribute_model(selected_clients)

        # Clients perform local training (handled by Agent class)

        # Collect updates
        client_updates = self.collect_updates(selected_clients)

        # Secure aggregation
        aggregated_update = self.secure_aggregate(client_updates)

        # Update global model
        self.update_global_model(aggregated_update)

    def train(self, num_rounds: Optional[int] = None) -> None:
        """
        Perform multiple rounds of federated learning.

        Args:
            num_rounds: Number of rounds to train for, or use config if None.
        """
        rounds_to_train = num_rounds or self.config.federated.rounds

        for _ in range(rounds_to_train):
            self.train_round()

        logger.info(f"Completed {rounds_to_train} rounds of training")

    def get_global_model_params(self) -> Dict[str, np.ndarray]:
        """
        Get the parameters of the global model.

        Returns:
            Dict[str, np.ndarray]: Global model parameters.
        """
        return self.global_model.get_adapter_params()

    def save_global_model(self, path: str) -> None:
        """
        Save the global model to a file.

        Args:
            path: Path to save the model.
        """
        self.global_model.save(path)
        logger.info(f"Saved global model to {path}")


# ============================
# Client Agent
# ============================


class Agent:
    """
    Client agent for federated learning.

    This class represents a client in the federated learning system,
    handling local training and secure communication.
    """

    def __init__(self, client_id: str, config: Config):
        """
        Initialize a client agent.

        Args:
            client_id: Identifier for the client.
            config: Configuration for the agent.
        """
        self.client_id = client_id
        self.config = config
        self.local_model = None
        self.secure_enclave = SecureEnclaveSimulation(config.security)
        self.he = MLXHomomorphicEncryption(config.privacy.he_precision_bits)
        self.core_ml = CoreMLPrivateInterface(self.secure_enclave)

        # Simulated local data
        self.local_data = self._generate_mock_data()

    def _generate_mock_data(self) -> Dict[str, Any]:
        """
        Generate mock data for simulation.

        Returns:
            Dict[str, Any]: Mock data.
        """
        # In a real implementation, this would be actual user data
        # For simulation, generate random data
        return {
            "samples_count": random.randint(50, 200),
            "has_sufficient_data": True,
            "data_categories": ["text", "interactions", "preferences"],
            "last_updated": time.time(),
        }

    def receive_model(self, model_params: Dict[str, np.ndarray]) -> None:
        """
        Receive model parameters from the server.

        Args:
            model_params: Model parameters.
        """
        # Initialize local model if needed
        if self.local_model is None:
            self.local_model = LoRAAdapter(
                base_model_name=self.config.model.model_name,
                adapter_dim=self.config.model.adapter_dim,
                alpha=self.config.model.adapter_alpha,
                dropout=self.config.model.dropout,
            )

        # Set parameters
        self.local_model.set_adapter_params(model_params)

        logger.info(f"Client {self.client_id} received model")

    def train_locally(self) -> Dict[str, np.ndarray]:
        """
        Perform local training on client data.

        Returns:
            Dict[str, np.ndarray]: Updated model parameters after training.
        """
        # In a real implementation, this would use actual training data
        # For simulation, generate random updates

        # Perform "training" within the secure enclave
        return self.secure_enclave.secure_compute(self._train_locally_impl)

    def _train_locally_impl(self) -> Dict[str, np.ndarray]:
        """
        Implementation of local training within secure enclave.

        Returns:
            Dict[str, np.ndarray]: Updated model parameters.
        """
        if self.local_model is None:
            logger.error(f"Client {self.client_id} has no model to train")
            return None

        # Get current parameters
        current_params = self.local_model.get_adapter_params()

        # Simulate training by adding small random updates
        gradients = {}
        for param_name, param in current_params.items():
            # Generate random gradient
            gradient = np.random.normal(0, 0.01, param.shape)

            # Apply differential privacy
            gradient = DifferentialPrivacy.clip_gradients(gradient, self.config.privacy.clip_norm)
            gradient = DifferentialPrivacy.add_gaussian_noise(
                gradient,
                self.config.privacy.clip_norm,
                self.config.privacy.noise_multiplier,
            )

            gradients[param_name] = gradient

        # Apply gradients to local model
        self.local_model.apply_gradient(gradients, self.config.federated.learning_rate)

        # Return updated parameters
        return self.local_model.get_adapter_params()

    def prepare_update(self) -> Dict[str, Any]:
        """
        Prepare an update to send to the server.

        Returns:
            Dict[str, Any]: Encrypted model update with attestation.
        """
        # Train locally
        updated_params = self.train_locally()

        if updated_params is None:
            return None

        # Encrypt parameters
        encrypted_params = {}
        for param_name, param in updated_params.items():
            encrypted_params[param_name] = self.he.encrypt(param)

        # Generate attestation
        attestation = self.secure_enclave.attest()

        return {
            "client_id": self.client_id,
            "encrypted_params": encrypted_params,
            "attestation": attestation,
            "num_samples": self.local_data["samples_count"],
            "timestamp": time.time(),
        }

    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """
        Update user preferences securely.

        Args:
            preferences: Updated preferences.
        """
        self.core_ml.update_preferences(self.client_id, preferences)

        logger.info(f"Client {self.client_id} updated preferences")

    def get_personalized_recommendation(self, input_data: Any) -> Dict[str, Any]:
        """
        Get a personalized recommendation using local model and preferences.

        Args:
            input_data: Input data for the recommendation.

        Returns:
            Dict[str, Any]: Personalized recommendation.
        """
        return self.core_ml.predict_private(input_data, self.client_id)

    def sync_across_devices(self, other_agent: "Agent") -> bool:
        """
        Synchronize preferences across devices securely.

        Args:
            other_agent: Another agent to sync with.

        Returns:
            bool: True if sync was successful.
        """
        # Generate attestation
        attestation = self.secure_enclave.attest()

        # Verify other agent's attestation
        other_attestation = other_agent.secure_enclave.attest()
        if not self.secure_enclave.verify_attestation(other_attestation):
            logger.warning(
                f"Client {self.client_id} failed to verify attestation from {other_agent.client_id}"
            )
            return False

        # Export user data
        my_data = self.core_ml.export_user_data(self.client_id)

        # In a real implementation, this would involve secure communication
        # For simulation, directly call the other agent's update method
        other_agent.update_preferences(my_data["preferences"])

        logger.info(f"Client {self.client_id} synced with {other_agent.client_id}")
        return True


# ============================
# Explainable Recommender Model
# ============================


class ExplainableRecommender:
    """
    Explainable recommendation model for GDPR compliance.

    This class provides explainable recommendations based on user preferences
    and model predictions.
    """

    def __init__(self, config: Config):
        """
        Initialize the explainable recommender.

        Args:
            config: Configuration for the recommender.
        """
        self.config = config
        self.secure_enclave = SecureEnclaveSimulation(config.security)
        self.core_ml = CoreMLPrivateInterface(self.secure_enclave)

        # Feature importance for explanation
        self.feature_importance = {
            "topic_relevance": 0.4,
            "user_interests": 0.3,
            "content_quality": 0.2,
            "recency": 0.1,
        }

    def recommend(self, user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate personalized recommendations with explanations.

        Args:
            user_id: Identifier for the user.
            items: Items to recommend from.

        Returns:
            Dict[str, Any]: Ranked items with explanations.
        """
        # Get user preferences (securely, through Core ML)
        prediction = self.core_ml.predict_private(items, user_id)

        # In a real implementation, this would rank items based on the model
        # For simulation, generate random rankings
        ranked_items = list(enumerate(items))
        random.shuffle(ranked_items)

        recommendations = []
        for rank, item in ranked_items:
            # Generate explanation for this recommendation
            explanation = self._generate_explanation(item, prediction["explanation"])

            recommendations.append({"item": item, "rank": rank, "explanation": explanation})

        return {
            "recommendations": recommendations,
            "explanation_factors": prediction["explanation"]["factors"],
            "timestamp": time.time(),
        }

    def _generate_explanation(
        self, item: Dict[str, Any], prediction_explanation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate an explanation for a recommendation.

        Args:
            item: Item being recommended.
            prediction_explanation: Explanation from the prediction.

        Returns:
            Dict[str, Any]: Explanation for the recommendation.
        """
        # In a real implementation, this would use actual item features
        # For simulation, generate a plausible explanation

        category_factors = {}
        for category in prediction_explanation.get("preference_categories_used", []):
            # Simulate category relevance scores
            category_factors[category] = random.random()

        # Normalize factor importance
        total = sum(category_factors.values())
        if total > 0:
            category_factors = {
                category: score / total for category, score in category_factors.items()
            }

        # Generate human-readable explanation
        factors = []
        for category, importance in sorted(
            category_factors.items(), key=lambda x: x[1], reverse=True
        ):
            if importance > 0.1:  # Only include significant factors
                factors.append(
                    {
                        "category": category,
                        "importance": importance,
                        "description": f"Your preferences in {category} match this item",
                    }
                )

        return {
            "relevance_factors": factors,
            "transparency_level": "detailed",  # GDPR compliance
            "attestation": prediction_explanation.get("attestation"),  # Include attestation
        }

    def explain_recommendation_history(self, user_id: str) -> Dict[str, Any]:
        """
        Provide an explanation of recommendation history for GDPR compliance.

        Args:
            user_id: Identifier for the user.

        Returns:
            Dict[str, Any]: Explanation of recommendation history.
        """
        # Export user data
        user_data = self.core_ml.export_user_data(user_id)

        # Create a GDPR-compliant explanation
        explanation = {
            "preference_categories": list(user_data.get("preferences", {}).keys()),
            "data_used": [
                "Your topic preferences",
                "Your interaction history",
                "Content relevance scores",
            ],
            "update_history": [
                {
                    "timestamp": entry.get("timestamp"),
                    "categories_updated": entry.get("categories_updated"),
                }
                for entry in user_data.get("preference_history", [])
            ],
            "how_to_update": "You can update your preferences in the settings menu",
            "how_to_delete": "You can delete your data in the privacy settings",
        }

        return explanation


# ============================
# Personalization Engine
# ============================


class PersonalizationEngine:
    """
    Main personalization engine that orchestrates privacy-preserving personalization.

    This class integrates federated learning, differential privacy, secure enclaves,
    and homomorphic encryption to provide privacy-preserving personalization.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the personalization engine.

        Args:
            config_path: Path to configuration file, or None to use environment variables.
        """
        # Initialize configuration
        if config_path is not None:
            self.config = Config.load(config_path)
        else:
            self.config = Config.from_env()

        # Set up logging
        logging.getLogger("llama_personalization").setLevel(getattr(logging, self.config.log_level))

        # Initialize components
        self.secure_enclave = SecureEnclaveSimulation(self.config.security)
        self.federated_env = FederatedLearningEnv(self.config)
        self.explainable_recommender = ExplainableRecommender(self.config)
        self.clients = {}  # Maps client IDs to Agent instances

        # Ensure storage directory exists
        os.makedirs(self.config.storage_path, exist_ok=True)

        logger.info("Initialized PersonalizationEngine")

    def add_client(self, client_id: str) -> Agent:
        """
        Add a client to the personalization system.

        Args:
            client_id: Identifier for the client.

        Returns:
            Agent: The created client agent.
        """
        # Create client agent
        agent = Agent(client_id, self.config)

        # Register with federated environment
        self.federated_env.register_client(client_id, agent)

        # Store in local mapping
        self.clients[client_id] = agent

        logger.info(f"Added client: {client_id}")
        return agent

    def train_federated(self, num_rounds: Optional[int] = None) -> None:
        """
        Perform federated training.

        Args:
            num_rounds: Number of rounds to train for, or use config if None.
        """
        self.federated_env.train(num_rounds)

    def get_recommendation(self, client_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get personalized recommendations for a client.

        Args:
            client_id: Identifier for the client.
            items: Items to recommend from.

        Returns:
            Dict[str, Any]: Personalized recommendations.
        """
        if client_id not in self.clients:
            logger.warning(f"Client {client_id} not found, adding new client")
            self.add_client(client_id)

        return self.explainable_recommender.recommend(client_id, items)

    def update_client_preferences(self, client_id: str, preferences: Dict[str, Any]) -> None:
        """
        Update preferences for a client.

        Args:
            client_id: Identifier for the client.
            preferences: Updated preferences.
        """
        if client_id not in self.clients:
            logger.warning(f"Client {client_id} not found, adding new client")
            self.add_client(client_id)

        self.clients[client_id].update_preferences(preferences)

    def save_global_model(self, path: Optional[str] = None) -> None:
        """
        Save the global model.

        Args:
            path: Path to save the model, or use default if None.
        """
        if path is None:
            path = os.path.join(self.config.storage_path, "global_model.json")

        self.federated_env.save_global_model(path)

    def get_gdpr_explanation(self, client_id: str) -> Dict[str, Any]:
        """
        Get a GDPR-compliant explanation of recommendations.

        Args:
            client_id: Identifier for the client.

        Returns:
            Dict[str, Any]: GDPR-compliant explanation.
        """
        return self.explainable_recommender.explain_recommendation_history(client_id)

    def delete_client_data(self, client_id: str) -> bool:
        """
        Delete all data for a client (GDPR right to be forgotten).

        Args:
            client_id: Identifier for the client.

        Returns:
            bool: True if data was deleted successfully.
        """
        if client_id not in self.clients:
            logger.warning(f"Client {client_id} not found")
            return False

        # Delete user data from Core ML
        success = self.clients[client_id].core_ml.delete_user_data(client_id)

        # Remove client from system
        if success:
            self.federated_env.clients.pop(client_id, None)
            self.clients.pop(client_id, None)

            logger.info(f"Deleted all data for client {client_id}")

        return success

    def export_client_data(self, client_id: str) -> Dict[str, Any]:
        """
        Export all data for a client (GDPR right to data portability).

        Args:
            client_id: Identifier for the client.

        Returns:
            Dict[str, Any]: All client data.
        """
        if client_id not in self.clients:
            logger.warning(f"Client {client_id} not found")
            return {}

        return self.clients[client_id].core_ml.export_user_data(client_id)

    def sync_clients(self, source_client_id: str, target_client_id: str) -> bool:
        """
        Sync preferences between two clients.

        Args:
            source_client_id: Source client ID.
            target_client_id: Target client ID.

        Returns:
            bool: True if sync was successful.
        """
        if source_client_id not in self.clients:
            logger.warning(f"Source client {source_client_id} not found")
            return False

        if target_client_id not in self.clients:
            logger.warning(f"Target client {target_client_id} not found")
            return False

        return self.clients[source_client_id].sync_across_devices(self.clients[target_client_id])


# ============================
# Command Line Interface
# ============================


def parse_args():
    """Parse command line arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="Privacy-focused personalization engine")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Train command
    train_parser = subparsers.add_parser("train", help="Train the federated model")
    train_parser.add_argument("--config", help="Path to configuration file", default=None)
    train_parser.add_argument(
        "--rounds", type=int, help="Number of rounds to train for", default=None
    )

    # Simulate command
    simulate_parser = subparsers.add_parser(
        "simulate", help="Simulate a federated learning environment"
    )
    simulate_parser.add_argument("--config", help="Path to configuration file", default=None)
    simulate_parser.add_argument(
        "--clients", type=int, help="Number of clients to simulate", default=10
    )
    simulate_parser.add_argument(
        "--rounds", type=int, help="Number of rounds to train for", default=5
    )

    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Generate GDPR-compliant explanation")
    explain_parser.add_argument("--config", help="Path to configuration file", default=None)
    explain_parser.add_argument("--client", help="Client ID to explain", required=True)

    return parser.parse_args()


def run_simulation(config_path: Optional[str], num_clients: int, num_rounds: int):
    """Run a simulation of the federated learning environment."""
    # Initialize personalization engine
    engine = PersonalizationEngine(config_path)

    # Add simulated clients
    for i in range(num_clients):
        client_id = f"client_{i}"
        engine.add_client(client_id)

        # Add some random preferences
        preferences = {
            "topics": random.sample(
                ["technology", "science", "art", "sports", "music", "food", "travel"],
                random.randint(1, 3),
            ),
            "language": random.choice(["en", "fr", "es", "de"]),
            "content_length": random.choice(["short", "medium", "long"]),
        }
        engine.update_client_preferences(client_id, preferences)

    # Train the federated model
    engine.train_federated(num_rounds)

    # Save the global model
    engine.save_global_model()

    # Print summary
    logger.info(f"Simulation completed with {num_clients} clients and {num_rounds} rounds")
    logger.info(
        f"Global model saved to {os.path.join(engine.config.storage_path, 'global_model.json')}"
    )


def main():
    """Main entry point."""
    args = parse_args()

    if args.command == "train":
        engine = PersonalizationEngine(args.config)
        engine.train_federated(args.rounds)
        engine.save_global_model()
    elif args.command == "simulate":
        run_simulation(args.config, args.clients, args.rounds)
    elif args.command == "explain":
        engine = PersonalizationEngine(args.config)
        if args.client not in engine.clients:
            engine.add_client(args.client)
        explanation = engine.get_gdpr_explanation(args.client)
        print(json.dumps(explanation, indent=2))
    else:
        print("Invalid command. Run with --help for usage information.")


if __name__ == "__main__":
    main()
