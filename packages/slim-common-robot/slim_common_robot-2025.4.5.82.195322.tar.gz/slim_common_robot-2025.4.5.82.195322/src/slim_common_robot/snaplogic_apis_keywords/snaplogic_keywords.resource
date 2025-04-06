*** Settings ***
Documentation       Common Used Keywords for API Testing
...                 This resource file contains high-level keywords that build upon the API keywords.
...                 Keywords cover project setup, account management, file operations, and task execution.

Library             Collections
Library             DateTime
Library             OperatingSystem
Library             JSONLibrary
Library             RequestsLibrary
Library             ../python_helper_files/account_helper.py
Library             ../python_helper_files/file_helper.py
Resource            platform_apis.resource


*** Variables ***
${ORG_SNODE_ID}                     ${EMPTY}
${ACCOUNTS_DETAIL}                  ${NONE}
${GLOBAL_SHARED}                    shared
${skip_project_setup}               ${FALSE}    # Default to running the setup
${TRIGGERED_TASK_PAYLOAD_FILE}      ${CURDIR}/../test_data/triggered.json
${SNAPLEX_FILE_PATH}                ${CURDIR}/../test_data/slim_groundplex.json


*** Keywords ***
Set Up Data
    [Documentation]    Sets up the test environment with necessary project structure and data.
    ...
    ...    *Arguments:*
    ...    - ``url``: Base URL for the API
    ...    - ``username``: Username for authentication
    ...    - ``password``: Password for authentication
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space
    ...    - ``project_name``: Name of the project
    ...    - ``env_file_path``: Path to environment file (default: ${None})
    ...    - ``cleanup``: Whether to clean up existing project space (default: True)
    ...    - ``create_acs``: Whether to create accounts (default: True)
    ...
    ...    *Example:*
    ...    | Set Up Data | https://example.com | user | pass | my_org | my_space | my_project |
    [Arguments]
    ...    ${url}
    ...    ${username}
    ...    ${password}
    ...    ${org_name}
    ...    ${project_space}
    ...    ${project_name}
    ...    ${env_file_path}=${None}
    ...    ${cleanup}=True
    ...    ${create_acs}=True
    ${auth}    Create List    ${username}    ${password}
    Login Api    ${auth}
    IF    $org_name == $NONE    RETURN
    ${org_snode_id}    Get Org Snode ID    ${org_name}
    Set Global Variable    ${ORG_SNODE_ID}    ${org_snode_id}
    Set Environment Variable    ORG_SNODE_ID    ${org_snode_id}
    IF    ${cleanup}==$True and '${skip_project_setup}' != 'True'
        Delete ProjectSpace    ${org_name}    ${project_space}
    END
    Run Keyword Unless    '${skip_project_setup}'=='True'    Create Project Space    ${org_name}    ${project_space}
    Run Keyword Unless
    ...    '${skip_project_setup}'=='True'
    ...    Create Project
    ...    ${org_name}
    ...    ${project_space}
    ...    ${project_name}
    Run Keyword Unless    '${skip_project_setup}'=='True'    Upload All Files In Directory
    IF    '${skip_project_setup}' != 'True' and '${env_file_path}' != '${None}'
        Create All Accounts    ${env_file_path}
    END
    RETURN    ${org_snode_id}

Get Project List
    [Documentation]    Retrieves the list of projects in a project space.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space
    ...
    ...    *Returns:*
    ...    - List of project entries
    ...
    ...    *Example:*
    ...    | ${projects} | Get Project List | my_organization | my_project_space |
    [Arguments]    ${org_name}    ${project_space}
    ${resp}    Get Project List Api    ${org_name}    ${project_space}
    RETURN    ${resp.json()['response_map']['entries']}

Create Project
    [Documentation]    Creates a new project if it doesn't already exist.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space
    ...    - ``project_name``: Name of the project to create
    ...
    ...    *Example:*
    ...    | Create Project | my_organization | my_project_space | my_project |
    [Arguments]    ${org_name}    ${project_space}    ${project_name}
    @{objects}    Get Project List    ${org_name}    ${project_space}
    ${exists}    Evaluate    any('${project_name}' == obj["name"] for obj in $objects)
    IF    ${exists}
        Log To Console    Project Name [${project_name}] exists"
    ELSE
        ${metadata}    Create Dictionary    pattern=false    validation=null
        ${request_payload}    Create Dictionary    asset_type=Dir    metadata=${metadata}    name=${project_name}
        ${resp}    Create Project Api    ${org_name}    ${project_space}    ${project_name}    ${request_payload}
    END

Get Org List
    [Documentation]    Retrieves the list of assets in an organization.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...
    ...    *Returns:*
    ...    - List of organization entries
    ...
    ...    *Example:*
    ...    | ${org_entries} | Get Org List | my_organization |
    [Arguments]    ${org_name}
    ${resp}    Get Org List Api    ${org_name}
    RETURN    ${resp.json()['response_map']['entries']}

Create Project Space
    [Documentation]    Creates a new project space if it doesn't already exist.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space to create
    ...
    ...    *Example:*
    ...    | Create Project Space | my_organization | my_project_space |
    [Arguments]    ${org_name}    ${project_space}
    @{objects}    Get Org List    ${org_name}
    ${exists}    Evaluate    any('${project_space}' == obj["name"] for obj in $objects)
    IF    ${exists}
        Log To Console    Project Space [${project_space}] exists"
    ELSE
        ${request_payload}    Create Dictionary    asset_type=Dir    name=${project_space}
        ${resp}    Create Project Space Api    ${org_name}    ${project_space}    ${request_payload}
    END

Delete ProjectSpace
    [Documentation]    Deletes a project space if it exists.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space to delete
    ...
    ...    *Example:*
    ...    | Delete ProjectSpace | my_organization | my_project_space |
    [Arguments]    ${org_name}    ${project_space}
    @{org_list}    Get Org List    ${org_name}
    ${org_list_exists}    Evaluate    any('${project_space}' == obj["name"] for obj in $org_list)
    IF    ${org_list_exists}
        ${resp}    Delete ProjectSpace Api    ${org_name}    ${project_space}
        Log    ProjectSpace Name [${project_space}] was deleted"    level=CONSOLE
    ELSE
        Log    ProjectSpace Name [${project_space}] do not exist"    level=CONSOLE
    END

Get Org Snode ID
    [Documentation]    Retrieves the snode ID for an organization.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...
    ...    *Returns:*
    ...    - The organization's snode ID
    ...
    ...    *Example:*
    ...    | ${snode_id} | Get Org Snode ID | my_organization |
    [Arguments]    ${org_name}
    ${resp}    Get Org List Api    ${org_name}
    RETURN    ${resp.json()['response_map']['entries'][0]['parent_snode_id']}

Create All Accounts
    [Documentation]    Creates all accounts defined in the environment file.
    ...
    ...    *Arguments:*
    ...    - ``env_file_path``: Path to the environment file containing account variables
    ...
    ...    *Example:*
    ...    | Create All Accounts | /path/to/env_file.json |
    [Arguments]    ${env_file_path}
    Log    env_file_path is:${env_file_path}    level=CONSOLE
    ${env_variables}    Load Env Variables    ${env_file_path}
    Log    Accounts_path is:${ACCOUNT_PATH}    level=CONSOLE
    ${acc_payloads}    Render Env Variables for JSON File    ${ACCOUNT_PATH}    ${env_variables}

    # Check if account payloads were found
    IF    $acc_payloads == [] or $acc_payloads == None
        Fail    No account templates found in path: ${ACCOUNT_PATH}
    END

    Log    org Name is:${org_name}    level=CONSOLE
    Log    Global shared is:${global_shared}    level=CONSOLE
    ${entries}    Get Project List    ${org_name}    ${global_shared}
    ${accounts_entries}    Evaluate    [x for x in $entries if x['asset_type'] == 'Account']
    FOR    ${payload}    IN    @{acc_payloads}
        ${acc_name}    Set Variable    ${payload}[account][property_map][info][label][value]
        ${account_exist}    Evaluate    any(x for x in $accounts_entries if x['name'] == '${acc_name}')
        IF    ${account_exist}
            Log    Account [${acc_name}] exists, skip creation    level=CONSOLE
        ELSE
            ${class_fqid}    Set Variable    ${payload}[account][class_fqid]
            ${class_fqid}    Get Account Version By Class Fqid    ${class_fqid}
            ${payload}[account][class_fqid]    Set Variable    ${class_fqid}
            ${resp}    Create Account API    ${org_name}/${global_shared}    ${acc_name}    ${payload}
            Log    Account [${acc_name}] created    level=CONSOLE
        END
    END

Upload All Files In Directory
    [Documentation]    Uploads all files from a directory to the platform.
    ...
    ...    Iterates over files and uploads each one using the API.
    ...    Continues to the next file if one file upload fails.
    ...
    ...    *Returns:*
    ...    - None
    ...
    ...    *Example:*
    ...    | Upload All Files In Directory |
    ${files_list}    Get Files In Dir    ${FILE_PATH}

    FOR    ${file}    IN    @{files_list}
        ${name}    Get From List    ${file}    0
        ${path}    Get From List    ${file}    1
        Log To Console    uploading: ${path} to Files folder
        TRY
            Upload File Api    ${org_name}/${global_shared}    ${name}    ${path}
        EXCEPT    AS    ${error}
            Log    Failed to upload file ${name}: ${error}    WARN
            CONTINUE
        END
    END

Get Account Version By Class Fqid
    [Documentation]    Retrieves the account version by class FQID.
    ...
    ...    *Arguments:*
    ...    - ``class_fqid``: The class FQID to get the version for
    ...
    ...    *Returns:*
    ...    - The account class FQID with version
    ...
    ...    *Example:*
    ...    | ${account_fqid} | Get Account Version By Class Fqid | my_class_fqid |
    [Arguments]    ${class_fqid}
    IF    ${ACCOUNTS_DETAIL} == None
        ${accounts_detail}    GET Accounts Detail
        ${ACCOUNTS_DETAIL}    Set Variable    ${accounts_detail}
    END

    ${class_fqid_match}    Evaluate    re.search(r"(.+?)_", $class_fqid)
    ${class_id}    Set Variable    ${class_fqid_match.group(1)}
    ${account_detail}    Set Variable    ${ACCOUNTS_DETAIL}[${class_id}]
    ${account_class_fqid}    Set Variable    ${account_detail}[class_fqid]
    RETURN    ${account_class_fqid}

Get Accounts Detail
    [Documentation]    Retrieves detailed information about all accounts.
    ...
    ...    *Returns:*
    ...    - A dictionary containing the response map with account details
    ...
    ...    *Example:*
    ...    | ${accounts} | Get Accounts Detail |
    ${resp}    Get Accounts Detail Api
    RETURN    ${resp.json()['response_map']}

Import Pipeline
    [Documentation]    Imports a pipeline from a JSON file to a specified path.
    ...
    ...    *Arguments:*
    ...    - ``pipeline_file_path``: Path to the pipeline JSON file
    ...    - ``pipeline_name``: Name to assign to the imported pipeline
    ...    - ``path``: Target path where the pipeline will be imported
    ...
    ...    *Returns:*
    ...    - The response map containing information about the imported pipeline
    ...
    ...    *Example:*
    ...    | ${pipeline_info} | Import Pipeline | ${PIPELINE_DIR}/my_pipeline.json | My Pipeline | /org/project |
    [Arguments]    ${pipeline_file_path}    ${pipeline_name}    ${path}
    ${pipeline}    Load Json From File    ${pipeline_file_path}
    ${pipeline_new}    Create Dictionary    pipe=EMPTY
    ${pipeline_new}    Set To Dictionary    ${pipeline_new}    pipe=${pipeline}
    ${import_pipeline_payload}    Set Variable    ${pipeline_new}

    # The value of the fields within ${import_pipeline_payload} are modified
    ${import_pipeline_payload}[pipe][property_map][info][label][value]    Set Variable    ${pipeline_name}
    Log    Payload created for Creating Pipeline is: ${import_pipeline_payload}
    ${response}    Import Pipeline Api    ${path}    ${import_pipeline_payload}
    Log    ...Import Pipeline URL is: ${response.url}    level=CONSOLE
    Log    ...pipeline_name is....:${pipeline_name}    level=CONSOLE
    Log    ...pipeline_filePath is....:${pipeline_file_path}    level=CONSOLE
    Log    ...pipeline:(${pipeline_name})_imported to projectpath...:${path}    level=CONSOLE
    log    ...pipeline_snodeID....:${response.json()['response_map']}
    RETURN    ${response.json()['response_map']}

GET Runtime Path Id
    [Documentation]    Retrieves the runtime path ID for a specified organization and plex.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Organization name (default: ${org_name})
    ...    - ``default_plex``: Plex name to find (default: ${default_plex})
    ...
    ...    *Returns:*
    ...    - The runtime path ID corresponding to the specified plex
    ...
    ...    *Example:*
    ...    | ${runtime_id} | GET Runtime Path Id | my_org | my_plex |
    [Arguments]    ${org_name}=${org_name}    ${default_plex}=${default_plex}
    ${response}    GET Runtime Path Id Api    ${org_name}
    @{snaplex_list}    Set Variable    ${response.json()['response_map']}
    FOR    ${line}    IN    @{snaplex_list}
        IF    $line['label'] == $default_plex
            RETURN    ${line['runtime_path_id']}
        END
    END

Create Task
    [Documentation]    Creates a task with the specified parameters.
    ...
    ...    *Arguments:*
    ...    - ``task_name``: Name for the new task
    ...    - ``pipeline_snodeid``: The pipeline snode ID
    ...    - ``plex_name``: Name of the plex to use
    ...    - ``path``: Path where the task will be created
    ...    - ``task_payload_file``: Filename of the task payload template
    ...    - ``pipeline_params``: Dictionary of pipeline parameters to add/update (optional)
    ...    - ``execution_timeout``: Value for execution timeout (optional)
    ...    - ``notification``: Dictionary with notification settings (optional)
    ...    - ``num_instances``: Number of instances (optional)
    ...    - ``debug_next_runs``: Number of debug next runs (optional)
    ...
    ...    *Returns:*
    ...    - A tuple containing the task payload and the snode ID of the created task
    ...
    ...    *Examples:*
    ...    | # Basic usage with required arguments only |
    ...    | ${task_payload}    ${task_snode_id} | Create Task | My Task | ${pipeline_id} | default_plex | /org/project | task_template.json |
    ...    |
    ...    | # With execution timeout and pipeline parameters |
    ...    | ${pipeline_params}= | Create Dictionary | param1=value1 | param2=value2 |
    ...    | ${task_payload}    ${task_snode_id} | Create Task | My Task | ${pipeline_id} | default_plex | /org/project | task_template.json | pipeline_params=${pipeline_params} | execution_timeout=3600 |
    ...    |
    ...    | # With notification settings |
    ...    | ${notification}= | Create Dictionary | email=${TRUE} | recipients=user@example.com |
    ...    | ${task_payload}    ${task_snode_id} | Create Task | Task With Notifications | ${pipeline_id} | default_plex | /org/project | task_template.json | notification=${notification} |
    ...    |
    ...    | # With multiple optional parameters |
    ...    | ${pipeline_params}= | Create Dictionary | env=production | debug=${FALSE} |
    ...    | ${notification}= | Create Dictionary | email=${TRUE} | slack=${TRUE} |
    ...    | ${task_payload}    ${task_snode_id} | Create Task | Complex Task | ${pipeline_id} | default_plex | /org/project | task_template.json | pipeline_params=${pipeline_params} | execution_timeout=7200 | notification=${notification} | num_instances=3 | debug_next_runs=2 |
    [Arguments]    ${task_name}    ${pipeline_snodeid}    ${plex_name}    ${path}    ${task_payload_file}
    ...    ${pipeline_params}=${None}    ${execution_timeout}=${None}    ${notification}=${None}
    ...    ${num_instances}=${None}    ${debug_next_runs}=${None}

    Log    Current directory: ${CURDIR}    level=CONSOLE
    ${payload}    Set Variable    ${TRIGGERED_TASK_PAYLOAD_FILE}
    ${task_payload}    Load Json From File    ${payload}
    Log To Console    payload is: ${payload}
    ${task_payload}    Load Json From File    ${payload}
    ${runtime_path_id}    GET Runtime Path Id    ${org_name}    ${plex_name}
    Log    Plex_name is: ${plex_name}    level=CONSOLE
    Log    runtime_path_id is: ${runtime_path_id}    level=CONSOLE

    # Only update these basic fields
    Set To Dictionary    ${task_payload}    path_id=${path}
    Set To Dictionary    ${task_payload}    job_name=${task_name}
    Set To Dictionary    ${task_payload}    name=${task_name}

    ${parameters_value}    Get From Dictionary    ${task_payload}    parameters

    # Always update these required fields
    Set To Dictionary    ${parameters_value}    runtime_path_id=${runtime_path_id}
    Set To Dictionary    ${parameters_value}    pipeline_snode_id=${pipeline_snodeid}

    # Only update pipeline_parameters if provided
    IF    ${pipeline_params} is not ${None}
        IF    'pipeline_parameters' not in $parameters_value
            Set To Dictionary    ${parameters_value}    pipeline_parameters=&{EMPTY}
        END
        Set To Dictionary    ${parameters_value}[pipeline_parameters]    &{pipeline_params}
    END

    # Only update execution_timeout if provided
    IF    ${execution_timeout} is not ${None}
        Set To Dictionary    ${parameters_value}    execution_timeout=${execution_timeout}
    END

    # Only update notification if provided
    IF    ${notification} is not ${None}
        Set To Dictionary    ${parameters_value}    notification=${notification}
    END

    # Only update num_instances if provided
    IF    ${num_instances} is not ${None}
        Set To Dictionary    ${parameters_value}    num_instances=${num_instances}
    END

    # Only update debug_next_runs if provided
    IF    ${debug_next_runs} is not ${None}
        Set To Dictionary    ${parameters_value}    debug_next_runs=${debug_next_runs}
    END

    Log    Payload created for Creating Task: ${task_payload}    level=CONSOLE
    ${response}    Create Task Api    ${task_payload}
    Should Be Equal As Strings    ${response.status_code}    201
    RETURN    ${task_payload}    ${response.json()['response_map']['snode_id']}

Get Unique Id
    [Documentation]    Generates a unique ID using the current timestamp.
    ...
    ...    *Returns:*
    ...    - A string containing a unique ID based on the current date and time
    ...
    ...    *Example:*
    ...    | ${unique_id} | Get Unique Id |
    ${UNIQUE_ID}    Get Current Date    result_format=%Y%m%d%H%M%S%f
    RETURN    ${UNIQUE_ID}

Run Triggered Task
    [Documentation]    Runs a triggered task with optional parameters and retries on failure.
    ...
    ...    *Arguments:*
    ...    - ``path``: Path where the task is located
    ...    - ``task_name``: Name of the task to run
    ...    - ``params``: Optional parameters for the task (default: ${EMPTY})
    ...
    ...    *Returns:*
    ...    - The response from the task execution
    ...
    ...    *Example:*
    ...    | ${task_response} | Run Triggered Task | /org/project | My Task | param1=value1&param2=value2 |
    [Arguments]    ${path}    ${task_name}    ${params}=${EMPTY}
    ${response}    Wait Until Keyword Succeeds
    ...    30 sec
    ...    5 sec
    ...    Run Triggered Task Api
    ...    ${path}
    ...    ${task_name}
    ...    ${params}
    RETURN    ${response}

Create Snaplex
    [Documentation]    Creates a new snaplex using configuration from files.
    ...
    ...    *Arguments:*
    ...    - ``env_file_path``: Path to the environment variables file
    ...    - ``GROUNDPLEX_NAME``: Name of the groundplex (optional, overrides env file)
    ...    - ``GROUNDPLEX_ENV``: Environment of the groundplex (optional, overrides env file)
    ...    - ``ORG_NAME``: Organization name (optional, overrides env file)
    ...    - ``RELEASE_BUILD_VERSION``: Release build version (optional, overrides env file)
    ...    - ``SNAP_PLEX_LOCATION``: Custom container path for the snaplex (optional, overrides env file)
    ...
    ...    *Returns:*
    ...    - A dictionary with the creation status and message
    ...
    ...    *Example:*
    ...    | ${result} | Create Snaplex | ${CONFIG_DIR}/snaplex.json | ${CONFIG_DIR}/env.json | slim-groundplex | slimgroundplexdev | my-org | main-30028 | /custom/container/path |
    [Arguments]
    ...    ${env_file_path}
    ...    ${GROUNDPLEX_NAME}=${EMPTY}
    ...    ${GROUNDPLEX_ENV}=${EMPTY}
    ...    ${ORG_NAME}=${EMPTY}
    ...    ${RELEASE_BUILD_VERSION}=${EMPTY}
    ...    ${SNAP_PLEX_LOCATION}=${EMPTY}

    Log    snaplex_file_path is: ${snaplex_file_path}    level=CONSOLE
    Log    env_file_path is: ${env_file_path}    level=CONSOLE

    # Log all input parameters to help with debugging
    Log    Input GROUNDPLEX_NAME: ${GROUNDPLEX_NAME}    level=CONSOLE
    Log    Input GROUNDPLEX_ENV: ${GROUNDPLEX_ENV}    level=CONSOLE
    Log    Input ORG_NAME: ${ORG_NAME}    level=CONSOLE
    Log    Input RELEASE_BUILD_VERSION: ${RELEASE_BUILD_VERSION}    level=CONSOLE
    Log    Input SNAP_PLEX_LOCATION: ${SNAP_PLEX_LOCATION}    level=CONSOLE

    # Load environment variables
    ${env_variables}    Load Env Variables    ${env_file_path}

    # Set a default SNAP_PLEX_LOCATION if not in env variables
    ${has_container_path}    Run Keyword And Return Status
    ...    Dictionary Should Contain Key
    ...    ${env_variables}
    ...    SNAP_PLEX_LOCATION
    IF    not ${has_container_path}
        ${org_name}    Get From Dictionary    ${env_variables}    ORG_NAME
        Set To Dictionary    ${env_variables}    SNAP_PLEX_LOCATION=/${org_name}/shared
        Log    Setting default SNAP_PLEX_LOCATION to "/${org_name}/shared"    level=CONSOLE
    END

    # Store original values for logging
    ${original_groundplex_name}    Get From Dictionary    ${env_variables}    GROUNDPLEX_NAME    default=Not Found
    ${original_groundplex_env}    Get From Dictionary    ${env_variables}    GROUNDPLEX_ENV    default=Not Found
    ${original_org_name}    Get From Dictionary    ${env_variables}    ORG_NAME    default=Not Found
    ${original_release_build}    Get From Dictionary    ${env_variables}    RELEASE_BUILD_VERSION    default=Not Found
    ${original_snap_plex_path}    Get From Dictionary    ${env_variables}    SNAP_PLEX_LOCATION    default=Not Found

    # Override environment variables with provided arguments if not empty or ${None}
    IF    '${GROUNDPLEX_NAME}' != '${EMPTY}' and '${GROUNDPLEX_NAME}' != '${None}'
        Set To Dictionary    ${env_variables}    GROUNDPLEX_NAME=${GROUNDPLEX_NAME}
        Log    Updated GROUNDPLEX_NAME from "${original_groundplex_name}" to "${GROUNDPLEX_NAME}"    level=CONSOLE
    END

    IF    '${GROUNDPLEX_ENV}' != '${EMPTY}' and '${GROUNDPLEX_ENV}' != '${None}'
        Set To Dictionary    ${env_variables}    GROUNDPLEX_ENV=${GROUNDPLEX_ENV}
        Log    Updated GROUNDPLEX_ENV from "${original_groundplex_env}" to "${GROUNDPLEX_ENV}"    level=CONSOLE
    END

    IF    '${ORG_NAME}' != '${EMPTY}' and '${ORG_NAME}' != '${None}'
        Set To Dictionary    ${env_variables}    ORG_NAME=${ORG_NAME}
        Log    Updated ORG_NAME from "${original_org_name}" to "${ORG_NAME}"    level=CONSOLE
    END

    IF    '${RELEASE_BUILD_VERSION}' != '${EMPTY}' and '${RELEASE_BUILD_VERSION}' != '${None}'
        Set To Dictionary    ${env_variables}    RELEASE_BUILD_VERSION=${RELEASE_BUILD_VERSION}
        Log
        ...    Updated RELEASE_BUILD_VERSION from "${original_release_build}" to "${RELEASE_BUILD_VERSION}"
        ...    level=CONSOLE
    END

    # Update SNAP_PLEX_LOCATION in env variables if provided
    IF    '${SNAP_PLEX_LOCATION}' != '${EMPTY}' and '${SNAP_PLEX_LOCATION}' != '${None}'
        Set To Dictionary    ${env_variables}    SNAP_PLEX_LOCATION=${SNAP_PLEX_LOCATION}
        Log
        ...    Updated SNAP_PLEX_LOCATION from "${original_snap_plex_path}" to "${SNAP_PLEX_LOCATION}"
        ...    level=CONSOLE
    END

    # Add special mapping for CONTAINER_PATH (for template compatibility)
    ${snap_plex_location}    Get From Dictionary    ${env_variables}    SNAP_PLEX_LOCATION
    Set To Dictionary    ${env_variables}    CONTAINER_PATH=${snap_plex_location}
    Log    Set CONTAINER_PATH to match SNAP_PLEX_LOCATION: ${snap_plex_location}    level=CONSOLE

    ${snaplex_file_path}    Set Variable    ${CURDIR}/../test_data/slim_groundplex.json
    ${snaplex_payloads}    Render Env Variables for JSON File    ${snaplex_file_path}    ${env_variables}

    # Assuming your function returns a list, take the first item or iterate as needed
    ${payload}    Set Variable    ${snaplex_payloads}[0]

    # Check if container_path is correctly rendered in the payload
    ${container_path_in_payload}    Get From Dictionary    ${payload}    container_path
    Log    container_path in rendered payload: ${container_path_in_payload}    level=CONSOLE

    # Ensure the container_path in the payload matches our location value
    ${snap_plex_location}    Get From Dictionary    ${env_variables}    SNAP_PLEX_LOCATION
    Set To Dictionary    ${payload}    container_path=${snap_plex_location}
    Log    Ensuring container_path in payload is set to: ${snap_plex_location}    level=CONSOLE

    Log    Final snaplex configuration: ${payload}    level=CONSOLE

    # Now send the fully rendered payload to the API
    # Try to create snaplex
    ${status}    ${response}    Run Keyword And Ignore Error    Create Snaplex Api    ${payload}

    # Success case: 201 Created
    ${is_success}    Run Keyword And Return Status
    ...    Run Keywords
    ...    Should Be Equal    ${status}    PASS    AND
    ...    Should Be Equal As Strings    ${response.status_code}    201

    # Conflict case: 409 Conflict
    ${is_conflict}    Run Keyword And Return Status
    ...    Run Keywords
    ...    Should Be Equal    ${status}    FAIL    AND
    ...    Should Contain    ${response}    409

    # Handle 409 conflict case
    IF    ${is_conflict}
        ${result}    Log    ***Resource already exists (409 Conflict). Skipping creation****.    level=CONSOLE
        ${result}    Evaluate    {"status": "success", "message": "Resource already exists"}
    ELSE
        ${result}    Set Variable    ${None}
    END

    # Handle 201 success case
    IF    ${is_success}
        ${result}    Evaluate    {"status": "success", "message": "Resource created"}
    ELSE IF    ${is_conflict}
        ${result}    Set Variable    ${result}
    ELSE
        ${result}    Set Variable    ${None}
    END

    # Fail if neither condition is met
    IF    not ${is_success} and not ${is_conflict}
        Fail    Status is neither 409 nor 201. Error: ${response}
    END
    RETURN    ${result}

Create Directory If Not Exists
    [Documentation]    Creates a directory if it doesn't already exist.
    ...
    ...    *Arguments:*
    ...    - ``directory``: Path of the directory to check/create
    ...
    ...    *Example:*
    ...    | Create Directory If Not Exists | ${CONFIG_DIR}/logs |
    [Arguments]    ${directory}
    ${dir_exists}    Run Keyword And Return Status    Directory Should Exist    ${directory}
    IF    not ${dir_exists}    Create Directory    ${directory}
    Log    Directory check completed for: ${directory}

Download And Save Config File
    [Documentation]    Downloads a configuration file from a URL and saves it to the specified location.
    ...
    ...    *Arguments:*
    ...    - ``url``: URL from which to download the file
    ...    - ``CONFIG_DIR``: Directory where the file should be saved
    ...    - ``SLPROPZ_FILE_NAME``: Filename to use when saving
    ...
    ...    *Example:*
    ...    | Download And Save Config File | https://example.com/config | ${CONFIG_DIR} | config.slpropz |
    [Arguments]    ${url}    ${CONFIG_DIR}    ${PROJECT_LOCATION}    ${SLPROPZ_FILE_NAME}
    Create Directory If Not Exists    ${CONFIG_DIR}
    ${response}    Download slpropz file Api    ${url}    ${PROJECT_LOCATION}
    Create Binary File    ${CONFIG_DIR}/${SLPROPZ_FILE_NAME}    ${response.content}
    Log    File saved to ${CONFIG_DIR}/${SLPROPZ_FILE_NAME}    level=CONSOLE

Download Config File
    [Documentation]    Downloads a config file from the URL and saves it to the specified location.
    ...
    ...    *Arguments:*
    ...    - ``CONFIG_FILE``: Path where the file should be saved
    ...
    ...    *Example:*
    ...    | Download Config File | ${CONFIG_DIR}/settings.cfg |
    [Arguments]    ${CONFIG_FILE}

    Create Session    download_session    ${URL}    verify=True
    ${response}    GET On Session    download_session    ${EMPTY}    stream=${TRUE}

    # Check if request was successful
    Should Be Equal As Strings    ${response.status_code}    200

    # Save the response content to file
    Create Binary File    ${CONFIG_FILE}    ${response.content}
    Log    File successfully downloaded and saved to ${CONFIG_FILE}
