# C:\Users\CRVI\OneDrive - Hall & Wilcox\promptflowcustomtools\pf-reasoning-tool-proj\pf_reasoning_tool\tools\reasoning_tool_call.py

# Required imports
from openai import AzureOpenAI, OpenAI
from typing import Union, List, Dict
from promptflow.core import tool
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection
from promptflow.contracts.types import PromptTemplate
from jinja2 import Template
import re

# === Helper Function: Get OpenAI Client (Remains unchanged) ===
def get_client(connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection]):
    # ... (code for get_client remains exactly the same) ...
    """Creates an OpenAI or AzureOpenAI client from a PromptFlow connection."""
    if not connection:
         raise ValueError("Connection object is required.")
    try:
        connection_dict = dict(connection)
    except TypeError:
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
        api_version = connection_dict.get("api_version") or "2025-01-01-preview" # Default from original
        if not azure_endpoint:
             raise ValueError("Azure endpoint ('azure_endpoint' or 'api_base') is missing in the Azure connection.")
        conn_params = {
            "api_key": api_key,
            "azure_endpoint": azure_endpoint,
            "api_version": api_version,
        }
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return AzureOpenAI(**client_args)

# === Helper Function: Dynamic List for Reasoning Effort (Remains unchanged) ===
def get_reasoning_effort_options(**kwargs) -> List[Dict[str, str]]:
    # ... (code for get_reasoning_effort_options remains exactly the same) ...
    """
    Provides the selectable options for the 'reasoning_effort' parameter.
    kwargs are accepted for compatibility but not used in this static list case.
    """
    options = ["low", "medium", "high"] # Define your allowed values
    result = []
    for option in options:
        result.append({
            "value": option,
            "display_value": option.capitalize() # Show capitalized in UI
        })
    return result


# === Main PromptFlow Tool Function (RENAMED) ===
@tool
# ---> Function name changed here <---
def reasoning_llm(
    connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection],
    deployment_name: str,
    prompt: PromptTemplate,
    max_completion_tokens: int = 5000,
    reasoning_effort: str = "low",
    **kwargs
) -> str:
    # --- Docstring updated to reflect new name potentially, but functionality is same ---
    """
    (Renamed from call_o3_mini_reasoning)
    Calls the specified Azure OpenAI deployment (expected to be o3-mini variant)
    using a PromptTemplate. It parses the rendered prompt for '# system:' and '# user:'
    markers to structure the API call. Allows configuring max tokens and reasoning effort.

    :param connection: PromptFlow connection object (Custom, AzureOpenAI, OpenAI).
    :param deployment_name: The name of the Azure OpenAI deployment.
    :param prompt: The PromptTemplate containing the base prompt structure.
    :param max_completion_tokens: The maximum number of tokens to generate.
    :param reasoning_effort: The reasoning effort level ('low', 'medium', 'high').
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

    # --- Parsing Logic (using rendered_prompt) ---
    developer_content = ""
    user_content = ""
    try:
        system_match = re.search(r'#\s*system:(.*?)(?=#\s*user:|$)', rendered_prompt, re.IGNORECASE | re.DOTALL)
        if system_match:
            developer_content = system_match.group(1).strip()
        else:
            print("Warning: '# system:' marker not found in rendered prompt. Using empty developer content.")

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

    # --- LLM Call (Remains unchanged) ---
    try:
        response = client.chat.completions.create(
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            model=deployment_name,
            reasoning_effort=reasoning_effort
        )
        txt = response.choices[0].message.content
        return txt
    except Exception as e:
        print(f"Error calling LLM: {e}")
        print(f"API Call Parameters (excluding key): messages={messages}, model={deployment_name}, max_completion_tokens={max_completion_tokens}, reasoning_effort={reasoning_effort}")
        raise e