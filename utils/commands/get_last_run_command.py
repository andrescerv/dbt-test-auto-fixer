"""
Get last run command - handles CLI concerns for getting last completed run ID.
"""

import os
from ..api_client import DbtCloudClient


def cmd_get_last_run(args):
    """Handle the get-last-run CLI command."""
    try:
        account_id = os.environ.get("DBT_CLOUD_ACCOUNT_ID")
        job_id = os.environ.get("DBT_CLOUD_JOB_ID")

        if not account_id or not job_id:
            print("❌ Error: DBT_CLOUD_ACCOUNT_ID and DBT_CLOUD_JOB_ID environment variables are required")
            return 1

        # Use API client utility to get last run
        client = DbtCloudClient()
        run_id = client.get_last_completed_run_id(account_id, job_id)

        if run_id:
            print(f"Last completed run ID: {run_id}")
            print(f"💡 Verify this is the latest run at: https://gi089.us1.dbt.com/deploy/17729/projects/29831/jobs/{job_id}")
            return 0
        else:
            print("No completed runs found")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
