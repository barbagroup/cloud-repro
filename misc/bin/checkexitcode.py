"""Check the exit code return by an Azure Batch job."""

import sys


with open(sys.argv[1], 'r') as infile:
    for line in infile:
        if 'exit code' in line:
            code = line.strip().split(': ')[-1]
            break
code = (0 if code == '0' else 1)
print(code)
