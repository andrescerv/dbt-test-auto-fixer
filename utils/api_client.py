"""
dbt Cloud API client.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class DbtCloudClient:
    """Client for interacting with dbt Cloud API."""

    def __init__(self, api_token: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the dbt Cloud client."""
        self.api_token = api_token or os.environ.get("DBT_CLOUD_API_TOKEN")
        self.base_url = base_url or os.environ.get("DBT_CLOUD_BASE_URL", "https://cloud.getdbt.com")

        if not self.api_token:
            raise ValueError("API token is required. Set DBT_CLOUD_API_TOKEN environment variable.")

        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Accept": "application/json"
        }

    def get_runs(self, account_id: str, job_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get runs for an account, optionally filtered by job."""
        url = f"{self.base_url}/api/v2/accounts/{account_id}/runs"
        params = {"limit": limit, "order_by": "-id"}

        if job_id:
            params["job_definition_id"] = job_id

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()["data"]

    def get_artifact(self, account_id: str, run_id: str, artifact_name: str) -> Dict[str, Any]:
        """Get an artifact from a specific run."""
        url = f"{self.base_url}/api/v2/accounts/{account_id}/runs/{run_id}/artifacts/{artifact_name}"

        # Use different headers for artifacts - they don't require application/json
        artifact_headers = {
            "Authorization": f"Token {self.api_token}"
        }

        response = requests.get(url, headers=artifact_headers)
        response.raise_for_status()

        return response.json()

    def get_last_completed_run_id(self, account_id: str, job_id: Optional[str] = None) -> Optional[str]:
        """Get the most recent completed run ID."""
        runs = self.get_runs(account_id, job_id, limit=5)

        # Find first completed run (status 10=success, 20=error, 30=cancelled)
        for run in runs:
            if run["status"] in [10, 20, 30]:
                return str(run["id"])

        return None


def get_last_run_id():
    """Get the most recent completed run_id from dbt Cloud."""
    # Get config from environment
    api_token = os.environ.get("DBT_CLOUD_API_TOKEN")
    base_url = os.environ.get("DBT_CLOUD_BASE_URL")
    account_id = os.environ.get("DBT_CLOUD_ACCOUNT_ID")
    job_id = os.environ.get("DBT_CLOUD_JOB_ID")

    if not all([api_token, base_url, account_id, job_id]):
        raise ValueError("Missing required environment variables. Check your .env file.")

    # Make API request
    url = f"{base_url}/api/v2/accounts/{account_id}/runs"
    headers = {"Authorization": f"Token {api_token}"}
    params = {"limit": 3, "order_by": "-id", "job_definition_id": job_id}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    runs = response.json()["data"]

    # Find first completed run (status 10=success, 20=error, 30=cancelled)
    for run in runs:
        if run["status"] in [10, 20, 30]:
            return str(run["id"])

    return None
