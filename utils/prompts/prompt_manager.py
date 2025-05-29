"""
Prompt Manager - Coordinates prompt generation for different test types.
"""

from .generators import AcceptedValuesGenerator, GenericGenerator


class PromptManager:
    """Manages prompt generation for different test types."""

    def __init__(self):
        """Initialize the prompt manager."""
        self.generators = {
            'accepted_values': AcceptedValuesGenerator(),
            'generic': GenericGenerator()
        }

    def generate_prompt(self, test_data):
        """
        Generate a prompt for fixing a failed test.

        Args:
            test_data: Dictionary containing test failure information

        Returns:
            String containing the generated prompt
        """
        # Determine test type using the simplified metadata
        test_type = test_data.get("test_type", "")
        unique_id = test_data.get("unique_id", "")

        # Get appropriate generator based on test type
        if test_type == "accepted_values" or "accepted_values" in unique_id:
            generator = self.generators['accepted_values']
        else:
            generator = self.generators['generic']

        # Generate prompt
        return generator.generate(test_data)
