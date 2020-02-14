import json
import csv
import os
import glob
import re
import pandas as pd
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
                id          = row['info']['id'] if 'id' in row['info'] else '',
                name        = row['info']['name'],
                address     = row['info']['address'],
                zip         = row['info'].get('zip'),
                city        = row['info'].get('city'),
                school_type = row['info']['school_type'] if 'school_type' in row['info'] else '',
                phone       = fix_phone_and_fax(row['info']['phone']),
                fax         = fix_phone_and_fax(row['info']['fax'] if 'fax' in row['info'] else ''),
                email       = row['info']['email'] if 'email' in row['info'] else '',
                website     = row['info']['website'] if 'website' in row['info'] else '',
            )

            output.writerow(s)


def fix_phone_and_fax(number):
    if number is not None:                
        number = number.split('oder')[0]  # sometimes there are two number with 'oder' in between: Just take the first one
        regex = re.compile('[")(\t;\xa0+/ -]')
        fixed_number = regex.sub('', number)
        return fixed_number.strip()


def combine_states():
    dtype_dict = {'id'          : str,    
                 'name'        : str,
                 'address'     : str,
                 'zip'         : str,
                 'city'        : str,
                 'school_type' : str,
                 'phone'       : str,
                 'fax'         : str,
                 'email'       : str,
                 'website'     : str,
                 }

    full_data = pd.DataFrame(columns=School._fields)

    for file_name in glob.glob('data/*.csv'):
        cur_file = pd.read_csv(file_name, dtype=dtype_dict)
        full_data = full_data.append(cur_file)
   
    full_data = full_data[full_data['zip'] != '0']        # remove test rows
    full_data.drop_duplicates(subset=['id'], inplace=True)

    full_data.to_csv("data/full_school_data.csv", index=False)

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
    # for state in STATES:
    #     print('Normalize', state)
    #     normalize(state)

    print('Create combined csv..')
    combine_states()