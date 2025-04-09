import logging
import os

from google.cloud import dataproc_v1, resourcemanager_v3, storage
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


def get_credentials(service_account_file=None):
    """Get credentials from service account JSON file if provided."""
    return service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )


def list_projects(credentials=None):
    """List all accessible Google Cloud projects.

    Args:
        credentials: Optional credentials to use for authentication

    Returns:
        List of project tuples containing (project_id, display_name)
    """
    # Create the projects client
    if credentials:
        client = resourcemanager_v3.ProjectsClient(credentials=credentials)
    else:
        client = resourcemanager_v3.ProjectsClient()

    # List projects - using search instead of list_projects
    # since list_projects requires a parent organization which may not be available
    projects = []
    try:
        # Use search_projects instead, which doesn't require a parent parameter
        request = resourcemanager_v3.SearchProjectsRequest()
        response = client.search_projects(request=request)

        for project in response:
            # Only include active projects
            if project.state == resourcemanager_v3.Project.State.ACTIVE:
                # Create a tuple of (project_id, display_name or project_id if no display_name)
                display_name = project.display_name or project.project_id
                projects.append((project.project_id, display_name))

    except Exception as e:
        logger.error(f"Error listing projects: {e}")

    return projects


def list_clusters(project_id, region, credentials=None):
    """List all Dataproc clusters in the specified project and region."""
    client_options = {"api_endpoint": f"{region}-dataproc.googleapis.com:443"}

    if credentials:
        client = dataproc_v1.ClusterControllerClient(
            client_options=client_options, credentials=credentials
        )
    else:
        client = dataproc_v1.ClusterControllerClient(client_options=client_options)

    request = dataproc_v1.ListClustersRequest(
        project_id=project_id,
        region=region,
    )

    clusters = []
    for cluster in client.list_clusters(request=request):
        status = cluster.status.state.name
        clusters.append(cluster)

    return clusters


def get_cluster_log_location(project_id, region, cluster_name, credentials=None):
    """Get the log location (temp bucket or event dir) for a specific cluster."""
    client_options = {"api_endpoint": f"{region}-dataproc.googleapis.com:443"}

    if credentials:
        client = dataproc_v1.ClusterControllerClient(
            client_options=client_options, credentials=credentials
        )
    else:
        client = dataproc_v1.ClusterControllerClient(client_options=client_options)

    request = dataproc_v1.GetClusterRequest(
        project_id=project_id, region=region, cluster_name=cluster_name
    )

    cluster = client.get_cluster(request=request)

    # Get the temp bucket from the cluster config
    temp_bucket = cluster.config.temp_bucket

    # Extract cluster UUID from the full details
    cluster_uuid = cluster.cluster_uuid

    # Try to find Spark event log directory in properties
    spark_event_log_dir = None
    if hasattr(cluster.config.software_config, "properties"):
        properties = cluster.config.software_config.properties
        spark_event_log_dir = properties.get("spark:spark.eventLog.dir")

    return {
        "temp_bucket": temp_bucket,
        "cluster_uuid": cluster_uuid,
        "spark_event_log_dir": spark_event_log_dir,
    }


def list_spark_applications(project_id, temp_bucket, cluster_uuid, credentials=None):
    """List all Spark applications for a given cluster using the temp bucket."""
    # Initialize the GCS client
    if credentials:
        storage_client = storage.Client(project=project_id, credentials=credentials)
    else:
        storage_client = storage.Client(project=project_id)

    # Remove the gs:// prefix if present
    bucket_name = temp_bucket.replace("gs://", "")

    # Path for Spark job history
    spark_job_history_path = f"{cluster_uuid}/spark-job-history/"

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # List all blobs with the prefix
    blobs = list(bucket.list_blobs(prefix=spark_job_history_path))

    # Extract application IDs
    app_ids = set()
    for blob in blobs:
        path_parts = blob.name.split("/")
        for part in path_parts:
            if part.startswith("application_"):
                app_ids.add(part)

    return list(app_ids)


def download_application_logs(
    project_id, temp_bucket, cluster_uuid, application_id, output_dir, credentials=None
):
    """Download all logs for a specific Spark application."""
    # Initialize the GCS client
    if credentials:
        storage_client = storage.Client(project=project_id, credentials=credentials)
    else:
        storage_client = storage.Client(project=project_id)

    # Remove the gs:// prefix if present
    bucket_name = temp_bucket.replace("gs://", "")

    # Path for the specific application logs
    app_logs_path = f"{cluster_uuid}/spark-job-history/{application_id}"

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # List all blobs with the prefix
    blobs = list(bucket.list_blobs(prefix=app_logs_path))
    logger.debug(f"{blobs=}")
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Download each blob
    for blob in blobs:
        # Create file path
        rel_path = blob.name[len(app_logs_path) :].lstrip("/")
        # if not rel_path:  # Skip directory entries
        #    continue

        file_path = os.path.join(output_dir, os.path.basename(blob.name))

        # Download the blob
        with open(file_path, "wb") as f:
            blob.download_to_file(f)
