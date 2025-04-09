# pf_reasoning_tool/tools/utils.py - RETRY HELPER, DEFAULT PATH
from pathlib import Path
from promptflow.core.tools_manager import list_package_tools as list_tools
print("Executing list_package_tools - Using PF Helper (Default Path)")
TOOLS_DIR = Path(__file__).parent # Define the directory containing this file
def list_package_tools():
    print(f"Using PF Helper - Looking in default path relative to: {TOOLS_DIR}")
    try:
        # Call helper, potentially pointing to the directory it's in
        tools = list_tools(tools_dir=TOOLS_DIR)
        print(f"PF Helper returned: {tools.keys()}")
        return tools
    except Exception as e:
        print(f"ERROR using PF Helper: {e}")
        import traceback
        traceback.print_exc()
        return {}