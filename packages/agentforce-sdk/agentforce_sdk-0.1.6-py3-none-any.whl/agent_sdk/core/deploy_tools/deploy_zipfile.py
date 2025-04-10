import argparse
import asyncio
import json
import time
import logging
from typing import Dict, Optional

import aiohttp
import requests
from simple_salesforce import Salesforce
from simple_salesforce import SalesforceLogin
from ...exceptions import AgentforceAuthError, MetadataDeploymentError
from ...config import Config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(Config.get_log_level())

CORE_API_VERSION = Config.API_VERSION


def login_to_salesforce(username, password, domain):
    """Logs in to Salesforce and returns the session ID and instance URL."""
    try:
        session_id, instance = SalesforceLogin(username=username, password=password, domain=domain)
        return session_id, f"https://{instance}"
    except Exception as e:
        logger.error(f"Error logging in to Salesforce: {e}")
        return None, None


def deploy_metadata_to_salesforce(zip_path: str, 
                                agent_name: str,
                                instance_url: str,
                                session_id: str,
                                check_auth_callback: Optional[callable] = None) -> Dict:
    """Deploy a metadata zip file to Salesforce.
    
    Args:
        zip_path (str): Path to the zip file containing metadata
        agent_name (str): The name of the agent being deployed
        instance_url (str): Salesforce instance URL
        session_id (str): Salesforce session ID
        check_auth_callback (callable, optional): Callback function to check authentication
        
    Returns:
        dict: Response from Salesforce containing deployment status
        
    Raises:
        AgentforceAuthError: If authentication to Salesforce fails
        MetadataDeploymentError: If deployment to Salesforce fails
    """
    try:
        if check_auth_callback:
            check_auth_callback()
    except Exception as e:
        logger.error(f"Authentication check failed during deployment: {str(e)}")
        raise AgentforceAuthError(f"Failed to authenticate to Salesforce during deployment: {str(e)}")
    
    headers = {
        'Authorization': f'Bearer {session_id}',
        'Content-Type': 'multipart/form-data; boundary=--------------------------BOUNDARY'
    }

    deploy_options = {
        "allowMissingFiles": False,
        "autoUpdatePackage": False,
        "checkOnly": False,
        "ignoreWarnings": False,
        "performRetrieve": False,
        "purgeOnDelete": False,
        "rollbackOnError": False,
        "runTests": None,
        "singlePackage": True,
        "testLevel": "NoTestRun"
    }

    body = b''.join([
        b'----------------------------BOUNDARY\r\n',
        b'Content-Disposition: form-data; name="json"\r\n',
        b'Content-Type: application/json\r\n',
        b'\r\n',
        json.dumps({"deployOptions": deploy_options}).encode('utf-8'),
        b'\r\n----------------------------BOUNDARY\r\n',
        f'Content-Disposition: form-data; name="file"; filename="{zip_path}"\r\n'.encode('utf-8'),
        b'Content-Type: application/zip\r\n',
        b'\r\n',
        open(zip_path, 'rb').read(),
        b'\r\n----------------------------BOUNDARY--\r\n'
    ])
  
    url = f"{instance_url}/services/data/{CORE_API_VERSION}/metadata/deployRequest"
    logger.info(f"Deploying agent {agent_name} to Salesforce")
    
    try:
        # Use the session for connection pooling
        response = requests.post(url, headers=headers, data=body, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        result = response.json()
        
        # Monitor deployment status
        deploy_id = result.get('id')
        if not deploy_id:
            logger.error("No deployment ID returned from Salesforce")
            raise MetadataDeploymentError("No deployment ID returned from Salesforce")
            
        logger.info(f"Deployment started with ID: {deploy_id}")
        status = check_deployment_status(deploy_id, instance_url, session_id, check_auth_callback)
        
        return status
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while deploying agent {agent_name}")
        raise MetadataDeploymentError(f"Deployment request timed out")
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP Error: {e}"
        try:
            error_details = response.json()
            error_message = f"{error_message} - {json.dumps(error_details)}"
        except:
            pass
        
        logger.error(f"HTTP error while deploying agent: {error_message}")
        raise MetadataDeploymentError(error_message)
    except Exception as e:
        logger.error(f"Unexpected error during deployment: {str(e)}")
        raise MetadataDeploymentError(f"Deployment failed: {str(e)}")


def check_deployment_status(deploy_id: str,
                          instance_url: str,
                          session_id: str,
                          check_auth_callback: Optional[callable] = None) -> Dict:
    """Check the status of a metadata deployment.
    
    Args:
        session (requests.Session): Session object for connection pooling
        deploy_id (str): ID of the deployment to check
        instance_url (str): Salesforce instance URL
        session_id (str): Salesforce session ID
        check_auth_callback (callable, optional): Callback function to check authentication
        
    Returns:
        dict: Status of the deployment
        
    Raises:
        AgentforceAuthError: If authentication to Salesforce fails
        MetadataDeploymentError: If checking deployment status fails
    """
    try:
        if check_auth_callback:
            check_auth_callback()
    except Exception as e:
        logger.error(f"Authentication check failed during status check: {str(e)}")
        raise AgentforceAuthError(f"Failed to authenticate to Salesforce during status check: {str(e)}")
    
    max_retries = Config.MAX_RETRIES
    initial_retry_delay = Config.RETRY_DELAY
    max_retry_delay = Config.MAX_RETRY_DELAY
    
    url = f"{instance_url}/services/data/v61.0/metadata/deployRequest/{deploy_id}"
    headers = {
        'Authorization': f'Bearer {session_id}'
    }
    
    logger.info(f"Checking deployment status for ID: {deploy_id}?includeDetails=true")
    
    # Use exponential backoff for polling
    retry_delay = initial_retry_delay
    
    for attempt in range(max_retries):
        logger.info(f"Status check attempt {attempt + 1} of {max_retries}")
        
        try:
            # Use the session for connection pooling
            response = requests.get(url, headers=headers, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            status = response.json()
            
            current_status = status['deployResult']['status']
            logger.info(f"Current deployment status: {current_status}")
            
            if current_status in ['Succeeded', 'Failed', 'SucceededPartial']:
                if current_status == 'Failed' or current_status == 'SucceededPartial':
                    errors = status.get('details', {}).get('errors', [])
                    if errors:
                        error_messages = [f"{error.get('problem', 'Unknown error')}" for error in errors[:3]]
                        error_summary = "; ".join(error_messages)
                        if len(errors) > 3:
                            error_summary += f" and {len(errors) - 3} more errors"
                        logger.error(f"Deployment failed with errors: {error_summary}")
                
                return status
            
            # Still in progress, wait and retry with exponential backoff
            logger.info(f"Deployment still in progress. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            
            # Implement exponential backoff with a maximum delay
            retry_delay = min(retry_delay * 1.5, max_retry_delay)
            
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error checking deployment status: {e}"
            try:
                error_details = response.json()
                error_message = f"{error_message} - {json.dumps(error_details)}"
            except:
                pass
            
            # If authentication error, try to refresh token
            if e.response.status_code == 401 and check_auth_callback:
                logger.warning("Authentication token expired. Refreshing...")
                try:
                    check_auth_callback()
                    # Update headers with new token
                    headers['Authorization'] = f'Bearer {session_id}'
                except Exception as auth_error:
                    logger.error(f"Failed to refresh authentication token: {str(auth_error)}")
                    raise AgentforceAuthError(f"Failed to refresh authentication token: {str(auth_error)}")
            
            logger.error(error_message)
            # Continue to retry rather than fail immediately
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 1.5, max_retry_delay)
            
        except Exception as e:
            logger.error(f"Error checking deployment status: {str(e)}")
            # Continue to retry rather than fail immediately
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 1.5, max_retry_delay)
    
    # If we reach here, we've exceeded the maximum retries
    logger.warning(f"Deployment status check timed out after {max_retries} attempts")
    return {"status": "Unknown", "message": "Deployment status check timed out"}


def undeploy(session_id, instance_url, bot_api_name='SampleBot'):
    """Handles undeploying the metadata."""

    if session_id and instance_url:
        # Get the Bot Version Id
        bot_version_id = get_bot_version_id(session_id, instance_url, bot_api_name)

        if not bot_version_id:
            return {'error': 'No valid bot version Id found.'}

        # deactivate the bot version before undeploying
        deactivate_status = update_bot_version_status(session_id, instance_url, bot_version_id, 'INACTIVE')
        logger.info(deactivate_status)

        result = clear_planner_data(session_id, instance_url, bot_api_name)

        # de-activate the bot version after undeploying
        # activate_status = update_bot_version_status(session_id, instance_url, bot_version_id, 'ACTIVE')
        # print(activate_status)

        return result
    else:
        return {'error': 'Login failed'}

def deploy_multiple(session_id, instance_url, deploy_files, bot_api_name, agent_id):
    is_success = False
    for deploy_file in deploy_files:
        logger.info(f"Deploying file {deploy_file}")
        try:
            result = deploy_and_monitor(session_id, instance_url, deploy_file, True, bot_api_name)
            status = result['deployResult']['status']
            is_success = (status == 'Succeeded')
            if not is_success:
                logger.error(json.dumps(result, indent=2))
        except Exception as e:
            logger.error("Failed to deploy", e)

def deploy_async(session_id, instance_url, zip_file_path, bot_api_name, agent_id):
    try:
        result = deploy_and_monitor(session_id, instance_url, zip_file_path, True, bot_api_name)
        status = result['deployResult']['status']
    except Exception as e:
        logger.error("Failed to deploy", e)
  

async def get_action_details(session_id, instance_url, action_url, session):
    try:
        u = f'{instance_url}{action_url}'
        logger.info("Calling ", action_url)
        async with session.get(u, headers={"Authorization": f"Bearer {session_id}"}) as response:
            return await response.json()
    except Exception as e:
        logger.error(e)
        return None


async def get_all_actions(session_id, instance_url, action_urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in action_urls:
            tasks.append(get_action_details(session_id, instance_url, url, session))
        return await asyncio.gather(*tasks)


async def get_actions(session_id, instance_url):
    headers = {
        'Authorization': f'Bearer {session_id}'
    }

    flow_url = f"{instance_url}/services/data/v61.0/actions/custom/flow"
    apex_url = f"{instance_url}/services/data/v61.0/actions/custom/apex"

    action_urls = []

    # noinspection PyBroadException
    try:
        response = requests.get(flow_url, headers=headers)
        response_body = response.json()
        for action in response_body['actions']:
            action_urls.append(action['url'])

        response = requests.get(apex_url, headers=headers)
        response_body = response.json()
        for action in response_body['actions']:
            action_urls.append(action['url'])

        action_metadata = await get_all_actions(session_id, instance_url, action_urls)
        return get_clean_actions(action_metadata)
    except Exception as e:
        logger.error(e)
        return {"error": "Failed to get action details"}


def check_items(items):
    if not items:
        return False
    if len(items) == 0:
        return False
    for item in items:
        if not item['type']:
            return False
        if item['type'].lower() == 'null':
            return False
    return True


def get_real_params(items):
    params = []
    for item in items:
        if item['name'] and item['name'].startswith('Flow__'):
            continue
        if item['type'] and item['type'] != 'STRING':
            return []
        if not item['description']:
            return []
        params.append(item)
    return params


def extract_param_data(items):
    output = []
    for item in items:
        required = False
        if 'required' in item and isinstance(item['required'], bool):
            required = item['required']
        output.append(
            {
                'name': item['name'],
                'description': item['description'],
                'type': item['type'],
                'required': required
            }
        )
    return output


def get_action_data(action):
    name = action['name']
    description = action['description']
    if not description:
        description = name
    return {
        'inputs': extract_param_data(get_real_params(action['inputs'])),
        'outputs': extract_param_data(get_real_params(action['outputs'])),
        'action_name': name,
        'action_type': f'{action["type"]}'.lower(),
        'description': description
    }


def get_clean_actions(action_metadata):
    actions = []
    for action in action_metadata:
        if isinstance(action, list):
            continue
        if '__' in action['name']:
            continue
        inputs = action['inputs']
        outputs = action['outputs']
        if check_items(inputs) and check_items(outputs):
            if len(get_real_params(inputs)) > 0 and len(get_real_params(outputs)) > 0:
                actions.append(get_action_data(action))
    logger.info(f"Got {len(actions)} actions from org")
    return actions


def deploy_and_monitor(session=None, zip_path=None, agent_name=None, instance_url=None, session_id=None, check_auth_callback=None, username=None, password=None, domain=None, zip_file_path=None, bot_api_name='SampleBot', single_package=True):
    """Handles the entire deployment and monitoring process.
    
    Args:
        session: Session object for connection pooling
        zip_path: Path to the zip file
        agent_name: Name of the agent being deployed
        instance_url: Salesforce instance URL
        session_id: Salesforce session ID
        check_auth_callback: Callback function to check authentication
        username: Salesforce username (legacy parameter)
        password: Salesforce password (legacy parameter)
        domain: Salesforce domain (legacy parameter)
        zip_file_path: Path to the zip file (legacy parameter)
        bot_api_name: API name for the bot (legacy parameter)
        single_package: Whether to deploy as a single package
        
    Returns:
        dict: Result of the deployment
    """
    # For backward compatibility
    if zip_file_path and not zip_path:
        zip_path = zip_file_path
        
    if bot_api_name and not agent_name:
        agent_name = bot_api_name
    
    # If session_id and instance_url are not provided, login using credentials
    if not (session_id and instance_url) and (username and password and domain):
        session_id, instance_url = login_to_salesforce(username, password, domain)

    if session_id and instance_url:
        # Get the Bot Version Id
        bot_version_id = get_bot_version_id(session_id, instance_url, agent_name)

        # deactivate the bot version before deployment
        if bot_version_id:
            deactivate_status = update_bot_version_status(session_id, instance_url, bot_version_id, 'INACTIVE')
            logger.info(deactivate_status)

        clear_planner_data(session_id, instance_url, agent_name)

        cancel_deployment_status = cancel_current_deployments(session_id, instance_url)

        if cancel_deployment_status['status'] == 'failed':
            logger.error(cancel_deployment_status['result'])
            return {'error': cancel_deployment_status['result']}

        logger.info(cancel_deployment_status['result'])

        deployment_response = deploy_metadata_to_salesforce(
            zip_path, agent_name, instance_url, session_id, check_auth_callback
        )
        deploy_request_id = deployment_response['id']
        logger.info(f"Deployment request initiated with ID: {deploy_request_id}")

        deployment_result = check_deployment_status(
            deploy_request_id, instance_url, session_id, check_auth_callback
        )

        # activate the bot version after deployment success
        if deployment_result['deployResult']['status'] == 'Succeeded':
            if not bot_version_id:
                bot_version_id = get_bot_version_id(session_id, instance_url, agent_name)
            activate_status = update_bot_version_status(session_id, instance_url, bot_version_id, 'ACTIVE')
            logger.info(activate_status)

        return deployment_result
    else:
        logger.error("Login failed or required parameters missing")
        return {'error': 'Login failed or required parameters missing'}

def get_bot_username(session_id, instance_url):
    """Retrieves the Username the Bot User."""

    sf = Salesforce(session_id=session_id, instance_url=instance_url)

    if sf:
        try:
            # Use a single SOQL query with a subquery
            result = sf.query(
                f"SELECT Username FROM User WHERE Name = 'AgentForce Bot'"
            )
            if result['records']:
                return result['records'][0]['Username']
            else:
                logger.info(f"No Username found for User with Name 'AgentForce Bot'")
                return None
        except Exception as e:
            logger.error(f"Error querying Bot Username: {e}")
            return None
    else:
        logger.error("Login failed, cannot retrieve Bot Username.")
        return None


def get_bot_version_id(session_id, instance_url, bot_developer_name):
    """Retrieves the BotVersion Id using the Bot's DeveloperName."""

    sf = Salesforce(session_id=session_id, instance_url=instance_url)

    if sf:
        try:
            # Use a single SOQL query with a subquery
            result = sf.query(
                f"SELECT Id FROM BotVersion WHERE BotDefinitionId IN "
                f"(SELECT Id FROM BotDefinition WHERE DeveloperName = '{bot_developer_name}')"
            )
            if result['records']:
                return result['records'][0]['Id']
            else:
                logger.info(f"No BotVersion found for Bot with DeveloperName '{bot_developer_name}'")
                return None
        except Exception as e:
            logger.error(f"Error querying BotVersion: {e}")
            return None
    else:
        logger.error("Login failed, cannot retrieve BotVersion Id.")
        return None


def clear_planner_data(session_id, instance_url, bot_developer_name):
    """Removes Topics, Actions and Instructions from the Planner."""

    sf = Salesforce(session_id=session_id, instance_url=instance_url, version='60.0')

    planner_id = None
    planner_join_topics = []
    topics_join_actions = []
    topics = []
    actions = []
    instructions = []
    if sf:
        # Fetch the Planner Definition
        try:
            result = sf.query(f"SELECT Id FROM GenAiPlannerDefinition WHERE DeveloperName = '{bot_developer_name}_v1'")
            if result['records']:
                planner_id = result['records'][0]['Id']
                logger.info(f"planner_id found {planner_id}")
            else:
                logger.info(f"No Planner Definition Found with '{bot_developer_name}_v1'")
                return None
        except Exception as e:
            logger.error(f"Error querying Planner Definition: {e}")
            return None

        # Fetch Plugins attached to Planner
        try:
            result = sf.query(f"SELECT Id, Plugin FROM GenAiPlannerFunctionDef WHERE PlannerId = '{planner_id}'")
            if result['records']:
                for record in result['records']:
                    topics.append(record['Plugin'])
                    planner_join_topics.append(record['Id'])
                logger.info(f"planner join topics found {planner_join_topics}")
            else:
                logger.info(f"No Plugins/Topics Found")
                return {'result': 'success'}
        except Exception as e:
            logger.error(f"Error querying Plugins/Topics: {e}")
            return None

        # Fetch Actions attached to Topics
        try:
            topic_list = ", ".join(f"'{topic}'" for topic in topics)
            result = sf.query(f"SELECT Id, Function FROM GenAiPluginFunctionDef WHERE PluginId IN ({topic_list})")
            if result['records']:
                for record in result['records']:
                    actions.append(record['Function'])
                    topics_join_actions.append(record['Id'])
                logger.info(f"topics join actions found {topics_join_actions}")
            else:
                logger.info(f"No Actions Found")
        except Exception as e:
            logger.error(f"Error querying Actions: {e}")
            return None

        # Fetch Instructions attached to Topics
        try:
            topic_list = ", ".join(f"'{topic}'" for topic in topics)
            result = sf.query(
                f"SELECT Id FROM GenAiPluginInstructionDef WHERE GenAiPluginDefinitionId IN ({topic_list})")
            if result['records']:
                for record in result['records']:
                    instructions.append(record['Id'])
                logger.info(f"instructions found {instructions}")
            else:
                logger.info(f"No Instructions Found")
        except Exception as e:
            logger.error(f"Error querying Instructions: {e}")
            return None

        headers = {
            'Authorization': f'Bearer {session_id}',
            'Content-Type': 'application/json'
        }

        # Delete Records
        try:
            for id in planner_join_topics:
                try:
                    url = f"{instance_url}/services/data/{CORE_API_VERSION}/sobjects/GenAiPlannerFunctionDef/{id}"
                    response = requests.delete(url, headers=headers)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f"Error deleting {id} object: {e}")

            for id in topics_join_actions:
                try:
                    url = f"{instance_url}/services/data/{CORE_API_VERSION}/sobjects/GenAiPluginFunctionDef/{id}"
                    response = requests.delete(url, headers=headers)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f"Error deleting {id} object: {e}")

            for id in instructions:
                try:
                    url = f"{instance_url}/services/data/{CORE_API_VERSION}/sobjects/GenAiPluginInstructionDef/{id}"
                    response = requests.delete(url, headers=headers)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f"Error deleting {id} object: {e}")

            for id in actions:
                try:
                    url = f"{instance_url}/services/data/{CORE_API_VERSION}/sobjects/GenAiFunctionDefinition/{id}"
                    response = requests.delete(url, headers=headers)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f"Error deleting {id} object: {e}")

            for id in topics:
                try:
                    url = f"{instance_url}/services/data/{CORE_API_VERSION}/sobjects/GenAiPluginDefinition/{id}"
                    response = requests.delete(url, headers=headers)
                    response.raise_for_status()
                except Exception as e:
                    logger.error(f"Error deleting {id} object: {e}")

        except Exception as e:
            logger.error(f"Error deleting object: {e}")
            return None

        return {'result': 'success'}
    else:
        logger.error("Login failed, can not clear metadata.")
        return None


def update_bot_version_status(session_id, instance_url, bot_version_id, status="ACTIVE"):
    """Updates the status of a Bot Version using the Connect API."""
    sf = Salesforce(session_id=session_id, instance_url=instance_url)

    if session_id and instance_url:
        headers = {
            'Authorization': f'Bearer {session_id}',
            'Content-Type': 'application/json'
        }

        url = f"{instance_url}/services/data/{CORE_API_VERSION}/connect/bot-versions/{bot_version_id}/activation"

        data = {
            "status": status
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        try:
            response.raise_for_status()  # Raise an exception for HTTP errors
            logger.info(f"Bot Version status updated to '{status}' successfully.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error updating Bot Version status: {e}")
            logger.error(response.text)
            return None
    else:
        logger.error("Login failed, cannot update Bot Version status.")
        return None


def cancel_current_deployments(session_id, instance_url, api_version=CORE_API_VERSION):
    """
    Cancel all in-progress deployments in Salesforce.

    Args:
        username (str): Salesforce username.
        password (str): Salesforce password (append security token if necessary).
        domain (str): Salesforce domain ('login' for production or 'test' for sandbox).

    Returns:
        None
    """

    headers = {
        'Authorization': f'Bearer {session_id}',
        'Content-Type': 'application/json'
    }

    try:
        # Using the Tooling API to execute the query
        soql_query = "SELECT Id FROM DeployRequest WHERE Status = 'InProgress'"
        encoded_query = requests.utils.quote(soql_query)
        query_url = f"{instance_url}/services/data/{api_version}/tooling/query/?q={encoded_query}"
        response = requests.get(query_url, headers=headers)
        deployments = response.json()['records']
    except Exception as e:
        # print(f"Failed to query in-progress deployments: {e}")
        return {
            'status': 'failed',
            'result': f"Failed to query in-progress deployments: {e}"
        }

    # Check if there are any in-progress deployments
    if not deployments:
        # print("No in-progress deployments found.")
        return {
            "status": "success",
            "result": "No in-progress deployments found."
        }

    # Step 4: Cancel each in-progress deployment
    for deployment in deployments:
        deployment_id = deployment['Id']
        cancel_url = f"{instance_url}/services/data/{api_version}/metadata/deployRequest/{deployment_id}"

        logger.info(cancel_url)
        patch_body = {
            'deployResult': {
                'status': "Canceling"
            }
        }

        try:
            cancel_response = requests.patch(cancel_url, headers=headers, json=patch_body)
            if cancel_response.status_code == 202:
                deployment_result = check_deployment_status(session_id, deployment_id, instance_url, session_id)
                logger.info(f"Deployment {deployment_id} canceling requested. Deployment cancel result {deployment_result}")
            else:
                # print(f"Failed to cancel deployment {deployment_id}: {cancel_response.text}")
                return {
                    "status": "failed",
                    "result": f"Failed to cancel deployment {deployment_id}: {cancel_response.text}"
                }

        except Exception as e:
            # print(f"Error canceling deployment {deployment_id}: {e}")
            return {
                "status": "failed",
                "result": f"Error canceling deployment {deployment_id}: {e}"
            }

    return {
        "status": "success",
        "result": f"Canceled f{len(deployments)} deployments"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy metadata to Salesforce.')
    parser.add_argument('session_id', type=str, help='Salesforce session ID')
    parser.add_argument('instance_url', type=str, help='Salesforce instance URL')
    parser.add_argument('zip_file', type=str, help='Path to the metadata zip file')
    parser.add_argument('--single_package', action='store_true',
                        help='Set to True if deploying a single package (default: True)')
    parser.add_argument(
        "--bot_api_name",
        nargs="?",
        default="SampleBot",  # Provide a default output directory
        help="Path to the template directory (default: templates)"
    )
    args = parser.parse_args()

    deployment_result = deploy_and_monitor(args.session_id, args.instance_url, args.zip_file, args.single_package,
                                           args.bot_api_name)
    print(deployment_result)
