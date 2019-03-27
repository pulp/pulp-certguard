"""Constants for Pulp certguard plugin tests."""
import os
from pulp_smash.pulp3.constants import BASE_PATH, CONTENT_GUARDS_PATH  # noqa:F401
from pulp_file.tests.functional.constants import FILE_REMOTE_PATH, FILE_PUBLISHER_PATH  # noqa:F401

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CERTS_BASE_PATH = os.path.join(
    _CURRENT_DIR, 'artifacts', 'x509', 'certificates'
)
CERT_CA_FILE_PATH = os.path.join(CERTS_BASE_PATH, 'ca.pem')
CERT_CLIENT_FILE_PATH = os.path.join(CERTS_BASE_PATH, 'client.pem')
KEYS_BASE_PATH = os.path.join(_CURRENT_DIR, 'x509', 'keys')
