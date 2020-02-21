# jedeschule-scraper
This scraper is based on https://github.com/Datenschule/jedeschule-scraper
It crawls the school data from the 16 different states of Germany as JSON files in different format and with different data depending on the websites where the school data is crawled. 
After that the files then can be normalized in 16 different and also be combined to one uniform CSV file.
# Pretty session protocols

## Installation
```bash
pip install -r requirements.txt
```

## Running:

Crawl the data, this will take quite a while. The script will generate a new directory "data". The result of each scraper is available as json file:
```bash
./run.py
```

Postprocess the files to uniform CSV files and one combined CSV file with all schools called full_school_data.csv.
Columns are id, name, address, zip, city, school_type, phone, fax, email and website:
```bash
./normalize.py
```

Additionally  use the run_scripts.py file to start both scripts together:
```bash
./run_scripts.py
```

## Docker:

You can also use docker to run the crawler and output your files. 

The Dockerfile is included in the repository. To build it use 
```bash
docker build --tag school_crawler .
```

and run it by matching the output "data" folder to a choosen local folder, for example
```bash
docker run -v $(pwd):/data school_crawler
```



## Sources:
* Schulverzeichnis Baden-Württemberg: ['https://lobw.kultus-bw.de/didsuche/'](https://lobw.kultus-bw.de/didsuche/)
* Schulverzeichnis Bayern: ['https://www.km.bayern.de/schueler/schulsuche.html?s=&t=9999&r=9999&o=9999&u=0&m=3&seite=1'](https://www.km.bayern.de/schueler/schulsuche.html?s=&t=9999&r=9999&o=9999&u=0&m=3&seite=1)
* Schulportraits Brandenburg: ['https://bildung-brandenburg.de/schulportraets/index.php?id=uebersicht'](https://bildung-brandenburg.de/schulportraets/index.php?id=uebersicht)
* Schulwegweiser Bremen: [http://www.bildung.bremen.de/detail.php?template=35_schulsuche_stufe2_d](http://www.bildung.bremen.de/detail.php?template=35_schulsuche_stufe2_d)
* Schulverzeichnis Hamburg: ['https://geoportal-hamburg.de/geodienste_hamburg_de/HH_WFS_Schulen?REQUEST=GetFeature&SERVICE=WFS&SRSNAME=EPSG%3A25832&TYPENAME=staatliche_schulen&VERSION=1.1.0'](https://geoportal-hamburg.de/geodienste_hamburg_de/HH_WFS_Schulen?REQUEST=GetFeature&SERVICE=WFS&SRSNAME=EPSG%3A25832&TYPENAME=staatliche_schulen&VERSION=1.1.0)
* Schuldaten Hessen: ['https://statistik.hessen.de/sites/statistik.hessen.de/files/Verz-6_19.xlsx'](https://statistik.hessen.de/sites/statistik.hessen.de/files/Verz-6_19.xlsx)
* Schuldaten Mecklenburg-Vorpommern: ['http://service.mvnet.de/_php/download.php?datei_id=1619185'](http://service.mvnet.de/_php/download.php?datei_id=1619185)
* Schulverzeichnis Niedersachsen: ['http://schulnetz.nibis.de/db/schulen/suche_2.php'](http://schulnetz.nibis.de/db/schulen/suche_2.php)
* Schulverzeichnis "Schule suchen" NRW:['https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/'](https://www.schulministerium.nrw.de/BiPo/OpenData/Schuldaten/)
* Rheinland Pfalz: ['https://www.statistik.rlp.de/service/adress-suche/'](https://www.statistik.rlp.de/service/adress-suche/)
* Schuladressen Saarland: ['https://www.saarland.de/schuldatenbank.htm?typ=alle&ort='](https://www.saarland.de/schuldatenbank.htm?typ=alle&ort=)
* Schulsuche Sachsen Anhalt: ['https://www.bildung-lsa.de/ajax.php?m=getSSResult&q=&lk=-1&sf=-1&so=-1&timestamp=1480082277128/'](https://www.bildung-lsa.de/ajax.php?m=getSSResult&q=&lk=-1&sf=-1&so=-1&timestamp=1480082277128/)
* Schuldatenbank Sachsen: ['https://schuldatenbank.sachsen.de/index.php?id=2'](https://schuldatenbank.sachsen.de/index.php?id=2)
* Schulportrait Schleswig Holstein: ['https://www.secure-lernnetz.de/schuldatenbank/'](https://www.secure-lernnetz.de/schuldatenbank/)
* Schulportal Thüringen: ['https://www.schulportal-thueringen.de/tip/schulportraet_suche/search.action?tspi=&tspm=&vsid=none&mode=&extended=0&anwf=schulportraet&freitextsuche=&name=&schulnummer=&strasse=&plz=&ort=&schulartDecode=&schulamtDecode=&schultraegerDecode=&sortierungDecode=Schulname&rowsPerPage=999&schulartCode=&schulamtCode=&schultraegerCode=&sortierungCode=10&uniquePortletId=portlet_schulportraet_suche_WAR_tip_LAYOUT_10301'](https://www.schulportal-thueringen.de/tip/schulportraet_suche/search.action?tspi=&tspm=&vsid=none&mode=&extended=0&anwf=schulportraet&freitextsuche=&name=&schulnummer=&strasse=&plz=&ort=&schulartDecode=&schulamtDecode=&schultraegerDecode=&sortierungDecode=Schulname&rowsPerPage=999&schulartCode=&schulamtCode=&schultraegerCode=&sortierungCode=10&uniquePortletId=portlet_schulportraet_suche_WAR_tip_LAYOUT_10301)
