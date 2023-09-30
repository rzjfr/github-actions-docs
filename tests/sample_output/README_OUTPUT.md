# <!-- BEGIN_GH_DOCS_NAME -->Valid Test<!-- END_GH_DOCS_NAME -->

<!-- BEGIN_GH_DOCS_DESCRIPTION -->

Proin nec massa orci. Vestibulum elementum purus sed scelerisque vestibulum.
Integer sed tincidunt metus.Cras laoreet ultrices ante, vel euismod nisi.
Etiam dolor augue, posuere in pretium a, tristique ac elit.

<!-- END_GH_DOCS_DESCRIPTION -->

> [!NOTE]
> This action is a <!-- BEGIN_GH_DOCS_RUNS -->`composite`<!-- END_GH_DOCS_RUNS --> action.

## Inputs

<!-- BEGIN_GH_DOCS_INPUTS -->

| parameter    | description                                                                                                                                                            | required | default         |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------- |
| tristique    | In pretium at libero in tempor.                                                                                                                                        | False    | ""              |
| sollicitudin | Nunc odio eros, sollicitudin cursus eros at, finibus sollicitudin nisi.                                                                                                | True     | "default_param" |
| mattis       | Praesent ut magna venenatis, facilisis erat consectetur, accumsan turpis.Pellentesque vulputate, arcu id mattis interdum, ipsum risus auctor eros.Suspendisse potenti. | True     | ""              |
| pellentesque | Nam et malesuada metus, eu interdum ante.                                                                                                                              | False    | "false"         |

<!-- END_GH_DOCS_INPUTS -->

## Outputs

<!-- BEGIN_GH_DOCS_OUTPUTS -->

This Action does not have any outputs.

<!-- END_GH_DOCS_OUTPUTS -->

## Usage

<!-- BEGIN_GH_DOCS_USAGE -->

```yaml
- name: Example Usage
  uses: rzjfr/github-actions-docs/tests/sample_composite_action@main
  with:
    tristique: ""
    sollicitudin: "default_param"
    mattis: ""
    pellentesque: "false"
```

<!-- END_GH_DOCS_USAGE -->
