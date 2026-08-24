# Publication de CoastProfile dans le dépôt QGIS

## Compatibilité annoncée

- QGIS 3.28 ou version ultérieure ;
- QGIS 4.x ;
- Qt 5 et Qt 6 ;
- couches ponctuelles projetées dans un CRS métrique ;
- altitude provenant de la géométrie Z ou d'un champ attributaire.

## Vérifications avant soumission

1. Installer `coastprofile-0.3.1.zip` dans un profil QGIS vierge.
2. Tester au minimum une version QGIS 3 LTR et une version QGIS 4.
3. Tester une couche `PointZ`, une couche 2D avec champ d'altitude et un identifiant numérique.
4. Vérifier les exports individuel et par lot.
5. Vérifier qu'une couche en EPSG:4326 est refusée avant le calcul des distances.
6. Vérifier que la fermeture réinitialise les résultats temporaires.
7. Publier la même archive dans une Release GitHub `v0.3.1`.
8. Créer un compte sur le portail officiel des extensions QGIS et soumettre le ZIP.

## Données non incluses

Les données GNSS métier ne sont pas distribuées. Les utilisateurs conservent la responsabilité du CRS, du référentiel altimétrique et de la qualité des mesures.
