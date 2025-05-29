"""
Generator for unique test failure prompts.
"""

from typing import Dict, Any
from .base_generator import BaseGenerator


class UniqueGenerator(BaseGenerator):
    """Generates prompts for unique test failures."""

    def get_template_sections(self, test_data: Dict[str, Any]) -> Dict[str, str]:
        """Get template sections for unique test failure."""
        data = self.extract_common_data(test_data)

        return {
            "test_type_title": "Unique",
            "critical_info_section": f"""- **Failing Test**: `{data['test_short_name']}`
- **Model**: {data['model_name']}
- **Model File**: {data['model_file_path']}
- **Column**: {data['column_name']}
- **Failures**: {data['failures']} record(s) with duplicate values
- **Schema File**: {data['schema_file']}""",
            "investigation_steps": f"""**SECOND**: Identify the duplicate values and their frequency:

```sql
SELECT
  {data['column_name']},
  COUNT(*) as duplicate_count
FROM {{{{ ref('{data['model_name']}') }}}}
WHERE {data['column_name']} IS NOT NULL
GROUP BY {data['column_name']}
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC
LIMIT 20
```

**THIRD**: Investigate the duplicate records in detail:

```sql
-- Show full records for the most common duplicate
WITH duplicates AS (
  SELECT {data['column_name']}
  FROM {{{{ ref('{data['model_name']}') }}}}
  GROUP BY {data['column_name']}
  HAVING COUNT(*) > 1
  LIMIT 1
)
SELECT *
FROM {{{{ ref('{data['model_name']}') }}}}
WHERE {data['column_name']} IN (SELECT {data['column_name']} FROM duplicates)
ORDER BY {data['column_name']}
```""",
            "decision_framework": """- **Missing deduplication logic** → Add DISTINCT or window functions to remove duplicates
- **Incorrect grain/grouping** → Review the model's intended grain and GROUP BY logic
- **Source data duplicates** → Investigate upstream data sources for duplicate records
- **JOIN issues** → Check for cartesian products from incorrect JOIN conditions
- **Historical data changes** → Verify if business rules changed about uniqueness
- **Incremental model issues** → Check if incremental logic is creating duplicates""",
            "scope_analysis": """Check for related issues:
- Look for other unique tests on the same model
- Search for similar patterns across other models
- Consider if this affects downstream models that expect unique values""",
            "branch_name": f"fix-{data['model_name']}-{data['column_name']}-unique",
            "implementation_steps": f"""3. **Run the investigation queries** above to understand the duplicate pattern
4. **Implement the appropriate fix** based on the decision framework:
   - **If deduplication needed**: Add DISTINCT or ROW_NUMBER() window function
   - **If grain issue**: Fix GROUP BY logic or model design
   - **If source duplicates**: Add deduplication logic or fix upstream
   - **If JOIN issue**: Fix JOIN conditions to prevent cartesian products""",
            "pr_title": f"🤖 Auto-fix: Fix duplicate values in {data['model_name']}.{data['column_name']}",
            "pr_summary": f"Auto-fix for failing unique test on `{data['model_name']}.{data['column_name']}`."
        }

    def generate(self, test_data: Dict[str, Any]) -> str:
        """Generate prompt for unique test failure."""
        return self.generate_from_base_template(test_data)
