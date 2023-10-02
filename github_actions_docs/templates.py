DOCS_TEMPLATE_ACTION = """# <!-- GH_DOCS_NAME -->

<!-- GH_DOCS_DESCRIPTION -->

> [!NOTE]
> This action is a <!-- GH_DOCS_RUNS --> action.

## Inputs

<!-- GH_DOCS_INPUTS -->

## Outputs

<!-- GH_DOCS_OUTPUTS -->

## Usage

<!-- GH_DOCS_USAGE -->
"""

DOCS_TEMPLATE_WORKFLOW_ITEM = """## <!-- GH_DOCS_NAME_ITEM_ID -->

<!-- GH_DOCS_DESCRIPTION_ITEM_ID -->

### Inputs

<!-- GH_DOCS_INPUTS_ITEM_ID -->

### Secrets

<!-- GH_DOCS_SECRETS_ITEM_ID -->

### Outputs

<!-- GH_DOCS_OUTPUTS_ITEM_ID -->

### Usage

<!-- GH_DOCS_USAGE_ITEM_ID -->
"""

DOCS_TEMPLATE_WORKFLOW_TOP = """# <!-- GH_DOCS_TITLE -->

## <!-- GH_DOCS_CONTENTS_TABLE_TITLE -->

<!-- GH_DOCS_CONTENTS_TABLE_ITEM -->
"""

DOCS_TEMPLATES = {
    "composite": DOCS_TEMPLATE_ACTION,
    "javascript": DOCS_TEMPLATE_ACTION,
    "docker": DOCS_TEMPLATE_ACTION,
    "reusable workflow": DOCS_TEMPLATE_WORKFLOW_TOP,
    "reusable workflow item": DOCS_TEMPLATE_WORKFLOW_ITEM,
}
