# github-actions-docs

Generate documentations for github actions and reusable workflows.

# Install

```bash
pip install github-actions-docs
```

Command line:

```bash
github-actions-docs --help
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
