``pulp_certguard`` Plugin
=========================

This is the ``pulp_certguard`` Plugin for the
`Pulp Project 3.0+ <https://pypi.org/project/pulpcore/>`__. This plugin provides X.509 certificate
based content protection. The `X509CertGuard` authenticates the web request by validating the client
certificate passed in the ``SSL_CLIENT_CERTIFICATE`` HTTP header using the CA (Certificate
Authority) certificate that it has been configured with.

All REST API examples bellow use `httpie <https://httpie.org/doc>`__ to perform the requests.
The ``httpie`` commands below assume that the user executing the commands has a ``.netrc`` file
in the home directory. The ``~/.netrc`` should have the following configuration:

.. code-block::

   machine localhost
   login admin
   password admin

If you configured the ``admin`` user with a different password, adjust the configuration
accordingly. If you prefer to specify the username and password with each request, please see
``httpie`` documentation on how to do that.

This documentation makes use of the `jq library <https://stedolan.github.io/jq/>`_
to parse the json received from requests, in order to get the unique urls generated
when objects are created. To follow this documentation as-is please install the jq
library with:

``$ sudo dnf install jq``

Install ``pulpcore``
--------------------

Follow the `installation
instructions <https://docs.pulpproject.org/en/3.0/nightly/installation/instructions.html>`__
provided with pulpcore.

Users should install from **either** PyPI or source.

Install ``pulp-certguard`` from source
--------------------------------------

.. code-block:: bash

   source ~/pulpvenv/bin/activate
   git clone https://github.com/pulp/pulp-certguard.git
   cd pulp-certguard
   pip install -e .

Install ``pulp-certguard`` From PyPI
------------------------------------

.. code-block:: bash

   source ~/pulpvenv/bin/activate
   pip install pulp-certguard

Make and Run Migrations
-----------------------

.. code-block:: bash

   django-admin makemigrations certguard
   django-admin migrate certguard


Create a content guard named ``foo``
------------------------------------

This example assumes that ``~/ca.pem`` is a PEM encoded CA certificate.

``$ http --form POST http://localhost:24817/pulp/api/v3/contentguards/certguard/x509/ name=foo ca_certificate@~/ca.pem``

.. code:: json

   {
       ...
       "_href": "/pulp/api/v3/contentguards/certguard/x509/3046291f-d432-4a85-9d7e-fad12b0aaed7/",
       ...
   }

``$ export GUARD_HREF=$(http localhost:24817/pulp/api/v3/contentguards/certguard/x509/?name=foo | jq -r '.results[0]._href')``


Create a distribution with content protection
---------------------------------------------

`` $ http POST http://localhost:24817/pulp/api/v3/distributions/ name=bar base_path=files content_guard=${GUARD_HREF}``

.. code:: json

   {
       ...
       "_href": "/pulp/api/v3/distributions/305adfe0-4851-432f-9de3-13f9b10fe131/"
       ...
   }


Add content protection to an existing distribution
--------------------------------------------------

`` $ http PATCH http://localhost:24817/pulp/api/v3/distributions/1/ content_guard=${GUARD_HREF}``

.. code:: json

   {
       ...
       "_href": "/pulp/api/v3/distributions/0fbb102a-cb38-4d5c-afc2-b9a76e862a1d/"
       ...
   }


Download ``protected`` content
------------------------------

The following examples assume there is a file named ``1.iso`` published under the ``files`` distribution.
Further, they assume there is a PEM encoded client certificate at ``~/client.pem`` signed by the CA at ``~/ca.pem``.
And, a PEM encoded private key at ``~/key.pem``.


Example of GET directly to the content application running on port 24816 over HTTP. When setting the
``SSL-CLIENT-CERTIFICATE`` manually, the newlines need to be stripped due to restrictions
on legal characters in HTTP header values.

``$ http localhost:24816/pulp/content/files/1.iso SSL-CLIENT-CERTIFICATE:"$(tr -d '\n' < ~/client.pem)"``

.. code-block::

   +-----------------------------------------+
   | NOTE: binary data not shown in terminal |
   +-----------------------------------------+


Example of GET through a reverse proxy using HTTPS (like apache or nginx) in front of the content
application. It's assumed that the reverse proxy has been configured to set the SSL-CLIENT-CERTIFICATE
header using the client certificate exchanged as part of the SSL negotiation.

``$ http https://localhost/pulp/content/files/1.iso --cert=~/client.pem --cert-key=~/key.pem --verify=no``

.. code-block::

   +-----------------------------------------+
   | NOTE: binary data not shown in terminal |
   +-----------------------------------------+
