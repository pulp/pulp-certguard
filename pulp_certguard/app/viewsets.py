from pulpcore.plugin.viewsets import ContentGuardFilter, ContentGuardViewSet

from .models import CertGuard
from .serializers import CertGuardSerializer


class CertGuardViewSet(ContentGuardViewSet):
    """CertGuard API Viewsets."""

    endpoint_name = 'x509'
    queryset = CertGuard.objects.all()
    serializer_class = CertGuardSerializer
    filterset_class = ContentGuardFilter
