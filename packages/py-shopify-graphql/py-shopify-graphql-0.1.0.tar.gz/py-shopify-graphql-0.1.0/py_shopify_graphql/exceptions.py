class GraphqlException(Exception):
    def __init__(self, message, code, errors, original_exception):
        super().__init__(message)
        self.code = code
        self.errors = errors
        self.original_exception = original_exception

    def __str__(self):
        return f"{self.args[0]} (Code: {self.code}) | Errors: {self.errors}"