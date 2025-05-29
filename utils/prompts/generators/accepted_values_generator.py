"""
Generator for accepted values test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class AcceptedValuesGenerator(BaseGenerator):
    """Generates prompts for accepted values test failures."""

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for accepted values test failure."""
        # Extract common data
        data = self.extract_common_data(test_data)

        # Extract accepted values specific data from simplified structure
        test_parameters = test_data.get("test_parameters", {})
        expected_values = test_parameters.get("values", [])

        # Load template
        template = self.load_template("accepted_values_template.md")

        # Prepare template variables
        template_vars = {
            **data,
            "expected_values": expected_values,
            "expected_values_sql": self.format_expected_values_sql(expected_values)
        }

        # Format template
        return template.format(**template_vars)
