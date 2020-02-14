import json
import os
import wget
import xlrd


LEGEND = {
    'Agy': 'Abendgymnasium',
    'BLS': 'Berufliche Schule',
    'FöL': 'Schule mit dem Förderschwerpunkt Lernen',
    'FöS': 'Schule mit dem Förderschwerpunkt Sehen',
    'FöSp': 'Schule mit dem Förderschwerpunkt Sprache',
    'FöK': 'Schule mit dem Förderschwerpunkt körperliche und motorische Entwicklung',
    'FöK/GS': 'Schule mit dem Förderschwerpunkt körperliche und motorische Entwicklung mit Grundschule',
    'FöK/FöSp': 'Schule mit dem Förderschwerpunkt körperliche und motorische Entwicklung und mit dem Förderschwerpunkt Sprache',
    'FöG': 'Schule mit dem Förderschwerpunkt geistige Entwicklung',
    'FöG/FöKr': 'Schule mit dem Förderschwerpunkt geistige Entwicklung und mit dem Förderschwerpunkt Unterricht kranker Schülerinnen und Schüler',
    'FöKr': 'Schule mit dem Förderschwerpunkt Unterricht kranker Schülerinnen und Schüler',
    'FöL/FöG': 'Schule mit dem Förderschwerpunkt Lernen und dem Förderschwerpunkt geistige Entwicklung',
    'FöL/FöV': 'Schule mit dem Förderschwerpunkt Lernen und dem Förderschwerpunkt emotionale und soziale Entwicklung',
    'FöL/FöKr': 'Schule mit dem Förderschwerpunkt Lernen und dem Förderschwerpunkt Unterricht kranker Schülerinnen und Schüler',
    'FöL/FöSp': 'Schule mit dem Förderschwerpunkt Lernen und mit dem Förderschwerpunkt Sprache',
    'FöL/FöV/FöSp': 'Schule mit dem Förderschwerpunkt Lernen, dem Förderschwerpunkt emotionale und soziale Entwicklung und mit dem Förderschwerpunkt Sprache',
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
    'Gy/OS': 'Gymnasium mit schulartunabhängiger Orientierungsstufe',
    'Gy/GS/OS': 'Gymnasium mit Grundschule und schulartunabhängiger Orientierungsstufe',
    'Gy/RegS/GS': 'Gymnasium mit Regionaler Schule und Grundschule',
    'Gy/RegS': 'Gymnasium mit Regionaler Schule',
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
}


def crawl_data():
    filename = 'mv.xlsx'
    url_mv = 'http://service.mvnet.de/_php/download.php?datei_id=1619185'
    wget.download(url_mv, filename)
    workbook = xlrd.open_workbook(filename)
    sheets = ['Schulverzeichnis öffentl. ABS', 'Schulverzeichnis öffentl. BLS','Schulverzeichnis freie ABS']

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

    os.remove(filename)
    return data


def normalize(data):
    normalized_data = []
    for row in data:
        if isinstance(row['Dst-Nr.:'], float):
            school_id = int(row['Dst-Nr.:'])
        else:
            school_id = row['Dst-Nr.:']

        if school_id != '':
            try:
                schulart = row['Schulart/ Org.form']
            except:
                schulart = row['Schulart/\nOrg.form']

            school_dict = {
                'id': 'MV-{}'.format(school_id),
                'name': row['Schulname'],
                'address': row['Straße, Haus-Nr.'],
                'zip': str(int(float(row['Plz']))) if row['Plz'] != '' else '',
                'city': row['Ort'],
                'school_type': LEGEND[schulart],
                'phone': row['Telefon'],
                'fax': row['Telefax'],
                'email': row['E-Mail'],
                'website': row['Homepage']
            }
            normalized_data.append({'info': school_dict})
            
    with open('data/mecklenburg-vorpommern.json', 'w') as json_file:
        json_file.write(json.dumps(normalized_data))


def crawl_mvp():
    return normalize(crawl_data())