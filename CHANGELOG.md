# Changelog

## 0.4.3 — 2026-08-26

- paquet rendu conforme au validateur du dépôt officiel QGIS ;
- ajout de `LICENSE` dans le dossier racine de l'extension ;
- ajout du `README.md` dans l'archive distribuée ;
- aucune modification des calculs ou de l'interface validée en 0.4.2.

## 0.4.2 — 2026-08-25

- ajout du bouton **Comprendre les indicateurs** dans l'analyse multiannuelle ;
- définitions intégrées de la longueur commune, de l'accrétion, de l'érosion et du bilan net ;
- rappel des unités de section, du rôle du seuil GNSS et des limites scientifiques.

## 0.4.1 — 2026-08-25

- correction scientifique des unités de comparaison ;
- remplacement de `m²/ml` par **m² de section** dans l'interface ;
- clarification : les aires entre deux courbes sont des surfaces de section verticale, pas des volumes ;
- mise à jour cohérente du README, des métadonnées et du paquet d'installation.

## 0.4.0 — 2026-08-24

- conservation intégrale de la génération et des exports de profils annuels ;
- archivage temporaire des campagnes par identifiant de profil ;
- nouvel onglet **Évolution multiannuelle** ;
- superposition de toutes les campagnes disponibles pour un même profil ;
- comparaison paramétrable entre une campagne de référence et une campagne cible ;
- mise en évidence de l'accrétion, de l'érosion et des variations comprises dans l'incertitude ;
- calcul du bilan net, des surfaces positives/négatives et des écarts altimétriques extrêmes ;
- export PNG du graphique comparatif.

## 0.3.1 — 2026-08-24

- compatibilité validée sur QGIS 3.44.13 LTR et QGIS 4.0.3 ;
- tri naturel des profils (`1, 2, 10` au lieu de `1, 10, 2`).

## 0.3.0 — 2026-08-24

- suppression complète des noms de profils codés en dur ;
- compatibilité QGIS 3.28+ et QGIS 4, Qt 5 et Qt 6 ;
- choix entre altitude de la géométrie Z et champ attributaire ;
- seuil d’isolement spatial réglable ;
- blocage du calcul dans un CRS géographique non métrique ;
- tests exécutables avec la bibliothèque standard Python.

## 0.2.2 — 2026-08-24

- réinitialisation de la liste, du graphique et des résultats à la fermeture ;
- nouvelle ouverture toujours propre, sans réafficher l'analyse précédente ;
- aucune modification des données sources ou des couches chargées dans QGIS.

## 0.2.1 — 2026-08-24

- nom simplifié en **CoastProfile** et paquet Python renommé `coastprofile` ;
- conservation du quadrillage et des graduations harmonisées ;
- conservation du filtre spatial qui exclut les points aberrants comme celui de P401 ;
- archive d'installation reconstruite pour QGIS 4 / Qt 6.

## 0.2.0 — 2026-08-24

- renommage en CoastProfile ;
- détection des points isolés ;
- axes arrondis et quadrillage amélioré ;
- graphique avec points GNSS ;
- export individuel et groupé ;
- icône dédiée et compatibilité QGIS 4 / Qt 6.
