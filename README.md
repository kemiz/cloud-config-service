Cloud Configuration Service
==========================

## Description

The service is a python web service based on [flask-restful]
(https://flask-restful.readthedocs.org/en/0.3.2/) that exposes a REST API to
 be consumed by clients who are interested in cloud configurations from a db of
 pre-existing configurations.

### [GET] /clouds

Queries the service for all cloud configurations.

```json
{
"clouds": [{
    "hpcloud": {
        "name": "hpcloud",
        "type": "openstack",
        "parameters": {
            "username": "username",
            "password": "password",
            ...
        },
    }
]}
```

### [GET] /clouds/{cloud}

Gets the configuration for a specific cloud. The cloud id / name must be passed.

```json
{
    "name": "hpcloud",
    "type": "openstack",
    "parameters": {
        "username": "username",
        "password": "password",
        ...
    }
}
```

### [POST] /clouds/{cloud}

Add a cloud.

```json
{
    "name": "hpcloud",
    "type": "openstack",
    "parameters": {
        "username": "username",
        "password": "password",
        ...
    }
}
```

### [DELETE] /clouds/{cloud}

Release a host by its id. response is the deleted cloud

```json
{
    "name": "hpcloud",
    "type": "openstack",
    "parameters": {
        "username": "username",
        "password": "password",
        ...
    }
}
```

