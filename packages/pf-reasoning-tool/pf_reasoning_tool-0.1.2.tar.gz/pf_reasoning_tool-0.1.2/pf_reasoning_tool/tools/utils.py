# pf_reasoning_tool/tools/utils.py - TEMPORARY RETRY HELPER TEST
from pathlib import Path
from promptflow.core.tools_manager import list_package_tools as list_tools
print("Executing list_package_tools - Using PF Helper")
# Assuming YAML is in ../yamls relative to this file
YAML_DIR = Path(__file__).resolve().parents[1] / "yamls"
def list_package_tools():
    print(f"Using PF Helper - Looking for tool YAMLs in: {YAML_DIR}")
    try:
        # The helper might expect YAMLs in the *same* dir or use package resources differently
        # Let's try pointing it to the yamls dir first
        tools = list_tools(tools_dir=YAML_DIR) # Pass the specific dir
        print(f"PF Helper returned: {tools.keys()}")
        return tools
    except Exception as e:
        print(f"ERROR using PF Helper: {e}")
        import traceback
        traceback.print_exc()
        return {} # Return empty on error