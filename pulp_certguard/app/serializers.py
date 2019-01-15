from gettext import gettext as _

from rest_framework import serializers

from pulpcore.plugin.serializers import ContentGuardSerializer

from .models import CertGuard, Validator


class CertGuardSerializer(ContentGuardSerializer):
    ca_certificate = serializers.FileField(
        help_text="The Certificate Authority (CA) certificate.",
        write_only=True
    )

    class Meta:
        model = CertGuard
        validators = [

        ]
        fields = ContentGuardSerializer.Meta.fields + (
            'ca_certificate',
        )

    @staticmethod
    def validate_ca_certificate(certificate):
        buffer = certificate.read()
        try:
            Validator.load(buffer.decode('utf8'))
        except ValueError:
            reason = _('Must be PEM encoded x.509 certificate.')
            raise serializers.ValidationError(reason)
