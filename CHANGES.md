# Changelog

[//]: # (You should *NOT* be adding new change log entries to this file, this)
[//]: # (file is managed by towncrier. You *may* edit previous change logs to)
[//]: # (fix problems like typo corrections or such.)
[//]: # (To add a new change log entry, please see the contributing docs.)
[//]: # (WARNING: Don't drop the towncrier directive!)

[//]: # (towncrier release notes start)

## 1.7.2 (2024-07-23) {: #1.7.2 }


No significant changes.

---

## 1.7.1 (2023-11-03) {: #1.7.1 }

### Features

-   Declared pulpcore compatibility up to 3.44.

---

## 1.7.0 (2023-10-19) {: #1.7.0 }

### Bugfixes

-   Allows for compatibility with pulpcore>3.25.
    [#252](https://github.com/pulp/pulp-certguard/issues/252)
-   Loosened restriction on pyOpenSSL to let us use 23.0 and its fixes.
    [#293](https://github.com/pulp/pulp-certguard/issues/293)

---

## 1.6.6 (2023-10-17) {: #1.6.6 }

### Bugfixes

-   Loosened restriction on pyOpenSSL to let us use 23.0 and its fixes.
    [#293](https://github.com/pulp/pulp-certguard/issues/293)

---

## 1.6.5 (2023-05-11) {: #1.6.5 }

No significant changes.

---

## 1.6.4 (2023-05-04) {: #1.6.4 }

No significant changes.

---

## 1.6.3 (2023-05-02) {: #1.6.3 }

### Bugfixes

-   Allows for compatibility with pulpcore>3.25.
    [#252](https://github.com/pulp/pulp-certguard/issues/252)

---

## 1.6.2 (2023-05-02) {: #1.6.2 }

No significant changes.

---

## 1.6.1 (2023-03-23) {: #1.6.1 }

No significant changes.

---

## 1.6.0 (2023-03-14) {: #1.6.0 }

### Bugfixes

-   Taught bad-certificate-failures emit warnings to the server-log.
    [#145](https://github.com/pulp/pulp-certguard/issues/145)
-   Improved the validation of certificates.
    [#232](https://github.com/pulp/pulp-certguard/issues/232)

---

## 1.5.9 (2023-10-17) {: #1.5.9 }

### Bugfixes

-   Loosened restriction on pyOpenSSL to let us use 23.0 and its fixes.
    [#293](https://github.com/pulp/pulp-certguard/issues/293)

---

## 1.5.8 (2023-03-03) {: #1.5.8 }

### Bugfixes

-   Taught bad-certificate-failures emit warnings to the server-log.
    [#145](https://github.com/pulp/pulp-certguard/issues/145)

---

## 1.5.7 (2023-02-03) {: #1.5.7 }

No significant changes.

---

## 1.5.6 (2023-01-31) {: #1.5.6 }

No significant changes.

---

## 1.5.5 (2022-08-16) {: #1.5.5 }

No significant changes.

---

## 1.5.4 (2022-08-15) {: #1.5.4 }

No significant changes.

---

## 1.5.3 (2022-06-23) {: #1.5.3 }

No significant changes.

---

## 1.5.2 (2021-12-16) {: #1.5.2 }

### Bugfixes

-   Bumped pulpcore requirement for core/3.17 compatibility.
    [#9641](https://pulp.plan.io/issues/9641)

---

## 1.5.1 (2021-10-06) {: #1.5.1 }

### Bugfixes

-   Bumped pulpcore requirement for core/3.16 compatibility.
    [#9494](https://pulp.plan.io/issues/9494)

---

## 1.5.0 (2021-08-04) {: #1.5.0 }

### Deprecations and Removals

-   Dropped support for Python 3.6 and 3.7. pulp-certguard now supports Python 3.8+.
    [#9054](https://pulp.plan.io/issues/9054)

---

## 1.4.0 (2021-06-30) {: #1.4.0 }

### Features

-   Extended CertGuard.ca_certificate to accept a cert-bundle in addition to a single cert.
    [#8783](https://pulp.plan.io/issues/8783)

---

## 1.3.0 (2021-05-19) {: #1.3.0 }

No significant changes.

---

## 1.2.0 (2021-03-17) {: #1.2.0 }

No significant changes.

---

## 1.1.0 (2020-12-14) {: #1.1.0 }

-   Adding version-info to pulp_certguard.app.PulpCertGuardPluginAppConfig.
-   Making pulp-certguard compatible with pulpcore 3.9.

---

## 1.0.3 (2020-09-25) {: #1.0.3 }

No significant changes. A compatibility release used to declare compatibility up to pulpcore==3.8.

---

## 1.0.2 (2020-08-18) {: #1.0.2 }

No significant changes.

---

## 1.0.1 (2020-07-20) {: #1.0.1 }

### Bugfixes

-   Making pulp-certguard compatible with pulpcore 3.5
    [#7177](https://pulp.plan.io/issues/7177)

---

## 1.0.0 (2020-07-01) {: #1.0.0 }

No significant changes.

---

## 0.1.0rc5 (2020-05-22)

### Features

-   Add support for non-urlencoded certificates to allow Apache < 2.6.10 reverse proxies to also work.
    [#6574](https://pulp.plan.io/issues/6574)

### Bugfixes

-   RHSMCertGuard now only checks for authorized URLs in the client cert against the
    `Distribution.base_path` and disincludes the `settings.CONTENT_PATH_PREFIX`, e.g.
    `/pulp/content/`
    [#6694](https://pulp.plan.io/issues/6694)

### Improved Documentation

-   Adds docs on configuring Apache 2.6.10+ and < 2.6.10 docs, which need different configs.
    [#6574](https://pulp.plan.io/issues/6574)
-   Adds documentation on RHSM path checking with examples. Also adds a debugging section on inspecting
    RHSM certificates with the `rct` command.
    [#6694](https://pulp.plan.io/issues/6694)
-   Adds debugging documentation on how users can enable, use, and interpret the debugging logging.
    [#6744](https://pulp.plan.io/issues/6744)

---

## 0.1.0rc4 (2020-04-22)

### Features

-   Adds RHSMCertGuard which offers both content protection and path-based entitlement checking.
    [#4664](https://pulp.plan.io/issues/4664)
-   Make repositories "typed". Repositories now live at a detail endpoint. Sync is performed by POSTing to {repo_href}/sync/ remote={remote_href}.
    [#5625](https://pulp.plan.io/issues/5625)
-   `X509CertGuard.ca_certificate` is now stored in the database and not on the filesystem.
    [#6352](https://pulp.plan.io/issues/6352)

### Improved Documentation

-   Adds documentation on how authorization checking works and that there are two types of Certguards
    now.
    [#4664](https://pulp.plan.io/issues/4664)
-   Move documentation from README.md to sphinx site to show on <https://pulp-certguard.readthedocs.io/>
    [#6298](https://pulp.plan.io/issues/6298)
-   Total rewrite of the documentation with tested reverse proxy examples, X509 Cert Guard usage, and
    RHSM Cert Guard usage.
    [#6445](https://pulp.plan.io/issues/6445)
-   Adds notes to docs that to use RHSMCertGuard you have to install rhsm Python module.
    [#6546](https://pulp.plan.io/issues/6546)

### Deprecations and Removals

-   Renames the `SSL_CLIENT_CERTIFICATE` to be `X-CLIENT-CERT`.
    [#4891](https://pulp.plan.io/issues/4891)

-   Change _id, _created, _last_updated, _href to pulp_id, pulp_created, pulp_last_updated, pulp_href
    [#5457](https://pulp.plan.io/issues/5457)

-   Sync is no longer available at the {remote_href}/sync/ repository={repo_href} endpoint.
    [#5625](https://pulp.plan.io/issues/5625)

-   Migrations had to be regenerated from scratch due to a backwards incompatible change where
    `X509ContentGuard.ca_certificate` is now stored in the database and not on the filesystem. Users
    who have already run migrations will need to drop the `RHSMCertGuard` and `X509CertGuard` tables
    manually from their databases, reapply migrations, and re-create their CertGuard objects.

    Also the submission of the client cert to the content app occurs via the X-CLIENT-CERT header, and
    is expected to be urlencoded.
    [#6352](https://pulp.plan.io/issues/6352)

### Misc

-   [#6105](https://pulp.plan.io/issues/6105), [#6296](https://pulp.plan.io/issues/6296), [#6424](https://pulp.plan.io/issues/6424), [#6545](https://pulp.plan.io/issues/6545)

---

## 0.1.0rc2 (2019-09-20)

### Improved Documentation

-   Switch to using [towncrier](https://github.com/hawkowl/towncrier) for better release notes.
    [#4875](https://pulp.plan.io/issues/4875)

### Misc

-   [#4681](https://pulp.plan.io/issues/4681)
