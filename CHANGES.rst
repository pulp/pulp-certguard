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

