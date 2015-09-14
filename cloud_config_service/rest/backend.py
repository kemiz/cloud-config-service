import filelock
import os

from cloud_config_service.storage import sqlite
from cloud_config_service.config import yaml_cloud_config_loader
from cloud_config_service import exceptions


# we currently don't expose these in the configuration because its somewhat
# internal. perhaps at a later time we can have this configurable, at which
# point we need to define the semantics of how to initialize the components.

FLock = filelock.FileLock('cloud-config-backend.lock')

# if this file exists, loading of the pool will not take place.
# note that this means that multiple instances of this application that
# execute from the same directory will only load the pool the first
# time, and all other instances will use the previously loaded pool.
INDICATOR = 'cloud-config-loaded-indicator'


class RestBackend(object):

    def __init__(self, clouds, storage=None):
        self.storage = sqlite.SQLiteStorage(storage)
        # allow only one process to do the initial load

        def _create_indicator():
            fd = os.open(INDICATOR, os.O_WRONLY |
                         os.O_CREAT | os.O_EXCL, 0600)
            os.close(fd)

        with FLock:
            if not os.path.exists(INDICATOR):
                self._load_clouds(clouds)
                _create_indicator()

    def _load_clouds(self, cloud_config):
        clouds = yaml_cloud_config_loader.load(cloud_config)
        for cloud in clouds:
            print clouds[cloud]
            self.storage.add_cloud(clouds[cloud])

    def list_clouds(self):
        print('Getting all clouds')
        clouds = self.storage.get_clouds()
        return clouds
        # return filter(lambda cloud: cloud['cloud_id'], clouds)

    def delete_cloud(self, cloud_id):
        cloud = self.get_cloud(cloud_id)
        # self.storage.delete_cloud(cloud['global_id'])
        # return host

    def get_cloud(self, cloud_id):
        print('Get cloud by id')
        clouds = self.storage.get_clouds(cloud_id=cloud_id)
        if len(clouds) == 0:
            print('CloudNotFoundException')
            raise exceptions.CloudNotFoundException(cloud_id)
        return clouds[0]