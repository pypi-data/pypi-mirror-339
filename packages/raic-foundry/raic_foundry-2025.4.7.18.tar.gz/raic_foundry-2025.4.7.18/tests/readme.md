# Raic Foundry Tests

## Initial Setup Required

Before executing the scenarios, written as python tests, the following script needs to be executed to pull down some dependencies locally that are not checked in.

Make sure that you are authenticated via the Azure CLI

```sh
az cloud set --name AzureCloud
az login
```

The following needs to be installed beforehand (may already be included as part of the devcontainer):

- Pip

```sh
cd pythonlibs/raic-foundry/tests
chmod +x ./setup/*.sh
./setup/initialize_test_data.sh
```

## Create and Select Python Environment

Ctrl+Shift+P Python: Create Environment...
-> Venv -> pythonlibs -> Python 3.12.7 -> OK
Ctrl+Shift+P Python: Clear Workspace Interpreter Setting -> Clear All
Restart vscode
Ctrl+Shift+P Python: Select Interpreter
-> Select at workspace level -> Python 3.12.17 (.venv) pythonlibs

Open a new prompt within pythonlibs

```sh
pip install -e /workspaces/raic-v2/pythonlibs/raic-foundry
```

To add these tests to the VS Code Test Explorer, open the Testing tab and click Configure Python Tests.
-> Select a test framework/tool to enable:  unittest
-> Select the directory containing the tests: test
-> Select the pattern to identity test files: test*.py

Close VS Code and reopen it.  The Test Explorer will refresh with the exist list if inference pipeline tests.

## Run Scenarios

Each test is designed to be a working example of how the inference pipeline executes in different circumstances.  

To execute a test:

Option 1:
In VS Code with the test py files open click on the colored circle along the right of each test.  This will execute that test.

Option 2:
Execute via the VS Code Test Python Test Explorer.  Make sure the execute the tests individually at the deepest level of the tree.  The higher levels do not appear to work correctly at this time.
