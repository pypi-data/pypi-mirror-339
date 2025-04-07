from .presets import Presets
from .client import ArkhamSolver
from .exceptions import (
    ArkhamSolverError,
    InvalidAPIKeyError,
    RateLimitExceededError,
    CaptchaNotSolvedError
)
from .models import BalanceResponse, SolveResponse

__all__ = [
    'ArkhamSolver',
    'Presets'
    'ArkhamSolverError',
    'InvalidAPIKeyError',
    'RateLimitExceededError',
    'CaptchaNotSolvedError',
    'BalanceResponse',
    'SolveResponse'
]

__version__ = '0.1.1'