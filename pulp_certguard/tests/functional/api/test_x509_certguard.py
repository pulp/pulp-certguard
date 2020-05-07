import uuid

from pulpcore.client.pulp_certguard import CertguardX509CertGuard, ContentguardsX509Api

from pulp_certguard.tests.functional.api.base import BaseCertGuard, CommonDenialTestsMixin
from pulp_certguard.tests.functional.constants import (
    X509_BASE_PATH,
    X509_CA_CERT_FILE_PATH,
    X509_CLIENT_CERT_FILE_PATH,
    X509_UNTRUSTED_CLIENT_CERT_FILE_PATH,
    X509_UN_URLENCODED_CLIENT_CERT_FILE_PATH,
)
from pulp_certguard.tests.functional.utils import (
    gen_certguard_client,
    set_distribution_base_path_and_download_a_content_unit_with_cert,
)


class X509CertGuardTestCase(BaseCertGuard, CommonDenialTestsMixin):
    """Api tests for X509CertGard."""

    DENIALS_BASE_PATH = X509_BASE_PATH
    UNTRUSTED_CLIENT_CERT_PATH = X509_UNTRUSTED_CLIENT_CERT_FILE_PATH

    @classmethod
    def _setup_content_guard(cls):
        # Create an X.509 Content Guard
        certguard_client = gen_certguard_client()
        cls.x509_content_guards_api = ContentguardsX509Api(certguard_client)

        with open(X509_CA_CERT_FILE_PATH, 'r') as x509_ca_cert_data_file:
            x509_ca_cert_data = x509_ca_cert_data_file.read()

        x509_cert_guard = CertguardX509CertGuard(
            name=str(uuid.uuid4()),
            ca_certificate=x509_ca_cert_data
        )
        cls.x509_content_guard_data = cls.x509_content_guards_api.create(x509_cert_guard)
        cls.teardown_cleanups.append(
            (cls.x509_content_guards_api.delete, cls.x509_content_guard_data.pulp_href)
        )
        return cls.x509_content_guard_data.pulp_href

    def test_allow_request_when_cert_is_trusted(self):
        """
        Assert a correctly configured client can fetch content.

        1. Configure the distribution with an X.509 CertGuard.
        2. Attempt to download content.
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            X509_BASE_PATH,
            self.repo.pulp_href,
            X509_CLIENT_CERT_FILE_PATH
        )

    def test_allow_request_when_apache_un_urlencoded_cert_is_trusted(self):
        """
        Assert a correctly configured client can fetch content with reverse proxy Apache < 2.6.10.

        1. Configure the distribution with an X.509 CertGuard.
        2. Attempt to download content with an un-urlencoded certificate (Apache < 2.6.10 style)
        """
        set_distribution_base_path_and_download_a_content_unit_with_cert(
            self.distribution.pulp_href,
            X509_BASE_PATH,
            self.repo.pulp_href,
            X509_UN_URLENCODED_CLIENT_CERT_FILE_PATH,
            url_encode=False,
        )
