from pulpcore.plugin import PulpPluginAppConfig


class PulpCertGuardPluginAppConfig(PulpPluginAppConfig):
    """App config for cert guard plugin."""

    name = 'pulp_certguard.app'
    label = 'certguard'
    version = '1.2.0'
