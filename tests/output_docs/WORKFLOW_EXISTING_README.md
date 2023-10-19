# Github Action: <!-- BEGIN_GH_DOCS_NAME -->Valid Workflow Test 2<!-- END_GH_DOCS_NAME -->

This action is a <!-- BEGIN_GH_DOCS_RUNS -->`reusable workflow`<!-- END_GH_DOCS_RUNS --> action and you can find description here:

<!-- BEGIN_GH_DOCS_DESCRIPTION -->

[tests/input_files/valid_workflow_2.yaml](valid_workflow_2.yaml)

<!-- END_GH_DOCS_DESCRIPTION -->

** Usage **

<!-- BEGIN_GH_DOCS_USAGE -->

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

<!-- END_GH_DOCS_USAGE -->

## Inputs

<!-- BEGIN_GH_DOCS_INPUTS -->

| parameter   | description                      | type        | required | default   |
| ----------- | -------------------------------- | ----------- | -------- | --------- |
| config-path |                                  | string      | false    | ""        |
| logLevel    | Log level                        | choice      | true     | "warning" |
| print_tags  | True to print to STDOUT          | boolean     | true     |           |
| tags        | Test scenario tags               | string      | true     | ""        |
| environment | Environment to run tests against | environment | true     | ""        |

<!-- END_GH_DOCS_INPUTS -->

## Suspendisse

Suspendisse sit amet ipsum interdum, blandit augue et, condimentum dolor.

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
