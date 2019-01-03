import datetime as datetime
from datetime import timedelta

import variables

# Variables data serial pour airbeam######################################
sep=' ' #separateur des data récupérées sur le port serie
baudRate=9600 #Vitesse acquisition des données sur le port serial

#Messages Airbeam #####
msg=['System Check','Checking Bluetooth Module.Good','Checking WiFi Module.Good','Checking Cellular Module.Good','GPS Powered Down','Checking PMS...Good','Airbeam2 Status: Currently on Bluetooth Configuration','Airbeam2 Status: Currently on Wifi Configuration','Bluetooth Connected','WiFi Asleep','Cellular Asleep']


#Fonctions de transformation des datas #################################################

def transformationData(data):
    """Fonction pour la transformation des datas - new firmware"""
    #dataExemple=['Temperature', 'Counts', '8', 'Plantower', 'Counts', '1', 'Airbeam2', 'MAC', '0018961054F1', 'Firmware', 'v11.5.18', '78F', '26C', '299K', '56RH', 'PM1', '3', 'PM2.5', '7', 'PM10', '9']
    data=data.split(sep)
    data.insert(0,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #Insertion de la date et heure
    data[12]=float(data[12].replace('F',"")) #Temperature F
    data[13]=float(data[13].replace('C',"")) #Temperature C
    data[15]=float(data[15].replace('RH',"")) #Humidite
    data[17]=float(data[17]) #PM1
    data[19]=float(data[19]) #PM2.5
    data[21]=float(data[21]) #PM10
    #print(data)
    #res={'time':data[0],'MAC':data[9],'tempF':data[12],'tempC':data[13],'hum':data[15],'PM1':data[17],'PM2.5':data[19],'PM10':data[21]}
    res={"tags":{
                    "capteur":"AirbeamV2",
                    "MAC":data[9],
                },
         "time":data[0],
         "fields":{
                     "F":data[12],
                     "C":data[13],
                     "RH":data[15],
                     "PM1":data[17],
                     "PM2.5":data[19],
                     "PM10":data[21]
                    }
         }
    print(res)
    return data,res
    
def transformationDataOld(data):
    """Fonction pour la transformation des datas - old airbeam"""
    #dataExemple=AirBeam2MAC: 00189610804D 72F 22C 74RH PM-Amb1:25 PM-Amb2.5:42 PM-Amb10:53 PM1:23 PM2.5:31 PM10:56
    data=data.split(sep)
    data.insert(0,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) #Insertion de la date et heure
    #data[1]=str(data[1].replace('AirBeam2MAC:',"")) #numero MAC
    data[3]=float(data[3].replace('F',"")) #Temperature F
    data[4]=float(data[4].replace('C',"")) #Temperature C
    data[5]=float(data[5].replace('RH',"")) #Humidite
    data[6]=float(data[6].replace('PM-Amb1:',""))
    data[7]=float(data[7].replace('PM-Amb2.5:',""))
    data[8]=float(data[8].replace('PM-Amb10:',""))
    data[9]=float(data[9].replace('PM1:',"")) #PM1
    data[10]=float(data[10].replace('PM2.5:',"")) #PM2.5
    data[11]=float(data[11].replace('PM10:',"")) #PM10
    #print(data)
    #res={'time':data[0],'MAC':data[2],'tempF':data[3],'tempC':data[4],'hum':data[5],'PM1':data[9],'PM2.5':data[10],'PM10':data[11]}
    res={"tags":{
                    "capteur":"AirbeamV2",
                    "MAC":data[2],
                },
         "time":data[0],
         "fields":{
                     "F":data[3],
                     "C":data[4],
                     "RH":data[5],
                     "PM1":data[9],
                     "PM2.5":data[10],
                     "PM10":data[11]
                    }
         }
    return data,res
