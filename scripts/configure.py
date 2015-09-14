import os
import json

from cloudify import ctx


cloud_config = ctx.node.properties['cloud_config']
work_directory = ctx.node.properties['working_directory']
config_path = os.path.join(work_directory, 'config.json')


def download_cloud_config():
    _cloud_config = os.path.join(work_directory, os.path.basename(cloud_config))
    ctx.logger.info('Downloading cloud configuration file')
    ctx.download_resource(cloud_config, target_path=_cloud_config)
    return _cloud_config


def write_cloud_config_file():
    config_json = {
        'clouds': cloud_config_path
    }
    ctx.logger.info('Creating service configuration file')
    with open(config_path, 'w') as f:
        json.dump(config_json, f, indent=2)

cloud_config_path = download_cloud_config()
write_cloud_config_file()

ctx.instance.runtime_properties['config_path'] = config_path
