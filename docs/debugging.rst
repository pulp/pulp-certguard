Debugging
=========

``pulp-certguard`` contains debug statements which show the raw, received value of the
``X-CLIENT-CERT`` header. This can be very valuable when debugging where the problem is in the chain
of certificates from the::

    client <--> reverse proxy <--> pulp-certguard

Enabling Debugging
------------------

Debugging is most easily enabled by adding the following line to your settings file, which is
by default located at ``/etc/pulp/settings.py``::

    LOGGING = {"dynaconf_merge": True, "loggers": {'': {'handlers': ['console'], 'level': 'DEBUG'}}}

After restarting your server-side services and making a request that sets the ``X-CLIENT-CERT``
header, you should see a log message for each request where pulp-certguard is receiving a
``X-CLIENT-CERT`` header.

Using Logging Info
------------------

If you make a request but do not see a log message, you could have one of the following problems:

1. Debug logging is not enabled or applied. Check your ``LOGGING`` config.

2. The client is not requesting content from a Distribution protected with ``pulp-certguard``. Check
   your ``Distribution`` configuration.

3. The reverse proxy isn't configured to pass along the ``X-CLIENT-CERT`` config correctly. Check
   your reverse proxy config against the example configs documented on this site.


If you do see a log message, but it's still not working you could have one of the following
problems:

1. The client isn't submitting the client certificate correctly to the reverse proxy. Ensure the
   client is submitting a certificate and key via TLS to the reverse proxy.

2. The reverse proxy configuration is not correct. Compare your reverse proxy config against the
   example configs documented on this site.
