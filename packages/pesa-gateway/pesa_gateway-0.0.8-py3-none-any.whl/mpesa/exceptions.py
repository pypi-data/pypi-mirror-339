class MPesaError(Exception):
    """Base exception for all MPesa errors"""

    pass


class MPesaAPIError(MPesaError):
    """Exception for errors returned by the MPesa API"""

    pass
