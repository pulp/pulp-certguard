import unittest
from random import choice
from requests import HTTPError
from pulp_smash import api, config, utils
from pulp_smash.pulp3.constants import (
    REPO_PATH,
)
from pulp_smash.pulp3.utils import (
    download_content_unit,
    gen_distribution,
    gen_repo,
    sync,
)
from pulp_certguard.tests.functional.constants import (
    CERT_CA_FILE_PATH,
    CERT_CLIENT_FILE_PATH,
    X509_CONTENT_GUARD_PATH,
    FILE_DISTRIBUTION_PATH,
    FILE_REMOTE_PATH,
)
from pulp_certguard.tests.functional.utils import (
    create_file_publication,
    gen_file_remote,
    get_file_content_paths
)


class CertGuardTestCase(unittest.TestCase):
    """Api tests for cerguard."""

    @classmethod
    def setUpClass(cls):
        """Initialize common use entities and variables.

        0. Prepare artifacts (ca and client certs)
        1. Create self.contentguard for ca.pem located in CERT_CA_PATH.
        2. create a repo.
        3. create a file remote.
        4. Sync it.
        5. Create a Publication.

        """
        cls.cfg = cfg = config.get_config()
        cls.client = client = api.Client(cfg, api.page_handler)
        cls.teardown_cleanups = []

        # The certificate header must have no \n chars
        with open(CERT_CLIENT_FILE_PATH, 'r') as cert_client_file:
            cls.client_cert = str(cert_client_file.read()).replace('\n', '')

        with utils.ensure_teardownclass(cls):
            # 1. Create certguard
            with open(CERT_CA_FILE_PATH, 'rb') as cert_ca_file:
                cls.certguard = client.post(
                    X509_CONTENT_GUARD_PATH,
                    data={'name': utils.uuid4()},
                    files={'ca_certificate': cert_ca_file}
                )
                cls.teardown_cleanups.append(
                    (client.delete, cls.certguard['_href'])
                )

            # 2. Create a repo
            _repo = client.post(REPO_PATH, gen_repo())
            cls.teardown_cleanups.append((cls.client.delete, _repo['_href']))

            # 3. Create a remote
            cls.remote = client.post(FILE_REMOTE_PATH, gen_file_remote())
            cls.teardown_cleanups.append(
                (cls.client.delete, cls.remote['_href'])
            )

            # 4. Sync and read synced repo
            sync(cfg, cls.remote, _repo)
            cls.repo = client.get(_repo['_href'])

            # 5. Create a publication
            cls.publication = create_file_publication(cfg, cls.repo)
            cls.teardown_cleanups.append(
                (cls.client.delete, cls.publication['_href'])
            )

    def test_negative_download_protected_content_without_keys(self):
        """Assert content protected by cert-guard cannot be downloaded.

        1. Create a protected distribution using the self.contentguard.
        2. Assert content cannot be downloaded without cert and key.
        """
        # Create a protected distribution
        distribution = self.client.using_handler(api.task_handler).post(
            FILE_DISTRIBUTION_PATH,
            gen_distribution(
                publication=self.publication['_href'],
                content_guard=self.certguard['_href']
            )
        )
        self.addCleanup(self.client.delete, distribution['_href'])

        # Pick a filename
        unit_path = choice(get_file_content_paths(self.repo))

        # Try to download it without the SSL-CLIENT-CERTIFICATE
        with self.assertRaises(HTTPError):
            download_content_unit(self.cfg, distribution, unit_path)

    def test_positive_download_protected_content_with_keys(self):
        """Assert content protected by cert-guard can be downloaded.

        1. Create a protected distribution using the self.contentguard.
        2. Assert content can be downloaded using the proper cert and key.
        """
        # Create a protected distribution
        distribution = self.client.using_handler(api.task_handler).post(
            FILE_DISTRIBUTION_PATH,
            gen_distribution(
                publication=self.publication['_href'],
                content_guard=self.certguard['_href']
            )
        )
        self.addCleanup(self.client.delete, distribution['_href'])

        # Pick a filename
        unit_path = choice(get_file_content_paths(self.repo))

        # Try to download it passing the proper SSL-CLIENT-CERTIFICATE
        download_content_unit(
            self.cfg,
            distribution,
            unit_path,
            headers={'SSL-CLIENT-CERTIFICATE': self.client_cert}
        )

    def test_positive_add_contentguard_to_existing_distribution(self):
        """Assert adding contentguard to existing distribution works well.

        1. Create a distribution without protection
        2. Assert content can be downloaded
        3. Add contentguard to the distribution
        4. Assert content cannot be downloaded without key
        5. Assert content can be downloaded with key
        """
        # 1 unprotected distribution
        distribution = self.client.using_handler(api.task_handler).post(
            FILE_DISTRIBUTION_PATH,
            gen_distribution(publication=self.publication['_href'])
        )
        self.addCleanup(self.client.delete, distribution['_href'])

        # Pick a filename
        unit_path = choice(get_file_content_paths(self.repo))

        # Download it without certificate
        download_content_unit(self.cfg, distribution, unit_path)

        # Update distribution adding the guard
        distribution = self.client.using_handler(api.task_handler).patch(
            distribution['_href'],
            {'content_guard': self.certguard['_href']}
        )

        # Cannot download without key
        with self.assertRaises(HTTPError):
            download_content_unit(self.cfg, distribution, unit_path)

        # Try to download it passing the proper SSL-CLIENT-CERTIFICATE
        download_content_unit(
            self.cfg,
            distribution,
            unit_path,
            headers={'SSL-CLIENT-CERTIFICATE': self.client_cert}
        )

    def test_positive_remove_contentguard(self):
        """Assert that content can be download without guard if it is removed.

        1. Create a protected distribution using the self.contentguard
        2. Assert content cannot be downloaded without keys
        3. Remove the contentguard
        4. Assert content can be downloaded without keys
        """
        # Create a protected distribution
        distribution = self.client.using_handler(api.task_handler).post(
            FILE_DISTRIBUTION_PATH,
            gen_distribution(
                publication=self.publication['_href'],
                content_guard=self.certguard['_href']
            )
        )
        self.addCleanup(self.client.delete, distribution['_href'])

        # Pick a filename
        unit_path = choice(get_file_content_paths(self.repo))

        # Try to download it without the SSL-CLIENT-CERTIFICATE
        with self.assertRaises(HTTPError):
            download_content_unit(self.cfg, distribution, unit_path)

        # Update distribution removing the guard
        distribution = self.client.using_handler(api.task_handler).patch(
            distribution['_href'],
            {'content_guard': None}
        )

        # Now content can be downloaded
        download_content_unit(self.cfg, distribution, unit_path)

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        for cleanup_function, args in reversed(cls.teardown_cleanups):
            cleanup_function(args)
