import csv
import json
from io import StringIO
from urllib.parse import urljoin
from lxml import etree
import requests


def __retrieve_keys(url):
    r = requests.get(url)
    r.encoding = 'utf-8'

    sio = StringIO(r.content.decode('utf-8'))
    sb_csv = csv.reader(sio, delimiter=';')

    # Skip the first two lines
    next(sb_csv)
    next(sb_csv)

    result = {row[0]: row[1] for row in sb_csv}
    return result


def __retrieve_xml(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    elem = etree.fromstring(r.content)
    data = []
    for member in elem:
        data_elem = {}
        for attr in member:
            data_elem[attr.tag] = attr.text

        data.append(data_elem)

    return data


def crawl_data():
    base_url_nrw = 'https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/'

    schulbetrieb = __retrieve_keys(urljoin(base_url_nrw, 'key_schulbetriebsschluessel.csv'))
    schulform = __retrieve_keys(urljoin(base_url_nrw, 'key_schulformschluessel.csv'))
    rechtsform = __retrieve_keys(urljoin(base_url_nrw, 'key_rechtsform.csv'))
    schuelerzahl = __retrieve_keys(urljoin(base_url_nrw, 'SchuelerGesamtZahl/anzahlen.csv'))

    traeger_raw = __retrieve_xml(urljoin(base_url_nrw, 'key_traeger.xml'))
    traeger = {x['Traegernummer']: x for x in traeger_raw}

    r = requests.get(urljoin(base_url_nrw, 'schuldaten.xml'))
    r.encoding = 'utf-8'
    elem = etree.fromstring(r.content)
    data = []
    for member in elem:
        data_elem = {}

        for attr in member:
            data_elem[attr.tag] = attr.text

            if attr.tag == 'Schulnummer':
                data_elem['Schuelerzahl'] = schuelerzahl.get(attr.text)

            if attr.tag == 'Schulbetriebsschluessel':
                data_elem['Schulbetrieb'] = schulbetrieb[attr.text]

            if attr.tag == 'Schulform':
                data_elem['Schulformschluessel'] = attr.text
                data_elem['Schulform'] = schulform[attr.text]

            if attr.tag == 'Rechtsform':
                data_elem['Rechtsformschluessel'] = attr.text
                data_elem['Rechtsform'] = rechtsform[attr.text]

            if attr.tag == 'Traegernummer':
                data_elem['Traeger'] = traeger.get(attr.text)

        data.append(data_elem)
    print('Parsed ' + str(len(data)) + ' data elements')
    return data


def normalize(data):
    normalized_data = []
    for row in data:
        school_dict = {
            'id': 'NRW-{}'.format(row['Schulnummer']),
            'name': row['Schulbezeichnung_1'],
            'address': row['Strasse'],
            'zip': row['PLZ'],
            'city': row['Ort'],
            'school_type': row['Schulform'],
            'phone': row['Telefonvorwahl'] + row['Telefon'] if row['Telefonvorwahl'] != None and row['Telefon'] != None else '',
            'fax': row['Faxvorwahl'] + row['Fax'] if row['Faxvorwahl'] != None and row['Fax'] != None else '',
            'email': row['E-Mail'],
            'website': row['Homepage']
        }
        normalized_data.append({'info': school_dict})
            
    with open('data/nordrhein-westfalen.json', 'w') as json_file:
        json_file.write(json.dumps(normalized_data))


def crawl_nrw():
    return normalize(crawl_data())