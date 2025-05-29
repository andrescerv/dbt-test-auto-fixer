"""
Generator for unique test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class UniqueGenerator(BaseGenerator):
    """Generates prompts for unique test failures."""

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for unique test failure."""
        # Extract common data
        data = self.extract_common_data(test_data)

        # Load template
        template = self.load_template("unique_template.md")

        # Format template
        return template.format(**data)
