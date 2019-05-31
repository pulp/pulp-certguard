import pkg_resources

__version__ = pkg_resources.get_distribution("pulp-certguard").version

default_app_config = 'pulp_certguard.app.PulpCertGuardPluginAppConfig'
