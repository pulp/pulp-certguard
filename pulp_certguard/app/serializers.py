from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin.serializers import ContentGuardSerializer

from .models import X509CertGuard, Validator


class CertGuardSerializer(ContentGuardSerializer):
    """Content Guard Serializer."""

    ca_certificate = serializers.FileField(
        help_text="The Certificate Authority (CA) certificate.",
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
            Validator.load(buffer.decode('utf8'))
        except ValueError:
            reason = _('Must be PEM encoded X.509 certificate.')
            raise serializers.ValidationError(reason)
        else:
            return certificate
