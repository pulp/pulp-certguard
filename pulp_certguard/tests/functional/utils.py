"""Utilities for tests for the certguard plugin."""

from random import choice
from time import sleep
from urllib.parse import quote

from pulp_smash import config
from pulp_smash.pulp3.utils import download_content_unit

from pulpcore.client.pulpcore import (
    ApiClient as CoreApiClient,
    TasksApi,
)

from pulpcore.client.pulp_certguard import ApiClient as CertguardApiClient

from pulpcore.client.pulp_file import (
    DistributionsFileApi,
    RepositoriesFileApi,
)

from pulp_file.tests.functional.utils import (
    gen_file_client,
    get_file_content_paths,
)


cfg = config.get_config()
configuration = cfg.get_bindings_config()

core_client = CoreApiClient(configuration)
tasks = TasksApi(core_client)


def read_cert(cert_path):
    """Return an string of data read from `cert_path`."""
    with open(cert_path, 'r') as cert_file:
        return cert_file.read()


def read_cert_and_urlencode(cert_path):
    """Return an string of data read from `cert_path` and urlencode."""
    return quote(read_cert(cert_path))


def gen_certguard_client():
    """Return an OBJECT for file client."""
    return CertguardApiClient(configuration)


def monitor_task(task_href):
    """Polls the Task API until the task is in a completed state.

    Prints the task details and a success or failure message. Exits on failure.

    Args:
        task_href(str): The href of the task to monitor

    Returns:
        list[str]: List of hrefs that identify resource created by the task

    """
    completed = ["completed", "failed", "canceled"]
    task = tasks.read(task_href)
    while task.state not in completed:
        sleep(2)
        task = tasks.read(task_href)

    if task.state == "completed":
        return task.created_resources

    return task.to_dict()


def set_distribution_base_path(file_distribution_href, base_path):
    """
    Set the base path of a FileDistribution and return the updated representation.

    Args:
        file_distribution_href: The distribution href that is to be updated. This must refer to a
            distribution of type `FileDistribution`.
        base_path: The base path to set on the `distribution`.

    Returns:
        The bindings object representing the updated FileDistribution.
    """
    file_client = gen_file_client()
    distributions_api = DistributionsFileApi(file_client)
    update_response = distributions_api.partial_update(
        file_distribution_href,
        {"base_path": base_path}
    )
    monitor_task(update_response.task)
    return distributions_api.read(file_distribution_href)


def set_distribution_base_path_and_download_a_content_unit_with_cert(
        file_distribution_href,
        base_path,
        file_repository_href,
        cert_path,
        content_path=None,
        url_encode=True):
    """
    Set the base path on the `distribution, read the cert, urlencode it, and then request one unit.

    If `content_path` is set, that path will be requested, otherwise a random, valid content unit
    path will be selected from the FileRepository at `file_repository_href`.

    1. Set the distribution referred to by `file_distribution_href` base_path to `base_path`.
    2. Read the cert from the filesystem and urlencode it.
    3. Make a request to `content_path` if specified, or to a random content item present in the
        `file_repository_href` repository. The urlencoded cert is submitted as the `X-CLIENT-CERT`
        header when requesting content.

    Args:
        file_distribution_href: The distribution href that is to be updated. This must refer to a
            distribution of type `FileDistribution`.
        base_path: The base path to set on the `distribution`.
        file_repository_href: The repository href that will have
        cert_path: The file system path to the certificate to be used in the content request. This
            will be read from the filesystem and urlencoded before being submitted as the
            `X-CLIENT-CERT` header when downloading content.
        content_path: The path to the specific content unit to be fetched. This is the portion of
            the url after the distribution URL. It's optional, and if unspecified a random, valid
            content unit will be selected instead from the repository.
        url_encode: If true, the certificate data read will be urlencoded, otherwise it won't be.
            This is an optional param, and defaults to True.

    Returns:
        The downloaded data.

    """
    distribution = set_distribution_base_path(file_distribution_href, base_path)

    if content_path is None:
        file_client = gen_file_client()
        file_repos_api = RepositoriesFileApi(file_client)
        repo = file_repos_api.read(file_repository_href)
        content_path = choice(get_file_content_paths(repo.to_dict()))

    if url_encode:
        cert_data = read_cert_and_urlencode(cert_path)
    else:
        cert_data = read_cert(cert_path)

    return download_content_unit(
        config.get_config(),
        distribution.to_dict(),
        content_path,
        headers={'X-CLIENT-CERT': cert_data}
    )
