import argparse
import datetime
import logging
from pathlib import Path

from parc.photos import PhotoCollection

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def setup():
    """Set up the CLI."""
    parser = configure_parser()
    args = parser.parse_args()

    # Enable debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")

    start_time = datetime.datetime.now()

    # Validate the input and output directories
    input_path = validate_dir(args.input)

    output_root_path = validate_dir(args.output)
    # TOOD session_path string should be configurable
    session_path = Path(start_time.strftime("%Y/%Y-%m-%d"))
    output_session_path = output_root_path / session_path
    if not args.dryrun:
        output_session_path.mkdir(exist_ok=True)

    logger.info(f"Input directory: {input_path}")
    logger.info(f"Root archive directory: {args.output}")
    logger.info(f"Session archive directory: {output_session_path}")

    return input_path, output_session_path


def configure_parser():
    """Configure the CLI parser."""
    parser = argparse.ArgumentParser(description="A simple Photo ARChive tool.")
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Specify the input directory"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Specify the output root archive directory",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="parc 1.0.0",
        help="Show the version",
    )
    # TODO implement the dryrun option
    parser.add_argument("--dryrun", action="store_true", help="Perform a dry run")
    # TODO implement verbosity option
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")

    # TODO add support for .parcconfig and/or env vars
    # TOOD add support for filtering file types

    return parser


def validate_dir(path_str: str) -> Path:
    """Validate that path_str is a valid existing accessible directory."""
    logger.debug(f"Validating directory: {path_str}")

    path = Path(path_str)
    if not path.exists() and not path.is_dir():
        logger.error(f"{path_str} is not a valid directory")
        raise argparse.ArgumentTypeError(f"{path_str} is not a valid directory")
    return path


def walk_input_directory(photos: PhotoCollection, input_dir: Path):
    """Walk the input directory and add photos to the collection."""
    logger.debug(f"Walk input directory: {input_dir}")

    # TODO file types should be configurable
    for photo_path in input_dir.rglob("*.jpg"):
        logger.info(f"Adding photo: {photo_path}")
        photos.add_photo(photo_path)


def main():
    """Main entry point for the CLI."""
    input_path, output_session_path = setup()

    # Add the main functionality here
    logger.debug("Processing started...")

    photos = PhotoCollection()
    walk_input_directory(photos, input_path)

    logger.debug("Processing completed successfully.")


if __name__ == "__main__":
    main()
