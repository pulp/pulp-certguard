from pulpcore.plugin import PulpPluginAppConfig


class PulpCertGuardPluginAppConfig(PulpPluginAppConfig):
    name = 'pulp_certguard.app'
    label = 'certguard'
