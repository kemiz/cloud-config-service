## Local Blueprint

[This blueprint](local-blueprint.yaml) allows you to install the cloudify-host-pool-service application on your local machine. <br>
Let see how this is done:

**The pool configuration file is located [here](test_cloud_config.yaml)**

### Step 1: Initialize

`cfy local init -p local-blueprint.yaml` <br>

This command (as the name suggests) initializes your working directory to work with the given blueprint.
Now, you can run any type of workflows on this blueprint. <br>

### Step 2: Install

Lets run the `install` workflow: <br>

```bash
cfy local execute -w install
2015-09-15 13:09:02 CFY <local> Starting 'install' workflow execution
2015-09-15 13:09:02 CFY <local> [host_7654a] Creating node
2015-09-15 13:09:02 CFY <local> [host_7654a] Configuring node
2015-09-15 13:09:03 CFY <local> [host_7654a] Starting node
2015-09-15 13:09:03 CFY <local> [cloud_config_service_ec270] Creating node
2015-09-15 13:09:03 CFY <local> [cloud_config_service_ec270.create] Sending task 'script_runner.tasks.run'
2015-09-15 13:09:03 CFY <local> [cloud_config_service_ec270.create] Task started 'script_runner.tasks.run'
2015-09-15 13:09:04 LOG <local> [cloud_config_service_ec270.create] INFO: Executing: /tmp/tmpdFgA6_-create.sh
2015-09-15 13:09:04 LOG <local> [cloud_config_service_ec270.create] INFO: Creating directory /tmp/cloud_config_service
2015-09-15 13:09:04 LOG <local> [cloud_config_service_ec270.create] INFO: Installing gunicorn
2015-09-15 13:09:04 LOG <local> [cloud_config_service_ec270.create] INFO: Installing pyyaml
2015-09-15 13:09:05 LOG <local> [cloud_config_service_ec270.create] INFO: Installing cloud-config-service
2015-09-15 13:09:07 LOG <local> [cloud_config_service_ec270.create] INFO: Execution done (return_code=0): /tmp/tmpdFgA6_-create.sh
2015-09-15 13:09:07 CFY <local> [cloud_config_service_ec270.create] Task succeeded 'script_runner.tasks.run'
2015-09-15 13:09:07 CFY <local> [cloud_config_service_ec270] Configuring node
2015-09-15 13:09:07 CFY <local> [cloud_config_service_ec270.configure] Sending task 'script_runner.tasks.run'
2015-09-15 13:09:07 CFY <local> [cloud_config_service_ec270.configure] Task started 'script_runner.tasks.run'
2015-09-15 13:09:08 LOG <local> [cloud_config_service_ec270.configure] INFO: Downloading cloud configuration file
2015-09-15 13:09:08 CFY <local> [cloud_config_service_ec270.configure] Task succeeded 'script_runner.tasks.run'
2015-09-15 13:09:08 CFY <local> [cloud_config_service_ec270] Starting node
2015-09-15 13:09:08 CFY <local> [cloud_config_service_ec270.start] Sending task 'script_runner.tasks.run'
2015-09-15 13:09:08 CFY <local> [cloud_config_service_ec270.start] Task started 'script_runner.tasks.run'
2015-09-15 13:09:08 LOG <local> [cloud_config_service_ec270.start] INFO: Executing: /tmp/tmpc2j4KN-start.sh
2015-09-15 13:09:09 LOG <local> [cloud_config_service_ec270.start] INFO: Starting cloudify-cloud-config-service with command: gunicorn --workers=5 --pid=/tmp/cloud_config_service/gunicorn.pid --log-level=INFO --log-file=/tmp/cloud_config_service/gunicorn.log --bind 0.0.0.0:8180 --daemon cloud_config_service.rest.service:app
2015-09-15 13:09:09 LOG <local> [cloud_config_service_ec270.start] INFO: Running Cloud-Config-Service liveness detection on port 8180
2015-09-15 13:09:09 LOG <local> [cloud_config_service_ec270.start] INFO: [GET] http://localhost:8180/status 200
2015-09-15 13:09:10 LOG <local> [cloud_config_service_ec270.start] INFO: Execution done (return_code=0): /tmp/tmpc2j4KN-start.sh
2015-09-15 13:09:10 CFY <local> [cloud_config_service_ec270.start] Task succeeded 'script_runner.tasks.run'
2015-09-15 13:09:10 CFY <local> 'install' workflow execution succeeded
```

This command will install all the application components on you local machine.
(It's all installed under the `tmp` directory by default)<br>
Once its done, you should be able to execute a GET request to [http://localhost:8180/clouds](http://localhost:8180/clouds) and see the result.
**Note that the result should be an array of cloud configurations as in the 'test_cloud_config.yaml'**
<br>


### Step 3: Uninstall

To uninstall the application we run the `uninstall` workflow: <br>

`cfy local execute -w uninstall`
