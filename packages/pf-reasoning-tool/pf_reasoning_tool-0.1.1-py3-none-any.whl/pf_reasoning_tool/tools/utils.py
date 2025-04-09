# pf_reasoning_tool/tools/utils.py
from ruamel.yaml import YAML
from pathlib import Path

def collect_tools_from_directory(base_dir) -> dict:
    tools = {}
    yaml_loader = YAML(typ='safe')
    if not Path(base_dir).is_dir():
        print(f"Warning: Tool YAML directory not found: {base_dir}")
        return tools
    for f_path in Path(base_dir).glob("*.yaml"):
        tool_identifier = f_path.stem
        print(f"Found potential tool YAML: {f_path.name}, attempting to load with identifier: {tool_identifier}")
        try:
            with open(f_path, "r", encoding='utf-8') as f_handle:
                tool_definition = yaml_loader.load(f_handle)
                if isinstance(tool_definition, dict) and tool_definition.get("function"):
                    tools[tool_identifier] = tool_definition
                    print(f"  > Successfully loaded tool: {tool_identifier}")
                else:
                    print(f"  > Warning: File {f_path.name} does not appear to be a valid tool definition. Skipping.")
        except Exception as e:
            print(f"  > Error loading or processing YAML file {f_path.name}: {e}")
    if not tools:
        print(f"Warning: No valid tool YAML files found in {base_dir}")
    return tools

def list_package_tools():
    yaml_dir = Path(__file__).resolve().parents[1] / "yamls"
    print(f"Executing list_package_tools - Looking for tool YAMLs in: {yaml_dir}")
    return collect_tools_from_directory(yaml_dir)