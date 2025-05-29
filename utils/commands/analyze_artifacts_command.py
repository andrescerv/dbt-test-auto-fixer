"""
Analyze artifacts command - handles CLI concerns for test analysis.
"""

import json
from ..test_analyzer import analyze_failed_tests


def cmd_analyze_artifacts(args):
    """Handle the analyze-artifacts CLI command."""
    try:
        # Call utility function to do the work
        output_path = analyze_failed_tests(output_path=args.output_path)
        
        # Load results for display unless quiet mode
        if not args.quiet:
            with open(output_path, 'r') as f:
                analysis_data = json.load(f)
            failed_tests_data = analysis_data.get("failed_tests", [])
            
            if not failed_tests_data:
                print("✅ No failed tests found!")
                return 0
            
            print(f"\n{'='*60}")
            print(f"FAILED DBT TESTS SUMMARY")
            print(f"{'='*60}")
            print(f"Total failed tests: {len(failed_tests_data)}")
            print(f"{'='*60}\n")
            
            for i, test in enumerate(failed_tests_data, 1):
                print(f"{i}. {test.get('test_name', 'unknown')}")
                print(f"   Status: {test.get('status', '')} | Failures: {test.get('failures', 0)}")
                print(f"   Message: {test.get('message', '')}")
                
                if test.get('test_type'):
                    print(f"   Test Type: {test.get('test_type')}")
                
                if test.get('tags'):
                    print(f"   Tags: {', '.join(test.get('tags', []))}")
                
                if test.get('related_models'):
                    print(f"   Related Models: {', '.join(test.get('related_models', []))}")
                
                print()
            
            print(f"📄 Detailed analysis saved to: {output_path}")
            
            # Print quick stats
            total_failures = sum(test.get('failures', 0) for test in failed_tests_data)
            test_types = {}
            for test in failed_tests_data:
                test_type = test.get('test_type') or "unknown"
                test_types[test_type] = test_types.get(test_type, 0) + 1
            
            print(f"\n📊 Quick Stats:")
            print(f"   • Total test failures: {total_failures}")
            print(f"   • Test types: {', '.join(f'{t}({c})' for t, c in test_types.items())}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have run 'fetch-artifacts' first to download run_results.json and manifest.json")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
