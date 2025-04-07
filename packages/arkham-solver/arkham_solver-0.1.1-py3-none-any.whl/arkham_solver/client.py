import requests
from typing import Optional, Dict, Any
from .exceptions import ArkhamSolverError, InvalidAPIKeyError, RateLimitExceededError
from .models import BalanceResponse, SolveResponse


class ArkhamSolver:
    """
    A client for solving captchas using the Arkham Solver API.

    Args:
        api_key (str): Your API key for the Arkham Solver service
        base_url (str, optional): Base URL for the API endpoint. Defaults to production endpoint.
    """

    def __init__(self, api_key: str, base_url: str = "https://beta.arkham-solver.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def solve(
        self,
        preset: str,
        blob: Optional[str] = None,
        proxy: Optional[str] = None,
        cookies: Optional[Dict[str, Any]] = None
    ) -> SolveResponse:
        """
        Solve a captcha with the given parameters.

        Args:
            preset: The preset identifier for the captcha
            blob: Additional blob data required by some captchas
            og_proxy: Proxy to use for solving in format "http://user:pass@ip:port"
            og_cookies: Dictionary of cookies to use for the captcha solving

        Returns:
            SolveResponse: Object containing the solve response data

        Raises:
            ArkhamSolverError: Base exception for captcha solving errors
            InvalidAPIKeyError: When the API key is invalid
            RateLimitExceededError: When rate limits are exceeded
        """

        if not isinstance(preset, str) or not preset.strip():
            raise ValueError("Preset must be a non-empty string")

        payload = {
            "api_key": self.api_key,
            "preset": preset,
            "blob": blob or None,
            "og_proxy": proxy or None,
            "og_cookies": cookies or {}
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = self.session.post(
                f"{self.base_url}/solve",
                json=payload
            )

            if response.status_code == 401:
                raise InvalidAPIKeyError("Invalid API key provided")
            elif response.status_code == 429:
                raise RateLimitExceededError("Rate limit exceeded")
            elif response.status_code != 200:
                raise ArkhamSolverError(
                    f"API returned status code {response.status_code}")

            data = response.json()

            if not data.get("solved", False):
                raise ArkhamSolverError("Captcha could not be solved")

            return SolveResponse(**data)

        except requests.RequestException as e:
            raise ArkhamSolverError(f"Network error: {str(e)}")

    def check_balance(self) -> BalanceResponse:
        """
        Check the current balance and subscription status.

        Returns:
            BalanceResponse: Object containing balance and subscription info

        Raises:
            ArkhamSolverError: If there's an error checking balance
            InvalidAPIKeyError: When the API key is invalid
        """
        payload = {
            "api_key": self.api_key
        }

        try:
            response = self.session.post(
                f"{self.base_url}/check_balance",
                json=payload
            )

            if response.status_code == 401:
                raise InvalidAPIKeyError("Invalid API key provided")
            elif response.status_code != 200:
                raise ArkhamSolverError(
                    f"API returned status code {response.status_code}")

            data = response.json()
            return BalanceResponse(**data)

        except requests.RequestException as e:
            raise ArkhamSolverError(f"Network error: {str(e)}")
