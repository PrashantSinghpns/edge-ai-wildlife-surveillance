from __future__ import annotations

import argparse
import logging

from .config import load_config
from .pipeline import EdgePipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the Edge AI wildlife surveillance pipeline."
    )
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Path to YAML configuration file.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
    )

    config = load_config(args.config)
    EdgePipeline(config).run()


if __name__ == "__main__":
    main()
