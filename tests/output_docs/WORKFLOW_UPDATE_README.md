# <!-- BEGIN_GH_DOCS_TITLE -->Reusable Workflows<!-- END_GH_DOCS_TITLE -->

## <!-- BEGIN_GH_DOCS_CONTENTS_TABLE_TITLE -->List of workflows<!-- END_GH_DOCS_CONTENTS_TABLE_TITLE -->

<!-- BEGIN_GH_DOCS_CONTENTS_TABLE_ITEM -->

- [Valid Workflow Test 1](#valid-workflow-test-1)
- [Valid Workflow Test 2](#valid-workflow-test-2)
<!-- END_GH_DOCS_CONTENTS_TABLE_ITEM -->

## <!-- BEGIN_GH_DOCS_NAME_VALID_WORKFLOW_TEST_1 -->Valid Workflow Test 1<!-- END_GH_DOCS_NAME_VALID_WORKFLOW_TEST_1 -->

<!-- BEGIN_GH_DOCS_DESCRIPTION_VALID_WORKFLOW_TEST_1 -->

[tests/input_files/valid_workflow_1.yaml](valid_workflow_1.yaml)

<!-- END_GH_DOCS_DESCRIPTION_VALID_WORKFLOW_TEST_1 -->

### Inputs

<!-- BEGIN_GH_DOCS_INPUTS_VALID_WORKFLOW_TEST_1 -->

| parameter     | description | type    | required | default |
| ------------- | ----------- | ------- | -------- | ------- |
| boolean_value |             | boolean | false    | true    |

<!-- END_GH_DOCS_INPUTS_VALID_WORKFLOW_TEST_1 -->

### Secrets

<!-- BEGIN_GH_DOCS_SECRETS_VALID_WORKFLOW_TEST_1 -->

This item does not have any secrets.

<!-- END_GH_DOCS_SECRETS_VALID_WORKFLOW_TEST_1 -->

### Outputs

<!-- BEGIN_GH_DOCS_OUTPUTS_VALID_WORKFLOW_TEST_1 -->

This item does not have any outputs.

<!-- END_GH_DOCS_OUTPUTS_VALID_WORKFLOW_TEST_1 -->

### Usage

<!-- BEGIN_GH_DOCS_USAGE_VALID_WORKFLOW_TEST_1 -->

```yaml
jobs:
  call-workflow:
    uses: rzjfr/github-actions-docs/tests/input_files/valid_workflow_1.yaml@main
    with:
      boolean_value: true
```

<!-- END_GH_DOCS_USAGE_VALID_WORKFLOW_TEST_1 -->

## <!-- BEGIN_GH_DOCS_NAME_VALID_WORKFLOW_TEST_2 -->Valid Workflow Test 2<!-- END_GH_DOCS_NAME_VALID_WORKFLOW_TEST_2 -->

<!-- BEGIN_GH_DOCS_DESCRIPTION_VALID_WORKFLOW_TEST_2 -->

[tests/input_files/valid_workflow_2.yaml](valid_workflow_2.yaml)

<!-- END_GH_DOCS_DESCRIPTION_VALID_WORKFLOW_TEST_2 -->

### Inputs

<!-- BEGIN_GH_DOCS_INPUTS_VALID_WORKFLOW_TEST_2 -->

| parameter   | description                      | type        | required | default   |
| ----------- | -------------------------------- | ----------- | -------- | --------- |
| config-path |                                  | string      | false    | ""        |
| logLevel    | Log level                        | choice      | true     | "warning" |
| print_tags  | True to print to STDOUT          | boolean     | true     |           |
| tags        | Test scenario tags               | string      | true     | ""        |
| environment | Environment to run tests against | environment | true     | ""        |

<!-- END_GH_DOCS_INPUTS_VALID_WORKFLOW_TEST_2 -->

### Secrets

<!-- BEGIN_GH_DOCS_SECRETS_VALID_WORKFLOW_TEST_2 -->

| parameter | description | required |
| --------- | ----------- | -------- |
| envPAT    |             | True     |

<!-- END_GH_DOCS_SECRETS_VALID_WORKFLOW_TEST_2 -->

### Outputs

<!-- BEGIN_GH_DOCS_OUTPUTS_VALID_WORKFLOW_TEST_2 -->

| parameter  | description              |
| ---------- | ------------------------ |
| firstword  | The first output string  |
| secondword | The second output string |

<!-- END_GH_DOCS_OUTPUTS_VALID_WORKFLOW_TEST_2 -->

### Usage

<!-- BEGIN_GH_DOCS_USAGE_VALID_WORKFLOW_TEST_2 -->

```yaml
jobs:
  call-workflow:
    uses: rzjfr/github-actions-docs/tests/input_files/valid_workflow_2.yaml@main
    with:
      config-path: ""
      logLevel: "warning"
      print_tags: 
      tags: ""
      environment: ""
```

<!-- END_GH_DOCS_USAGE_VALID_WORKFLOW_TEST_2 -->
