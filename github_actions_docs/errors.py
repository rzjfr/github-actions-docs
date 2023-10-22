class GithubActionsDocsError(Exception):
    """Parent class for user errors or input errors.

    Exceptions of this type are handled by the command line tool
    and result in clear error messages, as opposed to backtraces.
    """


class GithubActionsDocsSchemaError(GithubActionsDocsError):
    """Schema errors"""

    def __init__(self, required_fields, field):
        message = f"{required_fields} are required inside {field}.\n"
        super().__init__(message)
