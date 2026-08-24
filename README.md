# CoastProfile

![QGIS](https://img.shields.io/badge/QGIS-4.0%2B-589632?logo=qgis&logoColor=white) ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) ![Qt](https://img.shields.io/badge/Qt-6-41CD52?logo=qt&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-blue)

**CoastProfile** est une extension QGIS destinée à créer, contrôler et suivre dans le temps des profils topographiques de plage et de dune issus de campagnes GNSS.

## Problème traité

Les campagnes topographiques produisent des points 3D qu'il faut regrouper, ordonner, contrôler et transformer en profils comparables. CoastProfile automatise ce parcours sans modifier les données sources.

## Fonctionnalités — version 0.2.1

- sélection d'une couche ponctuelle 3D et choix des champs ;
- création automatique d'un profil par identifiant ;
- orientation homogène terre vers mer et distance cumulée ;
- détection des points spatialement isolés ;
- graphique professionnel avec quadrillage, axes et points GNSS ;
- synchronisation profil–carte avec sélection et zoom QGIS ;
- export PNG individuel ou par lot ;
- compatibilité QGIS 4 et Qt 6.

## Démonstration validée

La campagne pilote comprend **181 points GNSS 3D**, répartis en **12 profils côtiers**. CoastProfile crée les 12 graphiques et détecte notamment un point isolé qui allongeait artificiellement un profil à plus de 3 km.

> Les données métier originales ne sont pas incluses dans le dépôt.

## Installation

1. Télécharger `coastprofile-0.2.1.zip` depuis les Releases GitHub.
2. Dans QGIS : **Extensions → Installer/Gérer les extensions → Installer depuis un ZIP**.
3. Redémarrer QGIS puis ouvrir **CoastProfile**.
4. Charger une couche de points 3D dans un CRS métrique correctement défini.

Pour la campagne pilote : **RGF93 / CC50 — EPSG:3950**.

## Architecture

```text
coastprofile/
├── plugin.py          # cycle de vie QGIS
├── window.py          # interface Qt 6 et graphique
├── icon.svg           # identité visuelle
└── core/profiles.py   # moteur testable hors QGIS
```

Le moteur est séparé de l'interface afin de faciliter les tests et les évolutions.

## Méthode

1. lecture des sommets `PointZ` ou `MultiPointZ` ;
2. regroupement par identifiant métier ;
3. conservation de la composante spatiale principale ;
4. normalisation de l'orientation selon les altitudes des extrémités ;
5. calcul de la distance cumulée dans le CRS métrique ;
6. génération du profil et synchronisation avec la carte.

## Roadmap

- historique multiannuel 2025–2026–2027 ;
- superposition des campagnes sur un axe commun ;
- surfaces d'érosion et d'accumulation ;
- bilan sédimentaire et incertitudes GNSS ;
- atlas PDF automatisé ;
- publication dans le dépôt officiel des extensions QGIS.

## Auteur

**Mamadou Ndiaye LO** — Géomaticien / Administrateur SIG  
Python · QGIS · PostgreSQL/PostGIS · ETL géospatial · GNSS/LiDAR

Licence MIT.
