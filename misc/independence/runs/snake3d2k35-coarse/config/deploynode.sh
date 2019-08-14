#!/bin/bash
# Deploy one NC24 VM on Azure

RESOURCE_GROUP="snakenc24-rg"
VM_NAME="master"
LOCATION="southcentralus"
DNS_NAME="snakenc24"

az group create \
  --name ${RESOURCE_GROUP} \
  --location ${LOCATION}

az vm create \
  --name ${VM_NAME} \
  --resource-group ${RESOURCE_GROUP} \
  --location ${LOCATION} \
  --size Standard_NC24 \
  --image Canonical:UbuntuServer:16.04-LTS:latest \
  --admin-username mesnardo \
  --authentication-type ssh \
  --ssh-key-value ~/.ssh/id_rsa.pub \
  --public-ip-address-dns-name ${DNS_NAME} \
  --storage-sku Standard_LRS
