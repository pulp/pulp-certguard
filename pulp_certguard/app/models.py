from logging import getLogger
from gettext import gettext as _
from urllib.parse import unquote

from django.db import models

from OpenSSL import crypto as openssl

from pulpcore.plugin import storage
from pulpcore.plugin.models import ContentGuard

from pulp_certguard.app.utils import get_rhsm

try:
    from rhsm import certificate
except ImportError:
    pass


log = getLogger(__name__)


class RHSMCertGuard(ContentGuard):
    """
    A content-guard validating on a RHSM Certificate validated by `python-rhsm`.

    A Certificate Authority certificate to trust is required with each RHSMCertGuard created. With
    each request, the client certificate is first checked if it is signed by this CA cert. If not,
    it's untrusted and denied regardless of its paths.

    After determining the client certificate is trusted, the requested path is checked against the
    named paths in the certificate. A request is permitted if the current request path is a prefix
    of a path declared in the trusted RHSM Client Certificate.

    Fields:
        rhsm_certificate (models.TextField): The RHSM Ccertificate used to validate the client
            certificate at request time.
    """

    TYPE = 'rhsm'

    ca_certificate = models.TextField()

    def __init__(self, *args, **kwargs):
        """Initialize a RHSMCertGuard and ensure this system has python-rhsm on it."""
        get_rhsm()  # Validate that rhsm is installed
        super().__init__(*args, **kwargs)

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"

    def permit(self, request):
        """
        Validate the client cert is trusted and asserts a path that is prefix of the requested path.

        Args:
            request: The request from the user.

        Raises:
            PermissionError: If the request path is not a subpath of a path named in the
                certificate, or if the client certificate is not trusted from the CA certificated
                stored as `ca_certificate`.
        """
        get_rhsm()
        unquoted_certificate = unquote(self._get_client_cert_header(request))
        self._ensure_client_cert_is_trusted(unquoted_certificate)
        rhsm_cert = self._create_rhsm_cert_from_pem(unquoted_certificate)
        self._check_paths(rhsm_cert, request.path)

    @staticmethod
    def _get_client_cert_header(request):
        try:
            client_cert_data = request.headers["X-CLIENT-CERT"]
        except KeyError:
            msg = _("A client certificate was not received via the `X-CLIENT-CERT` header.")
            raise PermissionError(msg)
        return unquote(client_cert_data)

    def _ensure_client_cert_is_trusted(self, unquoted_certificate):
        try:
            openssl_ca_cert = openssl.load_certificate(
                openssl.FILETYPE_PEM, buffer=self.ca_certificate
            )
        except openssl.Error as exc:
            raise PermissionError(str(exc))

        try:
            openssl_client_cert = openssl.load_certificate(
                openssl.FILETYPE_PEM, buffer=unquoted_certificate
            )
        except openssl.Error as exc:
            raise PermissionError(str(exc))

        trust_store = openssl.X509Store()
        trust_store.add_cert(openssl_ca_cert)

        try:
            context = openssl.X509StoreContext(
                certificate=openssl_client_cert,
                store=trust_store,
            )
            context.verify_certificate()
        except openssl.X509StoreContextError:
            msg = _("Client certificate is not signed by the stored 'ca_certificate'.")
            raise PermissionError(msg)
        except openssl.Error as exc:
            raise PermissionError(str(exc))

    @staticmethod
    def _create_rhsm_cert_from_pem(unquoted_certificate):
        try:
            rhsm_cert = certificate.create_from_pem(unquoted_certificate)
        except certificate.CertificateException:
            msg = _("An error occured while loading the client certificate data into python-rhsm.")
            raise PermissionError(msg)
        return rhsm_cert

    @staticmethod
    def _check_paths(rhsm_cert, path):
        if rhsm_cert.check_path(path) is False:
            msg = _("Requested path is not a subpath of a path in the client certificate.")
            raise PermissionError(msg)


class X509CertGuard(ContentGuard):
    """
    A content-guard that authenticates the request based on a client provided X.509 Certificate.

    Fields:
        ca_certificate (models.FileField): The CA certificate used to
            validate the client certificate.
    """

    TYPE = 'x509'

    def _certpath(self, name):
        return storage.get_tls_path(self, name)

    ca_certificate = models.FileField(max_length=255, upload_to=_certpath)

    def permit(self, request):
        """Authorize the specified web request.

        Args:
            request (aiohttp.web.Request): A request for a published file.

        Raises:
            PermissionError: When the request cannot be authorized.

        """
        ca = self.ca_certificate.read()
        validator = X509Validator(ca.decode('utf8'))
        validator(request)

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class X509Validator:
    """An X.509 certificate validator."""

    CERT_HEADER_NAME = 'X-CLIENT-CERT'

    @staticmethod
    def format(pem):
        """Ensure the PEM encoded certificate is properly formatted.

        The certificate is passed as an HTTP header which does not permit newlines.

        Args:
            pem (str): A PEM encoded certificate.

        Returns:
            str: A properly PEM formatted certificate.

        """
        header = '-----BEGIN CERTIFICATE-----'
        footer = '-----END CERTIFICATE-----'
        body = pem.replace(header, '')
        body = body.replace(footer, '')
        body = body.strip(' \n\r')
        return '\n'.join((header, body, footer))

    @staticmethod
    def load(pem):
        """Load the PEM encoded certificate.

        Encapsulates complexity of OpenSSL.

        Args:
            pem (str): A PEM encoded certificate.

        Returns:
            openssl.X509: The loaded certificate.

        Raises:
            ValueError: On load failed.

        """
        try:
            return openssl.load_certificate(openssl.FILETYPE_PEM, buffer=X509Validator.format(pem))
        except Exception as le:
            raise ValueError(str(le))

    def client_certificate(self, request):
        """Extract and load the client certificate passed in the X-CLIENT-CERT header.

        Args:
            request (aiohttp.web.Request): A request for a published file.

        Returns:
            openssl.X509: The loaded certificate.

        Raises:
            KeyError: When the client certificate header has not
                been passed in the request.

        """
        name = self.CERT_HEADER_NAME
        try:
            certificate = request.headers[name]
        except KeyError:
            reason = _('HTTP header "{h}" not found.').format(h=name)
            raise KeyError(reason)
        else:
            return X509Validator.load(certificate)

    def __init__(self, ca_certificate):
        """Inits a new validator.

        Args:
            ca_certificate (str): A PEM encoded CA certificate.

        """
        self.ca_certificate = self.load(ca_certificate)

    @property
    def store(self):
        """A X.509 certificate (trust) store.

        Returns:
            openssl.X509Store: A store containing the CA certificate.

        """
        store = openssl.X509Store()
        store.add_cert(self.ca_certificate)
        return store

    def __call__(self, request):
        """Validate the client X.509 certificate passed in the request.

        Args:
            request (aiohttp.web.Request): A request for a published file.

        Raises:
            PermissionError: When validation the client certificate
                cannot be validated.

        """
        try:
            context = openssl.X509StoreContext(
                certificate=self.client_certificate(request),
                store=self.store,
            )
            context.verify_certificate()
        except openssl.X509StoreContextError:
            raise PermissionError(_('Client certificate cannot be validated.'))
        except Exception as pe:
            raise PermissionError(str(pe))
