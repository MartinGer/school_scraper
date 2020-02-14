import json
import csv
import os
import glob
from collections import namedtuple

BASE_PATH = '.'

School = namedtuple('School',
                    ['id', 'name', 'address', 'zip', 'city', 'school_type', 'phone', 'fax', 'email',
                     'website'])


def normalize(state):
    with open(os.path.join(BASE_PATH, 'data/{}.json'.format(state)), encoding="utf8") as f:
        data = json.load(f)
    with open(os.path.join(BASE_PATH, 'data/{}.csv'.format(state)), 'w', newline='', encoding="utf8") as f:
        output = csv.writer(f)
        output.writerow(School._fields)

        for row in data:
            s = School(
                id=row['info']['id'] if 'id' in row['info'] else '',
                name=row['info']['name'],
                address=row['info']['address'],
                zip=row['info'].get('zip'),
                city=row['info'].get('city'),
                school_type=row['info']['school_type'] if 'school_type' in row['info'] else '',
                phone=row['info']['phone'],
                fax=row['info']['fax'] if 'fax' in row['info'] else '',
                email=row['info']['email'] if 'email' in row['info'] else '',
                website=row['info']['website'] if 'website' in row['info'] else '',
            )

            output.writerow(s)


STATES = [
    'baden-württemberg',
    'bayern',
    'berlin',
    'brandenburg',
    'bremen',
    'hamburg',
    'hessen',
    'niedersachsen',
    'nordrhein-westfalen',
    'mecklenburg-vorpommern',
    'rheinland-pfalz',
    'saarland',
    'sachsen',
    'schleswig-holstein',
    'sachsen-anhalt',
    'thueringen'
]

if __name__ == '__main__':
    for state in STATES:
        normalize(state)
