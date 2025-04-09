"""Main entry point for the document generator."""

import importlib
import logging
import os
import sys
from pathlib import Path

import click
import yaml

from .common import deep_merge
from .render import create_env

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Generate PDF documents from YAML-configured SVG templates."""


@cli.command()
@click.argument("config_file", metavar="<config_file>", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-v", "--verbose", is_flag=True,
    help="Show debug information"
)
@click.option(
    "-q", "--quiet", is_flag=True,
    help="Show errors only"
)
def bake(config_file, verbose=False, quiet=False):
    """Parse config file and bake PDFs."""
    if quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    config = _load_config(config_file)
    base_dir = config_file.parent
    document_paths = _get_document_paths(base_dir, config.get("documents", []))
    build_dir, dist_dir = _setup_output_directories(base_dir)

    for doc_name, doc_path in document_paths.items():
        _process_document(doc_name, doc_path, config, build_dir, dist_dir)

    logger.info("Done.")
    return 0


def _load_config(config_file):
    """Load configuration from a YAML file."""
    with open(config_file, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _setup_output_directories(base_dir):
    """Create and return build and dist directories."""
    build_dir = base_dir / "build"
    dist_dir = base_dir / "dist"
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(dist_dir, exist_ok=True)
    return build_dir, dist_dir


def _get_document_paths(base_dir, documents):
    """Resolve document paths to absolute paths."""
    document_paths = {}

    for doc_name in documents:
        if isinstance(doc_name, dict):
            # Format: {"name": "doc_name", "path": "/absolute/path/to/doc"}
            doc_path = Path(doc_name["path"])
            doc_name = doc_name["name"]
        else:
            # Default: document in subdirectory with same name as doc_name
            doc_path = base_dir / doc_name

        document_paths[doc_name] = doc_path.resolve()

    return document_paths


def _validate_document_path(doc_name, doc_path):
    """Validate that a document has all required files."""
    if not doc_path.is_dir():
        logger.warning('Directory missing for document "%s" at %s', doc_name, doc_path)
        return False

    bake_path = doc_path / "bake.py"
    if not bake_path.exists():
        logger.warning('bake.py missing for document "%s"', doc_name)
        return False

    config_yml_path = doc_path / "config.yml"
    if not config_yml_path.exists():
        logger.warning('config.yml missing for document "%s"', doc_name)
        return False

    return bake_path, config_yml_path


def _process_document(doc_name, doc_path, config, build_dir, dist_dir):
    """Process an individual document."""
    validation_result = _validate_document_path(doc_name, doc_path)
    if not validation_result:
        logger.warning('Document "%s" at %s is invalid - skipping', doc_name, doc_path)
        return

    logger.info('Processing document "%s" from %s...', doc_name, doc_path)
    bake_path, config_yml_path = validation_result
    bake_module = _load_document_bake_module(doc_name, bake_path)
    with open(config_yml_path, encoding="utf-8") as f:
        doc_config = yaml.safe_load(f)

    doc_build_dir, doc_dist_dir = _setup_document_output_directories(
        build_dir, dist_dir, doc_name
    )
    paths = {
        "doc_dir": doc_path,
        "templates_dir": doc_path / "templates",
        "pages_dir": doc_path / "pages",
        "images_dir": doc_path / "images",
        "build_dir": doc_build_dir,
        "dist_dir": doc_dist_dir,
    }

    bake_module.process_document(
        paths=paths,
        config=deep_merge(config, doc_config),
        jinja_env=create_env(paths["templates_dir"]),
    )


def _load_document_bake_module(doc_name, bake_path):
    """Load the document's bake.py module."""
    doc_bake = importlib.util.spec_from_file_location(
        f"documents.{doc_name}.bake", bake_path
    )
    module = importlib.util.module_from_spec(doc_bake)
    doc_bake.loader.exec_module(module)
    return module


def _setup_document_output_directories(build_dir, dist_dir, doc_name):
    """Set up and clean document-specific build and dist directories."""
    doc_build_dir = build_dir / doc_name
    doc_dist_dir = dist_dir / doc_name
    os.makedirs(doc_build_dir, exist_ok=True)
    os.makedirs(doc_dist_dir, exist_ok=True)

    for dir_path in [doc_build_dir, doc_dist_dir]:
        for file in os.listdir(dir_path):
            file_path = dir_path / file
            if os.path.isfile(file_path):
                os.remove(file_path)

    return doc_build_dir, doc_dist_dir


if __name__ == "__main__":
    sys.exit(cli())
