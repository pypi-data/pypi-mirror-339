# C:\Users\CRVI\OneDrive - Hall & Wilcox\promptflowcustomtools\pf-reasoning-tool-proj\pf_reasoning_tool\tools\reasoning_tool_call.py
# --- Adding TEMPERATURE back ---

# Required imports (no changes)
from openai import AzureOpenAI, OpenAI
from typing import Union, List, Dict, Optional # Keep Optional/Dict for future
from promptflow.core import tool
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection
from promptflow.contracts.types import PromptTemplate
from jinja2 import Template
import re

# === Helper Function: Get OpenAI Client (Keep forced API version) ===
# ... (get_client function remains the same) ...
def get_client(connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection]):
    """
    Creates an OpenAI or AzureOpenAI client from a PromptFlow connection.
    Forces a specific API version for Azure connections required by this tool.
    """
    if not connection:
         raise ValueError("Connection object is required.")
    try:
        connection_dict = dict(connection)
    except (TypeError, ValueError):
         connection_dict = {
             "api_key": getattr(connection, 'api_key', None),
             "api_base": getattr(connection, 'api_base', None),
             "azure_endpoint": getattr(connection, 'azure_endpoint', None),
             "api_version": getattr(connection, 'api_version', None),
         }
    api_key = connection_dict.get("api_key")
    if not api_key:
        raise ValueError("API key is missing in the connection.")
    if api_key.startswith("sk-"):
        conn_params = {
            "api_key": api_key,
            "base_url": connection_dict.get("api_base")
        }
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return OpenAI(**client_args)
    else:
        azure_endpoint = connection_dict.get("azure_endpoint") or connection_dict.get("api_base")
        if not azure_endpoint:
             raise ValueError("Azure endpoint ('azure_endpoint' or 'api_base') is missing in the Azure connection.")
        forced_api_version = "2025-01-01-preview"
        print(f"INFO: Forcing Azure OpenAI API Version for this tool: {forced_api_version}")
        conn_params = {
            "api_key": api_key,
            "azure_endpoint": azure_endpoint,
            "api_version": forced_api_version,
        }
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return AzureOpenAI(**client_args)

# === Helper Function: Dynamic List for Reasoning Effort (Keep lowercase options) ===
# ... (get_reasoning_effort_options remains the same) ...
def get_reasoning_effort_options(**kwargs) -> List[Dict[str, str]]:
    """
    Provides the selectable options for the 'reasoning_effort' parameter.
    """
    options = ["low", "medium", "high"]
    result = []
    for option in options:
        result.append({
            "value": option,
            "display_value": option # Display lowercase
        })
    return result

# === Main PromptFlow Tool Function (ADDING temperature) ===
@tool
def reasoning_llm(
    connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection],
    deployment_name: str,
    prompt: PromptTemplate,
    max_completion_tokens: int = 5000,
    reasoning_effort: str = "low",
    # ---> ADDED temperature parameter <---
    temperature: float = 0.7,
    # Keep **kwargs
    **kwargs
) -> str:
    """
    (Version with Temperature)
    Calls the specified Azure OpenAI deployment using a PromptTemplate.
    Parses rendered prompt for '# system:'/'# developer:' and '# user:' markers.
    Allows configuring temperature, max tokens, and reasoning effort.
    (Designed for use with type: custom_llm in YAML)
    """
    client = get_client(connection)

    # --- Render the Prompt Template (no change) ---
    try:
        rendered_prompt = Template(prompt, trim_blocks=True, keep_trailing_newline=True).render(**kwargs)
        print(f"Rendered Prompt:\n{rendered_prompt}")
    except Exception as e:
         raise ValueError(f"Failed to render prompt template: {e}") from e

    # --- Parsing Logic (no change) ---
    developer_content = ""
    user_content = ""
    try:
        developer_marker_pattern = r'#\s*(?:system|developer):(.*?) (?=#\s*user:|$)'
        developer_marker_match = re.search(developer_marker_pattern, rendered_prompt, re.IGNORECASE | re.DOTALL)
        if developer_marker_match:
            developer_content = developer_marker_match.group(1).strip()
        else:
            print("Warning: Neither '# system:' nor '# developer:' marker found. Using empty developer content.")
        user_match = re.search(r'#\s*user:(.*)', rendered_prompt, re.IGNORECASE | re.DOTALL)
        if user_match:
            user_content = user_match.group(1).strip()
        else:
            raise ValueError("Could not find '# user:' marker in the rendered prompt.")
        print(f"Parsed Developer Content: {developer_content[:100]}...")
        print(f"Parsed User Content: {user_content[:100]}...")
    except Exception as e:
        raise ValueError(f"Failed to parse developer/user roles from rendered prompt: {e}") from e

    messages=[
        {"role": "developer", "content": developer_content},
        {"role": "user", "content": user_content}
    ]

    # --- LLM Call (ADDED temperature) ---
    try:
        api_params = {
            "messages": messages,
            "max_completion_tokens": max_completion_tokens,
            "model": deployment_name,
            "reasoning_effort": reasoning_effort,
            # ---> ADDED temperature to API call <---
            "temperature": temperature,
        }
        print(f"API Call Parameters (excluding key): {api_params}")
        response = client.chat.completions.create(**api_params)
        txt = response.choices[0].message.content
        return txt
    except Exception as e:
        print(f"Error calling LLM: {e}")
        raise e
    # --- End LLM Call ---