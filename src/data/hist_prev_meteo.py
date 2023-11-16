#!/usr/bin/env python3

import pandas as pd
import json
import httpx
import os
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")

from references import colors_pal


def get_meteo() -> pd.DataFrame:
    """Obtenir les données historique et prévisions météo

    Returns:
        pd.DataFrame: df contenant la température de 2018 jusqu'à aujourd'hui + 16 jours
    """

    path_to_interim_data = os.path.join(Path(__file__).parents[2], "data/interim/")
    path_to_img = os.path.join(Path(__file__).parents[2], "reports/figures/")
    file_parquet = "hist_prev_meteo.parquet"
    file_image = "hist_prev_meteo.png"

    # Import des prévisions météo
    prediction_url = "https://api.open-meteo.com/v1/forecast?latitude=45.5088&longitude=-73.5878&hourly=temperature_2m&timezone=America%2FNew_York&past_days=5&forecast_days=16"

    r = httpx.get(prediction_url)
    data_pred = json.loads(r.text)

    df_pred = (
        pd.DataFrame.from_records(data_pred["hourly"])
        .rename(
            columns={
                "time": "date",
                "temperature_2m": "temp",
            }
        )
        .set_index("date")
    )

    df_pred.index = pd.to_datetime(df_pred.index)

    # Import de l'historique météo
    date_dep: str = "2018-01-01"
    date_fin: str = str(df_pred.index.min().date())

    hist_url: str = f"https://archive-api.open-meteo.com/v1/archive?latitude=45.5088&longitude=-73.5878&start_date={date_dep}&end_date={date_fin}&hourly=temperature_2m&timezone=America%2FNew_York"

    r = httpx.get(hist_url)
    data_hist = json.loads(r.text)

    df_hist = (
        pd.DataFrame.from_records(data_hist["hourly"])
        .rename(
            columns={
                "time": "date",
                "temperature_2m": "temp",
            }
        )
        .set_index("date")
    )

    df_hist.index = pd.to_datetime(df_hist.index)

    # Jointure des 2 df
    df = pd.merge(
        df_hist,
        df_pred,
        how="outer",
        left_index=True,
        right_index=True,
    )

    # Création d'une moyenne entre les 2 séries de données
    df["moyenne"] = df.mean(axis=1)
    df = df.drop(columns=["temp_x", "temp_y"]).rename(columns={"moyenne": "temp"})

    # Création d'une visualisation
    df.plot(
        style=".",
        ms=0.5,
        figsize=(15, 5),
        xlabel="",
        ylabel="Température (C)",
        legend=False,
        color=colors_pal[4],
    )

    plt.axvline(
        linewidth=1,
        x=datetime.now(),
        ymin=0.1,
        ymax=0.9,
        color=colors_pal[6],
        alpha=0.5,
    )

    plt.title(
        label="Historique et prévisions météo - Montréal, QC",
        fontsize=24,
    )
    plt.tight_layout()

    plt.savefig(os.path.join(path_to_img, file_image), dpi=300)

    # Enregistrer les données
    df.to_parquet(
        path=os.path.join(path_to_interim_data, file_parquet),
        engine="pyarrow",
    )

    print(
        f"\nLe fichier de données météo possède maintenant {format(df.shape[0], ',d').replace(',',' ')} heures d'historiques et de prévisions.\n"
    )

    return df


if __name__ == "__main__":
    get_meteo()
