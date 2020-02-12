import json
import csv
import os
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



def normalize_nrw():
    state = 'nrw'
    with open(os.path.join(BASE_PATH, 'data/{}.json'.format(state)), encoding="utf8") as f:
        data = json.load(f)
    with open(os.path.join(BASE_PATH, 'data/{}.csv'.format(state)), 'w', newline='', encoding="utf8") as f:
        output = csv.writer(f)
        output.writerow(School._fields)

        for row in data:
            s = School(
                id='NRW-{}'.format(row['Schulnummer']),
                name=row['Schulbezeichnung_1'],
                address=row['Strasse'],
                address2='',
                zip=row['PLZ'],
                city=row['Ort'],
                school_type=row['Schulform'],
                phone=row['Telefonvorwahl'] + row['Telefon'] if row['Telefonvorwahl'] != None and row['Telefon'] != None else '',
                fax=row['Faxvorwahl'] + row['Fax'] if row['Faxvorwahl'] != None and row['Fax'] != None else '',
                email=row['E-Mail'],
                website=row['Homepage']
            )
            output.writerow(s)


if __name__ == '__main__':
    # normalize('baden-württemberg')
    # normalize('bayern')
    # normalize('berlin')
    # normalize('brandenburg')
    # normalize('bremen')
    # normalize('hamburg')
    # normalize_mv()
    # normalize('niedersachsen')
    # normalize_nrw()
    normalize('mecklenburg-vorpommern')
    # normalize('rheinland-pfalz')
    # normalize('saarland')
    # normalize('sachsen')
    # normalize('schleswig-holstein')
    # normalize('sachsen-anhalt')
    # normalize('thueringen')
    
