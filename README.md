# airbeam-serial
Script pour integration des donnees d un airbeam dans une base InfluxDB
airbeam-serial to Influxdb database

Pour appeler script:
python3 airbeamV2.py --device ttyACMXX --site nom_site
ou XX est le numero du port sur lequel est installe l airbeam.
ou nom_site correspond au nom du site de mesures

Par défaut, le script lit les données toutes les secondes puis  il y a un moyennage sur 60 secondes.
Le script transmet alors sur InfluxDB la valeur moyenne sur 60 secondes.

paramateres de la base InfluxDB sont dans le fichier variables.py
