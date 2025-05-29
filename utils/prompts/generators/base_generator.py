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
        model_file_paths = test_data.get("model_file_paths", [])
        test_parameters = test_data.get("test_parameters", {})

        return {
            "test_name": test_data.get("test_name", "unknown_test"),
            "unique_id": unique_id,
            "test_short_name": test_data.get("test_name", "unknown_test"),
            "message": test_data.get("message", ""),
            "failures": test_data.get("failures", 0),
            "compiled_code": test_data.get("compiled_code", ""),
            "related_models": related_models,
            "model_file_paths": model_file_paths,
            "model_name": related_models[0] if related_models else "unknown_model",
            "model_file_path": model_file_paths[0] if model_file_paths else "",
            "column_name": test_parameters.get("column_name", ""),
            "schema_file": test_data.get("schema_file", ""),
            "test_type": test_data.get("test_type", ""),
            "test_parameters": test_parameters,
            "tags": test_data.get("tags", []),
            "severity": test_data.get("severity", ""),
            "error_threshold": test_data.get("error_threshold", ""),
            "warn_threshold": test_data.get("warn_threshold", ""),
            "priority": test_data.get("priority", "unknown_priority")
        }

    def format_expected_values_sql(self, values: List[str]) -> str:
        """Format expected values for SQL IN clause."""
        return ', '.join([f"'{v}'" for v in values])

    def load_base_template(self) -> str:
        """Load the base template file."""
        return self.load_template("base_template.md")

    def get_template_sections(self, test_data: Dict[str, Any]) -> Dict[str, str]:
        """Get template sections - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_template_sections method")

    def generate_from_base_template(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt using base template with sections."""
        # Extract common data
        data = self.extract_common_data(test_data)

        # Get template sections from subclass
        sections = self.get_template_sections(test_data)

        # Load base template
        base_template = self.load_base_template()

        # Combine common data with sections
        template_vars = {**data, **sections}

        # Format template
        return base_template.format(**template_vars)

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement generate method")
