#!/usr/bin/env python3
"""
Example of using the llama_personalization package for federated learning
and privacy-preserving personalization.
"""

import json
import os
import random
import time
from typing import Any, Dict, List

from llama_personalization import PersonalizationEngine


def setup_environment():
    """Set up environment variables for the example."""
    # Set environment variables for configuration
    os.environ["LLAMA_STORAGE_PATH"] = "./example_data"
    os.environ["LLAMA_LOG_LEVEL"] = "INFO"
    os.environ["LLAMA_FEDERATED_ROUNDS"] = "5"
    os.environ["LLAMA_FEDERATED_CLIENT_FRACTION"] = "0.2"
    os.environ["LLAMA_PRIVACY_EPSILON"] = "2.0"


def generate_mock_items(num_items: int = 50) -> List[Dict[str, Any]]:
    """
    Generate mock items for recommendation.

    Args:
        num_items: Number of items to generate.

    Returns:
        List of items.
    """
    # List of possible topics
    topics = [
        "technology",
        "science",
        "art",
        "health",
        "finance",
        "sports",
        "food",
        "travel",
        "fashion",
        "education",
        "politics",
        "environment",
        "history",
        "literature",
        "music",
    ]

    # Generate items
    items = []
    for i in range(num_items):
        # Randomly select 1-3 topics
        item_topics = random.sample(topics, random.randint(1, 3))

        # Create item
        item = {
            "id": i,
            "title": f"Item {i}",
            "description": f"This is a description for item {i}",
            "topics": item_topics,
            "length": random.choice(["short", "medium", "long"]),
            "language": random.choice(["en", "fr", "es", "de", "ja"]),
            "created_at": time.time()
            - random.randint(0, 30 * 24 * 60 * 60),  # Random time in last 30 days
        }

        items.append(item)

    return items


def generate_mock_preferences(client_id: str) -> Dict[str, Any]:
    """
    Generate mock preferences for a client.

    Args:
        client_id: Identifier for the client.

    Returns:
        Generated preferences.
    """
    # List of possible topics
    topics = [
        "technology",
        "science",
        "art",
        "health",
        "finance",
        "sports",
        "food",
        "travel",
        "fashion",
        "education",
    ]

    # Randomly select 2-5 topics
    preferred_topics = random.sample(topics, random.randint(2, 5))

    # Create preferences
    preferences = {
        "topics": preferred_topics,
        "language": random.choice(["en", "fr", "es", "de", "ja"]),
        "content_length": random.choice(["short", "medium", "long"]),
        "update_frequency": random.choice(["daily", "weekly", "monthly"]),
    }

    return preferences


def main():
    """Run the federated learning example."""
    # Set up environment
    setup_environment()

    # Initialize personalization engine
    engine = PersonalizationEngine()

    # Create clients
    num_clients = 20
    print(f"Creating {num_clients} clients...")

    client_ids = []
    for i in range(num_clients):
        client_id = f"client_{i}"
        engine.add_client(client_id)
        client_ids.append(client_id)

        # Add preferences
        preferences = generate_mock_preferences(client_id)
        engine.update_client_preferences(client_id, preferences)

    # Print client information
    print("\nClient Information:")
    for i, client_id in enumerate(client_ids[:3]):  # Show first 3 clients
        exported = engine.export_client_data(client_id)
        print(f"Client {i}: {json.dumps(exported['preferences'], indent=2)}")
    print("...")  # Indicate there are more clients

    # Train federated model
    print("\nTraining federated model...")
    engine.train_federated()

    # Save global model
    model_path = os.path.join(engine.config.storage_path, "global_model.json")
    engine.save_global_model(model_path)
    print(f"Global model saved to {model_path}")

    # Generate items
    items = generate_mock_items(20)

    # Get recommendations for a client
    test_client = random.choice(client_ids)
    print(f"\nGetting recommendations for {test_client}...")
    recommendations = engine.get_recommendation(test_client, items)

    # Print recommendations
    print("\nTop 3 Recommendations:")
    for i, rec in enumerate(recommendations["recommendations"][:3]):
        print(f"Rank {i+1}: {rec['item']['title']} (Topics: {', '.join(rec['item']['topics'])})")
        print(f"Explanation: {json.dumps(rec['explanation'], indent=2)}")

    # Get GDPR explanation
    print("\nGDPR Explanation:")
    explanation = engine.get_gdpr_explanation(test_client)
    print(json.dumps(explanation, indent=2))

    # Test cross-device sync
    print("\nTesting cross-device sync...")
    if len(client_ids) >= 2:
        device1 = client_ids[0]
        device2 = client_ids[1]

        print(f"Syncing preferences from {device1} to {device2}...")
        success = engine.sync_clients(device1, device2)

        if success:
            print("Sync successful!")

            device1_data = engine.export_client_data(device1)
            device2_data = engine.export_client_data(device2)

            print(f"\nDevice 1 Preferences: {json.dumps(device1_data['preferences'], indent=2)}")
            print(f"Device 2 Preferences: {json.dumps(device2_data['preferences'], indent=2)}")

    # Test deleting client data (GDPR right to be forgotten)
    delete_client = client_ids[-1]  # Last client
    print(f"\nDeleting data for {delete_client}...")
    success = engine.delete_client_data(delete_client)

    if success:
        print("Data deleted successfully!")
        print(f"Client still exists: {delete_client in engine.clients}")


if __name__ == "__main__":
    main()
