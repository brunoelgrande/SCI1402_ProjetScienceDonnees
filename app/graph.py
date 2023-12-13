import pandas as pandas
import matplotlib.pyplot as plt
import streamlit as st

from src import *
from references import *
from datetime import datetime, time

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
            ylabel="Demande (MW)",
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


def graph_evenement_pointe(
    df: pd.DataFrame,
    jours_pointe_matin: list(),
    jours_pointe_soir: list(),
    pointeBascule: float = 32_000,
    withTemperature: bool = False,
) -> plt.plot:
    try:
        # jours_pointe_matin = pointes[0]
        # jours_pointe_soir = pointes[1]

        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(15)

        fig.suptitle(
            f"Prévision des évènements de pointe",
            ha="center",
            y=1.01,
            fontsize=32,
        )

        pb = "{:,}".format(int(pointeBascule)).replace(",", " ")

        fig.text(
            x=0.5,
            y=0.93,
            s=f"Déclanchement de l'évènement à {pb} MW",
            fontsize=18,
            ha="center",
        )

        ax = df.prediction.plot(
            ylabel="Demande (MW)",
            xlabel="",
            label="Prédiction",
            lw=2,
            color=col_demande_predite,
        )
        ax.axhline(
            y=pointeBascule,
            color=colors_pal[0],
            linewidth=1,
            alpha=0.8,
            label="Pointe déclanchement",
        )

        if withTemperature:
            ax2 = ax.twinx()

            color = col_temperature
            ax2.set_ylabel("Température (C)", color=color)

            df["Temp"].plot(
                ax=ax2,
                ms=1,
                lw=1.5,
                ls="dotted",
                label="Température",
                xlabel="",
                color=color,
            )

            ax2.tick_params(axis="y", labelcolor=color)

        if jours_pointe_matin:
            show_legend = True
            for d in jours_pointe_matin:
                ax.fill_betweenx(
                    y=range(
                        int(min(df.prediction) * 0.99), int(max(df.prediction) * 1.005)
                    ),
                    x1=datetime.combine(d, time(hour=6)),
                    x2=datetime.combine(d, time(hour=9)),
                    color=colors_pal[11],
                    alpha=0.4,
                    label="Prévision pointe AM" if show_legend else "",
                )
                show_legend = False

        if jours_pointe_soir:
            show_legend = True
            for d in jours_pointe_soir:
                ax.fill_betweenx(
                    y=range(
                        int(min(df.prediction) * 0.99), int(max(df.prediction) * 1.005)
                    ),
                    x1=datetime.combine(d, time(hour=16)),
                    x2=datetime.combine(d, time(hour=20)),
                    color=colors_pal[10],
                    alpha=0.4,
                    label="Prévision pointe PM" if show_legend else "",
                )
                show_legend = False

        fig.legend()
        plt.tight_layout()

        return fig
    except:
        st.error("Mauvaise sélection !")
        return False
