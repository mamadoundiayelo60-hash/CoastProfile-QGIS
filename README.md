# CoastProfile

![QGIS](https://img.shields.io/badge/QGIS-3.28%20à%204.x-589632?logo=qgis&logoColor=white) ![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white) ![Qt](https://img.shields.io/badge/Qt-5%20%7C%206-41CD52?logo=qt&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-blue)

**CoastProfile** est une extension QGIS destinée à créer, contrôler et suivre dans le temps des profils topographiques de plage et de dune issus de campagnes GNSS.

## Problème traité

Les campagnes topographiques produisent des points 3D qu'il faut regrouper, ordonner, contrôler et transformer en profils comparables. CoastProfile automatise ce parcours sans modifier les données sources.

## Fonctionnalités — version 0.4.4

- sélection d'une couche ponctuelle 3D et choix des champs ;
- altitude lue dans la géométrie Z ou dans un champ choisi ;
- identifiants entièrement issus des données utilisateur, sans nomenclature imposée ;
- tri naturel des identifiants numériques et alphanumériques ;
- seuil d’isolement spatial paramétrable ;
- création automatique d'un profil par identifiant ;
- orientation homogène terre vers mer et distance cumulée ;
- détection des points spatialement isolés ;
- graphique professionnel avec quadrillage, axes et points GNSS ;
- synchronisation profil–carte avec sélection et zoom QGIS ;
- export PNG individuel ou par lot ;
- archivage de plusieurs campagnes pendant la session d'analyse ;
- association automatique des campagnes portant le même identifiant ;
- superposition multiannuelle des courbes sur un axe commun ;
- sélection libre de l'année de référence et de l'année comparée ;
- cartographie graphique des hausses, baisses et variations non significatives ;
- calcul des surfaces d'érosion et d'accrétion, du bilan net et des écarts maximaux ;
- seuil d'incertitude altimétrique paramétrable et export PNG comparatif ;
- aide intégrée expliquant les indicateurs, les unités et les précautions scientifiques ;
- réinitialisation automatique des résultats à la fermeture du plugin ;
- compatibilité QGIS 3.28+ / QGIS 4 et Qt 5 / Qt 6.

## Démonstration validée

La campagne pilote comprend **181 points GNSS 3D**, répartis en **12 profils côtiers**. CoastProfile crée les 12 graphiques et détecte notamment un point isolé qui allongeait artificiellement un profil à plus de 3 km.

> Les données métier originales ne sont pas incluses dans le dépôt.

## Installation

1. Télécharger `coastprofile-0.4.4.zip` depuis les Releases GitHub.
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
2. regroupement par identifiant métier et campagne ;
3. conservation de la composante spatiale principale ;
4. normalisation de l'orientation selon les altitudes des extrémités ;
5. calcul de la distance cumulée dans le CRS métrique ;
6. génération du profil et synchronisation avec la carte ;
7. interpolation des campagnes sur leur longueur commune ;
8. intégration des écarts altimétriques pour estimer les surfaces d'érosion et d'accrétion de la section verticale du profil, en m².

## Comparaison multiannuelle

Créez d'abord les profils d'une campagne, puis sélectionnez une autre couche et relancez **Créer les profils**. CoastProfile conserve les campagnes déjà calculées dans la fenêtre. Dès qu'un identifiant possède au moins deux années, il apparaît dans l'onglet **Évolution multiannuelle**.

Le rouge représente une baisse altimétrique, le vert une hausse et le gris une variation comprise dans le seuil d'incertitude. Les aires calculées entre deux courbes sont des surfaces de section en m², et non des volumes. Les résultats doivent être interprétés uniquement si les campagnes utilisent le même système de coordonnées, le même référentiel altimétrique et une méthode d'acquisition comparable.

## Roadmap

- atlas PDF automatisé ;
- export CSV des indicateurs multiannuels ;
- persistance optionnelle de l'historique dans un GeoPackage ;
- publication dans le dépôt officiel des extensions QGIS.

## Auteur

**Mamadou Ndiaye LO** — Géomaticien – Administrateur SIG & Développeur SIG Web | Data spatiale, bases de données & automatisation 
Python · QGIS · PostgreSQL/PostGIS · ETL géospatial · GNSS/LiDAR

Licence MIT.

## Compatibilité validée

- QGIS 3.44.13 LTR sous Windows ;
- QGIS 4.0.3 sous Windows.
