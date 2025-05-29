"""
Base generator with common functionality for all prompt types.
"""

from pathlib import Path
from typing import Dict, Any, List


class BaseGenerator:
    """Base class for prompt generators."""

    def __init__(self):
        """Initialize the base generator."""
        self.templates_dir = Path(__file__).parent.parent / "templates"

    def load_template(self, template_name: str) -> str:
        """Load a template file."""
        template_path = self.templates_dir / template_name
        with open(template_path, 'r') as f:
            return f.read()

    def extract_common_data(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract common data fields from simplified test data."""
        unique_id = test_data.get("unique_id", "")
        related_models = test_data.get("related_models", [])
        test_parameters = test_data.get("test_parameters", {})

        return {
            "test_name": test_data.get("test_name", "unknown_test"),
            "unique_id": unique_id,
            "test_short_name": test_data.get("test_name", "unknown_test"),
            "message": test_data.get("message", ""),
            "failures": test_data.get("failures", 0),
            "compiled_code": test_data.get("compiled_code", ""),
            "related_models": related_models,
            "model_name": related_models[0] if related_models else "unknown_model",
            "column_name": test_parameters.get("column_name", ""),
            "schema_file": test_data.get("schema_file", ""),
            "test_type": test_data.get("test_type", ""),
            "test_parameters": test_parameters,
            "tags": test_data.get("tags", []),
            "severity": test_data.get("severity", ""),
            "error_threshold": test_data.get("error_threshold", ""),
            "warn_threshold": test_data.get("warn_threshold", "")
        }

    def detect_test_type(self, test_data: Dict[str, Any]) -> str:
        """Detect the type of test from simplified test data."""
        # Use the test_type field directly from our simplified metadata
        test_type = test_data.get("test_type")

        if test_type:
            # Map some test types to more user-friendly names
            if test_type == "expect_row_values_to_have_data_for_every_n_datepart":
                return "data_completeness"
            return test_type

        # Fallback to parsing unique_id if test_type is not available
        unique_id = test_data.get("unique_id", "")
        if "accepted_values" in unique_id:
            return "accepted_values"
        elif "not_null" in unique_id:
            return "not_null"
        elif "unique" in unique_id:
            return "unique"
        elif "expression_is_true" in unique_id:
            return "expression_is_true"
        elif "expect_row_values_to_have_data" in unique_id:
            return "data_completeness"
        else:
            return "custom_test"

    def format_expected_values_sql(self, values: List[str]) -> str:
        """Format expected values for SQL IN clause."""
        return ', '.join([f"'{v}'" for v in values])

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement generate method")
