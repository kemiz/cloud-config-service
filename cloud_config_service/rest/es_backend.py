from datetime import datetime
from elasticsearch import Elasticsearch

from cloud_config_service.config import yaml_cloud_config_loader

providers = {'aws', 'openstack'}


class RestBackend(object):
    def __init__(self, clouds):
        self.storage = Elasticsearch()
        self._load_clouds(cloud_config=clouds)

        self.storage.index(
            index='status',
            doc_type='service_status',
            body={
                'status': 'STARTED',
                'text': 'Cloud configuration service',
                'timestamp': datetime.now(),
            },
            id='current_status'
        )

    def _add_cloud(self, cloud):
        self.storage.index(index='clouds', doc_type='cloud', body=cloud, id='current_status')

    def _load_clouds(self, cloud_config):
        print("Loading clouds from file...")
        clouds = yaml_cloud_config_loader.load(cloud_config)
        for cloud in clouds.keys():
            print('Cloud_id: {0}'.format(cloud))
            self.storage.index(
                index='clouds',
                doc_type='cloud',
                body=clouds.get(cloud),
                id=cloud
            )

    def get_clouds_by_provider(self, provider):
        print('Getting cloud configurations for: {0}'.format(provider))
        response = self.storage.search(
            index='clouds',
            body={
                'query': {
                    'match': {
                        'type': provider
                    }
                }
            }
        )
        print(response)
        return response['hits']['hits']

    def delete_cloud(self, cloud_id):
        print('Delete cloud by id')

        response = self.storage.delete(
            index='clouds',
            doc_type='cloud',
            id=cloud_id
        )

        print(response)
        return response['_source']

    def get_cloud(self, cloud_id):
        print('Get cloud by id')

        response = self.storage.get(
            index='clouds',
            doc_type='cloud',
            id=cloud_id)

        print(response)
        return response['_source']

    def get_status(self):
        response = self.storage.get(
            index='status',
            doc_type='service_status',
            id='current_status'
        )
        return response['_source']