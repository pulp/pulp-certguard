============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:


Types of Contributions
----------------------


Report Bugs
~~~~~~~~~~~

Report bugs at https://pulp.plan.io/projects/certguard/issues/new.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.


Fix Bugs
~~~~~~~~

Look through the Redmine open issues:  https://tinyurl.com/y6mjcpvm


Implement Features
~~~~~~~~~~~~~~~~~~

Look through the Redmine Stories for features:  https://tinyurl.com/y35w3wxu


Write Documentation
~~~~~~~~~~~~~~~~~~~

pulp-certguard could always use more documentation, whether as part of the
official pulp-certguard docs, in docstrings, or even on the web in blog posts,
articles, and such.


Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://pulp.plan.io/projects/certguard/issues/new.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Get Started!
------------

Ready to contribute? Here's how to set up `pulp_certguard` for local development.

1. Fork the `pulp_certguard` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pulp_certguard.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv pulp_certguard
    $ cd pulp_certguard/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, add a :ref:`changelog update <changelog-update>`.

6. Check that your changes pass flake8 and the tests, including testing other Python versions with
   tox::

    $ flake8 pulp_certguard tests
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add a
   :ref:`changelog update <changelog-update>`

3. The pull request should work for Python 3.6 and 3.6 and both PostgreSQL and MaridDB.


.. _changelog-update:

Changelog update
----------------

The CHANGES.rst file is managed using the `towncrier tool <https://github.com/hawkowl/towncrier>`_
and all non trivial changes must be accompanied by a news entry.

To add an entry to the news file, you first need an issue in pulp.plan.io describing the change you
want to make. Once you have an issue, take its number and create a file inside of the ``CHANGES/``
directory named after that issue number with an extension of .feature, .bugfix, .doc, .removal, or
.misc. So if your issue is 3543 and it fixes a bug, you would create the file
``CHANGES/3543.bugfix``.

PRs can span multiple categories by creating multiple files (for instance, if you added a feature
and deprecated an old feature at the same time, you would create CHANGES/NNNN.feature and
CHANGES/NNNN.removal). Likewise if a PR touches multiple issues/PRs you may create a file for each
of them with the exact same contents and Towncrier will deduplicate them.

The contents of this file are reStructuredText formatted text that will be used as the content of
the news file entry. You do not need to reference the issue or PR numbers here as towncrier will
automatically add a reference to all of the affected issues when rendering the news file.


Tips
----

To run a subset of tests::

$ py.test tests.test_pulp_certguard


Deploying
---------

A reminder for the maintainers on how to deploy.

Use the ``towncrier`` command to generate the ``CHANGES.rst``. At release time this can be moved to
``HISTORY.rst``.

Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
