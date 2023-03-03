=========
Changelog
=========

..
    You should *NOT* be adding new change log entries to this file, this
    file is managed by towncrier. You *may* edit previous change logs to
    fix problems like typo corrections or such.
    To add a new change log entry, please see
    https://docs.pulpproject.org/en/3.0/nightly/contributing/git.html#changelog-update

    WARNING: Don't drop the next directive!

.. towncrier release notes start

1.5.8 (2023-03-03)
==================

Bugfixes
--------

- Taught bad-certificate-failures emit warnings to the server-log.
  `#145 <https://github.com/pulp/pulp-certguard/issues/145>`__


----


1.5.7 (2023-02-03)
==================

No significant changes.


----


1.5.6 (2023-01-31)
==================

No significant changes.


----


1.5.5 (2022-08-16)
==================

No significant changes.


----


1.5.4 (2022-08-15)
==================

No significant changes.


----


1.5.3 (2022-06-23)
==================

No significant changes.


----


1.5.2 (2021-12-16)
==================

Bugfixes
--------

- Bumped pulpcore requirement for core/3.17 compatibility.
  `#9641 <https://pulp.plan.io/issues/9641>`_


----


1.5.1 (2021-10-06)
==================

Bugfixes
--------

- Bumped pulpcore requirement for core/3.16 compatibility.
  `#9494 <https://pulp.plan.io/issues/9494>`_


----


1.5.0 (2021-08-04)
==================

Deprecations and Removals
-------------------------

- Dropped support for Python 3.6 and 3.7. pulp-certguard now supports Python 3.8+.
  `#9054 <https://pulp.plan.io/issues/9054>`_


----


1.4.0 (2021-06-30)
==================

Features
--------

- Extended CertGuard.ca_certificate to accept a cert-bundle in addition to a single cert.
  `#8783 <https://pulp.plan.io/issues/8783>`_


----


1.3.0 (2021-05-19)
==================

No significant changes.


----


1.2.0 (2021-03-17)
==================

No significant changes.


----


1.1.0 (2020-12-14)
==================

- Adding version-info to `pulp_certguard.app.PulpCertGuardPluginAppConfig`.
- Making pulp-certguard compatible with pulpcore 3.9.


----

1.0.3 (2020-09-25)
==================

No significant changes. A compatibility release used to declare compatibility up to pulpcore==3.8.


----


1.0.2 (2020-08-18)
==================

No significant changes.


----


1.0.1 (2020-07-20)
==================

Bugfixes
--------

- Making pulp-certguard compatible with pulpcore 3.5
  `#7177 <https://pulp.plan.io/issues/7177>`_


----


1.0.0 (2020-07-01)
==================

No significant changes.


----


0.1.0rc5 (2020-05-22)
=====================

Features
--------

- Add support for non-urlencoded certificates to allow Apache < 2.6.10 reverse proxies to also work.
  `#6574 <https://pulp.plan.io/issues/6574>`_


Bugfixes
--------

- RHSMCertGuard now only checks for authorized URLs in the client cert against the
  ``Distribution.base_path`` and disincludes the ``settings.CONTENT_PATH_PREFIX``, e.g.
  ``/pulp/content/``
  `#6694 <https://pulp.plan.io/issues/6694>`_


Improved Documentation
----------------------

- Adds docs on configuring Apache 2.6.10+ and < 2.6.10 docs, which need different configs.
  `#6574 <https://pulp.plan.io/issues/6574>`_
- Adds documentation on RHSM path checking with examples. Also adds a debugging section on inspecting
  RHSM certificates with the ``rct`` command.
  `#6694 <https://pulp.plan.io/issues/6694>`_
- Adds debugging documentation on how users can enable, use, and interpret the debugging logging.
  `#6744 <https://pulp.plan.io/issues/6744>`_


----


0.1.0rc4 (2020-04-22)
=====================

Features
--------

- Adds RHSMCertGuard which offers both content protection and path-based entitlement checking.
  `#4664 <https://pulp.plan.io/issues/4664>`_
- Make repositories "typed". Repositories now live at a detail endpoint. Sync is performed by POSTing to {repo_href}/sync/ remote={remote_href}.
  `#5625 <https://pulp.plan.io/issues/5625>`_
- ``X509CertGuard.ca_certificate`` is now stored in the database and not on the filesystem.
  `#6352 <https://pulp.plan.io/issues/6352>`_


Improved Documentation
----------------------

- Adds documentation on how authorization checking works and that there are two types of Certguards
  now.
  `#4664 <https://pulp.plan.io/issues/4664>`_
- Move documentation from README.md to sphinx site to show on https://pulp-certguard.readthedocs.io/
  `#6298 <https://pulp.plan.io/issues/6298>`_
- Total rewrite of the documentation with tested reverse proxy examples, X509 Cert Guard usage, and
  RHSM Cert Guard usage.
  `#6445 <https://pulp.plan.io/issues/6445>`_
- Adds notes to docs that to use RHSMCertGuard you have to install `rhsm` Python module.
  `#6546 <https://pulp.plan.io/issues/6546>`_


Deprecations and Removals
-------------------------

- Renames the ``SSL_CLIENT_CERTIFICATE`` to be ``X-CLIENT-CERT``.
  `#4891 <https://pulp.plan.io/issues/4891>`_
- Change `_id`, `_created`, `_last_updated`, `_href` to `pulp_id`, `pulp_created`, `pulp_last_updated`, `pulp_href`
  `#5457 <https://pulp.plan.io/issues/5457>`_
- Sync is no longer available at the {remote_href}/sync/ repository={repo_href} endpoint.
  `#5625 <https://pulp.plan.io/issues/5625>`_
- Migrations had to be regenerated from scratch due to a backwards incompatible change where
  ``X509ContentGuard.ca_certificate`` is now stored in the database and not on the filesystem. Users
  who have already run migrations will need to drop the ``RHSMCertGuard`` and ``X509CertGuard`` tables
  manually from their databases, reapply migrations, and re-create their CertGuard objects.

  Also the submission of the client cert to the content app occurs via the `X-CLIENT-CERT` header, and
  is expected to be urlencoded.
  `#6352 <https://pulp.plan.io/issues/6352>`_


Misc
----

- `#6105 <https://pulp.plan.io/issues/6105>`_, `#6296 <https://pulp.plan.io/issues/6296>`_, `#6424 <https://pulp.plan.io/issues/6424>`_, `#6545 <https://pulp.plan.io/issues/6545>`_


----


0.1.0rc2 (2019-09-20)
=====================

Improved Documentation
----------------------

- Switch to using `towncrier <https://github.com/hawkowl/towncrier>`_ for better release notes.
  `#4875 <https://pulp.plan.io/issues/4875>`_


Misc
----

- `#4681 <https://pulp.plan.io/issues/4681>`_

