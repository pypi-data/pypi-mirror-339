from typing import Callable, List
from arcanna_mcp_input_server.constants import GET_JOBS_URL, GET_JOB_BY_ID_URL, GET_JOB_LABELS_URL, GET_JOB_BY_NAME_URL
from arcanna_mcp_input_server.environment import API_KEY, ARCANNA_USER
import requests
from arcanna_mcp_input_server.utils.exceptions_handler import handle_exceptions


def export_tools() -> List[Callable]:
    return [
        get_external_input_jobs
    ]


@handle_exceptions
async def get_external_input_job_by_id(job_id: int) -> dict:
    """
        Retrieve Arcanna External Input Job by id.
        An Arcanna External Input Job refers to a job where the user's API Key is configured on the input integration, enabling data to be sent via HTTP calls.
        Use this tool only when:
            - 1. The user intends to send data to Arcanna
                 Example user query: "I want to start pushing/send data to Arcanna. What is the configuration for job id = <JOB_ID>?"
            - 2. The user specifically requests decision labels for one job configured with an external API Key
                 Example user query: "Can you show me the configuration for job with id <JOB_ID> that use an external API key input?"

    Parameters:
    -----------
    job_id : int
        Unique identifier for the job.

    Returns:
    --------
    dict
        A dictionary containing job details with the following keys:

        - job_id (int): Unique identifier for the job.
        - category (str): Category of the job.
        - title (str): Title or name of the job.
        - status (str): Current status of the job (e.g., ENABLED - the job is ingesting events. DISABLED - the job is stopped.
         READY_TO_SELECT_FEATURES - user must select decision points. etc.).
        - retrain_state (str): State of the retraining process.
        - retrain_msg (str): Message providing details about the retraining process.
        - labels (list of str): List of decision labels associated with the job.
        - features (list of str): List of decision points used in the job.
        - processed_documents_count (int): Number of events processed.
        - feedback_documents_count (int): Number of events that received feedback.
        - last_processed_timestamp (str): Timestamp of the last processed event.
        - last_feedback_timestamp (str): Timestamp of the last received feedback.
        - last_train_start_timestamp (str): Timestamp when the last training started.
        - last_train_finished_timestamp (str): Timestamp when the last training finished.
        - invalid (bool): Indicates whether the job is invalid (True/False).
    """
    headers = {
        "x-arcanna-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(GET_JOB_BY_ID_URL.format(job_id), headers=headers)
    return response.json()


@handle_exceptions
async def get_external_input_jobs() -> list:
    """
        Retrieve Arcanna External Input Jobs.
        An Arcanna External Input Job refers to a job where the user's API Key is configured on the input integration, enabling data to be sent via HTTP calls.
        Use this tool only when:
            - 1. The user intends to send data to Arcanna
                 Example user query: "I want to start pushing/send data to Arcanna. What jobs can I use?"
            - 2. The user specifically requests jobs configured with an external API Key
                 Example user query: "Can you show me the jobs that use an external API key input?"

        DO NOT use this tool outside the specific scenarios described. If you're unsure, ask the user for clarification before proceeding.
        DO NOT use this tool if the user is requesting a generic job retrieval, such as:
            - 1. "What are the available jobs?"
            - 2. "What jobs are in Arcanna?"
            - 3. "List the jobs."
            - 4. "Show the jobs."
            In such cases, use a different tool designed for general job listing instead.

    Returns:
    --------
    list
        A list of dictionaries, each representing job details with the following keys:

        - job_id (int): Unique identifier for the job.
        - category (str): Category of the job.
        - title (str): Title or name of the job.
        - status (str): Current status of the job (e.g., ENABLED - the job is ingesting events. DISABLED - the job is stopped.
         READY_TO_SELECT_FEATURES - user must select decision points. etc.).
        - retrain_state (str): State of the retraining process.
        - retrain_msg (str): Message providing details about the retraining process.
        - labels (list of str): List of decision labels associated with the job.
        - features (list of str): List of decision points used in the job.
        - processed_documents_count (int): Number of events processed.
        - feedback_documents_count (int): Number of events that received feedback.
        - last_processed_timestamp (str): Timestamp of the last processed event.
        - last_feedback_timestamp (str): Timestamp of the last received feedback.
        - last_train_start_timestamp (str): Timestamp when the last training started.
        - last_train_finished_timestamp (str): Timestamp when the last training finished.
        - invalid (bool): Indicates whether the job is invalid (True/False).

    """
    headers = {
        "x-arcanna-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(GET_JOBS_URL, headers=headers)
    return response.json()


@handle_exceptions
async def get_external_input_job_labels(job_id: int) -> list:
    """
        Retrieve decision labels for an Arcanna External Input Job.
        An Arcanna External Input Job refers to a job where the user's API Key is configured on the input integration, enabling data to be sent via HTTP calls.
        Use this tool only when:
            - 1. The user intends to send data to Arcanna
                 Example user query: "I want to start pushing/send data to Arcanna. What are the decision labels for job id = <JOB_ID>?"
            - 2. The user specifically requests decision labels for one job configured with an external API Key
                 Example user query: "Can you show me the decision labels for job with id <JOB_ID> that use an external API key input?"

    Parameters:
    --------
    job_id: Unique identifier of the job

    Returns:
    --------
    list
        A list containing decision labels configured for the job.
    """
    headers = {
        "x-arcanna-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(GET_JOB_LABELS_URL.format(job_id), headers=headers)
    return response.json()


@handle_exceptions
async def get_external_input_job_by_name(job_name: str) -> dict:
    """
        Retrieve Arcanna External Input Job by job name.
        An Arcanna External Input Job refers to a job where the user's API Key is configured on the input integration, enabling data to be sent via HTTP calls.
        Use this tool only when:
            - 1. The user intends to send data to Arcanna
                 Example user query: "I want to start pushing/send data to Arcanna. What is the configuration for job name = <JOB_NAME>?"
            - 2. The user specifically requests decision labels for one job configured with an external API Key
                 Example user query: "Can you show me the configuration for job with id <JOB_NAME> that use an external API key input?"

    Parameters:
    --------
    job_name: Name of the job you want to retrieve.

    Returns:
    --------
    dict
        A dictionary containing job details with the following keys:

        - job_id (int): Unique identifier for the job.
        - category (str): Category of the job.
        - title (str): Title or name of the job.
        - status (str): Current status of the job (e.g., ENABLED - the job is ingesting events. DISABLED - the job is stopped.
         READY_TO_SELECT_FEATURES - user must select decision points. etc.).
        - retrain_state (str): State of the retraining process.
        - retrain_msg (str): Message providing details about the retraining process.
        - labels (list of str): List of decision labels associated with the job.
        - features (list of str): List of decision points used in the job.
        - processed_documents_count (int): Number of events processed.
        - feedback_documents_count (int): Number of events that received feedback.
        - last_processed_timestamp (str): Timestamp of the last processed event.
        - last_feedback_timestamp (str): Timestamp of the last received feedback.
        - last_train_start_timestamp (str): Timestamp when the last training started.
        - last_train_finished_timestamp (str): Timestamp when the last training finished.
        - invalid (bool): Indicates whether the job is invalid (True/False).
    """
    headers = {
        "x-arcanna-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "job_name": job_name
    }
    response = requests.post(GET_JOB_BY_NAME_URL, json=body, headers=headers)
    return response.json()
