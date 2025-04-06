class WebChameleonError(Exception):
    """Base exception class for WebChameleon."""

    pass


class ConnectionBlockedError(WebChameleonError):
    """Raised when a connection is blocked by the target site."""

    def __init__(self, status_code: int, message: str = "Connection blocked"):
        self.status_code = status_code
        super().__init__(f"{message} (Status: {status_code})")


class InvalidTargetError(WebChameleonError):
    """Raised when the target URL is invalid."""

    pass


class AuthenticationError(WebChameleonError):
    """Raised when authentication fails."""

    pass
