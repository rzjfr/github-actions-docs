# github-actions-docs

[![Build Status](https://github.com/rzjfr/github-actions-docs/workflows/build/badge.svg)](https://github.com/rzjfr/github-actions-docs/actions) [![License](https://img.shields.io/github/license/rzjfr/github-actions-docs)](https://github.com/rzjfr/github-actions-docs/blob/master/LICENSE) [![Latest release](https://img.shields.io/github/v/release/rzjfr/github-actions-docs)](https://github.com/rzjfr/github-actions-docs/releases)

Generates documentations for github actions and reusable workflows.

## Features

- Supports reusable workflows.
- Highly customizable usage section.
- Inline tags for more flexibility.

For reusable workflows as they all should be under `.github/workflows`, one single
readme file will be generated for every reusable workflows under that directory.

Commenting `# Example: <value>` format, In the `description` part of the inputs
section will result in `<value>` being picked up as the default value of the
respecting parameter in the usage section. Otherwise the value would be empty
or equal to the `default:`.

## Installation

```bash
pip install github-actions-docs
```

## Usage

```bash
github-actions-docs .github/actions/example/action.yaml
# Creates or updates .github/actions/example/README.md
github-actions-docs .github/actions/example/action.yaml --verbose --dry-run --show-diff
# Does not save anything on the disk and shows the diff between what would have
# been generated if and existing .github/actions/example/README.md
github-actions-docs .github/workflows/reusable_workflow_1.yaml
# Creates or updates .github/workflows/README.md
```

### As a pre-commit hook

Check [pre-commit](https://github.com/pre-commit/pre-commit) for further information.

Sample `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/rzjfr/github-actions-docs
  rev: 0.2.3
  hooks:
    - id: generate-gh-actions-docs
```

### Options

```bash
github-actions-docs --help
#positional arguments:
#  input_files_path      Path of a github action or reusable workflow file(s).
#
#options:
#  -h, --help            show this help message and exit
#  --version             show program's version number and exit
#  --verbose             More verbosity in logging. (default: False)
#  --dry-run             Show content of the generated docs instead of writing it. (default: False)
#  --show-diff           Show diff between existing file and the newly generated one. (default: False)
#  --ignore              Silently ignore invalid files. (default: False)
#  --tag-prefix          Prefix used for the tags in the output. (default: GH_DOCS)
#  --output-mode         Method of output to file. (default: inject) Possible values: [replace, inject]
#  --generation-mode     Whether to create tags inline or only a pair of tags. (default: inline) Possible values: [inline, block]
#  --docs-filename       Creates or updates output on the same path as the input. (default: README.md)
#  --usage-ref-override  Override the uses reference in usage section. By default latest tag or current branch name will be used.
```

## Generation mode

A markdown file will be generated and injected based on a predefined template. You
can create your own template by adding [tags](#full-list-of-tags) directly to your
readme file. Each tag will be replaced by a pair of `BEGIN` and `END` tags enclosing
the corresponding content. That's the inline mode.

If the comment tags are too noisy, you can change the `generation-mode` to the block
mode in which only a pair of comment tags will be used to designate the entire
generated section.

### Full list of tags

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
