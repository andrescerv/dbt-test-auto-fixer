"""
Generator for generic test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class GenericGenerator(BaseGenerator):
    """Generates prompts for generic test failures."""

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for generic test failure."""
        # Extract common data
        data = self.extract_common_data(test_data)

        # Get test type from the data (already processed with user-friendly mapping)
        test_type = test_data.get("test_type", "custom_test")

        # Load template
        template = self.load_template("generic_template.md")

        # Prepare template variables
        template_vars = {
            **data,
            "test_type": test_type,
            "test_type_title": test_type.replace('_', ' ').title()
        }

        # Format template
        return template.format(**template_vars)
