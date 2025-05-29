# Test Auto-Fix 🤖: Not Null Test Failure

## Critical Information
- **Failing Test**: `{test_short_name}`
- **Model**: {model_name}
- **Column**: {column_name}
- **Failures**: {failures} record(s) with null values
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

**SECOND**: Investigate the null records in detail:

```sql
SELECT *
FROM {{{{ ref('{model_name}') }}}}
WHERE {column_name} IS NULL
LIMIT 100
```

**THIRD**: Check for patterns in the null data:

```sql
-- Check if nulls correlate with other columns
SELECT 
  COUNT(*) as null_count,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM {{{{ ref('{model_name}') }}}}) as null_percentage
FROM {{{{ ref('{model_name}') }}}}
WHERE {column_name} IS NULL
```

## Common Causes & Decision Framework
- **Missing JOIN conditions** → Check if nulls come from LEFT JOINs that should be INNER JOINs
- **Source data quality issues** → Investigate upstream data sources
- **Transformation logic gaps** → Review CASE statements, COALESCE usage
- **Recent data pipeline changes** → Check if new data sources introduced nulls
- **Business rule changes** → Verify if nulls are now acceptable for this column

## Scope Analysis
Check for related issues:
- Look for other not_null tests on the same model
- Search for similar column names across other models
- Consider if this affects downstream models that depend on this column

## Implementation Instructions
1. **Create a clean new branch from main**: `git checkout main && git pull origin main && git checkout -b fix-{model_name}-{column_name}-not-null`
2. **Run the investigation queries** above to understand the null data pattern
3. **Investigate the schema file**:
   ```bash
   cat {schema_file}
   ```
4. **Implement the appropriate fix** based on the decision framework:
   - **If JOIN issue**: Fix JOIN conditions in the model
   - **If source data**: Add data cleaning logic or COALESCE
   - **If business rule change**: Update test configuration or remove test
5. **Test your changes**: `dbt test --select {test_short_name}`
6. **Commit with descriptive message**: Explain the root cause and fix implemented
7. **Create PR** with title: `🤖 Auto-fix: Fix null values in {model_name}.{column_name}`

## PR Description Template
```
## Summary
Auto-fix for failing not_null test on `{model_name}.{column_name}`.

## Root Cause
- [Explain what was causing the null values]

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
