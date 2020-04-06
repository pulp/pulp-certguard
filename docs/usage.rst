Usage
=====


The REST API typically requires Basic Authentication. To use the examples in this section, the
following assumptions are made:

1. The `httpie <https://httpie.org/doc>`_ command is available to perform the requests.

2. A ``.netrc`` file configured with the username, password, and host of your Pulp server. See the
   `httpie .netrc docs <https://httpie.org/doc#netrc>`_ for more information on setting that.

3. The `jq library <https://stedolan.github.io/jq/>`_ is available to easily parse responses.


Pre-Setup
---------

To meaningfully use pulp-certguard you should already have a Pulp Distribution that requires
authorization and ideally it should have content in it. These examples assume you have `pulp_file
<https://pulp-file.readthedocs.io/en/latest/>`_ installed with a ``FileRepository`` with at least
one ``RepositoryVersion`` with content in it. Also you'll need a ``FileDistribution`` serving that
``RepositoryVersion``. Below are links to instructions on how to create those objects.

The pulp-certguard examples should be straightforward to port to protect another distribution type.


Create a pulp_file repository, and sync some basic content into it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is about creating some data to test with. The significant thing for pulp-certguard is
having a repository to protect and having some content in that repository to test against.

1. `Create a FileRepository <https://pulp-file.readthedocs.io/en/latest/workflows/sync.html#create-a-repository-foo>`_
2. `Create a FileRemote <https://pulp-file.readthedocs.io/en/latest/workflows/sync.html#create-a-new-remote-bar>`_
3. `Sync the repository to receive some test content <https://pulp-file.readthedocs.io/en/latest/workflows/sync.html#sync-repository-foo-using-remote-bar>`_
4. `Create a FilePublication <https://pulp-file.readthedocs.io/en/latest/workflows/publish-host.html#create-a-publication>`_
5. `Create a FileDistribution to serve the FilePublication <https://pulp-file.readthedocs.io/en/latest/workflows/publish-host.html#create-a-distribution-for-the-publication>`_

The examples below assume the Distribution href is saved to the bash variable ``DISTRIBUTION_HREF``
for example::

    $ echo $DISTRIBUTION_HREF
    /pulp/api/v3/distributions/file/file/efc690a5-7e29-4fe5-8c48-9fef7727223f/


X509 CertGuard
--------------

Create a content guard
~~~~~~~~~~~~~~~~~~~~~~

This example assumes that ``~/ca.pem`` is a PEM encoded Certificate Authority (CA) certificate. Each
X509 Content Guard needs a name so for this example we'll use ``myguard``.

``$ http POST http://localhost/pulp/api/v3/contentguards/certguard/x509/ name=myguard ca_certificate=@~/ca.pem``

.. code:: json

   {
       "pulp_href": "/pulp/api/v3/contentguards/certguard/x509/2432b932-a057-43ec-ba20-391bd99f943f/",
   }

``$ export X509_GUARD_HREF=$(http localhost/pulp/api/v3/contentguards/certguard/x509/?name=myguard | jq -r '.results[0].pulp_href')``


Protect the Distribution with the X509CertGuard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``$ http PATCH localhost$DISTRIBUTION_HREF content_guard=${X509_GUARD_HREF}``

.. code:: json

   {
       "pulp_href": "/pulp/api/v3/distributions/305adfe0-4851-432f-9de3-13f9b10fe131/"
   }


Download ``protected`` content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example assume the client will connect to the reverse proxy using TLS with the
following:

* The PEM encoded client certificate is stored at ``~/client.pem`` which is signed by the CA stored
  on the X509CertGuard.
* The corresponding PEM encoded private key at ``~/key.pem``.

It attempts to download the ``test.iso`` file from the FileDistribution at the path
``/pulp/content/somepath/`` Note the ``somepath`` part of this is from the ``base_url`` of the
Distribution you are testing against.

For example with httpie you can submit the client cert and key via TLS using:

``$ http --cert ~/client.pem --cert-key ~/key.pem https://localhost/pulp/content/somepath/test.iso``

This is expected to yield binary data with a response like::

    HTTP/1.1 200 OK
    Accept-Ranges: bytes
    Connection: keep-alive
    Content-Length: 3145728
    Content-Type: application/octet-stream
    Date: Tue, 21 Apr 2020 20:35:11 GMT
    Last-Modified: Tue, 21 Apr 2020 19:23:06 GMT
    Server: nginx/1.16.1



    +-----------------------------------------+
    | NOTE: binary data not shown in terminal |
    +-----------------------------------------+


RHSM CertGuard
--------------

Create a content guard
~~~~~~~~~~~~~~~~~~~~~~

This example assumes that ``~/ca.pem`` is a PEM encoded Certificate Authority (CA) certificate. Each
RHSM Content Guard needs a name so for this example we'll use ``myguard``.

``$ http POST http://localhost/pulp/api/v3/contentguards/certguard/rhsm/ name=myguard ca_certificate=@~/ca.pem``

.. code:: json

   {
       "pulp_href": "/pulp/api/v3/contentguards/certguard/rhsm/302971d1-48a9-439f-a6a9-052e33f75733/",
   }

``$ export RHSM_GUARD_HREF=$(http localhost/pulp/api/v3/contentguards/certguard/rhsm/?name=myguard | jq -r '.results[0].pulp_href')``


Protect the Distribution with the RHSMCertGuard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``$ http PATCH localhost$DISTRIBUTION_HREF content_guard=${RHSM_GUARD_HREF}``

.. code:: json

   {
       "pulp_href": "/pulp/api/v3/distributions/335ccd96-d8ca-4d07-8c2e-e45eda6b18ba/"
   }


Download ``protected`` content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example assume the client will connect to the reverse proxy using TLS with the
following:

* The PEM encoded, RHSM client certificate is stored at ``~/client.pem`` which is signed by the CA
  stored on the RHSMCertGuard.
* The corresponding PEM encoded private key at ``~/key.pem``.

It attempts to download the ``test.iso`` file from the FileDistribution at the path
``/pulp/content/somepath/`` Note the ``somepath`` part of this is from the ``base_url`` of the
Distribution you are testing against.

.. note::

    If the RHSM client cert contains entitlement paths, they must match the full path to the
    Distribution the client is fetching from. In this example that is ``/pulp/content/somepath/``.

For example with httpie you can submit the client cert and key via TLS using:

``$ http --cert ~/client.pem --cert-key ~/key.pem https://localhost/pulp/content/somepath/test.iso``

This is expected to yield binary data with a response like::

    HTTP/1.1 200 OK
    Accept-Ranges: bytes
    Connection: keep-alive
    Content-Length: 3145728
    Content-Type: application/octet-stream
    Date: Tue, 21 Apr 2020 20:35:11 GMT
    Last-Modified: Tue, 21 Apr 2020 19:23:06 GMT
    Server: nginx/1.16.1



    +-----------------------------------------+
    | NOTE: binary data not shown in terminal |
    +-----------------------------------------+
