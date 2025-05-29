"""
Generate prompts command - handles CLI concerns for prompt generation.
"""

import json
from pathlib import Path
from ..prompts import PromptManager


def cmd_generate_prompts(args):
    """Handle the generate-prompts CLI command."""
    try:
        # Check if analysis file exists
        analysis_file = Path("data/analysis/failed_tests_debug_data.json")
        if not analysis_file.exists():
            print("❌ No failed tests analysis found. Run 'analyze-artifacts' first.")
            return 1
        
        # Load failed tests data
        with open(analysis_file, 'r') as f:
            analysis_data = json.load(f)
        
        failed_tests = analysis_data.get("failed_tests", [])
        if not failed_tests:
            print("✅ No failed tests to generate prompts for!")
            return 0
        
        # Create prompts directory
        prompts_dir = Path("data/prompts")
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize prompt manager
        prompt_manager = PromptManager()
        
        print(f"🔧 Generating prompts for {len(failed_tests)} failed tests...")
        
        generated_count = 0
        for i, test in enumerate(failed_tests, 1):
            try:
                # Generate prompt using prompt manager
                prompt_content = prompt_manager.generate_prompt(test)
                
                # Create filename
                test_name = test.get("test_name", f"test_{i}")
                safe_test_name = "".join(c for c in test_name if c.isalnum() or c in "_-")
                filename = f"{i:02d}_{safe_test_name}.md"
                
                # Write prompt file
                prompt_file = prompts_dir / filename
                with open(prompt_file, 'w') as f:
                    f.write(prompt_content)
                
                print(f"  ✅ Generated: {filename}")
                generated_count += 1
                
            except Exception as e:
                print(f"  ❌ Failed to generate prompt for test {i}: {e}")
        
        print(f"\n🎉 Generated {generated_count} prompts in {prompts_dir}")
        return 0
        
    except Exception as e:
        print(f"❌ Error generating prompts: {e}")
        return 1
