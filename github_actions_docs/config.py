# https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddefault
GHA_ACTION_REQUIRED_FIELDS = {"name", "description", "runs"}
# https://docs.github.com/en/actions/using-workflows/reusing-workflows
GHA_WORKFLOW_REQUIRED_FIELDS = {"name", "on", "jobs"}

GH_DOCS_WORKFLOWS_TITLE = "Reusable Workflows"
GH_DOCS_WORKFLOWS_TABLE_OF_CONTENT_TITLE = "List of workflows"

# Templates
DOCS_TEMPLATE_ACTION = """# <!-- {prefix}_NAME -->

<!-- {prefix}_DESCRIPTION -->

> [!NOTE]
> This action is a <!-- {prefix}_RUNS --> action.

## Inputs

<!-- {prefix}_INPUTS -->

## Outputs

<!-- {prefix}_OUTPUTS -->

## Usage

<!-- {prefix}_USAGE -->
"""

DOCS_TEMPLATE_WORKFLOW = """# <!-- {prefix}_TITLE -->

## <!-- {prefix}_CONTENTS_TABLE_TITLE -->

<!-- {prefix}_CONTENTS_TABLE_ITEM -->
"""

DOCS_TEMPLATE_WORKFLOW_ITEM = """## <!-- {prefix}_NAME_ITEM_ID -->

<!-- {prefix}_DESCRIPTION_ITEM_ID -->

### Inputs

<!-- {prefix}_INPUTS_ITEM_ID -->

### Secrets

<!-- {prefix}_SECRETS_ITEM_ID -->

### Outputs

<!-- {prefix}_OUTPUTS_ITEM_ID -->

### Usage

<!-- {prefix}_USAGE_ITEM_ID -->
"""

DOCS_TEMPLATES = {
    "composite": DOCS_TEMPLATE_ACTION,
    "generic": DOCS_TEMPLATE_ACTION,
    "reusable workflow": DOCS_TEMPLATE_WORKFLOW,
    "reusable workflow item": DOCS_TEMPLATE_WORKFLOW_ITEM,
}
