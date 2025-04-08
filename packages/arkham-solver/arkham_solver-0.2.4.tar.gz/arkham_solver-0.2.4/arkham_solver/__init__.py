from .presets import Presets
from .client import ArkhamSolver
from .exceptions import (
    ArkhamSolverError,
    InvalidAPIKeyError,
    RateLimitExceededError,
    CaptchaNotSolvedError
)
from .models import BalanceResponse, TaskStatusResponse, TaskResult

__all__ = [
    'ArkhamSolver',
    'Presets',
    'ArkhamSolverError',
    'InvalidAPIKeyError',
    'RateLimitExceededError',
    'CaptchaNotSolvedError',
    'BalanceResponse',
    'TaskStatusResponse',
    'TaskResult'
]

__version__ = '0.2.4'