#!/usr/bin/env python3
"""
dbt Test Fixer - A simple tool for automating the fixing of failed dbt tests.

This script provides functionality to:
- Fetch dbt Cloud artifacts (run_results.json and manifest.json)
- Analyze failed tests and extract debugging metadata
- Generate prompts for fixing failed tests

Usage:
    python dbt_test_fixer.py get-last-run
    python dbt_test_fixer.py fetch-artifacts [--run-id RUN_ID]
    python dbt_test_fixer.py analyze-artifacts [--output OUTPUT_PATH] [--quiet]
    python dbt_test_fixer.py generate-prompts
"""

import sys
import argparse
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.commands import (
    cmd_get_last_run,
    cmd_fetch_artifacts,
    cmd_analyze_artifacts,
    cmd_generate_prompts
)


def cmd_default_workflow():
    """Execute the full workflow: get last run → fetch artifacts → analyze tests → generate prompts."""
    print("🚀 Starting dbt Test Fixer workflow...")
    print("=" * 60)

    try:
        # Step 1: Get last run
        print("📋 Step 1/4: Getting last completed run...")
        from types import SimpleNamespace
        args_mock = SimpleNamespace()

        result = cmd_get_last_run(args_mock)
        if result != 0:
            print("❌ Failed to get last run. Check your environment variables.")
            return 1

        # Step 2: Fetch artifacts
        print("📦 Step 2/4: Fetching artifacts from last run...")
        args_mock = SimpleNamespace(run_id=None)

        result = cmd_fetch_artifacts(args_mock)
        if result != 0:
            print("❌ Failed to fetch artifacts.")
            return 1

        # Step 3: Analyze tests
        print("🔬 Step 3/4: Analyzing failed tests...")
        args_mock = SimpleNamespace(quiet=True, output_path=None)

        result = cmd_analyze_artifacts(args_mock)
        if result != 0:
            print("❌ Failed to analyze tests.")
            return 1

        # Step 4: Generate prompts
        print("🔧 Step 4/4: Generating fix prompts...")
        args_mock = SimpleNamespace()

        result = cmd_generate_prompts(args_mock)
        if result != 0:
            # Check if it's because there are no failed tests
            debug_file = Path("data/analysis/failed_tests_debug_data.json")
            if not debug_file.exists():
                print("✅ No failed tests found - nothing to fix!")
                print("=" * 60)
                print("🎉 All tests are passing! No prompts needed.")
                return 0
            else:
                print("❌ Failed to generate prompts.")
                return 1

        # Success summary
        print("=" * 60)
        print("✅ Workflow completed successfully!")
        print("📁 Check data/prompts/ for individual test fix prompts")
        print("📄 Check data/analysis/failed_tests_debug_data.json for detailed analysis")
        return 0

    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="dbt Test Fixer - Automate fixing of failed dbt tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default workflow (recommended)
  python dbt_test_fixer.py

  # Individual commands for granular control
  python dbt_test_fixer.py get-last-run
  python dbt_test_fixer.py fetch-artifacts
  python dbt_test_fixer.py fetch-artifacts --run-id 70403155779359
  python dbt_test_fixer.py analyze-artifacts
  python dbt_test_fixer.py analyze-artifacts --output custom_analysis.json --quiet
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands (optional - runs full workflow if none specified)")

    # get-last-run command
    subparsers.add_parser("get-last-run", help="Get the last completed run ID")

    # fetch-artifacts command
    fetch_parser = subparsers.add_parser("fetch-artifacts", help="Fetch dbt Cloud artifacts")
    fetch_parser.add_argument("--run-id", help="Specific run ID to fetch artifacts from")

    # analyze-artifacts command
    analyze_parser = subparsers.add_parser("analyze-artifacts", help="Analyze failed tests")
    analyze_parser.add_argument("--output-path", help="Custom output path for analysis JSON")
    analyze_parser.add_argument("--quiet", action="store_true", help="Only output JSON file, no console output")

    # generate-prompts command
    subparsers.add_parser("generate-prompts", help="Generate prompts for fixing failed tests")

    args = parser.parse_args()

    # If no command specified, run the default workflow
    if args.command is None:
        return cmd_default_workflow()
    elif args.command == "get-last-run":
        return cmd_get_last_run(args)
    elif args.command == "fetch-artifacts":
        return cmd_fetch_artifacts(args)
    elif args.command == "analyze-artifacts":
        return cmd_analyze_artifacts(args)
    elif args.command == "generate-prompts":
        return cmd_generate_prompts(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
