# C:\Users\CRVI\OneDrive - Hall & Wilcox\promptflowcustomtools\pf-reasoning-tool-proj\pf_reasoning_tool\tools\reasoning_tool_call.py

# Required imports
from openai import AzureOpenAI, OpenAI
# ---> Make dict optional for response_format <---
from typing import Union, List, Dict, Optional
from promptflow.core import tool
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection
from promptflow.contracts.types import PromptTemplate
from jinja2 import Template
import re

# === Helper Function: Get OpenAI Client (Includes forced API version) ===
# ... (get_client function remains the same as the previous version with forced API) ...
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


# === Helper Function: Dynamic List for Reasoning Effort (Lowercase options) ===
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

# === Main PromptFlow Tool Function (ADDED temperature & response_format) ===
@tool
def reasoning_llm(
    connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection],
    deployment_name: str,
    prompt: PromptTemplate,
    max_completion_tokens: int = 5000,
    reasoning_effort: str = "low",
    # ---> ADDED temperature parameter <---
    temperature: float = 0.7, # Common default, adjust if needed
    # ---> ADDED response_format parameter <---
    response_format: Optional[Dict] = None, # Use dict for object type, default to None
    **kwargs
) -> str:
    """
    Calls the specified Azure OpenAI deployment using a PromptTemplate.
    Parses rendered prompt for '# system:'/'# developer:' and '# user:' markers.
    Allows configuring temperature, response_format, max tokens, and reasoning effort.
    (Designed for use with type: custom_llm in YAML)

    :param connection: PromptFlow connection object.
    :param deployment_name: The name of the Azure OpenAI deployment.
    :param prompt: The PromptTemplate containing the base prompt structure.
    :param max_completion_tokens: Max tokens for the completion.
    :param reasoning_effort: Reasoning effort level ('low', 'medium', 'high').
    :param temperature: Sampling temperature (e.g., 0.7).
    :param response_format: OpenAI response format object (e.g., {"type": "text"} or {"type": "json_object"}).
    :param kwargs: Additional keyword arguments used to render the PromptTemplate.
    :return: The content of the language model's response.
    """
    client = get_client(connection)

    # --- Render the Prompt Template ---
    try:
        rendered_prompt = Template(prompt, trim_blocks=True, keep_trailing_newline=True).render(**kwargs)
        print(f"Rendered Prompt:\n{rendered_prompt}")
    except Exception as e:
         raise ValueError(f"Failed to render prompt template: {e}") from e

    # --- Parsing Logic - Remains the same ---
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
    # --- End Parsing Logic ---

    # --- LLM Call (ADDED temperature & response_format) ---
    try:
        # Build parameters dynamically to handle optional response_format
        api_params = {
            "messages": messages,
            "max_completion_tokens": max_completion_tokens,
            "model": deployment_name,
            "reasoning_effort": reasoning_effort,
            "temperature": temperature, # Add temperature
        }
        if response_format: # Only add if response_format is provided
            api_params["response_format"] = response_format

        print(f"API Call Parameters (excluding key): {api_params}") # Updated print

        response = client.chat.completions.create(**api_params) # Unpack parameters

        txt = response.choices[0].message.content
        return txt
    except Exception as e:
        print(f"Error calling LLM: {e}")
        # Optionally log parameters again on error
        # print(f"API Call Parameters on Error (excluding key): {api_params}")
        raise e
    # --- End LLM Call ---