# SCI1402 Projet en Science des Données

Analyse de la demande en électricité au Québec dans le cadre du projet intégrateur du cours [SCI1402](https://www.teluq.ca/site/etudes/offre/cours/TELUQ/SCI%201402/) menant à l'obtention du [certificat en science des données de la TELUQ](https://www.teluq.ca/site/etudes/offre/prog/certificat-en-science-des-donnees/)

_**Automne 2023**_

## Objectifs

Le but de ce projet sera défini en trois étapes principales.

Tout d'abord, il sera requis d'effectuer l’agrégation, le nettoyage et l'analyse des données disponibles à propos de la demande en électricité des Québécois. Idéalement, ces données seront mises à jour en continu dans un pipeline de données (_data pipeline_), de façon automatisée.

Ces données serviront à produire un modèle d’apprentissage machine adapté aux données temporelles (_time series_), pour effectuer des prévisions de la demande électrique dans le futur à court terme. Plusieurs options de modèles seront évaluées dans cette étape, afin de déterminer une option offrant des résultats répondant à nos besoins de prévisions et visualisations.

Finalement, j'utiliserai un cadre d'application (_app framwork_) interactif permettant à un utilisateur d’interagir avec certains paramètres du modèle avec d'effectuer des prévisions à court terme sur la prévision de demande électrique, de même que d'en visualiser les résultats. 

**Cette visualisation est disponible ici : [https://sci1402projetsciencedonnees.streamlit.app/](https://sci1402projetsciencedonnees.streamlit.app/)**

## Prédictions

Les prédictions du modèle optimisé avec [XGBoost](https://github.com/dmlc/xgboost) et [Optuna](https://optuna.org) sont présentées dans ce graphique.

![Demande électrique prédite et réelle](https://raw.githubusercontent.com/brunoelgrande/SCI1402_ProjetScienceDonnees/main/reports/figures/predictions.png)

## Mises à jour 

Les données historiques de la demande d'HQ 2023 ont été intégrées à partir du **27 juin 2024**.

## Données

### Demande électrique horaire pour l'année 2019 et les suivantes

Données historiques de demande en MW importées du [site d'Hydro-Québec](https://www.hydroquebec.com/documents-donnees/donnees-ouvertes/historique-demande-electricite-quebec/).

![Demande électrique pour les années importées](https://raw.githubusercontent.com/brunoelgrande/SCI1402_ProjetScienceDonnees/main/reports/figures/historique_demande_HQ.png)

### Demande électrique journalière du dernier import quotidien

Données quotidiennes de demande en MW importées du [site d'Hydro-Québec](https://www.hydroquebec.com/documents-donnees/donnees-ouvertes/demande-electricite-quebec/).

![Demande électrique de la dernière journée importée](https://raw.githubusercontent.com/brunoelgrande/SCI1402_ProjetScienceDonnees/main/reports/figures/quotidien_demande_HQ.png)

### Données Météo

Utilisation de l'API de [Open-Météo](https://open-meteo.com/) pour obtenir la température en degré Celsius pour la période à l'étude de même que pour les prévisions des 16 prochaines jours.

![Historique météo](https://raw.githubusercontent.com/brunoelgrande/SCI1402_ProjetScienceDonnees/main/reports/figures/hist_prev_meteo.png)

### Données combinées

![Demande électrique en fonction de la météo](https://raw.githubusercontent.com/brunoelgrande/SCI1402_ProjetScienceDonnees/main/reports/figures/demande_vs_meteo.png)

## Organisation du projet

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
