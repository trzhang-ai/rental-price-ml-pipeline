#!/usr/bin/env python
"""Clean NYC short-term rental records and publish a versioned dataset."""
import argparse
import logging

import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    df = df.drop_duplicates()
    df = df.dropna(subset=["price"])
    df = df[df["price"].between(args.min_price, args.max_price)]
    df["last_review"] = pd.to_datetime(df["last_review"])
    idx = df["longitude"].between(-74.25, -73.50) & df["latitude"].between(40.5, 41.2)
    df = df[idx].copy()
    logger.info("Cleaned data has %s rows and %s columns", *df.shape)

    # Save cleaned data
    df.to_csv("clean_sample.csv", index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean NYC short-term rental records"
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name and version (or alias) of the versioned W&B dataset containing the raw rental data to clean.",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the new versioned W&B dataset that will contain the cleaned rental data.",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="Label describing the kind of output dataset being created, for example 'clean_data'.",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Plain-language description of the output dataset and the cleaning performed on it.",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Lowest nightly rental price to keep; rows below this value are removed.",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Highest nightly rental price to keep; rows above this value are removed.",
        required=True
    )

    args = parser.parse_args()

    go(args)
