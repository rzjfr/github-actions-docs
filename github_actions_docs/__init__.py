import logging
import sys

from importlib_metadata import metadata

from github_actions_docs.cli import build_args_parser
from github_actions_docs.generator import generate_docs

__version__ = metadata("github-actions-docs")["Version"]
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)


def main():
    """main"""
    description = metadata("github-actions-docs")["Description"]
    version = "%(prog)s {}".format(__version__)
    args = build_args_parser(description=description, version=version).parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    exit_code = generate_docs(
        file_paths=args.input_files_path,
        output_mode=args.output_mode,
        docs_filename=args.docs_filename,
        uses_ref_override=args.uses_ref_override,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
