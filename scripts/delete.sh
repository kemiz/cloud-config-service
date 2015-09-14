#!/bin/bash


_error(){
    echo "$1" 1>&2
    exit 1
}


    declare -r _cloud_config_dir=$(ctx node properties working_directory)

[ -d "${_cloud_config_dir}" ] || \
    _error "Host pool's directory '${_cloud_config_dir}' does not exist!"

ctx logger info "Deleting directory: ${_cloud_config_dir}"
rm -rvf "${_cloud_config_dir}"
