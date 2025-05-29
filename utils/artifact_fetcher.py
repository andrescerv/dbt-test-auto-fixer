"""
Simple artifact fetching functionality for dbt Cloud.
"""

import os
import json
from pathlib import Path
from typing import Optional
from .api_client import DbtCloudClient


def fetch_artifacts(account_id: str, run_id: Optional[str] = None, artifacts_dir: str = "data/artifacts") -> bool:
    """
    Fetch run_results.json and manifest.json artifacts from dbt Cloud.

    Args:
        account_id: dbt Cloud account ID
        run_id: Specific run ID, or None to use last completed run
        artifacts_dir: Directory to save artifacts to

    Returns:
        True if artifacts were successfully fetched and saved
    """
    # Initialize API client and output directory
    client = DbtCloudClient()
    output_dir = Path(artifacts_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get run_id if not provided
    if not run_id:
        job_id = os.environ.get("DBT_CLOUD_JOB_ID")
        run_id = client.get_last_completed_run_id(account_id, job_id)
        if not run_id:
            print("No completed runs found")
            return False

    print(f"Fetching artifacts for run {run_id}...")

    # Fetch both required artifacts
    artifacts = ["run_results.json", "manifest.json"]
    success = True

    for artifact_name in artifacts:
        try:
            print(f"Fetching {artifact_name}...")
            artifact_data = client.get_artifact(account_id, run_id, artifact_name)

            # Save to file
            artifact_path = output_dir / artifact_name
            with open(artifact_path, 'w') as f:
                json.dump(artifact_data, f, indent=2)

            print(f"Saved {artifact_name} to {artifact_path}")

        except Exception as e:
            print(f"Error fetching {artifact_name}: {e}")
            success = False

    return success


def fetch_artifacts_from_env(run_id: Optional[str] = None) -> bool:
    """
    Fetch artifacts using environment variables for configuration.

    Args:
        run_id: Specific run ID, or None to use last completed run

    Returns:
        True if artifacts were successfully fetched and saved
    """
    account_id = os.environ.get("DBT_CLOUD_ACCOUNT_ID")

    if not account_id:
        raise ValueError("DBT_CLOUD_ACCOUNT_ID environment variable is required")

    return fetch_artifacts(account_id, run_id)
