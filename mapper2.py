#!/opt/conda/default/bin/python

import sys
import re

ACCIDENT_DATE_COL = 0
ZIP_CODE_COL = 2
ON_STREET_NAME_COL = 6
CROSS_STREET_NAME_COL = 7
OFF_STREET_NAME_COL = 8
PEDESTRIANS_INJURED_COL = 11
PEDESTRIANS_KILLED_COL = 12
CYCLIST_INJURED_COL = 13
CYCLIST_KILLED_COL = 14
MOTORIST_INJURED_COL = 15
MOTORIST_KILLED_COL = 16

p = re.compile(r'\d+\/\d+\/(\d+)')

def generate_street_data(street_name, zip_code, pedestrians_injured, pedestrians_killed, cyclist_injured, cyclist_killed, motorist_injured, motorist_killed):
    if street_name != '':
        print(f'{street_name},{zip_code},pedestrian,injured\t{pedestrians_injured}')
        print(f'{street_name},{zip_code},pedestrian,killed\t{pedestrians_killed}')
        print(f'{street_name},{zip_code},cyclist,injured\t{cyclist_injured}')
        print(f'{street_name},{zip_code},cyclist,killed\t{cyclist_killed}')
        print(f'{street_name},{zip_code},motorist,injured\t{motorist_injured}')
        print(f'{street_name},{zip_code},motorist,killed\t{motorist_killed}')

for line in sys.stdin:
    data = line.strip().split(',')

    year = p.match(data[ACCIDENT_DATE_COL])
    zip_code =  data[ZIP_CODE_COL]
    if not year or int(year.group(1)) <= 2012 or not len(zip_code):
        continue

    on_street_name = data[ON_STREET_NAME_COL].upper().strip()
    cross_street_name = data[CROSS_STREET_NAME_COL].upper().strip()
    off_street_name = data[OFF_STREET_NAME_COL].upper().strip()
    pedestrians_injured = data[PEDESTRIANS_INJURED_COL]
    pedestrians_killed = data[PEDESTRIANS_KILLED_COL]
    cyclist_injured = data[CYCLIST_INJURED_COL]
    cyclist_killed = data[CYCLIST_KILLED_COL]
    motorist_injured = data[MOTORIST_INJURED_COL]
    motorist_killed = data[MOTORIST_KILLED_COL]

    generate_street_data(on_street_name, zip_code, pedestrians_injured, pedestrians_killed, cyclist_injured, cyclist_killed, motorist_injured, motorist_killed)

    generate_street_data(cross_street_name, zip_code, pedestrians_injured, pedestrians_killed, cyclist_injured, cyclist_killed, motorist_injured, motorist_killed)

    generate_street_data(off_street_name, zip_code, pedestrians_injured, pedestrians_killed, cyclist_injured, cyclist_killed, motorist_injured, motorist_killed)
