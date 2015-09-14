#!/bin/bash -e

SOURCE=$(ctx node properties source)

work_directory=$(ctx node properties working_directory)

ctx logger info "Creating directory ${work_directory}"
mkdir -p ${work_directory}
cd ${work_directory}

ctx logger info "Installing gunicorn"
pip install gunicorn==18.0
ctx logger info "Installing pyyaml"
pip install pyyaml==3.10
ctx logger info "Installing cloud-config-service"
echo ${SOURCE}
pip install ${SOURCE}

