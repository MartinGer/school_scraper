# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item
from scrapy.shell import inspect_response

import requests
import wget
import xlrd
import json
import os
from urllib.parse import urljoin
from twisted.internet import reactor, defer

from jedeschule.items import School

def crawl_mvp():
    filename = 'mv.xlsx'
    url_mv = 'http://service.mvnet.de/_php/download.php?datei_id=1619185'
    wget.download(url_mv, filename)
    workbook = xlrd.open_workbook(filename)
    sheets = ['Schulverzeichnis öffentl. ABS', 'Schulverzeichnis öffentl. BLS','Schulverzeichnis freie ABS']

    legend = {
        'schulart': {
            'Agy': 'Abendgymnasium',
            'FöL': 'Schule mit dem Förderschwerpunkt Lernen',
            'FöS': 'Schule mit dem Förderschwerpunkt Sehen',
            'FöSp': 'Schule mit dem Förderschwerpunkt Sprache',
            'FöK': 'Schule mit dem Förderschwerpunkt körperliche und motorische Entwicklung',
            'FöK/GS': 'Schule mit dem Förderschwerpunkt körperliche und motorische Entwicklung mit Grundschule',
            'FöG': 'Schule mit dem Förderschwerpunkt geistige Entwicklung',
            'FöKr': 'Schule mit dem Förderschwerpunkt Unterricht kranker Schülerinnen und Schüler',
            'FöL/FöG': 'Schule mit dem Förderschwerpunkt Lernen und  dem Förderschwerpunkt geistige Entwicklung',
            'FöV': 'Schule mit dem Förderschwerpunkt emotionale und soziale Entwicklung',
            'FöV/FöKr': 'Schule mit dem Förderschwerpunkt emotionale und soziale Entwicklung und dem Förderschwerpunkt Unterricht kranker Schülerinnen und Schüler',
            'FöV/FöL': 'Schule mit dem Förderschwerpunkt emotionale und soziale Entwicklung und dem Förderschwerpunkt Lernen)',
            'FöL/FöV/FöKr': 'Schule mit den Förderschwerpunkten Lernen, dem Förderschwerpunkt emotionale und soziale Entwicklung sowie dem Förderschwerpunkt Unterricht kranker Schülerinnen und Schüler',
            'FöH': 'Schule mit dem Förderschwerpunkt Hören',
            'GS': 'Grundschule',
            'GS/OS': 'Grundschule mit schulartunabhängiger Orientierungsstufe',
            'GS/FöSp': 'Grundschule mit selbstständigen Klassen mit dem Förderschwerpunkt Sprache',
            'GS/OS/Gy': 'Grundschule mit schulartunabhängiger Orientierungsstufe und Gymnasium',
            'Gy': 'Gymnasium',
            'Gy/GS/OS': 'Gymnasium mit Grundschule und schulartunabhängiger Orientierungsstufe',
            'Gy/RegS/GS': 'Gymnasium mit Regionaler Schule und Grundschule',
            'IGS': 'Integrierte Gesamtschule',
            'IGS/GS': 'Integrierte Gesamtschule mit Grundschule',
            'IGS/GS/FöG': 'Integrierte Gesamtschule mit Grundschule  und Schule mit dem Förderschwerpunkt geistige Entwicklung',
            'KGS': 'Kooperative Gesamtschule',
            'KGS/GS': 'Kooperative Gesamtschule mit Grundschule',
            'KGS/GS/\nFöL': 'Kooperative Gesamtschule mit Grundschule und Schule mit dem Förderschwerpunkt Lernen',
            'RegS': 'Regionale Schule',
            'RegS/GS': 'Regionale Schule mit Grundschule',
            'RegS/Gy': 'Regionale Schule mit Gymnasium',
            'WS': 'Waldorfschule'
        },
        'schulamt': {
            'GW': 'Greifswald',
            'NB': 'Neubrandenburg',
            'RO': 'Rostock',
            'SN': 'Schwerin'
        },
        'landkreis': {
            'HRO': 'Hansestadt Rostock',
            'SN': 'Landeshauptstadt Schwerin',
            'LRO': 'Landkreis Rostock',
            'LUP': 'Landkreis Ludwigslust-Parchim',
            'MSE': 'Landkreis Mecklenburgische Seenplatte',
            'NWM': 'Landkreis Nordwestmecklenburg',
            'VG': 'Landkreis Vorpommern-Greifswald',
            'VR': 'Landkreis Vorpommern-Rügen'
        }
    }
    data = []
    for sheet in sheets:
        worksheet = workbook.sheet_by_name(sheet)
        keys = [v.value for v in worksheet.row(0)]
        for row_number in range(worksheet.nrows):
            if row_number == 0:
                continue
            row_data = {}
            for col_number, cell in enumerate(worksheet.row(row_number)):
                row_data[keys[col_number]] = cell.value
            data.append(row_data)

    with open('data/mecklenburg-vorpommern.json', 'w') as json_file:
        json_file.write(json.dumps(data))
    os.remove(filename)




def normalize_mv():
    state = 'mecklenburg-vorpommern'
    with open(os.path.join(BASE_PATH, 'data/{}.json'.format(state)), encoding="utf8") as f:
        data = json.load(f)
    with open(os.path.join(BASE_PATH, 'data/{}.csv'.format(state)), 'w', newline='', encoding="utf8") as f:
        output = csv.writer(f)
        output.writerow(School._fields)

        for row in data:
            if isinstance(row['Dst-Nr.:'], float):
                school_id = int(row['Dst-Nr.:'])
            else:
                school_id = row['Dst-Nr.:']

            try:
                schulart = row['Schulart/ Org.form']
            except:
                schulart = row['Schulart/\nOrg.form']

            s = School(
                id='MV-{}'.format(school_id),
                name=row['Schulname'],
                address=row['Straße, Haus-Nr.'],
                address2='',
                zip=str(int(float(row['Plz']))) if row['Plz'] != '' else '',
                city=row['Ort'],
                school_type=schulart,
                phone=row['Telefon'],
                fax=row['Telefax'],
                email=row['E-Mail'],
                website=row['Homepage']
            )

            output.writerow(s)