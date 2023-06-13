# Getting Started

## Release JSON File

The scripts mentioned above are based on the release.json file. The file includes all components that need to be
deployed and any schedules or listener status that needs to be configured.

| Release JSON Element | Description                                                                                                                                                             | Required |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| processName          | Name of the process. Mainly used for human readability.                                                                                                                 | Yes      |
| packageVersion       | Define the package version. If one isn't specified, the latest version will be used.                                                                                    | Yes      | 
| componentId          | The component ID of the process to deploy.                                                                                                                              | Yes      |
| notes                | The notes that will be added to the packaged components and deployments.                                                                                                | No       |
| schedule             | The schedule that will be used to deploy the process. Each individual schedule is space delimited. Multiple schedules are semi-colon delimited. Additional notes below. | No       |
| listenerStatus       | The status of the listener when deployed. Values: RUNNING or PAUSED. RUNNING is default.                                                                                | No       |