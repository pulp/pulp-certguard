"""Constants for Pulp certguard plugin tests."""
import os


_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


X509_BASE_PATH = "my-content-view"
X509_CERTS_BASE_PATH = os.path.join(
    _CURRENT_DIR, 'artifacts', 'x509', 'certificates'
)
X509_CA_CERT_FILE_PATH = os.path.join(X509_CERTS_BASE_PATH, 'ca.pem')
X509_CLIENT_CERT_FILE_PATH = os.path.join(X509_CERTS_BASE_PATH, 'client.pem')
X509_UNTRUSTED_CLIENT_CERT_FILE_PATH = os.path.join(X509_CERTS_BASE_PATH, 'untrusted_client.pem')


RHSM_CA_CERT_FILE_PATH = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'katello-default-ca.crt'
)


RHSM_CLIENT_CERT_FROM_UNTRUSTED_CA = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'untrusted_cert.pem'
)

RHSM_CLIENT_CERT_TRUSTED_BUT_EXPIRED = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'trusted_but_expired.pem'
)


# Uber cert path: /pulp
RHSM_UBER_CLIENT_CERT = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'uber.cert'
)
RHSM_UBER_CERT_BASE_PATH_ONE = "my-content-view"
RHSM_UBER_CERT_BASE_PATH_TWO = "another-content-view"


# Zero_var path: /pulp/content/my-content-view/custom/custom_product/foo
RHSM_V1_ZERO_VAR_CLIENT_CERT = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'v1', '367265616451720695.pem'
)
RHSM_V1_ZERO_VAR_BASE_PATH = "my-content-view/custom/custom_product/foo"


# One var path: /pulp/content/my-content-view/content/dist/rhel/server/7/7Server/$basearch/extras/os
# Two var path: /pulp/content/my-content-view/content/dist/rhel/server/7/$releasever/$basearch/os
RHSM_V1_ONE_AND_TWO_VAR_CLIENT_CERT = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'v1', '4938399836766610274.pem'
)
RHSM_V1_ONE_VAR_BASE_PATH = "my-content-view/content/dist/rhel/server/7/7Server/x86_64/extras/os"
RHSM_V1_TWO_VAR_BASE_PATH = "my-content-view/content/dist/rhel/server/7/7.4/x86_64/os"


# Zero_var path: /pulp/content/my-content-view/custom/custom_product/foo
RHSM_V3_ZERO_VAR_CLIENT_CERT = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'v3', '6221403274536093008.pem'
)
RHSM_V3_ZERO_VAR_BASE_PATH = "my-content-view/custom/custom_product/foo"
RHSM_V3_INVALID_BASE_PATH = "this-is-not-a-valid-base-path"


# One var path: /pulp/content/my-content-view/content/dist/rhel8/$releasever/x86_64/baseos/os
# Two var path: /pulp/content/my-content-view/content/eus/rhel/server/7/$releasever/$basearch/os
RHSM_V3_ONE_AND_TWO_VAR_CLIENT_CERT = os.path.join(
    _CURRENT_DIR, 'artifacts', 'rhsm', 'v3', '3284681923705053889.pem'
)
RHSM_V3_ONE_VAR_BASE_PATH = "my-content-view/content/dist/rhel8/8/x86_64/baseos/os"
RHSM_V3_TWO_VAR_BASE_PATH = "my-content-view/content/eus/rhel/server/7/7.4/x86_64/os"
