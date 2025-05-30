# Test Auto-Fix 🤖: {test_type_title} Test Failure

## Objectives
**Primary Goal**: Fix the failing test to ensure data quality and pipeline reliability.

**Secondary Goal**: Create a human-readable pull request that clearly explains the issue and solution. Remember that a human will review this PR, so keep explanations concise and focused.

## Context Information
**Analysis Date**: {current_date}
**Today**: {day_of_week}, {formatted_date}

*Note: All analysis and decisions should consider data freshness relative to today's date.*

## Critical Information
{critical_info_section}

## Decision Framework
{decision_framework}

## Compiled Test Query
```sql
{compiled_code}
```

## Root Cause Analysis Required
**CRITICAL**: Always use production data for analysis, not local dev tables which may have stale data.

**FIRST**: Run the compiled test query above using gcloud to see the actual failing data:
```bash
bq query --use_legacy_sql=false "
[Copy the compiled test query from above]
"
```

**Important**: Local dbt commands may use dev tables (prefixed with "dbt_acervantes") that contain stale data, causing misleading test failures. Always use gcloud/BigQuery commands to query production data for accurate analysis.

{investigation_steps}

## Scope Analysis
{scope_analysis}

## Implementation Instructions
1. **Create a clean new branch from main**: `git checkout main && git pull origin main && git checkout -b {branch_name}`
2. **Locate and examine the failing model and schema files**: Use the file paths provided in the Critical Information section above to:
   - Locate and verify the failing model file exists
   - Locate and examine the corresponding schema.yml file using: `cat {schema_file}`
   - Understand the current test configuration before proceeding
{implementation_steps}
5. **Test your changes**: `dbt test --select {test_short_name}`
6. **Commit with descriptive message**: Explain the root cause and fix implemented
7. **Create PR** with title: `{pr_title}`

## PR Description Template
```
## Summary
{pr_summary}

## Root Cause
- [Explain what was causing the issue]

## Changes Made
- [Describe the specific fix implemented]

## Test Results
- ✅ `{test_short_name}` now passes
- [Include any other affected tests]

## Impact
- [Describe how this affects the data and downstream dependencies]

## Investigation Details (Optional)
[If helpful for understanding, you may include up to 2 queries that are queriable in BigQuery and their results to show your analysis process. Keep this section brief and only include if it adds value to the human reviewer's understanding.]

---
*This fix was suggested by Augment as part of dbt test fixing automation.*
```

Please investigate the issue and implement the appropriate fix using the decision framework above.
