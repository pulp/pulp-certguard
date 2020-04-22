.. highlight:: shell

============
Installation
============


Stable release
--------------

To install pulp-certguard, run this command in your terminal:

.. code-block:: console

    $ pip install pulp_certguard

This is the preferred method to install pulp-certguard, as it will always install the most recent
stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. note::

    To use the ``RHSMCertGuard`` you have to manually install the `rhsm Python module
    <https://pypi.org/project/rhsm/>`_ which provides RHSM certificate parsing on the pulp server.
    It requires some system level dependencies, e.g. OpenSSL libraries, which are not the same on
    all operating operating systems. ``rhsm`` from PyPI not being cross-distro is why this requires
    manual installation.


From sources
------------

The sources for pulp-certguard can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/pulp/pulp-certguard

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OJL https://github.com/pulp/pulp-certguard/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

Or you can skip download step and install directly with:

.. code-block:: console

    $ pip install https://github.com/pulp/pulp-certguard/tarball/master


.. _Github repo: https://github.com/pulp/pulp-certguard
.. _tarball: https://github.com/pulp/pulp_certguard/tarball/master


Using the Pulp Installer
------------------------

pulp-certguard is a Pulp plugin, and can be installed along with Pulp and other plugins using the
`Pulp Installer <https://github.com/pulp/ansible-pulp>`_. It can be installed by configuring the
installer's `pulp_install_plugins`_ variable with ``pulp-certguard`` as follows:

.. code-block:: yaml

    pulp_install_plugins:
      pulp-certguard: {}

.. _pulp_install_plugins: https://github.com/pulp/ansible-pulp/blob/master/roles/pulp/README.md#role-variables
