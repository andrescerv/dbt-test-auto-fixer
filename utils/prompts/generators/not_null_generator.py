"""
Generator for not_null test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class NotNullGenerator(BaseGenerator):
    """Generates prompts for not_null test failures."""

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for not_null test failure."""
        # Extract common data
        data = self.extract_common_data(test_data)

        # Load template
        template = self.load_template("not_null_template.md")

        # Format template
        return template.format(**data)
