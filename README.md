# StackStorm

- [StackStorm](#stackstorm)
  - [Introduction](#introduction)
  - [Documentation](#documentation)
  - [Architecture](#architecture)
  - [Installation](#installation)

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

