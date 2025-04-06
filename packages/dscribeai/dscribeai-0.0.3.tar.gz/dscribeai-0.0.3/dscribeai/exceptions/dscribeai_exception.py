class DScribeAIException(Exception):
    def __init__(self, error_code: str, error_message: str, status_code: int):
        self.error_code = error_code
        self.error_message = error_message
        self.status_code = status_code
        super().__init__(f"[{error_code}] {error_message} (status {status_code})")