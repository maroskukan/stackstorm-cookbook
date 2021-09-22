# StackStorm

- [StackStorm](#stackstorm)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [One-line Install](#one-line-install)

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