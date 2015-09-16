## Cloud Blueprint

[This blueprint](blueprint.yaml) allows you to install the cloudify-host-pool-service application on a cloud machine. <br>
Let see how this is done:

**The pool configuration file is located [here](test_cloud_config.yaml)**

#### Step 1: Upload blueprint

`cfy blueprints upload -p blueprint.yaml -b config_service` <br>

#### Step 2: Create deployment

Create the inputs and deployment.

```json
"provider": "my_ec2",
"provider_config": {
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

`cfy deployments create -b config_service -b config_service_v1 -i inputs.json` <br>

#### Step 3: Install

Run the `install` workflow: <br>

```bash
cfy executions -d config_service_v1 execute -w install
2015-09-14 18:33:29 CFY <local> Starting 'install' workflow execution
2015-09-14 18:33:29 CFY <local> [host_b625d] Creating node
2015-09-14 18:33:29 CFY <local> [host_b625d] Configuring node
2015-09-14 18:33:30 CFY <local> [host_b625d] Starting node
...
2015-09-14 18:33:39 CFY <local> 'install' workflow execution succeeded
```

This command will install all the application components on you local machine.
(It's all installed under the `tmp` directory by default)<br>
Once its done, you should be able to execute a GET request to [http://localhost:8180/status](http://localhost:8180/status) and see the result.
**Note that the result should be an array of cloud configurations as in the 'test_cloud_config.yaml'**
<br>


### Step 3: Uninstall

To uninstall the application we run the `uninstall` workflow: <br>

`cfy executions -d config_service_v1 execute -w uninstall`
