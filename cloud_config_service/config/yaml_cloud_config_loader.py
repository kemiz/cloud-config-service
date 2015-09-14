import yaml

from cloud_config_service import exceptions


def load(cloud_config):
    if isinstance(cloud_config, dict):
        return cloud_config
    else:
        raise exceptions.ConfigurationError(
            'Unexpected configuration '
            'type: {0}'.format(type(cloud_config)))


def validate(config):
    if 'hosts' not in config:
        raise exceptions.ConfigurationError(
            'Pool configuration '
            'is missing a hosts section')
