Welcome to pulp-certguard's documentation!
==========================================

The ``pulp_certguard`` plugin for `pulpcore 3.0+ <https://pypi.org/project/pulpcore/>`_ can cause
Pulp to refuse to serve content, e.g. rpms, Ansible Collections, etc, unless clients present a
valid certificate when they fetch content.

Example
-------

Company Foo only wants to serve rpms to customers who have paid, and they use Pulp 3.0+ to store
rpms for their customers. When a customer pays through, e.g. June 30, 2023, Company Foo generates
the customer a certificate signed by the certificate authority of Company Foo with an expiration
date of June 30, 2023. Company Foo also does the following:

1. Creates either a X.509 or RHSM Cert Guard offered by this plugin, configured with the Certificate
   Authority Certificate used to sign the customer certificates.

2. Configures one or more Pulp Distributions which serving rpm repositories to be protected by the
   X.509 or RHSM Cert Guard they created


.. toctree::
   :maxdepth: 2

   overview
   installation
   reverse_proxy_config
   usage
   rest_api
   contributing
   yum-howto
   changes

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
