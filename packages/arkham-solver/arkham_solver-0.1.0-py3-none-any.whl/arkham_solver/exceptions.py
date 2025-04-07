class ArkhamSolverError(Exception):
    """Base exception for all Arkham Solver related errors"""
    pass

class InvalidAPIKeyError(ArkhamSolverError):
    """Raised when an invalid API key is provided"""
    pass

class RateLimitExceededError(ArkhamSolverError):
    """Raised when the API rate limit is exceeded"""
    pass

class CaptchaNotSolvedError(ArkhamSolverError):
    """Raised when the captcha could not be solved"""
    pass