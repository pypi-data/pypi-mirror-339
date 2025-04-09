# A Model Context Protocol Server for the British Natural History Museum Data API

This project is a Python MCP (https://modelcontextprotocol.io/introduction) server that allows your LLM to fetch data
from the British Natural History Museum. Data can be fetched from their Specimens or Index Lots collections. More info 
on their Data API is available at https://naturalhistorymuseum.github.io/dataportal-docs/#introduction.

# Developing

This section is for anyone who wants to contribute to the codebase.

## Setup and Install Dependencies

Clone the repository.

The project is configured to use uv (Install link: https://docs.astral.sh/uv/#installation) for dependency management 
and building.
It uses npx (Install link: https://www.npmjs.com/package/npx) to run the MCP inspector.  

Create a virtual env with

```shell
uv venv
```

And install dependencies with

```shell
uv pip install -r pyproject.toml
```

Run the inspector with
```shell
./inspector.sh
```
The inspector should output the localhost URL for accessing its UI.
## Running Unit Tests

```shell
source .venv/bin/activate
pytest
```