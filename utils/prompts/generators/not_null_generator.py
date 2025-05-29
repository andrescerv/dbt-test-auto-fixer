"""
Generator for not_null test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class NotNullGenerator(BaseGenerator):
    """Generates prompts for not_null test failures."""

    def get_template_sections(self, test_data: Dict[str, Any]) -> Dict[str, str]:
        """Get template sections for not_null test failure."""
        data = self.extract_common_data(test_data)

        return {
            "test_type_title": "Not Null",
            "critical_info_section": f"""- **Failing Test**: `{data['test_short_name']}`
- **Model**: {data['model_name']}
- **Model File**: {data['model_file_path']}
- **Column**: {data['column_name']}
- **Failures**: {data['failures']} record(s) with null values
- **Schema File**: {data['schema_file']}""",
            "investigation_steps": f"""**SECOND**: Investigate the null records in detail:

```sql
SELECT *
FROM {{{{ ref('{data['model_name']}') }}}}
WHERE {data['column_name']} IS NULL
LIMIT 100
```

**THIRD**: Check for patterns in the null data:

```sql
-- Check if nulls correlate with other columns
SELECT
  COUNT(*) as null_count,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {{{{ ref('{data['model_name']}') }}}}) as null_percentage
FROM {{{{ ref('{data['model_name']}') }}}}
WHERE {data['column_name']} IS NULL
```""",
            "decision_framework": """- **Missing JOIN conditions** → Check if nulls come from LEFT JOINs that should be INNER JOINs
- **Source data quality issues** → Investigate upstream data sources
- **Transformation logic gaps** → Review CASE statements, COALESCE usage
- **Recent data pipeline changes** → Check if new data sources introduced nulls
- **Business rule changes** → Verify if nulls are now acceptable for this column""",
            "scope_analysis": """Check for related issues:
- Look for other not_null tests on the same model
- Search for similar column names across other models
- Consider if this affects downstream models that depend on this column""",
            "branch_name": f"fix-{data['model_name']}-{data['column_name']}-not-null",
            "implementation_steps": f"""2. **Run the investigation queries** above to understand the null data pattern
3. **Investigate the schema file**:
   ```bash
   cat {data['schema_file']}
   ```
4. **Implement the appropriate fix** based on the decision framework:
   - **If JOIN issue**: Fix JOIN conditions in the model
   - **If source data**: Add data cleaning logic or COALESCE
   - **If business rule change**: Update test configuration or remove test""",
            "pr_title": f"🤖 Auto-fix: Fix null values in {data['model_name']}.{data['column_name']}",
            "pr_summary": f"Auto-fix for failing not_null test on `{data['model_name']}.{data['column_name']}`."
        }

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for not_null test failure."""
        return self.generate_from_base_template(test_data)
