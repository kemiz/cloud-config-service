Cloud Configuration Service
==========================

## Description

The service is a python web service based on [flask-restful]
(https://flask-restful.readthedocs.org/en/0.3.2/) that exposes a REST API to
 be consumed by clients who are interested in cloud configurations from a db of
 pre-existing configurations.

#### [GET] /clouds/get_by_provider/<provider_id>

Queries the service for all cloud configurations for a specific provider.

```json
{
  "clouds": [
    {
      "_id": "my_hp_cloud",
      "_index": "clouds",
      "_score": 1.3101549,
      "_source": {
        "auth_url": "https://region-b.geo-1.identity.hpcloudsvc.com:35357/v2.0/tokens",
        "key_name": "my_key",
        "key_path": "~/.ssh/my_key.pem",
        "name": "my_hp_cloud",
        "neutron_url": "",
        "nova_url": "",
        "password": "password",
        "region": "region-b.geo-1",
        "tenant_name": "A-Project",
        "type": "openstack",
        "username": "username"
      },
      "_type": "cloud"
    },
    {
      "_id": "another_openstack",
      "_index": "clouds",
      "_score": 1.3101549,
      "_source": {
        "auth_url": "https://my-openstack:55347",
        "key_name": "another_key",
        "key_path": "~/.ssh/another_key.pem",
        "name": "another_openstack",
        "neutron_url": "",
        "nova_url": "",
        "password": "password",
        "region": "region",
        "tenant_name": "tenant",
        "type": "openstack",
        "username": "username"
      },
      "_type": "cloud"
    }
  ]
}
```

#### [GET] /cloud/get_by_id/<cloud_id>

Gets the configuration for a specific cloud. The cloud id / name must be passed.

```json
{
  "aws_access_key_id": "ANACCESSKEY",
  "aws_secret_access_key": "secretKey",
  "ec2_region_name": "us-east-1",
  "key_name": "key-us-east-1",
  "key_path": "~/.ssh/key-us-east-1.pem",
  "name": "my_ec2",
  "parameters": {},
  "resource_id": "",
  "type": "aws",
  "use_external_resource": false
}
```

#### [POST] /clouds/{cloud}

Adds a cloud.

**Not Implemented**

#### [DELETE] /clouds/{cloud}

Delete a cloud by its id.

**Not Implemented**

----

## Installation / Deployment

There are currently 2 types of installations, local and cloud.<br>
The local installation uses 'cfy local' to execute a workflow install the service.
The cloud blueprint uses the Cloudify libcloud plugin to enable deployment on any supported cloud provider.

## Local Deployment

[More here](https://github.com/kemiz/cloud-config-service/tree/master/blueprints/local-blueprint)

#### Step 1: Initialize

`cfy local init -p local-blueprint.yaml` <br>

#### Step 2: Install

Run the `install` workflow: <br>

`cfy local execute -w install`

## Cloud Deployment

[More here](https://github.com/kemiz/cloud-config-service/tree/master/blueprints/one_cloud_blueprint)

#### Step 1: Upload blueprint

`cfy blueprints upload -p blueprint.yaml -b config_service` <br>

#### Step 2: Create deployment

`cfy deployments create -b config_service -b config_service_v1` <br>

#### Step 3: Install

Run the `install` workflow: <br>

`cfy executions -d config_service_v1 execute -w install`
