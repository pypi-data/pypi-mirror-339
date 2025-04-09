Usage
=====

.. _installation:

Installation
------------

Raic Foundry offers both CLI and a python SDK, both of which can be installed via pip package.

Please note that the recommended python is version 3.12. And as always, working within a virtual environment is highly recommended

.. code-block:: console

   python3.12 -m venv .venv
   source .venv/bin/activate

To install the raic-foundry package:

.. code-block:: console

    (.venv) $ python3.12 -m pip install --upgrade raic-foundry


Command Line Inferface
----------------------

If you are looking for a command line interface rather than using the sdk, this has now been installed.  Feel free to start crreating data sources and inference runs using the commands below.  

For further information about using the SDK please continue reading the documentation.

.. typer:: raic.foundry.cli.raic_cli.raic_commands
    :prog: raic-foundry
    :width: 120
    :preferred: svg