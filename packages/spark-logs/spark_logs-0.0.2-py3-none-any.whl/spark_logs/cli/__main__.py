import argparse
import logging
import sys
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union

import inquirer

from spark_logs import setup_logging
from spark_logs.dataproc import (download_application_logs,
                                 get_cluster_log_location, get_credentials,
                                 list_clusters, list_projects,
                                 list_spark_applications)

T = TypeVar("T")  # Generic type for items
R = TypeVar("R")  # Generic type for return value

# Get the module logger
logger = logging.getLogger(__name__)


def prompt_selection(
    items: List[T],
    item_type: str,
    message: str,
    result_key: str,
    formatter: Optional[Callable[[T], Tuple[str, R]]] = None,
    empty_message: Optional[str] = None,
) -> Optional[Union[R, str]]:
    """
    Generic function to display a selection list and prompt the user to choose one option.

    Args:
        items: List of items to choose from
        item_type: Type of item being selected (for logging/messages)
        message: Prompt message to display
        result_key: Key for the result in the answers dict
        formatter: Function to format each item for display as (display_string, value)
        empty_message: Custom message to display when no items are found

    Returns:
        The selected item value or None if cancelled or error occurred
    """
    if not items:
        if empty_message:
            print(empty_message)
        else:
            print(f"No {item_type}s found")
        return None

    # Create choices using the formatter if provided
    choices = []
    if formatter:
        for item in items:
            if item is not None:  # Guard against None values
                display, value = formatter(item)
                choices.append((display, value))
    else:
        # If no formatter, use items directly (assumes they're strings)
        choices = [(str(item), item) for item in items if item is not None]

    questions = [inquirer.List(result_key, message=message, choices=choices)]

    answers = inquirer.prompt(questions)
    if answers and result_key in answers:
        return answers[result_key]

    # Handle case where user cancels input
    print("\nOperation cancelled by user")
    return None


def get_project(credentials: Any = None) -> Optional[str]:
    """
    Get a Google Cloud project ID by listing available projects and prompting for selection.

    Args:
        credentials: Optional GCP credentials

    Returns:
        Selected project ID or None if cancelled/error
    """
    print("Fetching available Google Cloud projects...")
    try:
        projects = list_projects(credentials)

        if not projects:
            print(
                "No accessible Google Cloud projects found. Please check your credentials."
            )
            return None

        # Format projects for display: (project_id, display_name) -> (display_str, project_id)
        def format_project(project_tuple):
            project_id, display_name = project_tuple
            return f"{display_name} ({project_id})", project_id

        return prompt_selection(
            items=projects,
            item_type="project",
            message="Select a Google Cloud project",
            result_key="project_id",
            formatter=format_project,
            empty_message="No accessible Google Cloud projects found. Please check your credentials.",
        )
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        print(
            "Unable to list Google Cloud projects. Please check your credentials and permissions."
        )
        return None


def get_cluster(project_id: str, region: str, credentials: Any = None) -> Optional[str]:
    """
    Get a Dataproc cluster by listing available clusters and prompting for selection.

    Args:
        project_id: GCP project ID
        region: GCP region
        credentials: Optional GCP credentials

    Returns:
        Selected cluster name or None if cancelled/error
    """
    print(f"Fetching clusters in project {project_id}, region {region}...")
    try:
        clusters = list_clusters(project_id, region, credentials)

        # Format clusters for display: cluster object -> (display_str, cluster_name)
        def format_cluster(cluster):
            status = cluster.status.state.name
            return f"{cluster.cluster_name} ({status})", cluster.cluster_name

        return prompt_selection(
            items=clusters,
            item_type="cluster",
            message="Select a cluster",
            result_key="cluster_name",
            formatter=format_cluster,
            empty_message=f"No clusters found in project {project_id}, region {region}",
        )
    except Exception as e:
        logger.error(f"Error listing clusters: {e}")
        print(
            f"Unable to list clusters. Please check if the project {project_id} exists and you have access."
        )
        return None


def get_application(
    project_id: str, temp_bucket: str, cluster_uuid: str, credentials: Any = None
) -> Optional[str]:
    """
    Get a Spark application ID by listing available applications and prompting for selection.

    Args:
        project_id: GCP project ID
        temp_bucket: Cluster temp bucket
        cluster_uuid: Cluster UUID
        credentials: Optional GCP credentials

    Returns:
        Selected application ID or None if cancelled/error
    """
    print(f"Fetching Spark applications for cluster...")
    try:
        app_ids = list_spark_applications(
            project_id, temp_bucket, cluster_uuid, credentials
        )

        # No special formatting needed for app IDs
        return prompt_selection(
            items=app_ids,
            item_type="Spark application",
            message="Select a Spark application",
            result_key="app_id",
            empty_message="No Spark applications found for this cluster",
        )
    except Exception as e:
        logger.error(f"Error listing applications: {e}")
        print("Unable to list Spark applications. Please check your permissions.")
        return None


def main():
    # Set up logging
    setup_logging()

    parser = argparse.ArgumentParser(description="Download logs from Dataproc clusters")
    parser.add_argument(
        "--region", default="us-central1", help="Dataproc region (default: us-central1)"
    )
    parser.add_argument("--project", help="Google Cloud Project ID")
    parser.add_argument("--cluster", help="Cluster name to operate on")
    parser.add_argument("--app-id", help="Application ID to download logs for")
    parser.add_argument(
        "--output-dir",
        default="./logs",
        help="Directory to save logs (default: ./logs)",
    )
    parser.add_argument(
        "--service-account-json", help="Path to service account JSON key file"
    )

    args = parser.parse_args()

    # Get credentials from service account JSON if provided
    credentials = None
    if args.service_account_json:
        try:
            credentials = get_credentials(args.service_account_json)
            logger.info(
                f"Using service account credentials from: {args.service_account_json}"
            )
        except Exception as e:
            logger.error(f"Failed to load service account credentials: {e}")
            return

    # Get project ID - either from args or by prompting the user
    project_id = args.project
    if not project_id:
        project_id = get_project(credentials)
        if not project_id:
            return  # User cancelled or error occurred

    region = args.region

    # Get or prompt for cluster
    cluster_name = args.cluster
    if not cluster_name:
        cluster_name = get_cluster(project_id, region, credentials)
        if not cluster_name:
            return  # User cancelled or error occurred

    # Get log location info for the cluster
    log_info = get_cluster_log_location(project_id, region, cluster_name, credentials)

    if log_info["temp_bucket"] is None:
        logger.error(f"Could not find temp bucket for cluster {cluster_name}")
        return

    # Get or prompt for application ID
    app_id = args.app_id
    if not app_id:
        app_id = get_application(
            project_id, log_info["temp_bucket"], log_info["cluster_uuid"], credentials
        )
        if not app_id:
            return  # User cancelled or error occurred

    # Confirmation message
    print(f"\nReady to download logs for application {app_id}")
    print(f"  Project: {project_id}")
    print(f"  Cluster: {cluster_name}")
    print(f"  Output directory: {args.output_dir}")

    # Confirm before proceeding
    questions = [
        inquirer.Confirm("confirm", message="Proceed with download?", default=True)
    ]
    answers = inquirer.prompt(questions)
    confirm = answers and answers.get("confirm")
    if not confirm:
        print("Download cancelled")
        return

    # Download the application logs
    try:
        download_application_logs(
            project_id,
            log_info["temp_bucket"],
            log_info["cluster_uuid"],
            app_id,
            args.output_dir,
            credentials,
        )
        print(f"\n✅ Successfully downloaded logs to {args.output_dir}")
    except Exception as e:
        logger.error(f"Error downloading logs: {e}")
        print("❌ Failed to download logs")
        return


if __name__ == "__main__":
    main()
