import time
import requests
from typing import Optional, Dict, Any
from .exceptions import ArkhamSolverError, InvalidAPIKeyError, RateLimitExceededError
from .models import TaskStatusResponse, BalanceResponse
from .constants import DEFAULT_POLL_INTERVAL, DEFAULT_TIMEOUT


class ArkhamSolver:
    """
    A client for solving captchas using the Arkham Solver API (task-based version).

    Args:
        api_key (str): Your API key for the Arkham Solver service
        base_url (str, optional): Base URL for the API endpoint
        poll_interval (float, optional): How often to check task status (seconds)
        timeout (float, optional): Max time to wait for solution (seconds)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://beta.arkham-solver.com",
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        timeout: float = DEFAULT_TIMEOUT
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.poll_interval = poll_interval
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def create_task(
        self,
        preset: str,
        blob: Optional[str] = None,
        proxy: Optional[str] = None,
        cookies: Optional[Dict[str, Any]] = None
    ) -> TaskStatusResponse:
        """
        Create a new captcha solving task.

        Args:
            preset: The preset identifier for the captcha
            blob: Additional blob data required by some captchas
            proxy: Proxy to use for solving
            cookies: Dictionary of cookies to use

        Returns:
            TaskStatusResponse: Initial task status with task_id

        Raises:
            ArkhamSolverError: If task creation fails
        """

        payload = {
            "api_key": self.api_key,
            "preset": preset,
            "blob": blob or None,
            "proxy": proxy,
            "cookies": cookies or {}
        }

        try:
            response = self.session.post(
                f"{self.base_url}/task/create",
                json={k: v for k, v in payload.items() if v is not None}
            )
            self._handle_errors(response)
            return TaskStatusResponse(**response.json())
        except requests.RequestException as e:
            raise ArkhamSolverError(f"Network error: {str(e)}")

    def get_task_status(self, task_id: str) -> TaskStatusResponse:
        """
        Get the current status of a task.

        Args:
            task_id: The ID of the task to check

        Returns:
            TaskStatusResponse: Current task status

        Raises:
            ArkhamSolverError: If status check fails
        """
        try:
            response = self.session.get(
                f"{self.base_url}/task/status/{task_id}"
            )
            self._handle_errors(response)
            return TaskStatusResponse(**response.json())
        except requests.RequestException as e:
            raise ArkhamSolverError(f"Network error: {str(e)}")

    def solve(
        self,
        preset: str,
        blob: Optional[str] = None,
        proxy: Optional[str] = None,
        cookies: Optional[Dict[str, Any]] = None,
        wait: bool = True
    ) -> TaskStatusResponse:
        """
        Solve a captcha (with optional automatic waiting for completion).

        Args:
            preset: The preset identifier for the captcha
            blob: Additional blob data required by some captchas
            proxy: Proxy to use for solving
            cookies: Dictionary of cookies to use
            wait: Whether to wait for solution or return immediately

        Returns:
            TaskStatusResponse: Task status (may be pending or completed)

        Raises:
            ArkhamSolverError: If solving fails
            TimeoutError: If waiting exceeds timeout
        """
        task = self.create_task(preset, blob, proxy, cookies)

        if not wait:
            return task

        start_time = time.time()
        while time.time() - start_time < self.timeout:
            status = self.get_task_status(task.task_id)

            if status.status == "completed":
                return status

            time.sleep(self.poll_interval)

        raise TimeoutError("Captcha solving timed out")

    def check_balance(self) -> BalanceResponse:
        """Check account balance and subscription status."""
        try:
            response = self.session.post(
                f"{self.base_url}/check_balance",
                json={"api_key": self.api_key}
            )
            self._handle_errors(response)
            return BalanceResponse(**response.json())
        except requests.RequestException as e:
            raise ArkhamSolverError(f"Network error: {str(e)}")

    def _handle_errors(self, response: requests.Response):
        """Handle common API errors."""
        if response.status_code == 401:
            raise InvalidAPIKeyError("Invalid API key provided")
        elif response.status_code == 429:
            raise RateLimitExceededError("Rate limit exceeded")
        elif response.status_code != 200:
            raise ArkhamSolverError(
                f"API returned status code {response.status_code}")
