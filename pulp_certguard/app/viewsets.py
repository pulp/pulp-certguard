from pulpcore.plugin.viewsets import ContentGuardFilter, ContentGuardViewSet

from .models import X509CertGuard
from .serializers import CertGuardSerializer


class CertGuardViewSet(ContentGuardViewSet):
    """X509CertGuard API Viewsets."""

    endpoint_name = 'x509'
    queryset = X509CertGuard.objects.all()
    serializer_class = CertGuardSerializer
    filterset_class = ContentGuardFilter
