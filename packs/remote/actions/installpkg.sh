#!/usr/bin/env bash

# Testing timeout parameter
sleep 61

# Retrieve package name
pkg=$1

# Retrieve OS Name
osName=$(cat /etc/*release | grep -w "ID" | cut -d= -f2|tr -d '"')

if [[ ${osName} == 'rhel' ]]
then
   yum install -y $pkg
   exit 0
elif [[ ${osName} == 'ubuntu' ]]
then
   apt install -y $pkg
   exit 0
else
   echo "Unsupported OS" 1>&2
   exit 5
fi