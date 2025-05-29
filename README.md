# dbt Test Fixer

A simple tool for automating the fixing of failed dbt tests by analyzing test failures and generating targeted prompts for LLM-based solutions.

## Features

- **Artifact Fetching**: Download dbt Cloud artifacts (run_results.json, manifest.json) via API
- **Failed Test Analysis**: Comprehensive analysis of failed tests with debugging metadata
- **Prompt Generation**: Create structured prompts for LLM-based test fixing
- **Simple CLI**: Single script with multiple commands

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
git clone https://github.com/andrescerv/dbt-test-auto-fixer.git
cd dbt-test-auto-fixer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Basic Usage

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
```

## Available Commands

```bash
# Get help
python dbt_test_fixer.py --help

# Get last completed run ID
python dbt_test_fixer.py get-last-run

# Fetch artifacts
python dbt_test_fixer.py fetch-artifacts [--run-id RUN_ID]

# Analyze failed tests
python dbt_test_fixer.py analyze-artifacts [--output OUTPUT_PATH] [--quiet]

# Generate prompts
python dbt_test_fixer.py generate-prompts
```

## Project Structure

```
dbt-test-auto-fixer/
├── dbt_test_fixer.py          # Main script with all commands
├── utils/                     # Helper modules
│   ├── api_client.py         # dbt Cloud API client
│   ├── artifact_fetcher.py   # Artifact fetching functionality
│   └── test_analyzer.py      # Test analysis functionality
├── data/
│   ├── artifacts/            # dbt artifacts (gitignored)
│   ├── analysis/             # Analysis outputs
│   └── prompts/              # Generated prompts
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

## Failed Test Analysis

The tool provides comprehensive analysis of failed dbt tests to help with debugging and fixing issues.

### Analysis Output

The analysis shows:
- List of all failed tests with key details
- Error messages and failure counts
- Execution times and data processed
- Related models and dependencies
- Quick statistics

### JSON Export

Detailed analysis is automatically saved to `data/analysis/failed_tests_debug_data.json` with complete metadata for each failed test.

## Production Deployment

The simplified structure makes this tool ideal for serverless deployment:

- **Cloud Functions**: Single script can be easily containerized
- **Airflow**: Simple to integrate as DAG tasks
- **Docker**: Minimal dependencies and straightforward packaging
