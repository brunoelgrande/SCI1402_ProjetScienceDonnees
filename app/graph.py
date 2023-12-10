import pandas as pandas
import matplotlib.pyplot as plt
import streamlit as st

from src import *
from references import *

plt.style.use(style="fivethirtyeight")


def graph_prediction(
    df: pd.DataFrame,
    startDate: list() = [2023, 11, 12],
    endDate: list() = [2099, 12, 31],
    onlyFuture: bool = False,
    withTemperature: bool = False,
) -> plt.plot:
    try:
        if onlyFuture:
            max_MW = df["MW"].dropna()
            date_debut = max_MW.index.date[-1]
            startDate = [date_debut.year, date_debut.month, date_debut.day]

        # Ajuster dataframe aux dates de début et fin
        df["d"] = df.index
        df["isShow"] = df["d"].apply(
            lambda x: x
            > datetime(year=startDate[0], month=startDate[1], day=startDate[2], hour=12)
            and x < datetime(year=endDate[0], month=endDate[1], day=endDate[2], hour=12)
        )

        # Conserver seulement les données pour le graph
        df_graph = df.query("isShow")

        # Ajuster la date de fin affichée aux données réelles
        date_fin = df_graph.index.date[-1]
        endDate = [date_fin.year, date_fin.month, date_fin.day]

        # Affichage du mois
        list_mois = mois_cat_type.categories
        mois_debut = (list_mois[startDate[1] - 1]).lower()
        mois_fin = (list_mois[endDate[1] - 1]).lower()

        # Graphique
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(15)

        # Visualisation
        ax = df_graph["prediction"].plot(
            ms=1,
            lw=2,
            label="Prédiction",
            ls="--",
            xlabel="",
            ylabel="MW",
            color=col_demande_predite,
        )

        df_graph["MW"].plot(
            ax=ax,
            ms=1,
            lw=1.5,
            label="Demande réelle",
            xlabel="",
            color=col_demande_relle,
        )

        ax.axvline(
            datetime.now(),
            color="black",
            ls="-.",
            linewidth=2,
            alpha=0.7,
        )

        if withTemperature:
            alpha, size = 0.9, 18

            ax2 = ax.twinx()

            color = col_temperature
            ax2.set_ylabel("Température (C)", color=color)

            df_graph["Temp"].plot(
                ax=ax2,
                ms=1,
                lw=1.5,
                ls="dotted",
                label="Température",
                xlabel="",
                color=color,
            )

            ax2.tick_params(axis="y", labelcolor=color)

        fig.suptitle(
            f"Prédiction de la demande électrique",
            ha="center",
            y=1.01,
            fontsize=32,
        )
        fig.text(
            x=0.5,
            y=0.93,
            s=f"Du {startDate[2]} {mois_debut} {startDate[0]} au {endDate[2]} {mois_fin} {endDate[0]}",
            fontsize=22,
            ha="center",
        )
        fig.legend()

        plt.tight_layout()

        return fig
    except:
        st.error("Mauvaise sélection !")
        return False


################################################################################
