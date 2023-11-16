#!/usr/bin/env python3

import pandas as pd
import os
from pathlib import Path

import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

from references import colors_pal


def plot_demande_temp(
    df: pd.DataFrame, path_to_img: str, file_image: str, fin_titre: str = ""
) -> None:
    alpha, size = 0.4, 8

    fig, ax1 = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(15)

    color = colors_pal[0]
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
        f'Demande électrique en fonction de la température{" - " if fin_titre != "" else ""}{fin_titre}',
        y=0.95,
        fontsize=24,
    )

    fig.tight_layout()

    plt.savefig(os.path.join(path_to_img, file_image), dpi=300)


def regroup_demande_meteo() -> pd.DataFrame:
    """Obtenir les données historique et prévisions météo

    Returns:
        pd.DataFrame: df contenant la température de 2018 jusqu'à aujourd'hui + 16 jours
    """
    path_to_interim_data = os.path.join(Path(__file__).parents[2], "data/interim/")
    path_to_img = os.path.join(Path(__file__).parents[2], "reports/figures/")
    demande_quotidien_parquet = "quotidien_demande_HQ.parquet"
    demande_historique_parquet = "historique_demande_HQ.parquet"
    temperature_parquet = "hist_prev_meteo.parquet"
    file_parquet = "demande_meteo.parquet"
    file_image = "demande_vs_meteo.png"

    # Regroupement des fichiers de demandes
    d_quotidien = pd.read_parquet(
        path=os.path.join(path_to_interim_data, demande_quotidien_parquet),
        engine="pyarrow",
    )
    d_hist = pd.read_parquet(
        path=os.path.join(path_to_interim_data, demande_historique_parquet),
        engine="pyarrow",
    )
    demandes = d_hist.rename(columns={"MW": "Historique"}).join(
        d_quotidien.rename(columns={"MW": "Prédiction"}), how="outer"
    )

    demandes["MW"] = demandes.mean(axis=1)
    df_demande = demandes.drop(columns=["Historique", "Prédiction"])

    # Ajout des températures
    tf = pd.read_parquet(
        path=os.path.join(path_to_interim_data, temperature_parquet),
        engine="pyarrow",
    )
    df = df_demande.join(tf, how="outer").rename(columns={"temp": "Temp"})

    # Enregistrer le graphique
    plot_demande_temp(df=df, path_to_img=path_to_img, file_image=file_image)

    # Enregistrer les données
    df.to_parquet(
        path=os.path.join(path_to_interim_data, file_parquet),
        engine="pyarrow",
    )

    print(
        f"\nLes données de demande électrique et de météo sont maintenant regroupées avec {format(df.shape[0], ',d').replace(',',' ')} heures d'historique.\n"
    )

    return df


if __name__ == "__main__":
    regroup_demande_meteo()
