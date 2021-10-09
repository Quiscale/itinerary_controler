# Prototype projet Jolibrain

Ce dossier comporte 3 partie réparties à la racine de celui-ci ainsi que dans le dossier `www` et le dossier `.git`.
A la racine se trouve le fichier `main.py` qui sert de serveur web, et le fichier `fastapp.py` qui sert de serveur pour l'API. le fichier `database.py` et `idea.db` servent pour la gestion des données.
Le dossier `www` est le dossier racine du serveur web.
Le dossier `.git` sert pour la gestion de version.

## Utilisation

Afin d'avoir accès aux pages web via un navigateur, il faut démarrer deux serveurs : le serveur web et l'API.
Ces serveurs ont été développé avec :
- python 3.9.5

- uvicorn 0.14.0
- installation : `python3 -m pip install uvicorn`

- fastapi
- installation : `python3 -m pip install fastapi`

note: intégrer un environnement virtuel pourrait être une bonne idée


Pour démarrer le serveur web :
`python3 main.py`
Attention, ce serveur n'est pas sécurisé. Il renvoie bêtement le fichier demandé sans rien vérifier. Il est donc possible d'accéder à tous les fichiers de l'ordinateur en lecture seulement.

Pour démarrer le serveur API :
`python3 -m uvicorn fastapp:app --no-use-colors`
Il est possible de choisir le port sur lequel l'API sera avec `--port PORT` et l'adresse avec `--host IP`. Plus d'information avec `python3 -m uvicorn --help`.

## Pages web

L'accès au page web se fait après avoir ouvert le serveur web à l'adresse 127.0.0.1 dans un navigateur web ou à l'adresse IP choisie depuis un ordinateur distant.
La page web présente deux possibilitées : Géoloc pour accéder à l'outil de géolocalisation des véhicules, ou Vide Plein pour voir les informations sur le vide/plein (cet outil n'est pas disponible pour le moment).

### Géolocalistion

Cette outil permet de :
- Créer/Supprimer des points avec : leur référence, leur type, et leurs coordonnées en pixel sur la carte.
- note : les coordonnées des points sont stockées sous la forme de nombre flottant en fonction des positions de A0 et R50

- Créer/Supprimer des itinéraires avec un nom, et composés de plusieurs points.

- Créer/Supprimer des véhicules avec : leur numéro, et leur type. Il est possible de lié un véhicule à un itinéraire pour ensuite le voir évolué sur celui-ci.

- Voir un résumé de l'avancement d'une tournée
- note : aucun bouton ne permet d'accéder à cette page, l'adresse est donc `/resume.html?path=PATH_ID`, PATH_ID étant le numéro du chemin

- Rentrer des données depuis un formulaire, pour cela il faut donner le numéro du véhicule, puis suivre les indications.
- note : aucun bouton ne permet d'accéder à cette page, l'adresse est donc `/operateur.html`

### Plein / Vide

Non programmé