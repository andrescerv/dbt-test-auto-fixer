"""
Command functions for dbt Test Fixer CLI.
"""

from .get_last_run_command import cmd_get_last_run
from .fetch_artifacts_command import cmd_fetch_artifacts
from .analyze_artifacts_command import cmd_analyze_artifacts
from .generate_prompts_command import cmd_generate_prompts

__all__ = [
    "cmd_get_last_run",
    "cmd_fetch_artifacts",
    "cmd_analyze_artifacts",
    "cmd_generate_prompts"
]
