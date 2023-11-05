import logging
import sys

from importlib_metadata import metadata

from github_actions_docs.cli import build_args_parser
from github_actions_docs.lib.generator import generate_docs

__version__ = metadata("github-actions-docs")["Version"]
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    """main"""
    description = metadata("github-actions-docs")["Summary"]
    version = "%(prog)s {}".format(__version__)
    args = build_args_parser(description=description, version=version).parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.ignore:
        logging.getLogger().setLevel(logging.WARNING)
    exit_code = generate_docs(
        file_paths=args.input_files_path,
        output_mode=args.output_mode,
        docs_filename=args.docs_filename,
        uses_ref_override=args.uses_ref_override,
        tag_prefix=args.tag_prefix,
        ignore=args.ignore,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
