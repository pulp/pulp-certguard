import unittest
import uuid

from requests import HTTPError

from pulp_smash import config

from pulpcore.client.pulp_certguard import CertguardRHSMCertGuard, ContentguardsRHSMApi
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

from pulp_certguard.tests.functional.constants import (
    RHSM_CA_CERT_FILE_PATH,
    RHSM_CLIENT_CERT_FROM_UNTRUSTED_CA,
    RHSM_UBER_CERT_BASE_PATH_ONE,
    RHSM_UBER_CERT_BASE_PATH_TWO,
    RHSM_UBER_CLIENT_CERT,
    RHSM_V1_ONE_AND_TWO_VAR_CLIENT_CERT,
    RHSM_V1_ONE_VAR_BASE_PATH,
    RHSM_V1_TWO_VAR_BASE_PATH,
    RHSM_V1_ZERO_VAR_CLIENT_CERT,
    RHSM_V1_ZERO_VAR_BASE_PATH,
    RHSM_V3_INVALID_BASE_PATH,
    RHSM_V3_ONE_AND_TWO_VAR_CLIENT_CERT,
    RHSM_V3_ONE_VAR_BASE_PATH,
    RHSM_V3_TWO_VAR_BASE_PATH,
    RHSM_V3_ZERO_VAR_CLIENT_CERT,
    RHSM_V3_ZERO_VAR_BASE_PATH,
)
from pulp_certguard.tests.functional.utils import (
    gen_certguard_client,
    monitor_task,
    set_distribution_base_path,
    set_distribution_base_path_and_download_a_content_unit_with_cert,
)


class RHSMCertGuardBase(unittest.TestCase):
    """A base class for all RHSMCertGuard tests which provides generic setup and teardown."""

    @classmethod
    def setUpClass(cls):
        """
        Initialize Pulp to make authorization assertions using client certificates.

        0. Create a FileRepository
        1. Create a FileRemote
        2. Sync in a few units we can use to fetch with
        3. Create a Publication
        4. Create a CertGuard with the CA cert used to sign all RHSM client certificates
        5. Create a Distribution for the publication that is protected by the CertGuard

        """
        cls.teardown_cleanups = []
        cls.cfg = config.get_config()

        file_client = gen_file_client()
        repo_api = RepositoriesFileApi(file_client)
        remote_api = RemotesFileApi(file_client)
        publications = PublicationsFileApi(file_client)
        cls.distributions_api = DistributionsFileApi(file_client)

        certguard_client = gen_certguard_client()
        cls.rhsm_content_guards_api = ContentguardsRHSMApi(certguard_client)

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

        # Create a RHSM Content Guard
        with open(RHSM_CA_CERT_FILE_PATH, 'r') as rhsm_ca_cert_data_file:
            rhsm_ca_cert_data = rhsm_ca_cert_data_file.read()

        rhsm_cert_guard = CertguardRHSMCertGuard(
            name=str(uuid.uuid4()),
            ca_certificate=rhsm_ca_cert_data
        )
        cls.rhsm_content_guard_data = cls.rhsm_content_guards_api.create(rhsm_cert_guard)
        cls.teardown_cleanups.append(
            (cls.rhsm_content_guards_api.delete, cls.rhsm_content_guard_data.pulp_href)
        )

        # Create a distribution.
        body = gen_distribution()
        body["publication"] = publication_href
        body["content_guard"] = cls.rhsm_content_guard_data.pulp_href
        distribution_response = cls.distributions_api.create(body)
        created_resources = monitor_task(distribution_response.task)
        cls.distribution = cls.distributions_api.read(created_resources[0])
        cls.teardown_cleanups.append((cls.distributions_api.delete, cls.distribution.pulp_href))

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        for cleanup_function, args in reversed(cls.teardown_cleanups):
            cleanup_function(args)


class RHSMV3CertGuardTestCase(RHSMCertGuardBase):
    """Api tests for RHSMCertGard with V3 RHSM Certificates."""

    def test_allow_request_when_cert_matches_zero_var_path(self):
        """
        Assert a correctly configured client can fetch content from a zero-variable path.

        1. Configure the distribution with a zero-variable path in the RHSM Cert.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V3_ZERO_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V3_ZERO_VAR_CLIENT_CERT
        )

    def test_allow_request_when_cert_matches_one_var_path(self):
        """
        Assert a correctly configured client can fetch content from a one-variable path.

        1. Configure the distribution with a one-variable path in the RHSM Cert.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V3_ONE_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V3_ONE_AND_TWO_VAR_CLIENT_CERT
        )

    def test_allow_request_when_cert_matches_two_var_path(self):
        """
        Assert a correctly configured client can fetch content from a two-variable path.

        1. Configure the distribution with a two-variable path in the RHSM Cert.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V3_TWO_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V3_ONE_AND_TWO_VAR_CLIENT_CERT
        )

    def test_allow_request_when_requesting_the_distribution_root(self):
        """
        Assert a correctly configured client can fetch content from the root of a distribution.

        1. Configure the distribution with a zero-variable path in the RHSM Cert.
        2. Attempt to fetch the url of the distribution itself (its root).
        """
        content_path = ""  # This causes the root to be fetched
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V3_ZERO_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V3_ZERO_VAR_CLIENT_CERT,
            content_path,
        )

    def test_allow_request_to_subdir_of_path(self):
        """
        Assert a correctly configured client can fetch content from a subdir of a distribution.

        1. Configure the distribution with a zero-variable path in the RHSM Cert.
        2. Attempt to download a content url with a subdir in it.
        3. Assert a 404 was received.
        """
        content_path = "somedir/made_up_content.iso"
        with self.assertRaises(HTTPError) as raised_exception:
            set_distribution_base_path_and_download_a_content_unit_with_cert(
                self.distribution.pulp_href,
                RHSM_V3_ZERO_VAR_BASE_PATH,
                self.repo.pulp_href,
                RHSM_V3_ZERO_VAR_CLIENT_CERT,
                content_path,
            )

        # The path doesn't exist so we expect a 404, but the authorization part we are testing works
        self.assertEqual(raised_exception.exception.response.status_code, 404)


class RHSMV1CertGuardTestCase(RHSMCertGuardBase):
    """Api tests for RHSMCertGard with V1 RHSM Certificates."""

    def test_allow_request_when_cert_matches_zero_var_path(self):
        """
        Assert a correctly configured client can fetch content from a zero-variable path.

        1. Configure the distribution with a zero-variable path in the RHSM Cert.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V1_ZERO_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V1_ZERO_VAR_CLIENT_CERT
        )

    def test_allow_request_when_cert_matches_one_var_path(self):
        """
        Assert a correctly configured client can fetch content from a one-variable path.

        1. Configure the distribution with a one-variable path in the RHSM Cert.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V1_ONE_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V1_ONE_AND_TWO_VAR_CLIENT_CERT
        )

    def test_allow_request_when_cert_matches_two_var_path(self):
        """
        Assert a correctly configured client can fetch content from a two-variable path.

        1. Configure the distribution with a two-variable path in the RHSM Cert.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V1_TWO_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V1_ONE_AND_TWO_VAR_CLIENT_CERT
        )

    def test_allow_request_when_requesting_the_distribution_root(self):
        """
        Assert a correctly configured client can fetch content from the root of a distribution.

        1. Configure the distribution with a zero-variable path in the RHSM Cert.
        2. Attempt to fetch the url of the distribution itself (its root).
        """
        content_path = ""  # This causes the root to be fetched
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_V1_ZERO_VAR_BASE_PATH,
            self.repo.pulp_href,
            RHSM_V1_ZERO_VAR_CLIENT_CERT,
            content_path,
        )

    def test_allow_request_to_subdir_of_path(self):
        """
        Assert a correctly configured client can fetch content from a subdir of a distribution.

        1. Configure the distribution with a zero-variable path in the RHSM Cert.
        2. Attempt to download a content url with a subdir in it.
        3. Assert a 404 was received.
        """
        content_path = "somedir/made_up_content.iso"
        with self.assertRaises(HTTPError) as raised_exception:
            set_distribution_base_path_and_download_a_content_unit_with_cert(
                self.distribution.pulp_href,
                RHSM_V1_ZERO_VAR_BASE_PATH,
                self.repo.pulp_href,
                RHSM_V1_ZERO_VAR_CLIENT_CERT,
                content_path,
            )

        # The path doesn't exist so we expect a 404, but the authorization part we are testing works
        self.assertEqual(raised_exception.exception.response.status_code, 404)


class RHSMUberCertTestCase(RHSMCertGuardBase):
    """Api tests for RHSMCertGard with an "Uber" Certificate."""

    def test_allow_request_with_uber_cert_for_any_subpath(self):
        """
        Assert a client with an uber cert can fetch any subpath.

        1. Configure the distribution with a subpath of the uber cert.
        2. Attempt to download content.
        3. Configure the distribution with a different subpath of the uber cert.
        4. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_UBER_CERT_BASE_PATH_ONE,
            self.repo.pulp_href,
            RHSM_UBER_CLIENT_CERT
        )
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            RHSM_UBER_CERT_BASE_PATH_TWO,
            self.repo.pulp_href,
            RHSM_UBER_CLIENT_CERT
        )


class RHSMCertGuardDenialTestCase(RHSMCertGuardBase):
    """Api tests for RHSMCertGard to assert denials for authorization."""

    def test_denial_when_client_cert_does_not_contain_subpath_of_distribution_base_path(self):
        """
        Assert denial when a client with a cert that does not contain a subpath of the distribution.

        1. Configure the distribution with path that is not a subpath contained in the cert.
        2. Attempt to download content.
        3. Assert a 403 Unauthorized is returned.
        """
        with self.assertRaises(HTTPError) as raised_exception:
            set_distribution_base_path_and_download_a_content_unit_with_cert(
                self.distribution.pulp_href,
                RHSM_V3_INVALID_BASE_PATH,
                self.repo.pulp_href,
                RHSM_V3_ZERO_VAR_CLIENT_CERT
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)

    def test_denial_when_empty_client_header_submitted(self):
        """
        Assert denial when a client submits an empty X-CLIENT-CERT header.

        1. Configure the distribution with a valid base path.
        2. Attempt to download content.
        3. Assert a 403 Unauthorized is returned.
        """
        distribution = set_distribution_base_path(
            self.distribution.pulp_href,
            RHSM_V3_ZERO_VAR_BASE_PATH
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
            RHSM_V3_ZERO_VAR_BASE_PATH
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
            RHSM_V3_ZERO_VAR_BASE_PATH
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
                RHSM_V3_ZERO_VAR_BASE_PATH,
                self.repo.pulp_href,
                RHSM_CLIENT_CERT_FROM_UNTRUSTED_CA
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)
