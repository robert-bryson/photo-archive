#!/usr/bin/env python3
"""
Script Name: parc.py
Description: Photo ARChive -- archive photos from input to archive destination.
Author: rsmb
"""

import os
import shutil
import argparse
import logging
from datetime import datetime

# Set up logging
LOG_FILE = "/var/log/parc.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)


def log(message, level=logging.INFO):
    """Logs a message to both console and file."""
    logging.log(level, message)


def process_files(input_dir, output_dir):
    """
    Process files from the input directory and archive them to the output directory.
    """
    if not os.path.isdir(input_dir):
        log(f"Error: Input directory '{input_dir}' does not exist.", logging.ERROR)
        exit(1)
    if not os.path.isdir(output_dir):
        log(f"Error: Output directory '{output_dir}' does not exist.", logging.ERROR)
        exit(1)

    log(f"Processing files from '{input_dir}' to '{output_dir}'...")
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(output_dir, os.path.relpath(src, input_dir))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            log(f"Copied '{src}' to '{dst}'")

    log("File processing completed successfully.")


def main():
    """
    Main function to parse arguments and trigger file processing.
    """
    parser = argparse.ArgumentParser(
        description="Photo ARChive -- Archive photos from input to archive destination."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Specify the input directory (required)"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Specify the output directory (required)"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="parc 1.0",
        help="Display the script version",
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log("Debug mode enabled.", logging.DEBUG)

    log("Starting script execution...")
    log(f"Input Directory: {args.input}")
    log(f"Output Directory: {args.output}")

    # Call the file processing function
    process_files(args.input, args.output)

    log("Script completed successfully.")


if __name__ == "__main__":
    main()
