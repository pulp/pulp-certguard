"""Constants for Pulp certguard plugin tests."""
import os
from urllib.parse import urljoin

from pulp_smash.pulp3.constants import BASE_PATH, BASE_CONTENT_GUARDS_PATH  # noqa:F401
from pulp_file.tests.functional.constants import (  # noqa:F401
    FILE_REMOTE_PATH,
    FILE_DISTRIBUTION_PATH,
)

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CERTS_BASE_PATH = os.path.join(
    _CURRENT_DIR, 'artifacts', 'x509', 'certificates'
)
CERT_CA_FILE_PATH = os.path.join(CERTS_BASE_PATH, 'ca.pem')
CERT_CLIENT_FILE_PATH = os.path.join(CERTS_BASE_PATH, 'client.pem')
KEYS_BASE_PATH = os.path.join(_CURRENT_DIR, 'x509', 'keys')
X509_CONTENT_GUARD_PATH = urljoin(BASE_CONTENT_GUARDS_PATH, "certguard/x509/")
