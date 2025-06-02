# dbt Test Auto-Fixer 🤖

An intelligent tool for automating the fixing of failed dbt tests by analyzing test failures and generating specialized, actionable prompts for LLM-based solutions.

## Features

- **🔄 One-Command Workflow**: Run the entire process with a single command or use individual commands for granular control
- **📦 Artifact Fetching**: Download dbt Cloud artifacts (run_results.json, manifest.json) via API
- **🔬 Intelligent Test Analysis**: Comprehensive analysis of failed tests with debugging metadata and test type detection
- **🎯 Specialized Prompt Generation**: Generate targeted prompts using specialized generators for different test types:
  - **Not Null Tests**: Focused on null value investigation and JOIN analysis
  - **Unique Tests**: Specialized for duplicate detection and resolution
  - **Accepted Values Tests**: Handles value validation and data quality issues
  - **Generic Tests**: Covers custom tests, expression_is_true, and other complex test types
- **📝 Template-Based System**: Centralized template management with consistent structure across all test types
- **🏷️ Priority-Based Organization**: Automatically categorizes tests by priority (high/medium/low) for efficient triage

## Quick Start

### 1. Environment Setup

Create a `.env` file with your dbt Cloud credentials:

```bash
# dbt Cloud API Configuration
DBT_CLOUD_API_TOKEN=your_api_token_here
DBT_CLOUD_BASE_URL=https://cloud.getdbt.com
DBT_CLOUD_ACCOUNT_ID=your_account_id
DBT_CLOUD_JOB_ID=your_job_id
```

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd auto-fix-dbt-tests

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Basic Usage

#### Recommended: One-Command Workflow
```bash
# Run the complete workflow (recommended for most users)
python dbt_test_fixer.py

# This automatically:
# 1. Gets the last completed run
# 2. Fetches artifacts
# 3. Analyzes failed tests
# 4. Generates specialized prompts for each test type
```

#### Individual Commands (for granular control)
```bash
# Get the last completed run ID
python dbt_test_fixer.py get-last-run

# Fetch artifacts from the last completed run
python dbt_test_fixer.py fetch-artifacts

# Fetch artifacts from a specific run
python dbt_test_fixer.py fetch-artifacts --run-id 70403155779359

# Analyze failed tests
python dbt_test_fixer.py analyze-artifacts

# Analyze failed tests (quiet mode, JSON output only)
python dbt_test_fixer.py analyze-artifacts --quiet --output custom_analysis.json

# Generate specialized prompts for failed tests
python dbt_test_fixer.py generate-prompts
```

## Available Commands

```bash
# Get help
python dbt_test_fixer.py --help

# Default workflow (recommended)
python dbt_test_fixer.py

# Individual commands
python dbt_test_fixer.py get-last-run
python dbt_test_fixer.py fetch-artifacts [--run-id RUN_ID]
python dbt_test_fixer.py analyze-artifacts [--output-path OUTPUT_PATH] [--quiet]
python dbt_test_fixer.py generate-prompts
```

## Project Structure

```
dbt-test-auto-fixer/
├── dbt_test_fixer.py          # Main CLI script with workflow orchestration
├── utils/                     # Core functionality modules
│   ├── __init__.py
│   ├── api_client.py         # dbt Cloud API client
│   ├── artifact_fetcher.py   # Artifact fetching functionality
│   ├── test_analyzer.py      # Test analysis and type detection
│   ├── commands/             # CLI command implementations
│   │   ├── __init__.py
│   │   ├── analyze_artifacts_command.py
│   │   ├── fetch_artifacts_command.py
│   │   ├── generate_prompts_command.py
│   │   └── get_last_run_command.py
│   └── prompts/              # Intelligent prompt generation system
│       ├── __init__.py
│       ├── prompt_manager.py # Coordinates prompt generation
│       ├── generators/       # Specialized prompt generators
│       │   ├── __init__.py
│       │   ├── base_generator.py      # Common functionality
│       │   ├── not_null_generator.py  # Not null test prompts
│       │   ├── unique_generator.py    # Unique test prompts
│       │   ├── accepted_values_generator.py # Accepted values prompts
│       │   └── generic_generator.py   # Custom/complex test prompts
│       └── templates/        # Centralized template system
│           ├── README.md     # Template documentation
│           └── base_template.md # Unified template structure
├── data/
│   ├── artifacts/            # dbt artifacts (gitignored)
│   ├── analysis/             # Analysis outputs with test metadata
│   └── prompts/              # Generated prompts organized by priority
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Environment Variables

The tool requires the following environment variables (set in `.env` file):

- `DBT_CLOUD_API_TOKEN`: Your dbt Cloud API token
- `DBT_CLOUD_BASE_URL`: dbt Cloud base URL (default: https://cloud.getdbt.com)
- `DBT_CLOUD_ACCOUNT_ID`: Your dbt Cloud account ID
- `DBT_CLOUD_JOB_ID`: The job ID to fetch runs from

## Getting dbt Cloud Credentials

1. **API Token**: Go to dbt Cloud → Account Settings → API Access → Create Token
2. **Account ID**: Found in your dbt Cloud URL: `https://cloud.getdbt.com/accounts/{account_id}/`
3. **Job ID**: Go to your dbt Cloud job → URL contains the job ID

## Intelligent Test Analysis & Prompt Generation

### Test Analysis Features

The tool provides comprehensive analysis of failed dbt tests with intelligent test type detection:

- **📊 Test Type Detection**: Automatically identifies test types (not_null, unique, accepted_values, custom, etc.)
- **🏷️ Priority Classification**: Categorizes tests by priority (high/medium/low) based on failure count and test type
- **📈 Detailed Metadata**: Extracts test parameters, related models, schema files, and execution details
- **🔍 Root Cause Hints**: Provides context for debugging with compiled queries and error messages

### Specialized Prompt Generation

Each test type gets a specialized prompt optimized for that specific failure pattern:

#### Not Null Test Prompts
- Focus on JOIN analysis and null value investigation
- Provide specific SQL queries to identify null patterns
- Include decision framework for different null scenarios

#### Unique Test Prompts
- Specialized duplicate detection queries
- Frequency analysis of duplicate values
- Strategies for handling different duplication patterns

#### Accepted Values Test Prompts
- Value validation and data quality focus
- Queries to identify unexpected values
- Framework for updating accepted values vs. fixing data

#### Generic Test Prompts
- Handles custom tests, expression_is_true, and complex business logic tests
- Flexible structure for various test types
- Comprehensive investigation steps

### Output Organization

- **Priority-based file naming**: `{priority}_{test_name}.md` for efficient triage
- **Consistent structure**: All prompts follow the same template for easy review
- **Production data focus**: Emphasizes using production data over potentially stale dev tables
- **Human-readable**: Designed for human review with clear explanations and actionable steps

## Example Workflow Output

When you run `python dbt_test_fixer.py`, you'll see output like:

```
🚀 Starting dbt Test Fixer workflow...
============================================================
📋 Step 1/4: Getting last completed run...
✅ Last completed run: 70403155779359

📦 Step 2/4: Fetching artifacts from last run...
✅ Downloaded run_results.json (1,234 bytes)
✅ Downloaded manifest.json (567,890 bytes)

🔬 Step 3/4: Analyzing failed tests...
📊 Found 5 failed tests:
  - 3 not_null tests (high priority)
  - 1 unique test (medium priority)
  - 1 custom test (low priority)

🔧 Step 4/4: Generating fix prompts...
✅ Generated 5 specialized prompts in data/prompts/
============================================================
✅ Workflow completed successfully!
📁 Check data/prompts/ for individual test fix prompts
📄 Check data/analysis/failed_tests_debug_data.json for detailed analysis
```

## Production Deployment

The modular architecture makes this tool ideal for various deployment scenarios:

- **🔄 CI/CD Integration**: Easily integrate into GitHub Actions or GitLab CI
- **☁️ Cloud Functions**: Containerize for serverless deployment
- **🔀 Airflow DAGs**: Use individual commands as separate DAG tasks
- **🐳 Docker**: Minimal dependencies and straightforward packaging
- **📊 Monitoring**: JSON outputs enable easy integration with monitoring systems

## Advanced Usage

### Custom Template Development

The template system is designed for extensibility. To add a new test type generator:

1. Create a new generator class inheriting from `BaseGenerator`
2. Implement the `get_template_sections()` method
3. Register it in the `PromptManager`

### Integration with LLM Tools

The generated prompts are optimized for use with:
- **Augment Code**: Direct integration for automated PR creation
- **GitHub Copilot**: Copy prompts for inline assistance
- **ChatGPT/Claude**: Structured prompts for manual fixing
- **Custom LLM Workflows**: JSON metadata enables programmatic processing
