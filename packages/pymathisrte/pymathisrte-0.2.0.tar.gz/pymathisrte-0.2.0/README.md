# Librarie pymathisrte

## Description 
La  librairie a pour but d'accéder à MATHIS et d'effectuer des requêtes SQL. 

## Installation

Pour installer le package il faut taper la commande suivante:

```
pip install pymathisrte==0.1.0
```
Qui peut être retrouvé sur ce lien : 
https://pypi.org/project/pymathisrte/0.1.0/


## Utilisation du package 

Il faut créer un fichier .env contenant ces variables :

```
DREMIO_URI=https://mathis.rte-france.com/apiv2/login
DREMIO_USERNAME=XXX
DREMIO_PASSWORD=XXX
CERT_PATH=XXX
DREMIO_LOCATION=grpc://mathis.rte-france.com:32010
```
Mettez vos identifiants de connexion à MATHIS, puis si vous avez un certificat mettez son chemin d'accès, sinon pas besoin de mettre la variable dans le fichier.

Le package doit être utilisé sur un notebook (un fichier .ipynb).
Vous pourrez importer les fonctions comme ceci: 

```
from src.functions import *
```

## Pré-requis

* Vous devez être habilité au service MATHIS pour pouvoir utiliser le
package. Contactez la BAL RTE-DSIT-DATA-DATALAKE.
* Même avec une habilitation, certains dossiers nécessitent une autorisation particulière.
Contactez la BAL RTE-DSIT-DATA-DATALAKE.
