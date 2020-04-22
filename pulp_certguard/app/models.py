from logging import getLogger
from gettext import gettext as _
from urllib.parse import unquote

from django.db import models

from OpenSSL import crypto as openssl

from pulpcore.plugin.models import ContentGuard

from pulp_certguard.app.utils import get_rhsm

try:
    from rhsm import certificate
except ImportError:
    pass


log = getLogger(__name__)


class BaseCertGuard(ContentGuard):
    """A Base class all CertGuard implementations should derive from."""

    ca_certificate = models.TextField()

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
        except openssl.X509StoreContextError as exc:
            if exc.args[0][0] == 20:  # The error code for client cert not signed by the CA
                msg = _("Client certificate is not signed by the stored 'ca_certificate'.")
                raise PermissionError(msg)
            if exc.args[0][0] == 10:  # The error code for an expired certificate
                msg = _("Client certificate is expired.")
                raise PermissionError(msg)
            raise PermissionError(str(exc))
        except openssl.Error as exc:
            raise PermissionError(str(exc))

    class Meta:
        abstract = True


class RHSMCertGuard(BaseCertGuard):
    """
    A content-guard validating on a RHSM Certificate validated by `python-rhsm`.

    A Certificate Authority certificate to trust is required with each RHSMCertGuard created. With
    each request, the client certificate is first checked if it is signed by this CA cert. If not,
    it's untrusted and denied regardless of its paths.

    After determining the client certificate is trusted, the requested path is checked against the
    named paths in the certificate. A request is permitted if the current request path is a prefix
    of a path declared in the trusted RHSM Client Certificate.

    Fields:
        rhsm_certificate (models.TextField): The RHSM Certificate used to validate the client
            certificate at request time.
    """

    TYPE = 'rhsm'

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


class X509CertGuard(BaseCertGuard):
    """
    A content-guard that authenticates the request based on a client provided X.509 Certificate.

    Fields:
        ca_certificate (models.FileField): The CA certificate used to
            validate the client certificate.
    """

    TYPE = 'x509'

    def permit(self, request):
        """
        Validate the client cert is trusted.

        Args:
            request: The request from the user.

        Raises:
            PermissionError: If the client certificate is not trusted from the CA certificated
                stored as `ca_certificate`.
        """
        unquoted_certificate = unquote(self._get_client_cert_header(request))
        self._ensure_client_cert_is_trusted(unquoted_certificate)

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"
