Welcome to pulp-certguard's documentation!
==========================================

This is the ``pulp_certguard`` Plugin for the `Pulp Project 3.0+ <https://pypi.org/project/
pulpcore/>`__. This plugin provides X.509 certificate based content protection. The `X509CertGuard`
authenticates the web request by validating the client certificate passed in the
``X-CLIENT-CERT`` HTTP header using the CA (Certificate Authority) certificate that it has
been configured with.

.. toctree::
   :maxdepth: 2

   installation
   usage
   contributing
   yum-howto
   changes

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
