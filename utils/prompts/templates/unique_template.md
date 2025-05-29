# Test Auto-Fix 🤖: Unique Test Failure

## Critical Information
- **Failing Test**: `{test_short_name}`
- **Model**: {model_name}
- **Column**: {column_name}
- **Failures**: {failures} record(s) with duplicate values
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

**SECOND**: Identify the duplicate values and their frequency:

```sql
SELECT 
  {column_name},
  COUNT(*) as duplicate_count
FROM {{{{ ref('{model_name}') }}}}
WHERE {column_name} IS NOT NULL
GROUP BY {column_name}
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC
LIMIT 20
```

**THIRD**: Investigate the duplicate records in detail:

```sql
-- Show full records for the most common duplicate
WITH duplicates AS (
  SELECT {column_name}
  FROM {{{{ ref('{model_name}') }}}}
  GROUP BY {column_name}
  HAVING COUNT(*) > 1
  LIMIT 1
)
SELECT *
FROM {{{{ ref('{model_name}') }}}}
WHERE {column_name} IN (SELECT {column_name} FROM duplicates)
ORDER BY {column_name}
```

## Common Causes & Decision Framework
- **Missing deduplication logic** → Add DISTINCT or window functions to remove duplicates
- **Incorrect grain/grouping** → Review the model's intended grain and GROUP BY logic
- **Source data duplicates** → Investigate upstream data sources for duplicate records
- **JOIN issues** → Check for cartesian products from incorrect JOIN conditions
- **Historical data changes** → Verify if business rules changed about uniqueness
- **Incremental model issues** → Check if incremental logic is creating duplicates

## Scope Analysis
Check for related issues:
- Look for other unique tests on the same model
- Search for similar patterns across other models
- Consider if this affects downstream models that expect unique values

## Implementation Instructions
1. **Create a clean new branch from main**: `git checkout main && git pull origin main && git checkout -b fix-{model_name}-{column_name}-unique`
2. **Run the investigation queries** above to understand the duplicate pattern
3. **Investigate the schema file**:
   ```bash
   cat {schema_file}
   ```
4. **Implement the appropriate fix** based on the decision framework:
   - **If deduplication needed**: Add DISTINCT or ROW_NUMBER() window function
   - **If grain issue**: Fix GROUP BY logic or model design
   - **If source duplicates**: Add deduplication logic or fix upstream
   - **If JOIN issue**: Fix JOIN conditions to prevent cartesian products
5. **Test your changes**: `dbt test --select {test_short_name}`
6. **Commit with descriptive message**: Explain the root cause and fix implemented
7. **Create PR** with title: `🤖 Auto-fix: Fix duplicate values in {model_name}.{column_name}`

## PR Description Template
```
## Summary
Auto-fix for failing unique test on `{model_name}.{column_name}`.

## Root Cause
- [Explain what was causing the duplicate values]

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
