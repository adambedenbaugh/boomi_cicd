boomi-cicd-cli-py docs
======================================

.. note::

   This is a work in progress.  Please check back later for more information.

The boomi-cicd-cli-py library is used to automate Boomi deployments through the CICD Pipelines that your are already using.
It performs orchestration for deploying and managing Boomi runtimes, components, and metadata required for CI/CD.
The Release Pipeline Configuration section has the common pipelines that are used

Project Structure
=================

The project is broken into three sections.

1. scripts - This directory contains the scripts that will be executed within a CI/CD pipeline.
   The release_pipeline.py is the main script. There are additional example scripts that can be used as a starting point
   for your own pipelines.
2. util - This directory contains the utility scripts that are used by the scripts in the scripts
   directory.
3. templates - This directory contains the release pipeline templates. These templates can be
   used as-is or as a starting point for your own release pipeline.

Below is a list of the documentation available:

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   getting_started/Getting Started
   example_scripts/Example CICD Scripts
   pipelines/Release Pipeline Configuration
   modules/Modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

