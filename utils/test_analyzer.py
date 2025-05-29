"""
Simple test analysis functionality for failed dbt tests.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List


def analyze_failed_tests(artifacts_dir: str = "data/artifacts", output_path: Optional[str] = None) -> str:
    """
    Analyze failed dbt tests and export simplified metadata.

    Args:
        artifacts_dir: Directory containing run_results.json and manifest.json
        output_path: Optional custom output path for the analysis JSON

    Returns:
        Path to the generated analysis file
    """
    artifacts_path = Path(artifacts_dir)

    # Load dbt artifacts
    with open(artifacts_path / "run_results.json", 'r') as f:
        run_results = json.load(f)

    with open(artifacts_path / "manifest.json", 'r') as f:
        manifest = json.load(f)

    # Find failed tests
    failed_tests = [
        result for result in run_results.get("results", [])
        if result.get("status") == "fail"
    ]

    # Process each failed test
    simplified_tests = []
    for test_result in failed_tests:
        unique_id = test_result.get("unique_id", "")

        # Extract test name from unique_id
        test_name = _extract_test_name(unique_id)

        # Get test definition from manifest
        test_definition = manifest.get("nodes", {}).get(unique_id, {})

        # Extract essential data
        config = test_definition.get("config", {})
        test_metadata = test_definition.get("test_metadata", {})
        refs = test_definition.get("refs", [])

        # Extract test type with fallback detection
        test_type = test_metadata.get("name")
        if not test_type:
            # Use fallback detection for custom tests
            test_type = detect_test_type_from_unique_id(unique_id)

        simplified_test = {
            "unique_id": unique_id,
            "test_name": test_name,
            "status": test_result.get("status", ""),
            "message": test_result.get("message"),
            "failures": test_result.get("failures", 0),
            "compiled_code": test_result.get("compiled_code", ""),
            "tags": config.get("tags", []),
            "severity": config.get("severity"),
            "error_threshold": config.get("error_if"),
            "warn_threshold": config.get("warn_if"),
            "test_type": test_type,
            "test_parameters": test_metadata.get("kwargs", {}),
            "related_models": [ref.get("name", "") for ref in refs if ref.get("name")],
            "dependencies": test_definition.get("depends_on", {}).get("nodes", []),
            "schema_file": test_definition.get("original_file_path")
        }
        simplified_tests.append(simplified_test)

    # Create summary
    summary = {
        "total_failed_tests": len(simplified_tests),
        "failed_tests": simplified_tests
    }

    # Set output path
    if not output_path:
        analysis_dir = Path("data/analysis")
        analysis_dir.mkdir(parents=True, exist_ok=True)
        output_path = analysis_dir / "failed_tests_debug_data.json"
    else:
        output_path = Path(output_path)

    # Write to file
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    return str(output_path)


def _extract_test_name(unique_id: str) -> str:
    """Extract a readable test name from unique_id."""
    if not unique_id:
        return "unknown_test"

    # Split the unique_id by dots
    parts = unique_id.split(".")
    if len(parts) < 2:
        return unique_id

    # dbt generates different patterns for different test types:
    # Generic tests: test.package.descriptive_name.HASH (e.g., accepted_values_table_column.a1b2c3d4e5)
    # Custom tests:  test.package.custom_test_name (e.g., my_custom_validation_test)

    last_part = parts[-1]
    if len(last_part) == 10 and last_part.isalnum():
        # Generic test with hash suffix - extract the descriptive name (second-to-last part)
        if len(parts) >= 3:
            return parts[-2]
        else:
            return last_part
    else:
        # Custom test without hash - use the test name (last part)
        return last_part


def detect_test_type_from_unique_id(unique_id: str) -> str:
    """
    Detect the type of test from unique_id when test_metadata is not available.
    This is the core logic for test type detection.
    """
    if not unique_id:
        return "custom_test"

    # Check for known generic test patterns in unique_id
    if "accepted_values" in unique_id:
        return "accepted_values"
    elif "not_null" in unique_id:
        return "not_null"
    elif "unique" in unique_id:
        return "unique"
    elif "expression_is_true" in unique_id:
        return "expression_is_true"
    elif "expect_row_values_to_have_data" in unique_id:
        return "expect_row_values_to_have_data_for_every_n_datepart"
    else:
        # Default to custom_test for any unrecognized pattern
        return "custom_test"
