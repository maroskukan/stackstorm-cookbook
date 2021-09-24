# StackStorm

- [StackStorm](#stackstorm)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [One-line Install](#one-line-install)
  - [Environment Setup](#environment-setup)
  - [Basic Configuration](#basic-configuration)
    - [Login Methods](#login-methods)
    - [User Management](#user-management)
  - [Packs](#packs)
    - [List packs](#list-packs)
    - [Install and Uninstall packs](#install-and-uninstall-packs)
    - [Pack information](#pack-information)
  - [Actions](#actions)
    - [List actions](#list-actions)
    - [Execute actions](#execute-actions)

## Introduction

StackStorm is an open source event-driven platform for automating your tools and infrastructure. It is licensed under the Apache 2.0 License.

There is also a commercial version of StackStorm called Extreme Workflow Composer (EWC) which adds additional features like priority support, workflow designer and RBAC.


## Documentation

- [StackStorm Documentation](https://docs.stackstorm.com/index.html)
- [StackStorm Exchange](https://exchange.stackstorm.org/)


## Architecture

Stackstorm is composed of the following main components:

- Sensors - monitor when an event happens
- Rules - check what needs to be done
- Workflows - run a set of instructions
- Actions - execute relevant commands
- Results - process results for analysus or additional triggers

When deployed for single system the reference architecture looks as follows:

![Architecture](https://docs.stackstorm.com/_images/st2-deployment-big-picture.png)


StackStorm provides great level of extensibility by using content packs. Packs combination of *Sensors*, *Rules*, *Workflows* and *Actions*. They are available for many different services and applications, visit [StackStorm Exchange](https://exchange.stackstorm.org/) for full lisf of maintaned packs. You can also create a custom pack for your own specific needs.

Tasks can be also executed manually by using one of the following methods:
- Command Line Interface - powerful and easy for administrators and developers
- Web User Interface - suited for operation team members
- REST API - excellent for integration with any upstream custom applications

Connectivity to managed nodes is handled through SSH or REST API.


## Installation

StackStorm is supported on Ubuntu, RHEL and CentOS Linux. The system requirements for testing and production are different, therefore always refer to [documentation](https://docs.stackstorm.com/install/system_requirements.html) when defining the underlying platform. At the time of writing they are:

| Testing      | Production   |
| ------------ | ------------ |
| 2 vCPU       | 4 vCPU       |
| 2GB RAM      | >16GB RAM    |
| 10GB HDD     | 40GB HDD     |
| t2.medium    | m4.xlarge    |

StackStorm is distributed as an RPMs and Debs packages as well as Docker images, therefore there ware multiple ways how to perform instalation, for example.

- **One-line Install** - using provided shell script for an opionated install for all components
- **Manual Installation** - great for custom needs
- **Vagrant / Virtual Appliance** - pre-installed, tested and shipped as virtual image, great for testing, pack develoment or demo
- **Docker** - quickiest way to get StackStorm running, useful for trying platform and development
- **Ansible Playbooks** - great for repeatable, consistent, and idempotent installation using Ansible
- **Puppet Module** - greate for repeatable, consistent and idempotent installation using Puppet
- **High Availability** - great for business critital automation by using StackStorm HA Cluster in Kubernetes

### One-line Install

Provision a clean installation of `Ubuntu2004` and install StackStorm using one-line script. It will automatically install required components.

```bash
# Provision and open an SSH session to VM
cd install/one-line && vagrant up && vagrant ssh

# Install StackStorm
bash <(curl -sSL https://stackstorm.com/packages/install.sh) --user=st2admin --password=Ch@ngeMe
```

One the installation completed the StackStorm components should be up and running. You can use the following methods to verify the installation.

Verify st2 and python version.

```bash
st2 --version
st2 3.5.0, on Python 3.8.10

/opt/stackstorm/st2/bin/python3 --version
Python 3.8.10
```

Verify `nginx`, `rabbitmq`, `mongod`, `st2api` service

```bash
systemctl status nginx
● nginx.service - nginx - high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-09-22 11:42:34 UTC; 11min ago
       Docs: https://nginx.org/en/docs/
   Main PID: 17659 (nginx)
      Tasks: 3 (limit: 4617)
     Memory: 3.3M
     CGroup: /system.slice/nginx.service
             ├─17659 nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf
             ├─17660 nginx: worker process
             └─17661 nginx: worker process

systemctl status rabbitmq-server.service 
● rabbitmq-server.service - RabbitMQ Messaging Server
     Loaded: loaded (/lib/systemd/system/rabbitmq-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-09-22 11:39:20 UTC; 15min ago
   Main PID: 5728 (beam.smp)
     Status: "Initialized"
      Tasks: 87 (limit: 4617)
     Memory: 76.0M
     CGroup: /system.slice/rabbitmq-server.service
             ├─5711 /bin/sh /usr/sbin/rabbitmq-server
             ├─5728 /usr/lib/erlang/erts-10.6.4/bin/beam.smp -W w -A 64 -MBas ageffcbf -MHas ageffcbf -MBlmbcs 512 -MHlmbcs>
             ├─5992 erl_child_setup 65536
             ├─6017 inet_gethost 4
             └─6018 inet_gethost 4

systemctl status mongod.service 
● mongod.service - MongoDB Database Server
     Loaded: loaded (/lib/systemd/system/mongod.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-09-22 11:40:01 UTC; 15min ago
       Docs: https://docs.mongodb.org/manual
   Main PID: 7358 (mongod)
     Memory: 191.6M
     CGroup: /system.slice/mongod.service
             └─7358 /usr/bin/mongod --config /etc/mongod.conf

Sep 22 11:40:01 stackstorm systemd[1]: Started MongoDB Database Server.

systemctl status st2api
● st2api.service - StackStorm service st2api
     Loaded: loaded (/lib/systemd/system/st2api.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-09-22 11:41:53 UTC; 26min ago
TriggeredBy: ● st2api.socket
   Main PID: 15881 (gunicorn)
      Tasks: 2 (limit: 4617)
     Memory: 91.2M
     CGroup: /system.slice/st2api.service
             ├─15881 /opt/stackstorm/st2/bin/python /opt/stackstorm/st2/bin/gunicorn st2api.wsgi:application -k eventlet -b>
             └─15892 /opt/stackstorm/st2/bin/python /opt/stackstorm/st2/bin/gunicorn st2api.wsgi:application -k eventlet -b>
```

You can use show sockets `ss` to verify which ports are listening.

```bash
ss -tlp
State      Recv-Q     Send-Q         Local Address:Port               Peer Address:Port    Process    
LISTEN     0          511                127.0.0.1:6379                    0.0.0.0:*                  
LISTEN     0          2048               127.0.0.1:9100                    0.0.0.0:*                  
LISTEN     0          2048               127.0.0.1:bacula-dir              0.0.0.0:*                  
LISTEN     0          2048               127.0.0.1:bacula-fd               0.0.0.0:*                  
LISTEN     0          511                  0.0.0.0:http                    0.0.0.0:*                  
LISTEN     0          4096           127.0.0.53%lo:domain                  0.0.0.0:*                  
LISTEN     0          128                  0.0.0.0:ssh                     0.0.0.0:*                  
LISTEN     0          511                  0.0.0.0:https                   0.0.0.0:*                  
LISTEN     0          128                127.0.0.1:amqp                    0.0.0.0:*                  
LISTEN     0          128                  0.0.0.0:25672                   0.0.0.0:*                  
LISTEN     0          4096               127.0.0.1:27017                   0.0.0.0:*                  
LISTEN     0          4096                       *:epmd                          *:*                  
LISTEN     0          128                     [::]:ssh                        [::]:* 
```

To verify st2 component status use the `st2ctl status` command:

```bash
st2ctl status
##### st2 components status #####
st2actionrunner PID: 15955
st2actionrunner PID: 15957
st2actionrunner PID: 15959
st2actionrunner PID: 15961
st2actionrunner PID: 15963
st2actionrunner PID: 15965
st2actionrunner PID: 15967
st2actionrunner PID: 15969
st2actionrunner PID: 15971
st2actionrunner PID: 15973
st2api PID: 15881
st2api PID: 15892
st2stream PID: 15830
st2stream PID: 15874
st2auth PID: 15775
st2auth PID: 15802
st2garbagecollector PID: 14548
st2notifier PID: 14549
st2rulesengine PID: 14550
st2sensorcontainer PID: 15898
st2chatops is not running.
st2timersengine PID: 14553
st2workflowengine PID: 15909
st2scheduler PID: 14552
```

Some important paths and files to remeber are:
- `/opt/stackstorm`
- `/etc/st2`
- `/etc/st2/st2.conf`
- `/var/log/st2`

With quick installation StackStorm Automation tasks will run by default with `stanley` system user on the OS. This use has sudo privileges. This use will be also used to connect to remote managed system by default.

```bash
id stanley
uid=1001(stanley) gid=1001(stanley) groups=1001(stanley)

cat /etc/sudoers.d/st2
Defaults env_keep += "http_proxy https_proxy no_proxy proxy_ca_bundle_path DEBIAN_FRONTEND"
stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL

grep -A2 system_user /etc/st2/st2.conf 
[system_user]
user = stanley
ssh_key_file = /home/stanley/.ssh/stanley_rsa
```

When you modify the st2.conf file you need to restart the service with `st2ctl restart` command to apply the new configuration.


## Environment Setup

To execute actions on remote hosts, StackStorm uses SSH connection. It is recommended to use password-less authentication using SSH keys.

One way to setup password-less authentication is to generate public key (if not available already) for `stanley` user on StackStorm Engine. And then create a `stanley` user on each managed node and copy the public key to `authorized_keys` file on each managed node. [documentation](https://docs.stackstorm.com/install/config/config.html#configure-ssh).


Start by creating a RSA key pair on StackStorm host if it is not already available.

```bash
sudo su stanley
ssh-keygen -f /home/stanley/.ssh/stanley_rsa -P ""
```

Next, on each managed system, create new user, update authorized_keys file and update sudoers.

```bash
useradd stanley
mkdir -p /home/stanley/.ssh
chmod 0700 /home/stanley/.ssh

cat <<EOF > /home/stanley/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDsMdrhVmDHIdfEDQvXDZCLbaY3e1E/wPz4q8s+XZAgg94aWK6i4HAWlT9jfxaCQIOAXWnIkYVrn5sgAbutCEPYE2uS0shymB4S1gO0YYIxuSP9OOMSR+zMA1SeYvPU4QfSEtYeYG9iMlwNmzsyq48Td40SMvdBMBOcMn9KyxW+IpPmbuXyk+fs//ulXlWEH744BoUzqz4jTzGR7yglplTL7QTxdxLfaAGXRyCkUUBK6x7qACXobim0YVBFk35/dIjW4gVPKvZhrBehhzBCTWSvCPNdWXGQQm4OQzExNhPndrY0+dKuhXTRemwn9bn3BEGZauLY7DDcWPxAiy45r9WeqkBF9n9SKM5AVjBP8LxzfHTHNNvDLh8eoUOlaAaRCQflEQWN5H0r4HNhcoWuVx7RtUNzFjMvnGUekhADIEdVjquOgSIo0TFyk+6mNUnujGjO283eY1Ba7zRdLlNU8fvwJgjZYb4btTwI4lyBlFHgMqI9eu1JcDCT5SNABNSpu88= root@stackstorm
EOF

chmod 0600 /home/stanley/.ssh/authorized_keys
chown -R stanley:stanley /home/stanley
echo "stanley    ALL=(ALL)       NOPASSWD: SETENV: ALL" >> /etc/sudoers.d/st2

sudo sed -i -r "s/^Defaults\s+\+requiretty/# Defaults +requiretty/g" /etc/sudoers
```

Finally, verify key-based authentication and sudo privileges from StackStorm host.

```bash
# ssh should not require a password since the key is already provided
ssh -i /home/stanley/.ssh/stanley_rsa stanley@host.example.com "sudo id"
uid=0(root) gid=0(root) groups=0(root)
```

## Basic Configuration

ST2 provides number of CLI commands for managing the instance. To get full list of them, just use `st2` command with tab completion and you will get the following result back.

```bash
st2                                st2-generate-symmetric-crypto-key  st2-self-check
st2-apply-rbac-definitions         st2-register-content               st2-track-result
st2-bootstrap-rmq                  st2-rule-tester                    st2-trigger-refire
st2ctl                             st2-run-pack-tests                 st2-validate-pack-config
```

From this list, the most used ones are `st2` and `st2ctl`.

The `st2ctl` is used for StackStorm administration. For example to start, stop, restart service or reload a component. This is required when you change the configuration.

The `st2` is used to login and execute automation tasks

### Login Methods

THere are two primary ways how to login into StackStorm:
- Web UI using https://<st2-ip-address>/
- CLI `st2 login st2admin`

```bash
st2 login st2admin
Password:
Logged in as st2admin

Note: You didn't use --write-password option so the password hasn't been stored in the client config and you will need to login again in 24 hours when the auth token expires.
As an alternative, you can run st2 login command with the "--write-password" flag, but keep it mind this will cause it to store the password in plain-text in the client config file (~/.st2/config).
```

When you login `.st2` directory will be created. It will contain the st2 user configuration with the authentication token.

```bash
ls -al .st2
-rw-r--r-- 1 vagrant vagrant   35 Sep 23 12:56 config
-rw-rw---- 1 vagrant vagrant   77 Sep 23 12:56 token-st2admin
```

### User Management

The default admin user `st2admin` credentials are stored in `/etc/st2/htpasswd` file.

```bash
ls -la /etc/st2/htpasswd
-rw------- 1 st2 st2 47 Sep 22 11:41 /etc/st2/htpasswd
```

As you can see this file is owned by `st2` service account with nologin. In order to update this password, login as `root` user and change the password.

```bash
sudo su
htpasswd /etc/st2/htpasswd st2admin
New password:
Re-type new password:
Updating password for user st2admin
```

## Packs

As mentioned in the [Architecture](#architecture) section a `pack` is a group of integration and automation tasks.

Imagine that you need to automate a docker implementation. You need to define tasks which you want to automate such as:

- Status of Docker
- Start Docker
- Stop Docker
- Restart Docker
- Clean up /var/log

You can aggregate the above tasks into `Actions` and execute them manuall or based on events such as:

- Monitor the Status of Docker (if down start it)
- Monitor the disk space (if low clean up logs)

You can classify these two monitor tasks as `Sensors` as they are monitoring the managed hosts.

Finally, you can implement additional logic based on conditions by using `workflows`.

- Start Docker if it is not running
- Stop Docker if it is running

In summary a pack may contain the following folders and files.

- actions
- workflows
- sensors
- rules
- pack.yml

### List packs

StackStorm contains some default packs such as:

```bash
ls -l /opt/stackstorm/packs/
total 24
drwxrwxr-x 5 root st2packs 4096 Sep 22 11:40 chatops
drwxrwxr-x 5 root st2packs 4096 Sep 22 11:40 core
drwxrwxr-x 5 root st2packs 4096 Sep 22 11:40 default
drwxrwxr-x 5 root st2packs 4096 Sep 22 11:40 linux
drwxrwxr-x 5 root st2packs 4096 Sep 22 11:40 packs
drwxrwxr-x 8 root st2packs 4096 Sep 22 11:42 st2

st2 pack list
+---------+---------+-----------------------------+---------+------------------+
| ref     | name    | description                 | version | author           |
+---------+---------+-----------------------------+---------+------------------+
| chatops | chatops | ChatOps integration pack    | 3.5.0   | StackStorm, Inc. |
| core    | core    | Basic core actions.         | 3.5.0   | StackStorm, Inc. |
| default | default | Default pack where all      | 3.5.0   | StackStorm, Inc. |
|         |         | resources created using the |         |                  |
|         |         | API with no pack specified  |         |                  |
|         |         | get saved.                  |         |                  |
| linux   | linux   | Generic Linux actions       | 3.5.0   | StackStorm, Inc. |
| packs   | packs   | Pack management             | 3.5.0   | StackStorm, Inc. |
|         |         | functionality.              |         |                  |
| st2     | st2     | StackStorm utility actions  | 2.0.1   | StackStorm, Inc. |
|         |         | and aliases                 |         |                  |
+---------+---------+-----------------------------+---------+------------------+
```

By default output is formatted as table, you have option to view it as json or yaml with `--json` or `--yaml` arguments.

### Install and Uninstall packs

To install a pack.

```bash
st2 pack search aws
+-----------+------------------------------------+---------+------------------+
| name      | description                        | version | author           |
+-----------+------------------------------------+---------+------------------+
| aws       | st2 content pack containing Amazon | 2.0.1   | StackStorm, Inc. |
|           | Web Services integrations.         |         |                  |
| libcloud  | st2 content pack containing        | 0.6.0   | StackStorm, Inc. |
|           | libcloud integrations              |         |                  |
| aws_boto3 | AWS actions using boto3            | 1.0.0   | StackStorm, Inc. |
| aws_s3    | AWS S3-specific actions            | 2.0.3   | StackStorm, Inc. |
+-----------+------------------------------------+---------+------------------+

st2 pack install aws
For the "aws" pack, the following content will be registered:

actions   |  3581
rules     |  0
sensors   |  2
aliases   |  3
triggers  |  0

Installation may take a while for packs with many items.

        [ succeeded ] init_task
        [ succeeded ] download_pack
        [ succeeded ] make_a_prerun
        [ succeeded ] get_pack_dependencies
        [ succeeded ] check_dependency_and_conflict_list
        [ succeeded ] install_pack_requirements
        [ succeeded ] get_pack_warnings
        [ succeeded ] register_pack

+-------------+--------------------------------------------------------------+
| Property    | Value                                                        |
+-------------+--------------------------------------------------------------+
| ref         | aws                                                          |
| name        | aws                                                          |
| description | st2 content pack containing Amazon Web Services              |
|             | integrations.                                                |
| version     | 2.0.1                                                        |
| author      | StackStorm, Inc.                                             |
+-------------+--------------------------------------------------------------+
```

To uninstall a pack.

```bash
st2 pack remove aws

        [ succeeded ] unregister packs
        [ succeeded ] delete packs

+-------------+--------------------------------------------------------------+
| Property    | Value                                                        |
+-------------+--------------------------------------------------------------+
| ref         | aws                                                          |
| name        | aws                                                          |
| description | st2 content pack containing Amazon Web Services              |
|             | integrations.                                                |
| version     | 2.0.1                                                        |
| author      | StackStorm, Inc.                                             |
+-------------+--------------------------------------------------------------+
```


### Pack information

Information about an installed pack.

```bash
st2 pack get aws
+-------------+--------------------------------------------------------------+
| Property    | Value                                                        |
+-------------+--------------------------------------------------------------+
| name        | aws                                                          |
| version     | 2.0.1                                                        |
| author      | StackStorm, Inc.                                             |
| email       | info@stackstorm.com                                          |
| keywords    | [                                                            |
|             |     "aws",                                                   |
|             |     "amazon web services",                                   |
|             |     "amazon",                                                |
|             |     "ec2",                                                   |
|             |     "sqs",                                                   |
|             |     "sns",                                                   |
|             |     "route53",                                               |
|             |     "cloud",                                                 |
|             |     "iam",                                                   |
|             |     "vpc",                                                   |
|             |     "s3",                                                    |
|             |     "CloudFormation",                                        |
|             |     "RDS",                                                   |
|             |     "SQS",                                                   |
|             |     "lambda",                                                |
|             |     "kinesis"                                                |
|             | ]                                                            |
| description | st2 content pack containing Amazon Web Services              |
|             | integrations.                                                |
+-------------+--------------------------------------------------------------+
```

Information about an installed or available pack at exchange.

```bash
st2 pack show terraform
+-----------------+-------------------------------------------------------------+
| Property        | Value                                                       |
+-----------------+-------------------------------------------------------------+
| name            | terraform                                                   |
| description     | Terraform integrations                                      |
| author          | Martez Reed                                                 |
| content         | {                                                           |
|                 |     "actions": {                                            |
|                 |         "count": 13,                                        |
|                 |         "resources": [                                      |
|                 |             "apply",                                        |
|                 |             "create_workspace",                             |
|                 |             "delete_workspace",                             |
|                 |             "destroy",                                      |
|                 |             "get_version",                                  |
|                 |             "import_object",                                |
|                 |             "init",                                         |
|                 |             "list_workspaces",                              |
|                 |             "output",                                       |
|                 |             "pipeline",                                     |
|                 |             "plan",                                         |
|                 |             "select_workspace",                             |
|                 |             "show"                                          |
|                 |         ]                                                   |
|                 |     },                                                      |
...
[ Output omitted  ]
...
```


## Actions

Actions are pieces of code or script that can perform automation. They can be written in any programming language. 

Usually actions are part of a pack, but there may be cases that they are deployed without pack, therefore they will be part of `default` pack.

### List actions

In order to list available actions use the `st2 action list` command. As you can see each action has a prefix of pack name and short description.

```bash
st2 action list
+---------------------------------+---------+------------------------------------------------+
| ref                             | pack    | description                                    |
+---------------------------------+---------+------------------------------------------------+
| chatops.format_execution_result | chatops | Format an execution result for chatops         |
| chatops.match                   | chatops | Match a string to an action alias              |
| chatops.match_and_execute       | chatops | Execute a chatops string to an action alias    |
| chatops.post_message            | chatops | Post a message to stream for chatops           |
| chatops.post_result             | chatops | Post an execution result to stream for chatops |
| chatops.run                     | chatops | Match a text chatops command, execute it and   |
|                                 |         | post the result                                |
| core.announcement               | core    | Action that broadcasts the announcement to all |
|                                 |         | stream consumers.                              |
| core.ask                        | core    | Action for initiating an Inquiry (usually in a |
...
[ Output omitted ]
...
```

To get more information about a particular action, use the `get` argument. This is useful for retrieving the required parameters.

```bash
st2 action get core.echo
+---------------+--------------------------------------------------------------+
| Property      | Value                                                        |
+---------------+--------------------------------------------------------------+
| id            | 614b1676586f7adc0a29e849                                     |
| uid           | action:core:echo                                             |
| ref           | core.echo                                                    |
| pack          | core                                                         |
| name          | echo                                                         |
| description   | Action that executes the Linux echo command on the           |
|               | localhost.                                                   |
| enabled       | True                                                         |
| entry_point   |                                                              |
| runner_type   | local-shell-cmd                                              |
| parameters    | {                                                            |
|               |     "message": {                                             |
|               |         "description": "The message that the command will    |
|               | echo.",                                                      |
|               |         "type": "string",                                    |
|               |         "required": true                                     |
|               |     },                                                       |
|               |     "cmd": {                                                 |
|               |         "description": "Arbitrary Linux command to be        |
|               | executed on the local host.",                                |
|               |         "required": true,                                    |
|               |         "type": "string",                                    |
|               |         "default": "echo "{{message}}"",                     |
|               |         "immutable": true                                    |
|               |     },                                                       |
|               |     "kwarg_op": {                                            |
|               |         "immutable": true                                    |
|               |     },                                                       |
|               |     "sudo": {                                                |
|               |         "default": false,                                    |
|               |         "immutable": true                                    |
|               |     },                                                       |
|               |     "sudo_password": {                                       |
|               |         "immutable": true                                    |
|               |     }                                                        |
|               | }                                                            |
| metadata_file | actions/echo.yaml                                            |
| notify        |                                                              |
| output_schema |                                                              |
| tags          |                                                              |
+---------------+--------------------------------------------------------------+
```

### Execute actions

In order to execute action manually, you can use Web UI Actions Tab. Select an action, fill mandatory parameters and hit Run.

You can also execute action using CLI using `st2`

```bash
st2 run core.local cmd="uptime"
.
id: 614c973618f0dd6e8c03e07b
action.ref: core.local
context.user: st2admin
parameters:
  cmd: uptime
status: succeeded
start_timestamp: Thu, 23 Sep 2021 15:03:18 UTC
end_timestamp: Thu, 23 Sep 2021 15:03:18 UTC
result:
  failed: false
  return_code: 0
  stderr: ''
  stdout: ' 15:03:18 up 11:07,  1 user,  load average: 0.17, 0.13, 0.10'
  succeeded: true
```