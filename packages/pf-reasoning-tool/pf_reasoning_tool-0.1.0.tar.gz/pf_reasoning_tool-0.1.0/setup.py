# C:\Users\CRVI\OneDrive - Hall & Wilcox\promptflowcustomtools\pf-reasoning-tool-proj\setup.py
from setuptools import find_packages, setup

PACKAGE_NAME = "pf_reasoning_tool"

setup(
    name=PACKAGE_NAME,
    version="0.1.0", # Consider incrementing version (e.g., 0.0.2)
    description="Custom PromptFlow tools for Hall & Wilcox", # Updated description
    packages=find_packages(),
    entry_points={
        # This entry point allows PF to find all tools via utils.py
        "package_tools": ["pf_reasoning_tool = pf_reasoning_tool.tools.utils:list_package_tools"],
    },
    # ---> Added Jinja2 and ruamel.yaml (used by current utils.py) <---
    install_requires=[
        "promptflow-core>=1.0.0", # Example: ensure base PF is listed
        "jinja2>=3.0",
        "ruamel.yaml>=0.17",
        "openai>=1.0"
    ],
    include_package_data=True,   # Tells setuptools to include files from MANIFEST.in
)