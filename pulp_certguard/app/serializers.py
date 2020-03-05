from gettext import gettext as _

from OpenSSL import crypto as openssl

from pulpcore.plugin.serializers import ContentGuardSerializer

from rest_framework import serializers

from pulp_certguard.app.utils import get_rhsm
from .models import RHSMCertGuard, X509CertGuard, X509Validator


class RHSMCertGuardSerializer(ContentGuardSerializer):
    """RHSM Content Guard Serializer."""

    ca_certificate = serializers.CharField(
        help_text=_("The Certificate Authority (CA) certificate."),
    )

    class Meta:
        model = RHSMCertGuard
        fields = ContentGuardSerializer.Meta.fields + (
            'ca_certificate',
        )

    @staticmethod
    def validate_ca_certificate(ca_certificate):
        """Validates the given certificate."""
        get_rhsm()  # Validate that rhsm is installed
        try:
            openssl.load_certificate(openssl.FILETYPE_PEM, buffer=ca_certificate)
        except ValueError:
            reason = _('Must be PEM encoded X.509 certificate.')
            raise serializers.ValidationError(reason)
        else:
            return ca_certificate


class X509CertGuardSerializer(ContentGuardSerializer):
    """X.509 Content Guard Serializer."""

    ca_certificate = serializers.FileField(
        help_text=_("The Certificate Authority certificate."),
        write_only=True
    )

    class Meta:
        model = X509CertGuard
        fields = ContentGuardSerializer.Meta.fields + (
            'ca_certificate',
        )

    @staticmethod
    def validate_ca_certificate(certificate):
        """Validates the given certificate."""
        buffer = certificate.read()
        try:
            X509Validator.load(buffer.decode('utf8'))
        except ValueError:
            reason = _("Must be PEM encoded X.509 certificate.")
            raise serializers.ValidationError(reason)
        else:
            return certificate
