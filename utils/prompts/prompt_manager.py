"""
Prompt Manager - Coordinates prompt generation for different test types.
"""

from .generators import NotNullGenerator, UniqueGenerator, AcceptedValuesGenerator, GenericGenerator


class PromptManager:
    """Manages prompt generation for different test types."""

    def __init__(self):
        """Initialize the prompt manager."""
        self.generators = {
            'not_null': NotNullGenerator(),
            'unique': UniqueGenerator(),
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
        # Get test type from the improved detection logic
        test_type = test_data.get("test_type", "")

        # Route to appropriate generator based on test type (ordered by importance/frequency)
        if test_type == "not_null":
            generator = self.generators['not_null']
        elif test_type == "unique":
            generator = self.generators['unique']
        elif test_type == "accepted_values":
            generator = self.generators['accepted_values']
        else:
            # Use generic generator for all other test types including:
            # - expression_is_true
            # - expect_row_values_to_have_data_for_every_n_datepart (data_completeness)
            # - custom_test
            # - any unrecognized test types
            generator = self.generators['generic']

        # Generate prompt
        return generator.generate(test_data)
