from datetime import datetime
from elasticsearch import Elasticsearch

from cloud_config_service.config import yaml_cloud_config_loader


class RestBackend(object):

    def __init__(self, clouds):
        self.storage = Elasticsearch()
        self._load_clouds(cloud_config=clouds)

        doc = {
            'status': 'STARTED',
            'text': 'Cloud configuration service',
            'timestamp': datetime.now(),
        }

        self.storage.index(index="status", doc_type='service_status', body=doc, id='current_status')

    def _load_clouds(self, cloud_config):
        clouds = yaml_cloud_config_loader.load(cloud_config)
        for cloud in clouds.keys():
            print('Cloud_id: {0}'.format(cloud))
            es_res = self.storage.index(index="clouds", doc_type='cloud', body=clouds.get(cloud), id=cloud)
            print(es_res)

    def list_clouds(self, provider):
        print('Getting all clouds')
        response = self.storage.search(index="clouds",
                                       body={"query": {"match": {'type': provider}}})

        return response['hits']['hits']

    def delete_cloud(self, cloud_id):
        pass
        # cloud = self.get_cloud(cloud_id)
        # self.storage.delete_cloud(cloud['global_id'])
        # return host

    def get_cloud(self, cloud_id):
        print('Get cloud by id')
        response = self.storage.get(index="clouds", doc_type='cloud', id=cloud_id)
        print(response['_source'])
        return response['_source']

    def get_status(self):
        return self.storage.get(index="status", doc_type='service_status', id='current_status')