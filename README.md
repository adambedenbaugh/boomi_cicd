The releasePipeline.py script is used to deploy processes to a Boomi environment. It is designed to be used in a CI/CD
pipeline. It will parse a release.json file, check if a package has been created, if not create one, and check if the
package has been deployed, if not deploy it.

The environment varialbes must be set either with an environment file with the command line arguments (-e) or with all
the values set an environment varialbes. The
release file must also be set a release file with the command line arguments (-r) or by defining the file with an
environment varialble.

```bash
releasePipeline.py -r <release-file-location>
```

## Environment Variables

The following environment variables are required to run the releasePipeline.py script. They can be set by environment
variables or by using a .env file.

| Environment Variable   | Description                                              | Required |  
|------------------------|----------------------------------------------------------|----------|
| BOOMI_BASE_URL         | This is the base URL of the Boomi account.               | Yes      |
| BOOMI_USERNAME         | This is the username of the Boomi account.               | Yes      |
| BOOMI_PASSWORD         | This is the password of the Boomi account.               | Yes      |
| BOOMI_ACCOUNT_ID       | This is the account ID of the Boomi account.             | Yes      |
| BOOMI_ATOM_NAME        | This is the atom ID of the Boomi account.                | Yes      |
| BOOMI_ENVIRONMENT_NAME | This is the environment ID of the Boomi account.         | Yes      |
| WORKING_DIRECTORY      | This is the working directory of the CICD runtime agent. | Yes      |

## Release JSON Elements

| Release JSON Element | Description                                                                                                                                                                     | Required        |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| processName          | This is the name of the process and only used for human readability.                                                                                                            | No, but helpful |
| packageVersion       | This is the package version. If one isn't specified, the latest version will be used.                                                                                           | Yes             |       
| componentId          | This is the component ID of the process you want to deploy.                                                                                                                     | Yes             |
| notes                | This is the notes that will be added to the Code Review.                                                                                                                        | No              |
| schedule             | This is the schedule that will be used to deploy the process. Each individual schedule is space delimited. Multiple schedules are semi-colon delimited. Additional notes below. | No              |
| listenerStatus       | This is the status that the listener will be set to when deployed. Values: RUNNING or PAUSED. RUNNING is default.                                                               | No              |

### Schedule Configuration

The schedule element requires 6 space-delimited values in this order: minutes, hours, days of the week, days of the
month,
month, and years. The example `0 0 1 * * *` would execute the process on every Sunday at midnight.

| Field       | Description                                                                                                           |
|-------------|-----------------------------------------------------------------------------------------------------------------------|
| minutes     | 0 is the first minute of the hour — for example, 1:00 A.M. 59 is the last minute of the hour — for example, 1:59 A.M. |
| hours       | Uses a 24-hour clock. 0 is midnight and 12 is noon.                                                                   |
| daysOfWeek  | 1 is Sunday and 7 is Saturday.                                                                                        |
| daysOfMonth | 1 is the first day of the month and 31 is the last day of the month.                                                  |
| month       | 	1 is January and 12 is December. In most cases this is set to an asterisk [*].                                       |
| years       |                                                                                                                       |

Example Release JSON with a batch process, a listener process, and a custom library.

```json
{
  "pipelines": [
    {
      "processName": "An Example Batch Process",
      "packageVersion": "2.0",
      "componentId": "83d6013f-96f5-4a75-a97b-f4934b0ec2e8",
      "notes": "This is an example set of notes",
      "schedule": "0 0 1 * * * ; 30 0 2-7 * * *"
    },
    {
      "processName": "An Example Listener Process",
      "packageVersion": "1.0",
      "componentId": "b24f310b-6a66-4e0d-97a3-26f1e812b79a",
      "notes": "This is an example set of notes",
      "listenerStatus": "RUNNING"
    },
    {
      "processName": "Oracle JDBC Driver",
      "componentId": "7bd40730-6df3-4ba9-b4b2-ed9153dbca6d",
      "packageVersion": "1.0",
      "notes": "Initial deployment"
    }
  ]
}
```

## Release Templates

The following release templates are available. Each template has its own README with instructions on how to use it. They
demonstrate how to use a basic release pipeline to deploy processes to a Boomi environment. The release pipelines can be
used as-is or as a starting point for your own release pipeline. Each release pipeline will parse a release.json file,
check if a package has been created, if not create one, and check if the package has been deployed, if not deploy it.

* [Azure DevOps](boomi_cicd/templates/azure_devops/README.md)
* GitHub Actions: TODO
* Jenkins: TODO