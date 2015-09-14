import os

from cloudify import ctx


cloud_config = ctx.node.properties['cloud_config']
work_directory = ctx.node.properties['working_directory']


def download_cloud_config():
    _cloud_config = os.path.join(work_directory, os.path.basename(cloud_config))
    ctx.logger.info('Downloading cloud configuration file')
    ctx.download_resource(cloud_config, target_path=_cloud_config)
    return _cloud_config


ctx.instance.runtime_properties['config_path'] = download_cloud_config()
