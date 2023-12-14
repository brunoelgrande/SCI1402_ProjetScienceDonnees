import pandas as pandas
import streamlit as st

from references import *
from fonctions import *
from graph import *
from sidebar import *

st.set_option("deprecation.showPyplotGlobalUse", False)
st.set_page_config(layout="wide", page_title="Prédiction de la demande électrique")
################################################################################
#### Contenu de l'entête ####

head1, head2 = st.columns([1, 3])

head1.image("././img/logo.png")

head2.title("Prédiction de la demande électrique")

head2.markdown(
    """
            ### Modèle de prédiction de la demande électrique au Québec pour les prochains jours  

            Présentation d'un modèle de prévision conçu dans le cadre du cours [SCI1402 - Projet en science des données](https://www.teluq.ca/site/etudes/offre/cours/TELUQ/SCI%201402/) de la [TELUQ](https://www.teluq.ca/) à l'automne 2023.
            
            Ce modèle a été réalisé avec la librairie d'apprentissage machine [XGBoost](https://xgboost.readthedocs.io/en/stable) et le cadre d'optimisation [Optuna](https://optuna.org/) sur les données rendus disponibles par :orange[**Hydro-Québec**] sur leur de [données ouvertes](https://www.hydroquebec.com/documents-donnees/donnees-ouvertes/demande-electricite-quebec/).
            """
)

st.markdown("---")

################################################################################

#### Chargement des données et prédictions ####

with st.spinner("Chargement du modèle et des données...."):
    model = st_load_model()
    df, FEATURES = st_load_data_features()
    df = st_make_predictions(df=df, _model=model, FEATURES=FEATURES)

    startDate = [df.index.date[0].year, df.index.date[0].month, df.index.date[0].day]
    endDate = [df.index.date[-1].year, df.index.date[-1].month, df.index.date[-1].day]

    df_pointe = st_make_df_evenement_pointe()


################################################################################

##### Contenu du sidebar : sidebar.py  #####
with st.sidebar:
    st.title("Choix à sélectionner")

    st.header("Température :thermometer:")

    choice_showTemp = sidebar_showTemperature()

    st.markdown("---")

    st.header("Dates :date:")
    choice_onlyFuture = sidebar_onlyFuture()

    if not choice_onlyFuture:
        (startDate, endDate) = sidebar_dateInput(startDate=startDate, endDate=endDate)

    st.markdown("---")

    st.header("Prévision de la pointe 	:electric_plug:")

    pointe_utilisateur = sidebar_pointeMW_input()


################################################################################

##### Contenu du corps  #####

# st.text(f"Meilleur RMSE du modèle : {model.best_score:0.1f}")


st.header("Graphique des prédictions")

st.markdown(
    """
        Le modèle d'apprentissage machine est en mesure de réaliser des prédictions sur la **demande électrique à venir** au Québec, mais aussi sur des données historiques (à partir de 2019). 

        Vous pouvez **ajuster les dates** et **ajouter la température** en surimpression dans le panneau latéral. 

"""
)

st.pyplot(
    fig=graph_prediction(
        df=df,
        onlyFuture=choice_onlyFuture,
        startDate=startDate,
        endDate=endDate,
        withTemperature=choice_showTemp,
    )
)

################################################################################
st.markdown("---")

st.header("Prévision des prochaines périodes de pointe")

st.markdown(
    """
        Avec sa [tarification dynamique](https://www.hydroquebec.com/residentiel/mieux-consommer/economiser-en-periode-de-pointe/tarification-dynamique/), Hydro-Québec offre des rabais aux clients ayant souscrit au **tarif D avec option de crédit hivernal** ou un tarif plus élevé en période d'évènement de pointes pour ceux au **tarif Flex D**.

        Afin de profiter au maximum de cette tarification, voici les prévisions sur les prochains évènements à venir, afin d'aider les clients à optimiser leur consommation.

        Vous pouvez **ajuster** la demande minimale d'un évènement de pointe dans le panneau latéral ou utiliser la **valeur par défaut** de **32&nbsp;000 MW**.

""",
    unsafe_allow_html=True,
)


(jours_pointe_matin, jours_pointe_soir) = st_make_list_evenement_pointe(
    df=df_pointe,
    pointeBascule=pointe_utilisateur,
)


col1, col2 = st.columns(2)

col1.subheader("Évènements du matin")
col2.subheader("Évènements du soir")


for j in jours_pointe_matin:
    col1.markdown("- " + str(j))

if not jours_pointe_matin:
    col1.markdown("Aucun évènement prévu")

for j in jours_pointe_soir:
    col2.markdown("- " + str(j))

if not jours_pointe_soir:
    col2.markdown("Aucun évènement prévu")


st.text("")

st.pyplot(
    fig=graph_evenement_pointe(
        df=df_pointe,
        jours_pointe_matin=jours_pointe_matin,
        jours_pointe_soir=jours_pointe_soir,
        pointeBascule=pointe_utilisateur,
        withTemperature=choice_showTemp,
    )
)

################################################################################
####  Footer  ####

st.markdown("---")
st.markdown(
    """
    Une réalisation de :blue[**Bruno Gauthier**] avec un code libre de droits disponible sur [**Github.**](https://github.com/brunoelgrande/SCI1402_ProjetScienceDonnees) 
    """,
    unsafe_allow_html=True,
)
