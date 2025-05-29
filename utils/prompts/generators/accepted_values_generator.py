"""
Generator for accepted values test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class AcceptedValuesGenerator(BaseGenerator):
    """Generates prompts for accepted values test failures."""

    def get_template_sections(self, test_data: Dict[str, Any]) -> Dict[str, str]:
        """Get template sections for accepted values test failure."""
        data = self.extract_common_data(test_data)

        # Extract accepted values specific data from simplified structure
        test_parameters = test_data.get("test_parameters", {})
        expected_values = test_parameters.get("values", [])
        expected_values_sql = self.format_expected_values_sql(expected_values)

        return {
            "test_type_title": "Accepted Values",
            "critical_info_section": f"""- **Failing Test**: `{data['test_short_name']}`
- **Model**: {data['model_name']}
- **Model File**: {data['model_file_path']}
- **Column**: {data['column_name']}
- **Expected Values**: {expected_values}
- **Failures**: {data['failures']} record(s) with unexpected values
- **Schema File**: {data['schema_file']}""",
            "investigation_steps": f"""**SECOND**: Identify the actual failing values:

```sql
SELECT {data['column_name']}, COUNT(*) as count
FROM {{{{ ref('{data['model_name']}') }}}}
WHERE {data['column_name']} NOT IN ({expected_values_sql})
GROUP BY {data['column_name']}
ORDER BY count DESC
```""",
            "decision_framework": """- **If failing values are valid per source system** → Update accepted values in schema
- **If failing values are data quality issues** → Fix model logic or add data cleaning
- **If failing values are edge cases** → Add CASE statements to handle them
- **If multiple models affected** → Fix all related models consistently""",
            "scope_analysis": """Check for related models that might have the same issue:
- Look for other models using the same source data
- Search for similar column names across the project
- Consider if this affects both main and export/workspace versions""",
            "branch_name": f"fix-{data['model_name']}-{data['column_name']}",
            "implementation_steps": f"""3. **Run the compiled test query** to understand the failing data using gcloud:
   ```bash
   bq query --use_legacy_sql=false "
   [Copy the compiled test query from above and run it to see the actual failing records]
   "
   ```
4. **Investigate and implement** the appropriate fix based on the decision framework""",
            "pr_title": f"{data['priority']} 🤖 Auto-fix: Add missing accepted values for {data['model_name']}.{data['column_name']}",
            "pr_summary": f"Auto-fix for failing accepted values test on `{data['model_name']}`."
        }

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for accepted values test failure."""
        return self.generate_from_base_template(test_data)
