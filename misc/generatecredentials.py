"""Generate a credentials.yaml configuration file from template."""

import argparse
import pathlib

from shipyard_setup import *


def parse_command_line():
    """Parse the command-line options."""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    description = 'Batch Shipyard: setup the configuration files.'
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=formatter_class)
    parser.add_argument('--resource-group', dest='resource_group',
                        type=str,
                        required=True,
                        help='Name of resource group.')
    parser.add_argument('--account-name', dest='account_name',
                        type=str,
                        required=True,
                        help='Storage account name.')
    parser.add_argument('--share-name', dest='share_name',
                        type=str,
                        required=True,
                        help='Storage fileshare name.')
    parser.add_argument('--output', dest='output',
                        type=str,
                        required=False,
                        default='credentials.yaml',
                        help='Path of the output file with credentials.')
    args = parser.parse_args()
    return args


# Parse the command-line parameters.
args = parse_command_line()

# Get information about custom account.
info = {}
info['<resource-group>'] = args.resource_group
info['<location>'] = get_resource_group_location(args.resource_group)
info['<subscription-id>'], info['<tenant-id>'] = get_subscription_ids()
info['<username>'] = get_username()
info['<batch-account-name>'] = get_batch_account_name(args.resource_group)
url = 'https://' + get_batch_account_endpoint(args.resource_group)
info['<batch-account-service-url>'] = url
info['<storage-account-name>'] = args.account_name
key = get_storage_account_key(args.resource_group, args.account_name)
info['<storage-account-key>'] = key
info['<storage-share-name>'] = args.share_name

# Read the credentials file template and generate a custom one.
scriptdir = pathlib.Path(__file__).absolute().parent
inpath = scriptdir / 'credentials-template.yaml'
# outpath = scriptdir / 'credentials.yaml'
replace_strings_in_file(inpath, info, output=args.output)
