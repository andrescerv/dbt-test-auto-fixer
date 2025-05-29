# Test Auto-Fix 🤖: Accepted Values Failure

## Critical Information
- **Failing Test**: `{test_short_name}`
- **Model**: {model_name}
- **Column**: {column_name}
- **Expected Values**: {expected_values}
- **Failures**: {failures} record(s) with unexpected values
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

**SECOND**: Identify the actual failing values:

```sql
SELECT {column_name}, COUNT(*) as count
FROM {{{{ ref('{model_name}') }}}}
WHERE {column_name} NOT IN ({expected_values_sql})
GROUP BY {column_name}
ORDER BY count DESC
```

## Decision Framework
- **If failing values are valid per source system** → Update accepted values in schema
- **If failing values are data quality issues** → Fix model logic or add data cleaning
- **If failing values are edge cases** → Add CASE statements to handle them
- **If multiple models affected** → Fix all related models consistently

## Scope Analysis
Check for related models that might have the same issue:
- Look for other models using the same source data
- Search for similar column names across the project
- Consider if this affects both main and export/workspace versions

## Implementation Instructions
1. **Create a clean new branch from main**: `git checkout main && git pull origin main && git checkout -b fix-{model_name}-{column_name}`
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
7. **Create PR** with title: `🤖 Test auto-fix: Add missing accepted values for {model_name}.{column_name}`

## PR Description Template
```
## Summary
Auto-fix for failing accepted values test on `{model_name}`.

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
