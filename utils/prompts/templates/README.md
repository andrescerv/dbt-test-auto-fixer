# Prompt Templates

This directory contains the base template system for generating dbt test fix prompts.

## Template Architecture

### Base Template System
- `base_template.md` - The unified template structure used by all test types
- Contains common sections like "Compiled Test Query", "Implementation Instructions", and "PR Description Template"
- Uses placeholders for variable sections that are filled by specialized generators

## How It Works

Each test type generator (NotNull, Unique, AcceptedValues, Generic) implements the `get_template_sections()` method to define their specific content, which gets inserted into the base template structure.

### Template Variables

The base template uses these placeholder variables:

| Variable | Description |
|----------|-------------|
| `{test_type_title}` | The formatted test type title (e.g., "Not Null", "Unique") |
| `{critical_info_section}` | Test-specific critical information and metadata |
| `{investigation_steps}` | Test-specific investigation queries and analysis steps |
| `{decision_framework}` | Test-specific decision framework bullets |
| `{scope_analysis}` | Test-specific scope analysis guidance |
| `{branch_name}` | Suggested branch name for the fix |
| `{implementation_steps}` | Test-specific implementation steps |
| `{pr_title}` | Suggested PR title |
| `{pr_summary}` | PR summary text |

Plus all standard variables from `BaseGenerator.extract_common_data()`:
- `{test_short_name}`, `{model_name}`, `{column_name}`, `{failures}`, `{compiled_code}`, `{schema_file}`, etc.

## Benefits

- **🎯 Consistency**: All templates share identical structure and formatting
- **🔧 Maintainability**: Changes to shared sections only need to be made in one place
- **📝 DRY Principle**: Eliminates duplication across template files
- **🚀 Flexibility**: Each test type can customize variable sections as needed
- **➕ Extensibility**: Adding new test types requires minimal code

## Usage Example

```python
from utils.prompts.generators import NotNullGenerator

generator = NotNullGenerator()
prompt = generator.generate(test_data)
```

The generator will automatically combine the base template with test-specific sections to create a complete, formatted prompt.
