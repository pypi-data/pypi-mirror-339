*** Settings ***
Documentation       Common Used Keywords for API Testing
...                 This resource file contains keywords for API testing with RequestsLibrary.
...                 Keywords cover authentication, CRUD operations for projects, tasks, accounts and pipelines.

Library             RequestsLibrary
Library             JSONLibrary
Library             Collections
Library             String
Library             ../python_helper_files/account_helper.py


*** Variables ***
${ORG_ADMIN_SESSION}        snaplogic-org-admin
${GLOBAL_ORG_SNODE_ID}      ${EMPTY}
${SESSION}                  snaplogic
${GLOBAL_ORG_SNODE_ID}      ${EMPTY}    # Initialize global variable


*** Keywords ***
Login Api
    [Documentation]    Creates a session with authentication for API access.
    ...
    ...    *Arguments:*
    ...    - ``auth``: Authentication object for session creation
    ...
    ...    *Example:*
    ...    | ${auth} | Create Dictionary | username=user | password=pass |
    ...    | Login Api | ${auth} |
    [Arguments]    ${auth}
    Create Session    ${ORG_ADMIN_SESSION}    ${url}    auth=${auth}    verify=true

Get Org List Api
    [Documentation]    Retrieves the list of assets for a specific organization.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Org List Api | my_organization |
    [Arguments]    ${org_name}
    ${resp}    GET On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/asset/list/${org_name}
    RETURN    ${resp}

Get Project List Api
    [Documentation]    Retrieves the list of projects for a specific organization and project space.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Project List Api | my_organization | my_project_space |
    [Arguments]    ${org_name}    ${project_space}
    Log    project list api is:/api/1/rest/asset/list/${org_name}/${project_space}
    ${resp}    GET On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/asset/list/${org_name}/${project_space}
    RETURN    ${resp}

Create Project Space Api
    [Documentation]    Creates a new project space in the specified organization.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space to create
    ...    - ``payload``: JSON payload with project space details
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Create Project Space Api | my_organization | my_project_space | ${payload} |
    [Arguments]    ${org_name}    ${project_space}    ${payload}
    ${params}    Create Dictionary    path=${org_name}/${project_space}
    ${resp}    POST On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/asset/${org_name}/${project_space}
    ...    params=${params}    json=${payload}
    RETURN    ${resp}

Create Project Api
    [Documentation]    Creates a new project in the specified organization and project space.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space
    ...    - ``project_name``: Name of the project to create
    ...    - ``payload``: JSON payload with project details
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Create Project Api | my_organization | my_project_space | my_project | ${payload} |
    [Arguments]    ${org_name}    ${project_space}    ${project_name}    ${payload}
    ${params}    Create Dictionary    path=${org_name}/${project_space}/${project_name}
    ${resp}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/asset/${org_name}/${project_space}/${project_name}
    ...    params=${params}
    ...    json=${payload}
    RETURN    ${resp}

Delete Project Api
    [Documentation]    Soft-deletes a project in the specified organization and project space.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space
    ...    - ``project_name``: Name of the project to delete
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Delete Project Api | my_organization | my_project_space | my_project |
    [Arguments]    ${org_name}    ${project_space}    ${project_name}
    ${params}    Create Dictionary    soft_delete=True    asset_type=Dir
    ${resp}    DELETE On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/asset/${org_name}/${project_space}/${project_name}
    ...    params=${params}
    RETURN    ${resp}

Delete ProjectSpace Api
    [Documentation]    Soft-deletes a project space in the specified organization.
    ...
    ...    *Arguments:*
    ...    - ``org_name``: Name of the organization
    ...    - ``project_space``: Name of the project space to delete
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Delete ProjectSpace Api | my_organization | my_project_space |
    [Arguments]    ${org_name}    ${project_space}
    ${params}    Create Dictionary    soft_delete=True    asset_type=Dir

    TRY
        ${resp}    DELETE On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/asset/${org_name}/${project_space}
        ...    params=${params}    expected_status=any

        # Check for error status code
        IF    ${resp.status_code} == 500
            ${json}    Evaluate    json.loads('''${resp.content}''')    json
            ${error_msg}    Set Variable    ${json['response_map']['error_list'][0]['message']}
            Log    Error deleting project space [${project_space}]: ${error_msg}    level=ERROR
            Fail    ${error_msg}
        END

        RETURN    ${resp}
    EXCEPT    AS    ${error}
        Log    Exception during DELETE operation: ${error}    level=ERROR
        Fail    Failed to delete project space [${project_space}]: ${error}
    END
    RETURN    ${resp}

GET Runtime Path Id Api
    [Documentation]    Retrieves runtime path ID for a specified organization.
    ...
    ...    *Arguments:*
    ...    - ``org_name_passed``: Name of the organization
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | GET Runtime Path Id Api | my_organization |
    [Arguments]    ${org_name_passed}    ${expected_status}=200
    ${params}    Create Dictionary    subscriber_id=${org_name_passed}
    ${resp}    GET On Session    ${ORG_ADMIN_SESSION}    api/1/rest/slserver/snaplex_cc_details_with_info
    ...    params=${params}
    RETURN    ${resp}

Create Task Api Old
    [Documentation]    Creates a new task using the old API endpoint.
    ...
    ...    *Arguments:*
    ...    - ``payload``: JSON payload with task details
    ...    - ``duplicate_check``: Whether to check for duplicates (default: True)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Create Task Api Old | ${payload} | ${TRUE} |
    [Arguments]    ${payload}    ${duplicate_check}=True
    ${params}    Create Dictionary    duplicate_check=${duplicate_check}
    ${resp}    POST On Session    ${ORG_ADMIN_SESSION}    api/1/rest/slsched/job    json=${payload}
    ...    params=${params}
    RETURN    ${resp}

Get Accounts Detail Api
    [Documentation]    Retrieves detailed information about accounts in the organization.
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Accounts Detail Api |
    ${params}    Create Dictionary    org_path=${org_name}    level=detail
    ${resp}    GET On Session    ${ORG_ADMIN_SESSION}    api/1/rest/admin/snappack/catalog/accounts
    ...    params=${params}
    RETURN    ${resp}

Update Task Api
    [Documentation]    Updates an existing task with new parameters.
    ...
    ...    *Arguments:*
    ...    - ``task_snode_id``: The snode ID of the task to update
    ...    - ``payload``: JSON payload with updated task details
    ...    - ``duplicate_check``: Whether to check for duplicates (default: True)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Update Task Api | task_123 | ${payload} | ${TRUE} |
    [Arguments]    ${task_snode_id}    ${payload}    ${duplicate_check}=True
    ${params}    Create Dictionary    duplicate_check=${duplicate_check}
    ${resp}    PUT On Session    ${ORG_ADMIN_SESSION}    api/1/rest/slsched/job/${task_snode_id}    json=${payload}
    ...    params=${params}
    RETURN    ${resp}

Get Account Api
    [Documentation]    Retrieves information about a specific account.
    ...
    ...    *Arguments:*
    ...    - ``account_id``: ID of the account to retrieve
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Account Api | account_123 |
    [Arguments]    ${account_id}
    ${response}    Get On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    api/1/rest/admin/account/${account_id}
    RETURN    ${response}

Create Account Api
    [Documentation]    Creates a new account in the specified path.
    ...
    ...    *Arguments:*
    ...    - ``path``: Path where the account should be created
    ...    - ``account_name``: Name of the account to create
    ...    - ``payload``: JSON payload with account details
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Create Account Api | my_path | my_account | ${payload} |
    [Arguments]    ${path}    ${account_name}    ${payload}
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    api/1/rest/admin/account/${path}/${account_name}
    ...    json=${payload}
    Log    Create Accounts API URL is...${response.url}    level=CONSOLE
    RETURN    ${response}

Upload File Api
    [Documentation]    Uploads a file to a specified path.
    ...
    ...    *Arguments:*
    ...    - ``sl_path``: Path where the file should be uploaded
    ...    - ``fileName``: Name to use for the uploaded file
    ...    - ``file_path``: Local path to the file to upload
    ...
    ...    *Example:*
    ...    | Upload File Api | my_path | file.txt | /local/path/to/file.txt |
    [Arguments]    ${sl_path}    ${fileName}    ${file_path}
    Log To Console    uploading ${file_path} to ${sl_path}
    ${file_open_path}    Get File For Streaming Upload    ${file_path}
    ${files}    Create Dictionary    file    ${file_open_path}
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/slfs/${sl_path}/${fileName}
    ...    files=${files}

Get Asset Details Api
    [Documentation]    Retrieves details about a specific asset.
    ...
    ...    *Arguments:*
    ...    - ``asset_name``: Name of the asset
    ...    - ``path``: Path to the asset
    ...    - ``asset_type``: Type of the asset
    ...    - ``exact_search``: Whether to use exact matching (default: False)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Asset Details Api | my_asset | my_path | Directory | ${TRUE} |
    [Arguments]    ${asset_name}    ${path}    ${asset_type}    ${exact_search}=False
    ${params}    Create Dictionary    exact_search=${exact_search}    asset_type=${asset_type}
    ${response}    GET On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/asset/${path}/${asset_name}
    ...    params=${params}
    Log To Console    Get Asset Details API URL is...${response.url}
    RETURN    ${response}

Get Account Id By Name And Path
    [Documentation]    Retrieves account ID by account name and path.
    ...
    ...    *Arguments:*
    ...    - ``account_name``: Name of the account
    ...    - ``path``: Path to the account
    ...
    ...    *Returns:*
    ...    - The account ID
    ...
    ...    *Example:*
    ...    | ${account_id} | Get Account Id By Name And Path | my_account | my_path |
    [Arguments]    ${account_name}    ${path}
    ${params}    Create Dictionary    exact_search=True    asset_type=Account    search=${account_name}
    ${response}    GET On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/asset/list/${path}
    ...    params=${params}

    ${asset_id}    Retrieve Asset Id    ${response.json()}
    Log To Console    asset_id::${asset_id}
    ${account}    Get Account Api    ${asset_id}
    RETURN    ${account.json()['response_map']['_id']}

Delete Account Api
    [Documentation]    Deletes a specific account.
    ...
    ...    *Arguments:*
    ...    - ``asset_id``: ID of the account to delete
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Delete Account Api | account_123 |
    [Arguments]    ${asset_id}
    ${response}    DELETE On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/admin/account/${asset_id}
    Log To Console    Delete Account Api URL is...${response.url}
    RETURN    ${response}

Import Pipeline Api
    [Documentation]    Imports a pipeline to a specified path.
    ...
    ...    *Arguments:*
    ...    - ``path``: Path where the pipeline should be imported
    ...    - ``pipeline_payload``: JSON payload with pipeline details
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Import Pipeline Api | my_path | ${payload} |
    [Arguments]    ${path}    ${pipeline_payload}
    Log    Org Snode Id is:${ORG_SNODE_ID}    level=CONSOLE
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/2/${ORG_SNODE_ID}/rest/project/import/pipe/slp/${path}
    ...    params=duplicate_check=false
    ...    json=${pipeline_payload}
    RETURN    ${response}

Create Task Api
    [Documentation]    Creates a new task.
    ...
    ...    *Arguments:*
    ...    - ``task_paylod``: JSON payload with task details
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Create Task Api | ${payload} |
    [Arguments]    ${task_paylod}
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/slsched/job
    ...    params=duplicate_check=True
    ...    json=${task_paylod}
    Log To Console    Create Task Api URL is:${response.url}
    RETURN    ${response}

Run Triggered Task Api
    [Documentation]    Runs a triggered task with specified parameters.
    ...
    ...    *Arguments:*
    ...    - ``path``: Path to the task
    ...    - ``task_name``: Name of the task to run
    ...    - ``params``: Parameters for running the task
    ...    - ``expected_status``: Expected HTTP status code (default: 200)
    ...
    ...    *Example:*
    ...    | ${run_params} | Create Dictionary | param1=value1 |
    ...    | Run Triggered Task Api | my_path | my_task | ${run_params} | 200 |
    [Arguments]    ${path}    ${task_name}    ${params}    ${expected_status}=200
    ${response}    Get On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/slsched/feed/${path}/${task_name}
    ...    params=${params}
    ...    expected_status=${expected_status}
    Log    Run Task Api URL is:${response.url}
    Log    Execute triggered task response is:${response}

Execute Pipeline Api
    [Documentation]    Executes a pipeline with specified parameters.
    ...
    ...    *Arguments:*
    ...    - ``pipeline_snode_ID``: The snode ID of the pipeline to execute
    ...    - ``run_pipeline_payload``: JSON payload with execution parameters
    ...    - ``expected_status``: Expected HTTP status code (default: 200)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Execute Pipeline Api | pipeline_123 | ${payload} | 200 |
    [Arguments]    ${pipeline_snode_ID}    ${run_pipeline_payload}    ${expected_status}=200
    ${response}    POST On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/pipeline/prepare/${pipeline_snode_ID}
    ...    json=${run_pipeline_payload}
    ...    expected_status=${expected_status}
    Log To Console    Execute pipeline response code is :${response.status_code}
    Log To Console    Response URL for_Execute Pipeline Api_ is...${response.url}
    RETURN    ${response}

Get Run Time Pipeline Api
    [Documentation]    Retrieves runtime information for a specific pipeline execution.
    ...
    ...    *Arguments:*
    ...    - ``pipeline_ruuid``: Runtime UUID of the pipeline execution
    ...    - ``expected_status``: Expected HTTP status code (default: 200)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Run Time Pipeline Api | runtime_uuid_123 | 200 |
    [Arguments]    ${pipeline_ruuid}    ${expected_status}=200
    ${params}    Create Dictionary    level=detail
    ${response}    Get On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/2/${org_snode_id}/rest/pm/runtime/${pipeline_ruuid}
    ...    params=${params}
    ...    expected_status=${expected_status}
    Log To Console    Run Time response code is :${response.status_code}
    Log To Console    Get Run Time Pipeline Api URL is:${response.url}
    RETURN    ${response}

Get Pipeline Logs Api
    [Documentation]    Retrieves logs for a specific pipeline execution.
    ...
    ...    *Arguments:*
    ...    - ``pipeline_ruuid``: Runtime UUID of the pipeline execution
    ...
    ...    *Example:*
    ...    | Get Pipeline Logs Api | runtime_uuid_123 |
    [Arguments]    ${pipeline_ruuid}
    ${params}    Create Dictionary    ruuid=${pipeline_ruuid}
    ${response}    Get On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/public/log/${org_snode_id}    params=${params}

Delete Pipeline Api
    [Documentation]    Deletes a specific pipeline.
    ...
    ...    *Arguments:*
    ...    - ``pipeline_snode_id``: The snode ID of the pipeline to delete
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Delete Pipeline Api | pipeline_123 |
    [Arguments]    ${pipeline_snode_id}
    ${response}    POST On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/pipeline/delete/${pipeline_snode_id}
    Log To Console    Response URL for_Delete PipelineApi_ is...${response.url}
    RETURN    ${response}

Delete Task Api
    [Documentation]    Deletes a specific task.
    ...
    ...    *Arguments:*
    ...    - ``task_snode_id``: The snode ID of the task to delete
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Delete Task Api | task_123 |
    [Arguments]    ${task_snode_id}
    ${response}    DELETE On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/slsched/job/${task_snode_id}
    RETURN    ${response}

Create Org Api
    [Documentation]    Creates a new organization.
    ...
    ...    *Arguments:*
    ...    - ``PAYLOAD``: JSON payload with organization details
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${response} | Create Org Api | ${payload} |
    [Arguments]    ${PAYLOAD}
    ${headers}    Create Dictionary    Content-Type=application/json
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    ${url}/api/1/rest/admin/org/provision
    ...    json=${PAYLOAD}
    ...    headers=${headers}
    Log To Console    Response:${response.content}
    RETURN    ${response}

Get Org Snode Id Api
    [Documentation]    Retrieves the snode ID for a specific organization.
    ...
    ...    *Arguments:*
    ...    - ``ORG_NAME``: Name of the organization
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get Org Snode Id Api | my_organization |
    [Arguments]    ${ORG_NAME}
    ${GET_SNODE_API_URL}    Set Variable
    ...    ${url}/api/1/rest/slserver/snaplex_cc_details_with_info?subscriber_id=${ORG_NAME}
    ${response}    GET On Session    ${ORG_ADMIN_SESSION}    ${GET_SNODE_API_URL}
    RETURN    ${response}

Set JCC Node Api
    [Documentation]    Sets JCC node parameters.
    ...
    ...    *Arguments:*
    ...    - ``snode_id``: The snode ID of the node
    ...    - ``jcc_payload``: JSON payload with node parameters
    ...    - ``headers``: HTTP headers for the request
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${payload} | Create Dictionary | key=value |
    ...    | ${headers} | Create Dictionary | Content-Type=application/json |
    ...    | ${response} | Set JCC Node Api | node_123 | ${payload} | ${headers} |
    [Arguments]    ${snode_id}    ${jcc_payload}    ${headers}
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    ${url}/api/1/rest/plex/nodes/${snode_id}
    ...    json=${jcc_payload}
    ...    headers=${headers}
    RETURN    ${response}

Get ADM Settings Api
    [Documentation]    Retrieves ADM settings.
    ...
    ...    *Arguments:*
    ...    - ``session_to_use``: Session to use for the request (default: ${ORG_ADMIN_SESSION})
    ...    - ``expected_status``: Expected HTTP status code (default: 200)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Get ADM Settings Api | ${ORG_ADMIN_SESSION} | 200 |
    [Arguments]    ${session_to_use}=${ORG_ADMIN_SESSION}    ${expected_status}=200
    ${response}    GET On Session
    ...    ${session_to_use}
    ...    ${url}/api/2/${ORG_SNODE_ID}/rest/adm/settings
    ...    expected_status=${expected_status}
    RETURN    ${response}

Update ADM Settings Api
    [Documentation]    Updates ADM settings with specified access level.
    ...    Should be 'ALL' or 'ORG_ADMIN'
    ...
    ...    *Arguments:*
    ...    - ``access``: Access level to set ('ALL' or 'ORG_ADMIN')
    ...    - ``session_to_use``: Session to use for the request (default: ${ORG_ADMIN_SESSION})
    ...    - ``expected_status``: Expected HTTP status code (default: 200)
    ...
    ...    *Returns:*
    ...    - Response object from the API call
    ...
    ...    *Example:*
    ...    | ${response} | Update ADM Settings Api | ALL | ${ORG_ADMIN_SESSION} | 200 |
    [Arguments]    ${access}    ${session_to_use}=${ORG_ADMIN_SESSION}    ${expected_status}=200
    ${body}    Create Dictionary    access=${access}
    ${response}    PUT On Session
    ...    ${session_to_use}
    ...    ${url}/api/2/${ORG_SNODE_ID}/rest/adm/settings
    ...    json=${body}
    ...    expected_status=${expected_status}
    RETURN    ${response}

Get Auth Token
    [Documentation]    Gets authentication token via API.
    ...
    ...    *Arguments:*
    ...    - ``username``: Username for authentication
    ...    - ``password``: Password for authentication
    ...
    ...    *Returns:*
    ...    - Authentication token
    ...
    ...    *Example:*
    ...    | ${token} | Get Auth Token | user | pass |
    [Arguments]    ${username}    ${password}

    # Create session if it doesn't exist
    # Create Admin Session

    # Encode credentials
    ${auth_string}    Evaluate    "${username}:${password}"
    ${encoded_str}    Evaluate    base64.b64encode($auth_string.encode()).decode()    modules=base64

    # Prepare session URL and headers
    ${session_url}    Set Variable    /api/1/rest/asset/session?caller=${username}
    ${headers}    Create Dictionary    Authorization=Basic ${encoded_str}

    ${resp}    GET On Session    ${ORG_ADMIN_SESSION}    ${session_url}    headers=${headers}    expected_status=200

    # Extract the token from the nested response structure
    ${response}    Set Variable    ${resp.json()}
    ${token}    Get From Dictionary    ${response}[response_map]    token
    Log    Extracted Token: ${token}

    RETURN    ${token}

Extract Cookies From API Response
    [Documentation]    Extracts cookies from an API response.
    ...
    ...    *Arguments:*
    ...    - ``response``: Response object from which to extract cookies
    ...
    ...    *Returns:*
    ...    - Dictionary containing cookies
    ...
    ...    *Example:*
    ...    | ${cookies} | Extract Cookies From API Response | ${response} |
    [Arguments]    ${response}
    ${cookies}    Create Dictionary
    FOR    ${cookie}    IN    @{response.cookies}
        ${name}    Get From Dictionary    ${cookie}    name
        ${value}    Get From Dictionary    ${cookie}    value
        Set To Dictionary    ${cookies}    ${name}    ${value}
    END
    RETURN    ${cookies}

Create Snaplex Api
    [Arguments]    ${snaplex_payload}
    Log    Snaplex Payload: ${snaplex_payload}
    ${response}    POST On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/plex
    ...    json=${snaplex_payload}
    RETURN    ${response}

Download slpropz file Api
    [Arguments]    ${snaplex_payload}    ${project_location}    ${expected_status}=200
    ${response}    Get On Session
    ...    ${ORG_ADMIN_SESSION}
    ...    /api/1/rest/plex/config/${org_name}/${project_location}/${groundplex_name}
    ...    expected_status=${expected_status}
    Log    Download slpropz file Api URL is:${response.url}    level=CONSOLE
    RETURN    ${response}

Delete snaplex Api
    [Documentation]    Deletes snap plex
    [Arguments]    ${snaplex_snode_id}    ${expected_status}=200
    ${response}    DELETE On Session    ${ORG_ADMIN_SESSION}    /api/1/rest/slsched/job/${snaplex_snode_id}
    RETURN    ${response}
