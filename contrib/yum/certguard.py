#!/usr/bin/python
#
# This code is contribued to and licencensed under the terms of the
# pulp-certguard project as a whole.
#
# The original author officially turns over all licensing rights to
# the pulp project/maintainers.


from contextlib import closing
from yum.plugins import TYPE_CORE

requires_api_version = '2.3'
plugin_type = (TYPE_CORE,)

ID_SSL_HEADER = "X-CLIENT-CERT"
CERT_PATH = "/etc/boomi/yum.pem"
# Repos that begin with this prefix will be handled by this plugin
REPO_PREFIX = "boomi-"


def init_hook(conduit):
    """Plugin initialization hook.

    For each boomi repo, replace yum's representation of the repo with
    a subclass that adds in the necessary headers.

    """
    # Only process boomi repos
    repos = conduit.getRepos()
    boomi_repos = repos.findRepos(REPO_PREFIX)

    # Retrieve the Amazon metadata
    id_cert = _load_cert()

    if id_cert:
        # Add the headers to all BOOMI repos
        for repo in boomi_repos:
            repo.http_headers[ID_SSL_HEADER] = id_cert


def _load_cert():
    """Loads and returns the certificate.

    @rtype: string
    """
    with closing(open(CERT_PATH, 'r')) as fd:
        id_doc = fd.read()
    # Newlines in http headers aren't valid
    return id_doc.replace("\n", "")
