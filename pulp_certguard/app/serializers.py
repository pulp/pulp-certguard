from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin.serializers import ContentGuardSerializer

from .models import X509CertGuard, X509Validator


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
