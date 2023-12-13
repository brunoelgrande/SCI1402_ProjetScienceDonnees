# import pandas as pandas
import streamlit as st
from datetime import datetime, timedelta


################################################################################

### Dictionnaires de choix

dict_oui_non = {"Oui": True, "Non": False}

################################################################################


def sidebar_showTemperature() -> bool:
    choice_showTemp = dict_oui_non[
        st.radio(
            label="Afficher la température ?",
            options=("Oui", "Non"),
            horizontal=True,
            index=1,
            key="#showTemperature",
            help="Affichage de la température en surimpression.",
        )
    ]

    return choice_showTemp


def sidebar_onlyFuture() -> bool:
    choice_onlyFuture = dict_oui_non[
        st.radio(
            label="Afficher seulement le futur ?",
            options=("Oui", "Non"),
            horizontal=True,
            index=0,
            key="#onlyFuture",
            help="Les valeurs futures de prédictions seulement.",
        )
    ]

    return choice_onlyFuture


def sidebar_dateInput(startDate, endDate) -> tuple():
    try:
        with st.form("date_range_form"):
            dts = st.date_input(
                label="Plage de dates: ",
                min_value=(
                    datetime(
                        year=startDate[0],
                        month=startDate[1],
                        day=startDate[2],
                    )
                ),
                value=(
                    datetime(
                        year=startDate[0],
                        month=startDate[1],
                        day=startDate[2],
                        hour=12,
                    ),
                    datetime.now() + timedelta(days=16),
                ),
                key="#date_range",
                help="Le début et la fin des prédictions.",
            )

            startDate = [dts[0].year, dts[0].month, dts[0].day]
            endDate = [dts[1].year, dts[1].month, dts[1].day]

            submitted = st.form_submit_button("Soumettre")

            if submitted:
                return (startDate, endDate)
            else:
                return (startDate, endDate)
    except:
        st.error("Mauvaise sélection !")


def sidebar_pointeMW_input():
    try:
        pointe_utilisateur = st.slider(
            label="Sélectionner la demande minimale pour déterminer un évènement de pointe (10³ MW)",
            value=32.0,
            min_value=25.0,
            max_value=40.0,
            step=0.25,
            key="#pointeMW",
            help="La valeur minimale de la demande prévue en MW pour un évènement de pointe.",
        )

        return pointe_utilisateur * 1000

    except:
        st.error("Mauvaise sélection !")
