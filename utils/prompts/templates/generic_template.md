# Test Auto-Fix 🤖: {test_type_title} Test Failure

## Critical Information
- **Failing Test**: `{test_short_name}`
- **Test Type**: {test_type}
- **Model**: {model_name}
- **Failures**: {failures} record(s) failing
- **Error Message**: {message}
- **Schema File**: {schema_file}

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

**SECOND**: Analyze the failing records to understand the root cause.

## Decision Framework
- **If data quality issue** → Fix model logic or add data cleaning
- **If test configuration issue** → Update test parameters or thresholds
- **If business logic change** → Update test to reflect new requirements
- **If multiple models affected** → Fix all related models consistently

## Scope Analysis
Check for related models that might have the same issue:
- Look for other models using the same source data
- Search for similar tests across the project
- Consider downstream dependencies

## Implementation Instructions
1. **Create a clean new branch from main**: `git checkout main && git pull origin main && git checkout -b fix-{model_name}-{test_type}`
2. **Run the compiled test query** to understand the failing data using gcloud:
   ```bash
   bq query --use_legacy_sql=false "
   [Copy the compiled test query from above and run it to see the actual failing records]
   "
   ```
3. **Investigate the schema file** (if applicable) using cat command:
   ```bash
   cat {schema_file}
   ```
4. **Investigate and implement** the appropriate fix based on the decision framework
5. **Test your changes**: `dbt test --select {test_short_name}`
6. **Commit with descriptive message**: Explain the root cause and fix implemented
7. **Create PR** with title: `🤖 Auto-fix: {test_type} test for {model_name}`

## PR Description Template
```
## Summary
Auto-fix for failing {test_type} test on `{model_name}`.

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
