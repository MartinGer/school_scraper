from jedeschule.spiders.school_spider import SchoolSpider


class SchoolPipeline(object):
<<<<<<< HEAD
    def process_item(self, item, spider: SchoolSpider):
        school = spider.normalize(item)
=======
    def process_item(self, item, spider):
        if spider.name == 'saarland':
            address = u"{} {}".format(item.get('street', ""), item.get('zip', ""))
            if item.get('email'):
                email = item['email'].replace('mailto:', '').replace('%40', '@')
            else:
                email = None
            school = School(name=item.get('name'),
                            phone=item.get('telephone'),
                            director=item.get('telephone'),
                            website=item.get('website'),
                            fax=item.get('fax'),
                            email=email,
                            address=address)
        elif spider.name == 'niedersachsen':
            address = u"{} {}".format(item.get('Straße', ""), item.get('Ort', ""))
            school = School(name=item.get('Schule'),
                            phone=item.get('Tel'),
                            email=item.get('E-Mail'),
                            website=item.get('Homepage'),
                            address=address,
                            id='NDS-{}'.format(item.get('Schulnummer')))
        elif spider.name == 'bayern':
            school = School(name=item.get('Name'),
                            phone=item.get('Telefon'),
                            website=item.get('website'),
                            address=item.get('Anschrift'),
                            id='BAY-{}'.format(item.get('Schulnummer')))
        elif spider.name == 'thueringen':
            school = School(name=item.get('Schulname'),
                            id='TH-{}'.format(item.get('Schulnummer')),
                            address=u"{} {}".format(item.get('Straße'), item.get('Ort')),
                            website=item.get('Internet'),
                            email=item.get('E-Mail'),
                            school_type=item.get('Schulart'),
                            provider=item.get('Schulträger'),
                            fax=item.get('Telefax'),
                            phone=item.get('Telefon'))
        elif spider.name == 'schleswig-holstein':
            school = School(name=item.get('Name'),
                            id='SH-{}'.format(item.get('Dienststellen Nr.')),
                            address=u"{} {} {}".format(item.get('Straße'), item.get("PLZ"), item.get("Ort")),
                            email=item.get('EMail'),
                            school_type=item.get('Organisationsform'),
                            legal_status=item.get('Rechtsstatus'),
                            provider=item.get('Träger'),
                            fax=item.get('Fax'),
                            phone=item.get('Telefon'),
                            director=item.get('Schulleiter(-in)'))
        elif spider.name == 'bremen':
            ansprechpersonen = item['Ansprechperson'].replace('Schulleitung:', '').replace('Vertretung:', ',').split(',')
            item['Schulleitung'] = ansprechpersonen[0]
            item['Vertretung'] = ansprechpersonen[1]
            school = School(name=item.get('name'),
                            address=item.get('Anschrift:'),
                            website=item.get('Internet'),
                            email=item.get('E-Mail-Adresse'),
                            fax=item.get('Telefax'),
                            phone=item.get('Telefon'))
        elif spider.name == 'sachsen':
            school = School(name=item.get('title'),
                            id='SN-{}'.format(item.get('Dienststellenschlüssel')),
                            address=item.get('Postanschrift'),
                            website=item.get('Homepage'),
                            email=item.get('E-Mail'),
                            school_type=item.get('Einrichtungsart'),
                            legal_status=item.get('Rechtsstellung'),
                            provider=item.get('Schulträger'),
                            fax=item.get('Telefax'),
                            phone=item.get('phone_numbers'),
                            director=item.get('Schulleiter'))
        elif spider.name == 'sachsen-anhalt':
            school = School(name=item.get('Name'),
                            address=item.get('Addresse'),
                            website=item.get('Homepage'),
                            email=item.get('E-Mail'),
                            fax=item.get('Fax'),
                            phone=item.get('Telefon')
                            )
        elif spider.name == 'brandenburg':
            school = School(
                name=item.get('name'),
                id=item.get('nummer'),
                address=item.get('Adresse'),
                website=item.get('Internet'),
                email=item.get('E-Mail'),
                school_type=item.get('Schulform'),
                provider=item.get('Schulamt'),
                fax=item.get('Fax'),
                phone=item.get('Telefon'),
                director=item.get('Schulleiter/in'))
        elif spider.name == 'rheinland-pfalz':
            school = School(name=item.get('name'),
                            address=item.get('Adresse'),
                            website=item.get('Internet'),
                            email=item.get('E-Mail'),
                            school_type=item.get('Schulform'),
                            fax=item.get('Fax'),
                            phone=item.get('Telefon'))
        else:
            return item
            raise DropItem("Missing name in %s" % item)
>>>>>>> d4015adf9440234ad6ccacb664ed895372a4927a
        return {'info': school, 'item': item}
