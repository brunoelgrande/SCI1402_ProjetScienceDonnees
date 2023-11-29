import pandas as pd
import numpy as np
import os
import locale
import calendar
from pathlib import Path
from references import mois_cat_type, jours_cat_type


import warnings

warnings.filterwarnings(action="ignore")

pd.options.mode.chained_assignment = None

locale.setlocale(category=locale.LC_ALL, locale="fr_CA.UTF-8")


def import_data(dep="20181228", fin="20221231") -> pd.DataFrame:
    """
    Import des données avec dates actuellement disponibles
    """
    path_to_interim_data = os.path.join(Path(__file__).parents[2], "data/interim/")
    file_parquet = "demande_meteo.parquet"

    df = pd.read_parquet(
        path=os.path.join(path_to_interim_data, file_parquet),
        engine="pyarrow",
    )
    return df[dep:fin]


def create_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Création des features concernant les dates
    """
    df = df.copy()
    df["date"] = df.index
    df["hourofday"] = df["date"].dt.hour
    df["quarter"] = df["date"].dt.quarter
    df["year"] = df["date"].dt.year
    df["dayofyear"] = df["date"].dt.dayofyear
    df["dayofmonth"] = df["date"].dt.day
    df["weekofyear"] = df["date"].dt.isocalendar().week.astype("int32")

    # Saisons
    df["date_offset"] = (df.date.dt.month * 100 + df.date.dt.day - 320) % 1300
    df["season"] = pd.cut(
        df["date_offset"],
        [0, 300, 602, 900, 1300],
        labels=[
            "Printemps",
            "Été",
            "Automne",
            "Hiver",
        ],
    )

    # Mois et jour comme variable "catégorie"
    df["idx_Mois"] = df.index.month
    df["idx_Jour"] = df.index.dayofweek

    df["month"] = (
        df["idx_Mois"]
        .apply(lambda x: calendar.month_name[x].capitalize())
        .astype(mois_cat_type)
    )
    df["dayofweek"] = (
        df["idx_Jour"]
        .apply(lambda x: calendar.day_name[x].capitalize())
        .astype(jours_cat_type)
    )

    df["isWeekend"] = df["idx_Jour"].apply(lambda x: 1 if x in [5, 6] else 0)

    # Application d'un cycle sur la durée du jour et de l'année
    # [-1 : 1] avec sinus et cosinus
    day = 60 * 60 * 24
    year = 365.2425 * day

    df["Seconds"] = df.index.map(pd.Timestamp.timestamp)

    df["day_sin"] = np.sin(df["Seconds"] * (2 * np.pi / day))
    df["day_cos"] = np.cos(df["Seconds"] * (2 * np.pi / day))
    df["year_sin"] = np.sin(df["Seconds"] * (2 * np.pi / year))
    df["year_cos"] = np.cos(df["Seconds"] * (2 * np.pi / year))

    # Éliminons les colonnes non requises
    df = df.drop(columns=["date", "Seconds", "date_offset", "idx_Jour", "idx_Mois"])

    return df


def create_deltaTemp_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Création des features concernant les dates
    """
    df = df.copy()

    base_CDD_21 = 21
    base_CDD_24 = 24
    base_HDD_18 = 18
    base_HDD_16 = 16

    df["CDD_21"] = df.Temp.apply(lambda t: 0 if t <= base_CDD_21 else t - base_CDD_21)
    df["HDD_18"] = df.Temp.apply(lambda t: 0 if t >= base_HDD_18 else base_HDD_18 - t)
    df["CDD_24"] = df.Temp.apply(lambda t: 0 if t <= base_CDD_24 else t - base_CDD_24)
    df["HDD_16"] = df.Temp.apply(lambda t: 0 if t >= base_HDD_16 else base_HDD_16 - t)

    df["DT_18-21"] = df["HDD_18"] + df["CDD_21"]
    df["DT_16-24"] = df["HDD_16"] + df["CDD_24"]

    df["DT_18"] = abs(df["Temp"] - base_HDD_18)
    df["DT_21"] = abs(df["Temp"] - base_CDD_21)

    return df


def create_lag_features(
    df: pd.DataFrame,
    caract: [str] = ["Temp", "DT_18-21", "DT_16-24", "DT_18", "DT_21"],
    lags: [int] = [1, 2, 3, 4, 6, 24],
) -> pd.DataFrame:
    """
    Création des caractéristiques avec délai (lag ou shift)
    """
    df = df.copy()

    df_lag = df[caract]

    df_lagged = df_lag.assign(
        **{f"{col}_LAG_t-{lag}h": df[col].shift(lag) for lag in lags for col in df_lag},
    )

    return df.join(df_lagged.drop(columns=df_lag.columns.to_list(), axis=1))


def create_window_features(
    df: pd.DataFrame,
    caract: [str] = ["Temp", "DT_18-21", "DT_16-24", "DT_18", "DT_21"],
    fenetres: [int] = [1, 2, 3, 4, 6, 24],
) -> pd.DataFrame:
    """
    Création des caractéristiques avec moyenne mobile (rolling windows)
    """
    df = df.copy()

    df_fen = df[caract]

    df_fenetres = df_fen.assign(
        **{
            f"{col}_MOYMOBILE_t-{fenetre}h": df[col].rolling(fenetre).mean()
            for fenetre in fenetres
            for col in df_fen
        },
    )

    return df.join(df_fenetres.drop(df_fen.columns.to_list(), axis=1))


def import_and_create_features(
    dep="20181228",  # Départ plus tôt pour permettre calcul lag / moy mobile sur Température
    fin="20221231",
    caract: [str] = ["Temp", "DT_18-21", "DT_16-24", "DT_18", "DT_21"],
    lags: [int] = [1, 2, 3, 4, 6, 24],
    fenetres: [int] = [1, 2, 3, 4, 6, 24],
) -> pd.DataFrame:
    """
    Import des données intérimaires d'entrées et création des features pour le ML
    """
    df = import_data(dep=dep, fin=fin)
    df = create_date_features(df=df)
    df = create_deltaTemp_features(df=df)
    df = create_lag_features(df=df, caract=caract, lags=lags)
    df = create_window_features(df=df, caract=caract, fenetres=fenetres)

    return df


if __name__ == "__main__":
    df = import_and_create_features()
    print(df)
