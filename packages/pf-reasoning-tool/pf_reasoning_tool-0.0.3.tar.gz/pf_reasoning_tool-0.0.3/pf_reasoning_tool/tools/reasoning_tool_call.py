# C:\Users\CRVI\OneDrive - Hall & Wilcox\promptflowcustomtools\pf-reasoning-tool-proj\pf_reasoning_tool\tools\reasoning_tool_call.py

# Required imports
from openai import AzureOpenAI, OpenAI
from typing import Union, List, Dict
from promptflow.core import tool
from promptflow.connections import CustomConnection, AzureOpenAIConnection, OpenAIConnection
from promptflow.contracts.types import PromptTemplate
from jinja2 import Template
import re

# === Helper Function: Get OpenAI Client (MODIFIED API VERSION HANDLING) ===
def get_client(connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection]):
    """
    Creates an OpenAI or AzureOpenAI client from a PromptFlow connection.
    **MODIFIED**: Forces a specific API version for Azure connections required by this tool.
    """
    if not connection:
         raise ValueError("Connection object is required.")
    try:
        # Attempt to treat connection as a dictionary first
        connection_dict = dict(connection)
    except (TypeError, ValueError):
         # If not dict-like, access attributes (common for typed connections)
         connection_dict = {
             "api_key": getattr(connection, 'api_key', None),
             "api_base": getattr(connection, 'api_base', None), # Used for OpenAI or fallback for Azure endpoint
             "azure_endpoint": getattr(connection, 'azure_endpoint', None), # Preferred for Azure
             "api_version": getattr(connection, 'api_version', None), # Will be overridden for Azure below
         }

    api_key = connection_dict.get("api_key")
    if not api_key:
        raise ValueError("API key is missing in the connection.")

    if api_key.startswith("sk-"):
        # Standard OpenAI client - remains unchanged
        conn_params = {
            "api_key": api_key,
            "base_url": connection_dict.get("api_base")
        }
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return OpenAI(**client_args)
    else:
        # Azure OpenAI Client
        azure_endpoint = connection_dict.get("azure_endpoint") or connection_dict.get("api_base")
        if not azure_endpoint:
             raise ValueError("Azure endpoint ('azure_endpoint' or 'api_base') is missing in the Azure connection.")

        # ---> Force the required API version here <---
        # Ignore the api_version potentially set in the connection object.
        forced_api_version = "2025-01-01-preview" # Or "2024-12-01-preview" if needed
        print(f"INFO: Forcing Azure OpenAI API Version for this tool: {forced_api_version}")

        conn_params = {
            "api_key": api_key,
            "azure_endpoint": azure_endpoint,
            "api_version": forced_api_version, # Use the forced version
        }
        # Filter None args before creating client
        client_args = {k: v for k, v in conn_params.items() if v is not None}
        return AzureOpenAI(**client_args)
    # --- End get_client function ---


# === Helper Function: Dynamic List for Reasoning Effort (Kept as provided) ===
def get_reasoning_effort_options(**kwargs) -> List[Dict[str, str]]:
    """
    Provides the selectable options for the 'reasoning_effort' parameter.
    kwargs are accepted for compatibility but not used in this static list case.
    """
    options = ["low", "medium", "high"] # Define your allowed values
    result = []
    for option in options:
        result.append({
            "value": option,
            # Kept .capitalize() as it was in the code you just provided
            "display_value": option.capitalize()
        })
    return result


# === Main PromptFlow Tool Function (Name and Arguments Corrected) ===
@tool
def reasoning_llm( # Correct function name
    connection: Union[CustomConnection, AzureOpenAIConnection, OpenAIConnection],
    deployment_name: str,
    prompt_template: PromptTemplate, # Correct argument name
    max_completion_tokens: int = 5000,
    reasoning_effort: str = "low",
    **kwargs
) -> str:
    """
    Calls the specified Azure OpenAI deployment (expected to be o3-mini variant)
    using a PromptTemplate. It parses the rendered prompt for '# system:' and '# user:'
    markers to structure the API call. Allows configuring max tokens and reasoning effort.

    :param connection: PromptFlow connection object (Custom, AzureOpenAI, OpenAI).
    :param deployment_name: The name of the Azure OpenAI deployment.
    :param prompt_template: The PromptTemplate containing the base prompt structure.
    :param max_completion_tokens: The maximum number of tokens to generate.
    :param reasoning_effort: The reasoning effort level ('low', 'medium', 'high').
    :param kwargs: Additional keyword arguments used to render the PromptTemplate.
    :return: The content of the language model's response.
    """
    client = get_client(connection) # This will now use the forced API version for Azure

    # --- Render the Prompt Template ---
    try:
        # Use the correct argument name here
        rendered_prompt = Template(prompt_template, trim_blocks=True, keep_trailing_newline=True).render(**kwargs)
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

    # --- LLM Call (Uses client with forced API version) ---
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