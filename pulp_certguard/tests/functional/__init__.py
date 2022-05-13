import uuid
import pytest

try:
    from pulpcore.client.pulp_certguard import (
        ApiClient,
        ContentguardsX509Api,
        ContentguardsRhsmApi,
    )
except ImportError:
    pass
else:
    @pytest.fixture
    def cid():
        """A correlation-id unique to the test."""
        return str(uuid.uuid4())

    @pytest.fixture
    def pulp_certguard_client(cid, bindings_cfg):
        """Api client for certguards."""
        api_client = ApiClient(bindings_cfg)
        api_client.default_headers["Correlation-ID"] = cid
        return api_client

    @pytest.fixture
    def x509_content_guards_api_client(pulp_certguard_client):
        """Api for x509 content guards."""
        return ContentguardsX509Api(pulp_certguard_client)

    @pytest.fixture
    def rhsm_content_guards_api_client(pulp_certguard_client):
        """Api for rhsm content guards."""
        return ContentguardsRhsmApi(pulp_certguard_client)
