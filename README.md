# github-actions-docs

Generate documentations for github actions and reusable workflows.

## Install

```bash
pip install github-actions-docs
```

Command line:

```bash
github-actions-docs --help

```

## Quick start

Following command creates or updates `.github/actions/example/README.md`.

```bash
github-actions-docs .github/actions/example/action.yaml --output-mode inject
```

Sample `README.md`

```markdown
# <!-- GH_DOCS_NAME -->

<!-- GH_DOCS_DESCRIPTION -->

> [!NOTE]
> This action is a <!-- GH_DOCS_RUNS --> action.

## Inputs

<!-- GH_DOCS_INPUTS -->

## Outputs

<!-- GH_DOCS_OUTPUTS -->

## Usage

<!-- GH_DOCS_USAGE -->
```

## As a pre-commit hook

Check [pre-commit](https://github.com/pre-commit/pre-commit) for further information.

Sample `.pre-commit-config.yaml`

```yaml
- repo: https://github.com/rzjfr/github-actions-docs
  rev: 0.1.0
  hooks:
    - id: generate-gh-actions-docs
```
