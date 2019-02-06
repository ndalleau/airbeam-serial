#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 21:41:29 2018

@author: dalleau Nicolas
"""

#Paramètres de la base InfluxDB #######################################################
#InfluxDB est la base de données qui collecte les résultats des mesures

bddInflux={'airbeam2':
    {'serveur':'XXXXX',
    'port':8086,
    'login':'XXXXX',
    'mdp':'XXXX!',
    'nom':'airbeam2'},
    }


jsonModel={
           "measurement":"measurement_name",
           "tags":{
                   "capteur":"capteur_name",
                   "MAC":"mac",
                   "site":"site_mesure"},
                   "time":'%Y-%m-%d %H:%M:%S',
                   "fields":{
                             "F":0,
                             "C":0,
                             "RH":0,
                             "PM1":0,
                             "PM2.5":0,
                             "PM10":0}
           }
    
#######################################################################################


# Variables data serial ######################################
sep=' ' #separateur des data récupérées sur le port serie
baudRate=9600 #Vitesse acquisition des données sur le port serial


ficDataRep = '/home/pi/Documents/python/airbeamV2/data/'  #Fichier de stockage des résultats csv
csv = False
##############################################################
