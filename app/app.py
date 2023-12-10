import pandas as pandas
import streamlit as st

# from datetime import datetime, date
from src import *
from references import *
from fonctions import *
from graph import *
from sidebar import *

st.set_option("deprecation.showPyplotGlobalUse", False)

################################################################################
#### Contenu de l'entête ####

st.title("Prédiction de la demande électrique")
st.markdown(
    "### Modèle de prédiction de la demande électrique au Québec pour les prochains jours"
)
st.markdown(
    """
            Texte explications ici.

            ---
            """
)

################################################################################

#### Chargement des données et prédictions ####

with st.spinner("Chargement du modèle et des données...."):
    model = st_load_model()
    df, FEATURES = st_load_data_features()
    df = st_make_predictions(df=df, model=model, FEATURES=FEATURES)

    startDate = [df.index.date[0].year, df.index.date[0].month, df.index.date[0].day]
    endDate = [df.index.date[-1].year, df.index.date[-1].month, df.index.date[-1].day]


################################################################################

##### Contenu du sidebar : sidebar.py  #####
with st.sidebar:
    st.title("Choix à sélectionner")

    st.header("Température")

    choice_showTemp = sidebar_showTemperature()

    st.markdown("---")

    st.header("Dates")
    choice_onlyFuture = sidebar_onlyFuture()

    if not choice_onlyFuture:
        (startDate, endDate) = sidebar_dateInput(startDate=startDate, endDate=endDate)

    st.markdown("---")

    st.header("Prévision de la pointe")

    pointe_utilisateur = sidebar_pointeMW_input()


################################################################################

##### Contenu du corps  #####

# st.text(f"Meilleur RMSE du modèle : {model.best_score:0.1f}")


st.header("Graphique des prédictions")

st.markdown(
    """
        Notre modèle d'apprentissage machine est en mesure de réaliser des prédictions sur la **demande électrique à venir** au Québec. 

        Vous pouvez ajuster les dates et ajouter la température en surimpression dans le panneau de gauche. 

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


st.header("Prévision des prochaines périodes de pointe")

st.markdown(
    """
        Avec sa [tarification dynamique](https://www.hydroquebec.com/residentiel/mieux-consommer/economiser-en-periode-de-pointe/tarification-dynamique/), Hydro-Québec offre des rabais aux clients ayant souscrit au **tarif D avec option de crédit hivernal** ou un tarif plus élevé en période d'évènement de pointes pour ceux au **tarif Flex D**.

        Afin de profiter au maximum de cette tarification, voici nos prévisions sur les prochains évènements de pointe, afin d'aider les clients à prévoir quand ils auront à réduire leur consommation.

        Vous pouvez ajuster la demande minimale d'un évènement de pointe dans le panneau de gauche. 

"""
)


st.markdown(
    """
        - [ ] TODO : Faire graphique avec prédictions seulements + zone grisées autour des période ayant potentiellement un évènement de pointes
        - [ ] TODO : ajout d'une ligne horizontale à la valeur de `pointe_utilisateur`.
        - Tableau et graphique
        """
)
