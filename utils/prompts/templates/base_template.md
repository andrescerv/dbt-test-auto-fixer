# Test Auto-Fix 🤖: {test_type_title} Test Failure

## Critical Information
{critical_info_section}

## Compiled Test Query
```sql
{compiled_code}
```

## Root Cause Analysis Required
**FIRST**: Run the compiled test query above using gcloud to see the actual failing data:
```bash
bq query --use_legacy_sql=false "
[Copy the compiled test query from above]
"
```

{investigation_steps}

## Decision Framework
{decision_framework}

## Scope Analysis
{scope_analysis}

## Implementation Instructions
1. **Create a clean new branch from main**: `git checkout main && git pull origin main && git checkout -b {branch_name}`
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

---
*This fix was suggested by Augment as part of dbt test fixing automation.*
```

Please investigate the issue and implement the appropriate fix using the decision framework above.
