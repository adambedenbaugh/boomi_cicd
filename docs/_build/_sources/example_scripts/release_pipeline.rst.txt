.. _release_pipeline:

release_pipeline.py
###################

The release_pipeline script is the main script used within the boomi_cicd library. It will read through a release JSON
file and creating the package, deploy the processes, schedules, and listener status as defined in the file.

If the package version is not created, then the script will create the package component. Then it will deploy the
version of the packaged component to the desired environment. If the process is a listener, then the listener status
will be set to what is within the release JSON file. If nothing is set, then it defaults to RUNNING. Finally, if a
schedule is defined, then the schedule will be set to the desired schedule.

.. literalinclude:: ../../boomi_cicd/scripts/release_pipeline.py
   :language: python
   :linenos:

Required Environment Variables
------------------------------

* BOOMI_BASE_URL
* BOOMI_ACCOUNT_ID
* BOOMI_USERNAME
* BOOMI_PASSWORD
* BOOMI_ENVIRONMENT_NAME
* BOOMI_WORKING_DIRECTORY
* BOOMI_CLI_BASE_DIR
* BOOMI_RELEASE_BASE_DIR
* BOOMI_RELEASE_FILE (Required if not using the -r command line argument)

Command Line Arguments
----------------------

* -r, --release_file: The release JSON file to use. If not specified, then the BOOMI_RELEASE_FILE environment variable
  will be used.

Release JSON File
-----------------

.. literalinclude:: ../../boomi_cicd/templates/release.json
   :language: json
   :linenos:

