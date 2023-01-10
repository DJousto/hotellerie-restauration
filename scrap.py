#!/usr/bin/env python
# coding: utf-8

from requests_html import HTMLSession
import re
import pandas as pd
import warnings
import json
warnings.filterwarnings("ignore")
session = HTMLSession()

# lecture des anciennes offres déjà scrapées si existantes
try:
    anciennes_offres = pd.read_excel('./annonces.xls')
except:
    print('Ancien fichier non trouvé, scrap de toutes les offres')
    anciennes_offres = pd.DataFrame()


# liste des départements permettant de générer les urls
departements = ["/emploi/offre/ain-01","/emploi/offre/aisne-02","/emploi/offre/allier-03","/emploi/offre/alpes-maritimes-06","/emploi/offre/alpes-de-haute-provence-04","/emploi/offre/ardeche-07","/emploi/offre/ardennes-08","/emploi/offre/ariege-09","/emploi/offre/aube-10","/emploi/offre/aude-11","/emploi/offre/aveyron-12","/emploi/offre/bas-rhin-67","/emploi/offre/bouches-du-rhone-13","/emploi/offre/calvados-14","/emploi/offre/cantal-15","/emploi/offre/charente-16","/emploi/offre/charente-maritime-17","/emploi/offre/cher-18","/emploi/offre/correze-19","/emploi/offre/corse-20","/emploi/offre/cote-d-or-21","/emploi/offre/cotes-d-armor-22","/emploi/offre/creuse-23","/emploi/offre/deux-sevres-79","/emploi/offre/dordogne-24","/emploi/offre/doubts-25","/emploi/offre/drome-26","/emploi/offre/essonne-91","/emploi/offre/eure-27","/emploi/offre/eure-et-loir-28","/emploi/offre/finistere-29","/emploi/offre/gard-30","/emploi/offre/gers-32","/emploi/offre/gironde-33","/emploi/offre/haute-garonne-31","/emploi/offre/haute-loire-43","/emploi/offre/haute-marne-52","/emploi/offre/haute-saone-70","/emploi/offre/haute-savoie-74","/emploi/offre/haute-vienne-87","/emploi/offre/hautes-pyrenees-65","/emploi/offre/hautes-alpes-05","/emploi/offre/haut-rhin-68","/emploi/offre/hauts-de-seine-92","/emploi/offre/herault-34","/emploi/offre/ille-et-vilaine-35","/emploi/offre/indre-36","/emploi/offre/indre-et-loire-37","/emploi/offre/isere-38","/emploi/offre/jura-39","/emploi/offre/landes-40","/emploi/offre/loire-42","/emploi/offre/loire-atlantique-44","/emploi/offre/loiret-45","/emploi/offre/loir-et-cher-41","/emploi/offre/lot-46","/emploi/offre/lot-et-garonne-47","/emploi/offre/lozere-48","/emploi/offre/maine-et-loire-49","/emploi/offre/manche-50","/emploi/offre/marne-51","/emploi/offre/mayenne-53","/emploi/offre/meurthe-et-moselle-54","/emploi/offre/meuse-55","/emploi/offre/morbihan-56","/emploi/offre/moselle-57","/emploi/offre/nievre-58","/emploi/offre/nord-59","/emploi/offre/oise-60","/emploi/offre/orne-61","/emploi/offre/paris-75","/emploi/offre/pas-de-calais-62","/emploi/offre/puy-de-dome-63","/emploi/offre/pyrenees-atlantiques-64","/emploi/offre/pyrenees-orientales-66","/emploi/offre/rhone-69","/emploi/offre/saone-et-loire-71","/emploi/offre/sarthe-72","/emploi/offre/savoie-73","/emploi/offre/seine-maritime-76","/emploi/offre/seine-et-marne-77","/emploi/offre/seine-saint-denis-93","/emploi/offre/somme-80","/emploi/offre/tarn-81","/emploi/offre/tarn-et-garonne-82","/emploi/offre/territoire-de-belfort-90","/emploi/offre/tout-outre-mer-160","/emploi/offre/val-de-marne-94","/emploi/offre/val-d-oise-95","/emploi/offre/var-83","/emploi/offre/vaucluse-84","/emploi/offre/vendee-85","/emploi/offre/vienne-86","/emploi/offre/vosges-88","/emploi/offre/yonne-89","/emploi/offre/yvelines-78"]
urls_offres = set()

# boucle sur tous les départements
for departement in departements:
    print(f'departement {departement}')
    url_dep = "https://www.lhotellerie-restauration.fr"+departement
    page = session.get(url_dep)
    # récupération des catégories disponibles pour le département courant
    categories = page.html.xpath('//a[.//h2]/@href')
    for categorie in categories:
        print(f'categorie {categorie}')
        url_categorie = "https://www.lhotellerie-restauration.fr"+categorie
        # récupération de la page de la categorie en question
        page_cat = session.get(url_categorie)
        # récupération des urls des offres d'emploi de la page
        nouvelles_offres = page_cat.html.xpath('//a[contains(@href,"/emploi/") and (contains(@class,"job"))]/@href')
        urls_offres = urls_offres.union(nouvelles_offres)
        print(f'{len(nouvelles_offres)} offres')
        # tant qu'il y a une "page suivante" on la charge
        while len(page_cat.html.xpath('//a[@aria-label="Next"]/@href')):
            print('nouvelle page')
            page_cat = session.get("https://www.lhotellerie-restauration.fr"+page_cat.html.xpath('//a[@aria-label="Next"]/@href')[0])
            nouvelles_offres = page_cat.html.xpath('//a[contains(@href,"/emploi/") and (contains(@class,"job"))]/@href')
            urls_offres = urls_offres.union(nouvelles_offres)
            print(f'{len(nouvelles_offres)} offres')

# urls_offres contient la liste des urls des pages détaillées de chaque offre d'emploi
print(f'Nombre total d\'offres d\'emploi : {len(urls_offres)}')
if len(anciennes_offres):
    urls_offres = urls_offres.difference(list(anciennes_offres.url))
    print(f'Nombre de nouvelles offres : {len(urls_offres)}')


# data va contenir nos données, url de l'offre, mail, téléphone, recruteur
data = pd.DataFrame()
nb_offres = len(set(urls_offres))
print('Debut scraping offres')
for i,url_offre in enumerate(set(urls_offres)):
    print(f'\r{i+1} / {nb_offres}',end='')
    offre = dict()
    offre['url'] = url_offre
    page = session.get("https://www.lhotellerie-restauration.fr"+url_offre)
    if page.status_code!=200:
        print(url_offre, " erreur")
        #break
    offre['lieu'] = page.html.xpath('//small[.//i[@class="icon-map"]]/text()')[0]
    try:
        liste = page.html.xpath('//p[@id="offerText"]/span[contains(@class,"icon")]/@class')
        offre['email'] = "".join([x.replace('point','.').replace('arobase','@').replace('tiret','-').replace('underscore','_')[-1] for x in liste])
    except:
        pass
    infos = json.loads(page.html.xpath('//script[@type="application/ld+json" and contains(text(),"hiringOrganization")]/text()')[0].strip().replace('\r','').replace('\n','').replace('\t',''))
    offre['recruteur'] = infos['hiringOrganization']['name']
    tel = re.findall(r'\d\d[^\d]?\d\d[^\d]?\d\d[^\d]?\d\d[^\d]?\d\d',  infos['description'])
    if len(tel):
        offre['telephone'] = tel[0]
    data=data.append(offre,ignore_index=True)

# enregistrement sous format excel
data.to_excel('./nouvelles_annonces.xls', index=False)
if len(anciennes_offres):
    data.append(anciennes_offres).to_excel('./annonces.xls', index=False, encoding='utlf8')
else:
    data.to_excel('./annonces.xls', index=False, encoding='utlf8')



