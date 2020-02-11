# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item
from scrapy.shell import inspect_response

import requests
import csv
import json
from lxml import etree
from io import StringIO
from urllib.parse import urljoin
from jedeschule.utils import get_first_or_none, cleanjoin


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


def crawl_nrw():
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
    with open('data/nrw.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data))
