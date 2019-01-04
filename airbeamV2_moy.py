#dataExemple=['Temperature', 'Counts', '8', 'Plantower', 'Counts', '1', 'Airbeam2', 'MAC', '0018961054F1', 'Firmware', 'v11.5.18', '78F', '26C', '299K', '56RH', 'PM1', '3', 'PM2.5', '7', 'PM10', '9']


"""Script pour importer des donnees issues de l airbeam V2
modifié avec affichage temperature en degre celsius"""

#Liste des modules à importer
from serial import *
import datetime as datetime
import pytz
from datetime import timedelta
import os as os
import time
from influxdb import InfluxDBClient
import argparse

import variables #Fichier avec les variables
import airbeamFunction #Fichier description et fonctions propres à airbeams

tz=pytz.timezone('Europe/Paris')
deb=datetime.datetime.now()  #Date de début execution du script
debText=deb.strftime('%Y-%m-%d %H:%M:%S')


#Paramètres de la base InfluxDB #######################################################
#InfluxDB est la base de données qui collecte les résultats des mesures
bdd='airbeam2in' #Nom de la base InfluxDB
if bdd not in variables.bddInflux.keys(): print("Attention: {0} n est pas une base Influx".format(bdd))

client = InfluxDBClient(variables.bddInflux[bdd]['serveur'], variables.bddInflux[bdd]['port'], variables.bddInflux[bdd]['login'],variables.bddInflux[bdd]['mdp'],variables.bddInflux[bdd]['nom'])
influx = True #Mettre True pour permettre ecriture des données dans la base InfluxDB
#######################################################################################


#Integration temporelle ##############################################################
#Gestion du moyennage temporel acquisition sur port serie
sampleTime= 3  #nbre d'échantillons de données
json_bodySum={
              "fields":{
                        "F":0,
                        "C":0,
                        "RH":0,
                        "PM1":0,
                        "PM2.5":0,
                        "PM10":0}}

def json_bodySumIni():
    """Fonction pour initialiser le json à envoyer à InfluxDB"""
    r={
              "fields":{
                        "F":0,
                        "C":0,
                        "RH":0,
                        "PM1":0,
                        "PM2.5":0,
                        "PM10":0}}
    return r
    

#######################################################################################



#Parseur #############################################################################
#Le parseur definit les paramètres à compléter lors du lancement du script
#Dans le cadre de ce script il s'agit du numéro du device et du site de mesures
description="""description"""
parseur=argparse.ArgumentParser(description=description)
parseur.add_argument('-d','--device',dest='device',default='ttyACM0',help='device dans /dev',type=str)
parseur.add_argument('-s','--site',dest='site',default='site_test',help='site de mesures',type=str)

args=parseur.parse_args()
COM="/dev/"+args.device #Port surlequel est branché l airbeam V2
######################################################################################

# Gestion csv ########################################################################
ficDataRep = 'data'  #repertoire de stockage des résultats csv
ficData = str(args.device)+".txt"
csv = False #Mettre True pour permettre ecriture des données dans un fichier csv

def dataToCsvDevice(res):
    """Ecriture des résultats dans un fichier texte"""
    with open(ficData,'a') as fic:
        fic.write(str(res['time'])+",F: "+str(res['tempF'])+",C: "+str(res['tempC'])+",RH: "+str(res['hum'])+",PM1: "+str(res['PM1'])+",PM2.5: "+str(res['PM2.5'])+",PM10: "+str(res['PM10'])+"\r\n")       
######################################################################################


# Fonction Acquisition sur port serie #################################################
def acquisition():
    """Fonction pour lire les données sur le port serie"""
    with Serial(port=COM, baudrate=variables.baudRate) as port_serie:
        data=port_serie.readline().decode("utf-8").rstrip('\r\n')
        print("{0}{1}: {2}".format("Acquisition: ",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data))#Affichage des datas brutes récupérées sur le port serie
        return data
#######################################################################################


# Fonction Ecriture dans InfluxDB #################################################    
def insertInfluxDBRes(res):
    """Ecriture des resultats res dans la base InfluxDB"""
    json_body = [
        {
            "measurement":"particules",
            "tags":{
                        "capteur":"AirbeamV2",  #Remplacer ici par res['capteur']
                        "MAC":res['MAC'],
                        "site":args.site
                    },
                        "time":res['time'],
                        "fields": {
                                    "F": res['tempF'],
                                    "C": res['tempC'],
                                    "RH": res['hum'],
                                    "PM1":res['PM1'],
                                    "PM2.5": res['PM2.5'],
                                    "PM10": res['PM10']
                                    }
            }
        ]
    #print(json_body)
    client.write_points(json_body)
    print("Ecriture dans la base InfluxDB OK")
######################################################################



def jsonSum(json):
    """Addition des json avant division"""
    json_bodySum['fields']['F']=json['fields']['F']+json_bodySum['fields']['F']
    json_bodySum['fields']['C']=json['fields']['C']+json_bodySum['fields']['C']
    json_bodySum['fields']['RH']=json['fields']['RH']+json_bodySum['fields']['RH']
    json_bodySum['fields']['PM1']=json['fields']['PM1']+json_bodySum['fields']['PM1']
    json_bodySum['fields']['PM2.5']=json['fields']['PM2.5']+json_bodySum['fields']['PM2.5']
    json_bodySum['fields']['PM10']=json['fields']['PM10']+json_bodySum['fields']['PM10']
    return json_bodySum

def jsonSumDiv(json,den):
    """Division json"""
    json['fields']['F']=json['fields']['F']/den
    json['fields']['C']=json['fields']['C']/den
    json['fields']['RH']=json['fields']['RH']/den
    json['fields']['PM1']=json['fields']['PM1']/den
    json['fields']['PM2.5']=json['fields']['PM2.5']/den
    json['fields']['PM10']=json['fields']['PM10']/den
    return json    
        
if __name__ == '__main__':
    print('\n')
    print("***************************")
    print("Debut des mesures: ",debText)
    print("Device :",args.device)
    print("Site de mesures: ",args.site)
    print("***************************")
    print('\n')
    
    if args.device in os.listdir("/dev"):
        while True:
            i=1
            while i<=sampleTime:
                f=acquisition() #Acquisition des données sur le port serie
                if len(f)>=50 and f not in airbeamFunction.msg:
                    print(i)
                    #d,r=airbeamFunction.transformationData(f) #Pour les nouveaux firmware airbeam
                    d,r=airbeamFunction.transformationDataOld(f) #Pour les anciens firmware airbeam
                    json_bodySum=jsonSum(r) #Addition des Json data
                    json_bodySum['tags']=r['tags']
                    json_bodySum['tags']['site']=args.site
                    json_bodySum['time']=datetime.datetime.strptime(r['time'],'%Y-%m-%d %H:%M:%S').isoformat() #Conversion de la date avec fuseau horaire
                    json_bodySum['measurement']="particules"
                    print(json_bodySum)
                    i=i+1
                else:
                    print("Incomplete data or no data")
            if influx == True:
                #insertInfluxDBRes(json_bodySum) #Ecriture des resultats dans la base InfluxDB
                print("--------")
                print("Ecriture dans la base InfluxDB")
                json_bodySum=jsonSumDiv(json_bodySum,i-1)
                print(json_bodySum)
                client.write_points([json_bodySum])
            if csv == True:
                dataToCsvDevice(rjson_bodySum) #Ecriture des resultats airbeams dans un fichier csv Device
            json_bodySum=json_bodySumIni()
    else:
        print("Attention device "+str(args.device)+" n est pas dans la liste: ")
        for i in os.listdir("/dev"):
            if 'tty' in i[:3]:
                print(i)
