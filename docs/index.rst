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


Presenting a Client Certificate
-------------------------------

The presentation of the client certificate should be done using TLS so the client can prove it not
only has the certificate but also the key for that certificate. This TLS connection terminates at
the reverse proxy, e.g. Nginx or Apache, and the client certificate is then forwarded to the
``pulpcore-content`` app for Authorization checking. The forwarded certificate is expected to be
delivered to ``pulpcore-content`` as a urlencoded version of the client certificate stored in the
``X-CLIENT-CERT`` HTTP header. Here's a diagram of the call flow:

client <-- TLS --> Nginx <-- X-CLIENT-CERT header --> pulpcore-content

.. note::

    The ``X-CLIENT-CERT`` header needs to be urlencoded because newline characters present in valid
    client certificates are not allowed in headers.


Authorization
-------------

Any client presenting an X.509 or RHSM based certificate at request time will be authorized if and
only if the client cert is unexpired and signed by stored Certificate Authority Certificate stored
on the Certguard when it was created.

This allows for a use case where multiple Certificate Authority Certificates can be used to allow
some Pulp Distributions to be give access to some clients but not others depending on which CA Cert
signed the client certificate. While that is useful, it can become unwieldy to have to also manage
many CA Certificates. To resolve this an optional, additional authorization mechanism is available
where paths to Pulp Distributions are contained in the certificate itself.


Path Based Authorization
------------------------

.. warning::

    At this time only the RHSM Cert Guard provides path based authorization.

RHSM Certificates allow for the embedding of Distribution paths within them. If they are present in
a client certificate, in addition to the authorization requirements from above, the client will be
granted access if and only if the requested path is a subpath of a path contained in the client
certificate.


RHSM vs X.509 Cert Guards
-------------------------

pulp_certguard has two types of Cert Guards, the X509CertGuard and the RHSMCertGuard. Both are X.509
certificates, but the X509CertGuard can be made using common openssl tools, while RHSM Certificates
can only be made using `python-rhsm <https://pypi.org/project/rhsm/>`_.


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
