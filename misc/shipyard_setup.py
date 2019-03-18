"""
Setup Batch Shipyard configuration files.
"""

import os
import argparse
import subprocess
import ast
import glob


def get_storage_account_key(resource_group, account_name):
    cmd_str = ('az storage account keys list '
               '--resource-group {} --account-name {} '
               '--output json --query "[0].value"'
               .format(resource_group, account_name))
    output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
    return ast.literal_eval(output)


def get_resource_group_location(resource_group):
    cmd_str = ('az group show '
               '--resource-group {} '
               '--output json --query "location"'
               .format(resource_group))
    output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
    return ast.literal_eval(output)


def get_subscription_ids():
    cmd_str = ('az account show --output json --query "[id, tenantId]"')
    output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
    return ast.literal_eval(output)


def get_username():
    cmd_str = ('az account show --output json --query "user.name"')
    output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
    return ast.literal_eval(output)


def get_batch_account_name(resource_group):
    cmd_str = ('az batch account list '
               '--resource-group {} '
               '--output json --query "[0].name"'
               .format(resource_group))
    output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
    return ast.literal_eval(output)


def get_batch_account_endpoint(resource_group):
    cmd_str = ('az batch account list '
               '--resource-group {} '
               '--output json --query "[0].accountEndpoint"'
               .format(resource_group))
    output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
    return ast.literal_eval(output)


def replace_strings_in_file(filepath, info, filemode='w', output=None):
    with open(filepath, 'r') as infile:
        lines = infile.readlines()
    for i, line in enumerate(lines):
        for key, value in info.items():
            if key in line:
                lines[i] = line.replace(key, value)
    filepath = filepath if output is None else output
    with open(filepath, filemode) as outfile:
        outfile.writelines(lines)


def replace_strings_in_files(filepaths, info, filemode='r', outputs=None):
    for i, filepath in enumerate(filepaths):
        output = None if outputs is None else outputs[i]
        replace_strings_in_file(filepath, info,
                                filemode=filemode, output=output)
