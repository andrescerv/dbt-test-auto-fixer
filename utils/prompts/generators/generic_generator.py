"""
Generator for generic test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class GenericGenerator(BaseGenerator):
    """Generates prompts for generic test failures."""

    def get_template_sections(self, test_data: Dict[str, Any]) -> Dict[str, str]:
        """Get template sections for generic test failure."""
        data = self.extract_common_data(test_data)

        # Get test type from the data (already processed with user-friendly mapping)
        test_type = test_data.get("test_type", "custom_test")
        test_type_title = test_type.replace('_', ' ').title()

        # Format model file paths for display
        model_file_paths = data['model_file_paths']
        if len(model_file_paths) == 1:
            model_files_display = f"- **Model File**: {model_file_paths[0]}"
        elif len(model_file_paths) > 1:
            model_files_display = "- **Model Files**:\n" + "\n".join([f"  - {path}" for path in model_file_paths])
        else:
            model_files_display = "- **Model File**: (not found)"

        return {
            "test_type_title": test_type_title,
            "critical_info_section": f"""- **Failing Test**: `{data['test_short_name']}`
- **Test Type**: {test_type}
- **Model**: {data['model_name']}
{model_files_display}
- **Failures**: {data['failures']} record(s) failing
- **Error Message**: {data['message']}
- **Schema File**: {data['schema_file']}""",
            "investigation_steps": """**SECOND**: Analyze the failing records to understand the root cause.""",
            "decision_framework": """- **If data quality issue** → Fix model logic or add data cleaning
- **If test configuration issue** → Update test parameters or thresholds
- **If business logic change** → Update test to reflect new requirements
- **If multiple models affected** → Fix all related models consistently""",
            "scope_analysis": """Check for related models that might have the same issue:
- Look for other models using the same source data
- Search for similar tests across the project
- Consider downstream dependencies""",
            "branch_name": f"fix-{data['model_name']}-{test_type}",
            "implementation_steps": f"""3. **Run the compiled test query** to understand the failing data using gcloud:
   ```bash
   bq query --use_legacy_sql=false "
   [Copy the compiled test query from above and run it to see the actual failing records]
   "
   ```
4. **Investigate and implement** the appropriate fix based on the decision framework""",
            "pr_title": f"{data['priority']} 🤖 Auto-fix: {test_type} test for {data['model_name']}",
            "pr_summary": f"Auto-fix for failing {test_type} test on `{data['model_name']}`."
        }

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for generic test failure."""
        return self.generate_from_base_template(test_data)
