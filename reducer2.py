#!/opt/conda/default/bin/python

import sys

current_key = None
current_count = 0
key = None

for line in sys.stdin:
    key, casualties  = line.strip().split('\t', 1)
    count = int(casualties)

    if current_key == key:
        current_count += count
    else:
        if current_key:
            print(f'{current_key}\t{current_count}')
        current_count = count
        current_key = key

if current_key == key:
    print(f'{current_key}\t{current_count}')
