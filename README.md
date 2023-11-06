# github-actions-docs

[![Build Status](https://github.com/rzjfr/github-actions-docs/workflows/build/badge.svg)](https://github.com/rzjfr/github-actions-docs/actions) [![License](https://img.shields.io/github/license/rzjfr/github-actions-docs)](https://github.com/rzjfr/github-actions-docs/blob/master/LICENSE) [![Latest release](https://img.shields.io/github/v/release/rzjfr/github-actions-docs)](https://github.com/rzjfr/github-actions-docs/releases)

Generates documentations for github actions and reusable workflows. For github
actions by default the readme file would be in the same directory as the
`action.yaml`. It's possible to control the name of the generated file.

For reusable workflows as they all should be under
`.github/workflows`, one single readme file will be created or the existing one
will be updated for every reusable workflows under that directory.

In the `description` part of the inputs section if you comment your desired value
in `# Example: <value>` format, `<value>` will be used to generate the `Usage`
section, otherwise, it will try to fill the value of the parameter with default
or it will be empty if none has been detected.

By default the generated file will be generated and injected based on a predefined
template. You can either change the template or modify the tags after generation
to modify the format. If the tags are too much for you can change the `generation-mode`
to be block mode in which only a pair of comment tags will be used instead of a pair
of comment tags per item as it's in the default inline mode.

## Features

- Supports reusable workflows.
- Highly customizable usage section.
- Inline tags for more flexibility.

## Installation

```bash
pip install github-actions-docs
```

Options:

```bash
github-actions-docs --help
#positional arguments:
#  input_files_path      Path of a github action or reusable workflow file(s).
#
#options:
#  -h, --help            show this help message and exit
#  --version             show program's version number and exit
#  --verbose             More verbosity in logging. (default: False)
#  --ignore              Continue on inputs file not being a valid github action or workflow. (default: False)
#  --tag-prefix TAG_PREFIX
#                        Prefix used for the tags in the output. (default: GH_DOCS)
#  --output-mode [{replace,inject}]
#                        Method of output to file. (default: inject)
#  --generation-mode [{inline,block}]
#                        Whether to create tags inline (more flexibility but more noise). (default: inline)
#  --docs-filename DOCS_FILENAME
#                        Creates or updates output on the same path as the input. (default: README.md)
#  --usage-ref-override USAGE_REF_OVERRIDE
#                        Override the uses reference in usage section. By default latest tag or current branch name will be used. (default: )

```

## As a pre-commit hook

Check [pre-commit](https://github.com/pre-commit/pre-commit) for further information.

Sample `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/rzjfr/github-actions-docs
  rev: 0.2.3
  hooks:
    - id: generate-gh-actions-docs
```

## Quick start

Following command creates or updates `.github/actions/example/README.md`.

```bash
github-actions-docs .github/actions/example/action.yaml --verbose
```

If the output file (determined by `--docs-filename`) does not exist, it would be
created based on a default template. If not it would check content of the existing
file for the [tags](#full-list-of-tags) and updates them.

## Full list of tags (for inline generation mode)

| tag name                                | corresponding yaml path                                                       | description                                                                   | type               |
| --------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------ |
| `<!-- GH_DOCS_NAME -->`                 | `.name`                                                                       | Name of the workflow or action                                                | both               |
| `<!-- GH_DOCS_DESCRIPTION -->`          | `.description`                                                                | Description of the workflow or action defaults to file path in workflows      | both               |
| `<!-- GH_DOCS_RUNS -->`                 | `.runs` only for actions                                                      | Type of the action, in workflows it defaults to `reusable workflow` constant  | both               |
| `<!-- GH_DOCS_INPUTS -->`               | `.inputs` for actions and `.on.workflow_call.inputs` for reusable workflows   |                                                                               | both               |
| `<!-- GH_DOCS_OUTPUTS -->`              | `.outputs` for actions and `.on.workflow_call.outputs` for reusable workflows |                                                                               | both               |
| `<!-- GH_DOCS_SECRETS -->`              | `.on.workflow_call.secrets` for reusable workflows                            |                                                                               | reusable workflows |
| `<!-- GH_DOCS_TITLE -->`                | NA                                                                            | Top level header for the reusable workflows, defaults to `Reusable Workflows` | reusable workflows |
| `<!-- GH_DOCS_CONTENTS_TABLE_TITLE -->` | NA                                                                            | Header of table of contents, defaults to `List of workflows`                  | reusable workflows |
| `<!-- GH_DOCS_CONTENTS_TABLE_ITEM -->`  | NA                                                                            | Content of the table of contents, created dynamically.                        | reusable workflows |
| `<!-- GH_DOCS_USAGE -->`                | NA                                                                            | Creates simple usage block. Check `--usage-ref-override`                      | both               |
