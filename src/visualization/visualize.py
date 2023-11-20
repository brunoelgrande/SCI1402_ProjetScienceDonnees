import pandas as pd
import os
from pathlib import Path


import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

from references import colors_pal


def plot_demande_temp(df: pd.DataFrame, fin_titre: str = "", **kwargs):
    """Scatterplot de la température et demande MW en fonction du temps

    Args:
        df (pd.DataFrame): Données en `temp`  et `MW` (demande)
        fin_titre (str, optional): Fin du titre du graphique
        kwargs : file_image et path_to_img : pour enregistre le graphique plutôt que de le visualiser
    """
    alpha, size = 0.4, 8

    fig, ax1 = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(15)

    color = colors_pal[11]
    ax1.set_xlabel("")
    ax1.set_ylabel("Demande (MW)", color=color)
    ax1.scatter(
        x=df.index,
        y=df.MW,
        color=color,
        s=size,
        alpha=alpha,
    )
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()

    color = colors_pal[4]
    ax2.set_ylabel("Température (C)", color=color)
    ax2.scatter(
        x=df.index,
        y=df.Temp,
        color=color,
        s=size,
        alpha=alpha,
    )
    ax2.tick_params(axis="y", labelcolor=color)

    plt.suptitle(
        f'Demande électrique et température dans le temps{" - " if fin_titre != "" else ""}{fin_titre}',
        y=0.95,
        fontsize=24,
    )

    fig.tight_layout()

    # Si nous voulons sauver le graph

    if file_image := kwargs.get("file_image", False):
        print(f"Sauvegardons le graphique : {file_image}\n")
        plt.savefig(os.path.join(kwargs.get("path_to_img"), file_image), dpi=300)

    else:
        plt.show()


def line_demande_temp(df: pd.DataFrame, fin_titre: str = "", **kwargs):
    """Lineplot de la température et demande MW en fonction du temps

    Args:
        df (pd.DataFrame): Données en `temp`  et `MW` (demande)
        fin_titre (str, optional): Fin du titre du graphique
        kwargs : file_image et path_to_img : pour enregistre le graphique plutôt que de le visualiser
    """
    alpha, size = 0.8, 6

    fig, ax1 = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(15)

    color = colors_pal[11]
    ax1.set_xlabel("")
    ax1.set_ylabel("Demande (MW)", color=color)
    ax1.plot(
        df.MW,
        color=color,
        # s=size,
        alpha=alpha,
    )
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()

    color = colors_pal[4]
    ax2.set_ylabel("Température (C)", color=color)
    ax2.plot(
        df.Temp,
        color=color,
        # s=size,
        alpha=alpha,
    )
    ax2.tick_params(axis="y", labelcolor=color)

    plt.suptitle(
        f'Demande électrique et température dans le temps{" - " if fin_titre != "" else ""}{fin_titre}',
        y=0.95,
        fontsize=24,
    )

    fig.tight_layout()

    # Si nous voulons sauver le graph

    if file_image := kwargs.get("file_image", False):
        print(f"Sauvegardons le graphique : {file_image}\n")
        plt.savefig(os.path.join(kwargs.get("path_to_img"), file_image), dpi=300)

    else:
        plt.show()
