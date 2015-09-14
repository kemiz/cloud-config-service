import os
import httplib
import yaml

from flask import Flask
from flask import jsonify
from flask_restful import Api

from cloud_config_service import exceptions
from cloud_config_service.rest import backend as rest_backend
from cloud_config_service.rest import config


app, backend = None, None


def setup():

    global app, backend

    # initialize flask application
    app = Flask(__name__)
    Api(app)

    # load application configuration file if it exists
    config_file_path = os.environ.get('CLOUD_CONFIG_SERVICE_CONFIG_PATH')
    if config_file_path:
        with open(config_file_path) as f:
            yaml_conf = yaml.load(f.read())
            config.configure(yaml_conf)
    else:
        raise exceptions.ConfigurationError(
            'Failed loading application: '
            'CLOUD_CONFIG_SERVICE_CONFIG_PATH environment '
            'variable is not defined. Use this variable to '
            'point to the application configuration file ')

    backend = rest_backend.RestBackend(clouds=config.get().clouds)

    print('Initialized application backend: {0}'.format(backend))


def reset_backend():
    global app, backend
    # initialize application backend
    backend = rest_backend.RestBackend(clouds=config.get().clouds)

setup()


@app.errorhandler(exceptions.CloudConfigServiceHTTPException)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.get_code()
    return response


@app.route('/clouds', methods=['GET'])
def get_clouds():

    """
    List cloud configurations
    """
    print('Getting all cloud configurations...')
    clouds = backend.list_clouds()
    return jsonify(clouds=clouds), httplib.OK


@app.route('/clouds/<cloud_id>', methods=['DELETE'])
def delete_cloud(cloud_id):

    """
    Delete a cloud configuration with the given cloud_id
    """

    host = backend.delete_cloud(cloud_id)
    return jsonify(host), httplib.OK


@app.route('/clouds/<cloud_id>', methods=['GET'])
def get_cloud(cloud_id):

    """
    Get the cloud configuration with the given cloud_id
    """

    cloud = backend.get_cloud(cloud_id)
    return jsonify(cloud), httplib.OK


if __name__ == '__main__':
    app.run()
