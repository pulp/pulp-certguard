pulp-certguard
==============

.. warning:: This pulp plugin has been merged into the main pulpcore project.
   This repository can only accept bugfixes on release branches.

.. figure:: https://github.com/pulp/pulp-certguard/actions/workflows/nightly.yml/badge.svg?branch=main
   :alt: Certguard Nightly CI/CD

A Pulp plugin that provides an X.509 capable ``ContentGuard`` for pulpcore. Instances of
``X509CertGuard`` are useful for requiring clients to submit a certificate proving their entitlement
to content before receiving the content.

For more information, please see the `documentation <https://docs.pulpproject.org/pulp_certguard>`_
or the `Pulp project page <https://pulpproject.org>`_.

Development moved to Pulpcore
-----------------------------

Since this plugin has been moved to pulpcore, issues can no longer be reported here. Please go to
`Pulpcore - Issues <https://github.com/pulp/pulpcore/issues>`_ instead.
Any issues that arise should also be solved there first and if needed backported here.
