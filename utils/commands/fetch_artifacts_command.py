"""
Fetch artifacts command - handles CLI concerns for artifact fetching.
"""

import os
from ..artifact_fetcher import fetch_artifacts, fetch_artifacts_from_env


def cmd_fetch_artifacts(args):
    """Handle the fetch-artifacts CLI command."""
    try:
        if args.run_id:
            # Use specific run ID
            account_id = os.environ.get("DBT_CLOUD_ACCOUNT_ID")
            if not account_id:
                print("❌ Error: DBT_CLOUD_ACCOUNT_ID environment variable is required")
                return 1
            success = fetch_artifacts(account_id, args.run_id)
        else:
            # Use last completed run
            success = fetch_artifacts_from_env()

        if success:
            print("✅ Artifacts fetched successfully!")
            return 0
        else:
            print("❌ Failed to fetch artifacts")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
