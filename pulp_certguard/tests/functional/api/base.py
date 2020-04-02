from requests import HTTPError
import unittest

from pulp_smash import config

from pulpcore.client.pulp_file import (
    DistributionsFileApi,
    FileFilePublication,
    PublicationsFileApi,
    RepositoriesFileApi,
    RepositorySyncURL,
    RemotesFileApi,
)

from pulp_file.tests.functional.utils import (
    gen_file_client,
    gen_file_remote,
)
from pulp_smash.pulp3.utils import (
    download_content_unit,
    gen_distribution,
    gen_repo,
)

from pulp_certguard.tests.functional.utils import (
    monitor_task,
    set_distribution_base_path,
    set_distribution_base_path_and_download_a_content_unit_with_cert,
)


class BaseCertGuard(unittest.TestCase):
    """A base class for all CertGuard tests which provides generic setup and teardown."""

    @classmethod
    def setUpClass(cls):
        """
        Initialize Pulp to make authorization assertions using client certificates.

        0. Create a FileRepository
        1. Create a FileRemote
        2. Sync in a few units we can use to fetch with
        3. Create a Publication
        4. Create a CertGuard with the CA cert used to sign all client certificates
        5. Create a Distribution for the publication that is protected by the CertGuard

        """
        cls.teardown_cleanups = []
        cls.cfg = config.get_config()

        file_client = gen_file_client()
        repo_api = RepositoriesFileApi(file_client)
        remote_api = RemotesFileApi(file_client)
        publications = PublicationsFileApi(file_client)
        cls.distributions_api = DistributionsFileApi(file_client)

        cls.repo = repo_api.create(gen_repo())
        cls.teardown_cleanups.append((repo_api.delete, cls.repo.pulp_href))

        body = gen_file_remote(policy="immediate")
        remote = remote_api.create(body)
        cls.teardown_cleanups.append((remote_api.delete, remote.pulp_href))

        # Sync a Repository
        repository_sync_data = RepositorySyncURL(remote=remote.pulp_href)
        sync_response = repo_api.sync(cls.repo.pulp_href, repository_sync_data)
        monitor_task(sync_response.task)
        cls.repo = repo_api.read(cls.repo.pulp_href)

        # Create a publication.
        publish_data = FileFilePublication(repository=cls.repo.pulp_href)
        publish_response = publications.create(publish_data)
        created_resources = monitor_task(publish_response.task)
        publication_href = created_resources[0]
        cls.teardown_cleanups.append((publications.delete, publication_href))

        content_guard_href = cls._setup_content_guard()

        # Create a distribution.
        body = gen_distribution()
        body["publication"] = publication_href
        body["content_guard"] = content_guard_href
        distribution_response = cls.distributions_api.create(body)
        created_resources = monitor_task(distribution_response.task)
        cls.distribution = cls.distributions_api.read(created_resources[0])
        cls.teardown_cleanups.append((cls.distributions_api.delete, cls.distribution.pulp_href))

    @classmethod
    def _setup_content_guard(cls):
        raise NotImplementedError("subclasses must implement '_setup_content_guard'")

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        for cleanup_function, args in reversed(cls.teardown_cleanups):
            cleanup_function(args)


class CommonDenialTestsMixin:
    """Common tests between X.509 and RHSM Cert Guards which should all produce denials."""

    DENIALS_BASE_PATH = None
    UNTRUSTED_CLIENT_CERT_PATH = None

    def test_denial_when_empty_client_header_submitted(self):
        """
        Assert denial when a client submits an empty X-CLIENT-CERT header.

        1. Configure the distribution with a valid base path.
        2. Attempt to download content.
        3. Assert a 403 Unauthorized is returned.
        """
        distribution = set_distribution_base_path(
            self.distribution.pulp_href,
            self.DENIALS_BASE_PATH
        )

        content_path = ""

        with self.assertRaises(HTTPError) as raised_exception:
            download_content_unit(
                config.get_config(),
                distribution.to_dict(),
                content_path,
                headers={'X-CLIENT-CERT': ""}
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)

    def test_denial_when_no_client_header_submitted(self):
        """
        Assert denial when a client submits no X-CLIENT-CERT header.

        1. Configure the distribution with a valid base path.
        2. Attempt to download content.
        3. Assert a 403 Unauthorized is returned.
        """
        distribution = set_distribution_base_path(
            self.distribution.pulp_href,
            self.DENIALS_BASE_PATH
        )

        content_path = ""

        with self.assertRaises(HTTPError) as raised_exception:
            download_content_unit(
                config.get_config(),
                distribution.to_dict(),
                content_path
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)

    def test_denial_when_client_header_contains_an_invalid_certificate(self):
        """
        Assert denial when a client submits X-CLIENT-CERT header with invalid certificate data.

        1. Configure the distribution with a valid base path.
        2. Attempt to download content.
        3. Assert a 403 Unauthorized is returned.
        """
        distribution = set_distribution_base_path(
            self.distribution.pulp_href,
            self.DENIALS_BASE_PATH
        )

        content_path = ""

        with self.assertRaises(HTTPError) as raised_exception:
            download_content_unit(
                config.get_config(),
                distribution.to_dict(),
                content_path,
                headers={'X-CLIENT-CERT': "this is not cert data"}
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)

    def test_denial_when_client_header_contains_an_untrusted_certificate(self):
        """
        Assert denial when a client submits a valid but rhsm certificate but not for the trusted CA.

        1. Configure the distribution with a valid base path.
        2. Attempt to download content with an untrusted client certificate.
        3. Assert a 403 Unauthorized is returned.
        """
        with self.assertRaises(HTTPError) as raised_exception:
            set_distribution_base_path_and_download_a_content_unit_with_cert(
                self.distribution.pulp_href,
                self.DENIALS_BASE_PATH,
                self.repo.pulp_href,
                self.UNTRUSTED_CLIENT_CERT_PATH
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)
