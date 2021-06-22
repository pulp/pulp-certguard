import uuid

from requests import HTTPError

from pulpcore.client.pulp_certguard import CertguardRHSMCertGuard, ContentguardsRhsmApi

from pulp_certguard.tests.functional.api.base import BaseCertGuard, CommonDenialTestsMixin
from pulp_certguard.tests.functional.constants import (
    RHSM_CA_CERT_FILE_PATH,
    RHSM_CLIENT_CERT_FROM_UNTRUSTED_CA,
    RHSM_CLIENT_CERT_TRUSTED_BUT_EXPIRED,
    THIRDPARTY_CA_CERT_FILE_PATH,
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
    set_distribution_base_path_and_download_a_content_unit_with_cert,
)


class RHSMCertGuardBase(BaseCertGuard):
    """A base class for all RHSMCertGuard tests which provides generic setup and teardown."""

    @classmethod
    def _setup_content_guard(cls):
        # Create a RHSM Content Guard
        certguard_client = gen_certguard_client()
        cls.rhsm_content_guards_api = ContentguardsRhsmApi(certguard_client)

        rhsm_ca_cert_data = cls._load_rhsm_ca_cert_file()

        rhsm_cert_guard = CertguardRHSMCertGuard(
            name=str(uuid.uuid4()),
            ca_certificate=rhsm_ca_cert_data
        )
        cls.rhsm_content_guard_data = cls.rhsm_content_guards_api.create(rhsm_cert_guard)
        cls.teardown_cleanups.append(
            (cls.rhsm_content_guards_api.delete, cls.rhsm_content_guard_data.pulp_href)
        )
        return cls.rhsm_content_guard_data.pulp_href

    @classmethod
    def _load_rhsm_ca_cert_file(cls):
        with open(RHSM_CA_CERT_FILE_PATH, 'r') as rhsm_ca_cert_data_file:
            rhsm_ca_cert_data = rhsm_ca_cert_data_file.read()

        return rhsm_ca_cert_data


class RHSMCABundleCertGuardBase(RHSMCertGuardBase):
    """A base class for all RHSMCertGuard tests with a CA-bundle file."""

    @classmethod
    def _load_rhsm_ca_cert_file(cls):
        with open(RHSM_CA_CERT_FILE_PATH, 'r') as rhsm_ca_cert_data_file:
            rhsm_ca_cert_data = rhsm_ca_cert_data_file.read()

        with open(THIRDPARTY_CA_CERT_FILE_PATH, 'r') as thirdparty_ca_cert_file:
            thirdparty_ca_cert_data = thirdparty_ca_cert_file.read()

        # build a bundle to use (i.e., a list-of-CA-certs we will trust)
        return thirdparty_ca_cert_data + rhsm_ca_cert_data


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


class RHSMCertGuardDenialTestCase(RHSMCertGuardBase, CommonDenialTestsMixin):
    """Api tests for RHSMCertGard to assert denials for authorization."""

    DENIALS_BASE_PATH = RHSM_V3_ZERO_VAR_BASE_PATH
    UNTRUSTED_CLIENT_CERT_PATH = RHSM_CLIENT_CERT_FROM_UNTRUSTED_CA

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

    def test_denial_when_client_cert_is_trusted_but_expired(self):
        """
        Assert denial when a client sends a trusted but expired cert that has a valid subpath.

        1. Configure the distribution with valid path contained in the cert.
        2. Attempt to download content with a trusted but expired cert.
        3. Assert a 403 Unauthorized is returned.
        """
        with self.assertRaises(HTTPError) as raised_exception:
            set_distribution_base_path_and_download_a_content_unit_with_cert(
                self.distribution.pulp_href,
                RHSM_V1_ONE_VAR_BASE_PATH,
                self.repo.pulp_href,
                RHSM_CLIENT_CERT_TRUSTED_BUT_EXPIRED
            )
        self.assertEqual(raised_exception.exception.response.status_code, 403)


class RHSMV3CABundleCertGuardTestCase(RHSMCABundleCertGuardBase):
    """Api tests for RHSMCertGard with V3 RHSM Certificates and a bundle of CAs in a file."""

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
