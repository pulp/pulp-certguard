from logging import getLogger
from gettext import gettext as _

from django.db import models

from OpenSSL import crypto as openssl

from pulpcore.plugin import storage
from pulpcore.plugin.models import ContentGuard


log = getLogger(__name__)


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
        validator = Validator(ca.decode('utf8'))
        validator(request)

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s"


class Validator:
    """An X.509 certificate validator."""

    SSL_CERTIFICATE_HEADER = 'SSL-CLIENT-CERTIFICATE'

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
            return openssl.load_certificate(openssl.FILETYPE_PEM, buffer=Validator.format(pem))
        except Exception as le:
            raise ValueError(str(le))

    def client_certificate(self, request):
        """Extract and load the client certificate passed in the SSL-CLIENT-CERTIFICATE header.

        Args:
            request (aiohttp.web.Request): A request for a published file.

        Returns:
            openssl.X509: The loaded certificate.

        Raises:
            KeyError: When the client certificate header has not
                been passed in the request.

        """
        name = self.SSL_CERTIFICATE_HEADER
        try:
            certificate = request.headers[name]
        except KeyError:
            reason = _('HTTP header "{h}" not found.').format(h=name)
            raise KeyError(reason)
        else:
            return Validator.load(certificate)

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
