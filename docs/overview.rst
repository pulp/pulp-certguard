========
Overview
========


Example Usage
-------------

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
