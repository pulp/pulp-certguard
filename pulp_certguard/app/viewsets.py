from pulpcore.plugin.viewsets import ContentGuardFilter, ContentGuardViewSet

from .models import CertGuard
from .serializers import CertGuardSerializer


class CertGuardViewSet(ContentGuardViewSet):
    endpoint_name = 'certguard'
    queryset = CertGuard.objects.all()
    serializer_class = CertGuardSerializer
    filterset_class = ContentGuardFilter
