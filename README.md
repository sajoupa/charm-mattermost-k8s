# Mattermost charm

A juju charm deploying Mattermost, using a custom-built built image,
configurable to use a postgresql backend.

## Overview

This is a k8s charm and can only be deployed to to a Juju k8s cloud,
attached to a controller using `juju add-k8s`.

The image to spin up is specified in the `image` charm configuration
option using standard docker notation (eg. 'localhost:32000/mywork-rev42').

Configuration for the Mattermost image is in standard Juju config. In
particular:

* `pg_db_host`, `pg_db_port`, `pg_user`, `pg_password`: this charm should be
  able in the future, to relate to postgresql, but as of now these parameters
  allow setting up the connection.

## Details

See config option descriptions in config.yaml.

## Quickstart

Notes for deploying a test setup locally using microk8s:

    sudo snap install juju --classic
    sudo snap install juju-wait --classic
    sudo snap install microk8s --classic
    sudo snap alias microk8s.kubectl kubectl

    microk8s.reset  # Warning! Clean slate!
    microk8s.enable dns dashboard registry storage
    microk8s.status --wait-ready
    microk8s.config | juju add-k8s myk8s
    juju bootstrap myk8s
    juju add-model mattermost-test
    juju deploy ./charm-mattermost mattermost
    juju config mattermost pg_db_host=10.1.1.1 pg_password=secret
    juju wait
    juju status # Shows IP address, and port is 8000
