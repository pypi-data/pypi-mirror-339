#!/usr/bin/env python3
"""
Command-line interface for llama_personalization.
"""

import argparse
import json
import logging
import os
import sys

from llama_personalization import PersonalizationEngine

logger = logging.getLogger("llama_personalization.cli")


def setup_logging(log_level: str = "INFO") -> None:
    """
    Set up logging configuration.

    Args:
        log_level: Logging level.
    """
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Privacy-focused personalization engine")

    parser.add_argument("--config", help="Path to configuration file", default=None)

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Train command
    train_parser = subparsers.add_parser("train", help="Train the federated model")
    train_parser.add_argument(
        "--rounds", type=int, help="Number of rounds to train for", default=None
    )

    # Simulate command
    simulate_parser = subparsers.add_parser(
        "simulate", help="Simulate a federated learning environment"
    )
    simulate_parser.add_argument(
        "--clients", type=int, help="Number of clients to simulate", default=10
    )
    simulate_parser.add_argument(
        "--rounds", type=int, help="Number of rounds to train for", default=5
    )

    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Generate GDPR-compliant explanation")
    explain_parser.add_argument("--client", help="Client ID to explain", required=True)

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export user data (GDPR right to data portability)"
    )
    export_parser.add_argument("--client", help="Client ID to export", required=True)
    export_parser.add_argument("--output", help="Output file path", default=None)

    # Delete command
    delete_parser = subparsers.add_parser(
        "delete", help="Delete user data (GDPR right to be forgotten)"
    )
    delete_parser.add_argument("--client", help="Client ID to delete", required=True)
    delete_parser.add_argument("--confirm", action="store_true", help="Confirm deletion")

    return parser.parse_args()


def run_train(args: argparse.Namespace) -> None:
    """
    Run the train command.

    Args:
        args: Command-line arguments.
    """
    engine = PersonalizationEngine(args.config)
    engine.train_federated(args.rounds)
    engine.save_global_model()
    logger.info("Training completed successfully")


def run_simulate(args: argparse.Namespace) -> None:
    """
    Run the simulate command.

    Args:
        args: Command-line arguments.
    """
    # Initialize personalization engine
    engine = PersonalizationEngine(args.config)

    # Add simulated clients
    for i in range(args.clients):
        client_id = f"client_{i}"
        engine.add_client(client_id)

        # Add some random preferences
        import random

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
    engine.train_federated(args.rounds)

    # Save the global model
    engine.save_global_model()

    # Print summary
    logger.info(f"Simulation completed with {args.clients} clients and {args.rounds} rounds")
    logger.info(
        f"Global model saved to {os.path.join(engine.config.storage_path, 'global_model.json')}"
    )


def run_explain(args: argparse.Namespace) -> None:
    """
    Run the explain command.

    Args:
        args: Command-line arguments.
    """
    engine = PersonalizationEngine(args.config)

    try:
        explanation = engine.get_gdpr_explanation(args.client)
        print(json.dumps(explanation, indent=2))
    except Exception as e:
        logger.error(f"Failed to get explanation: {e}")
        sys.exit(1)


def run_export(args: argparse.Namespace) -> None:
    """
    Run the export command.

    Args:
        args: Command-line arguments.
    """
    engine = PersonalizationEngine(args.config)

    try:
        user_data = engine.export_client_data(args.client)

        if not user_data:
            logger.error(f"No data found for client {args.client}")
            sys.exit(1)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(user_data, f, indent=2)
            logger.info(f"User data exported to {args.output}")
        else:
            print(json.dumps(user_data, indent=2))
    except Exception as e:
        logger.error(f"Failed to export user data: {e}")
        sys.exit(1)


def run_delete(args: argparse.Namespace) -> None:
    """
    Run the delete command.

    Args:
        args: Command-line arguments.
    """
    if not args.confirm:
        logger.error("Please confirm deletion with --confirm flag")
        sys.exit(1)

    engine = PersonalizationEngine(args.config)

    try:
        success = engine.delete_client_data(args.client)

        if success:
            logger.info(f"Data for client {args.client} deleted successfully")
        else:
            logger.error(f"Failed to delete data for client {args.client}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to delete user data: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()

    # Set up logging
    setup_logging(args.log_level)

    # Set environment variable for logging level
    os.environ["LLAMA_LOG_LEVEL"] = args.log_level

    # Run the appropriate command
    if args.command == "train":
        run_train(args)
    elif args.command == "simulate":
        run_simulate(args)
    elif args.command == "explain":
        run_explain(args)
    elif args.command == "export":
        run_export(args)
    elif args.command == "delete":
        run_delete(args)
    else:
        logger.error("No command specified. Run with --help for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
