import pandas as pandas
import streamlit as st
import xgboost as xgb
import os

from src import *
from references import *
from pathlib import Path


@st.cache_resource
def st_load_model() -> xgb.XGBRegressor:
    # Fichier du modèle
    path_to_models = os.path.join(Path(__file__).parents[1], "models")
    file_model = "optuna_best_model.json"

    # Charger le modèle
    model = xgb.XGBRegressor()
    model.load_model(os.path.join(path_to_models, file_model))

    return model


def st_load_data_features() -> tuple:
    # DF avec données historiques + 16 jours de prédictions de températures
    (df_all_time, InfoDates) = import_and_create_features_no_categorical(
        getInfoDate=True
    )

    # Création des FEATURES
    FEATURES = df_all_time.columns.to_list()[1:]  # Enlevons MW en première colonne

    # Créer séparation entre valeurs futures et existantes
    df_all_time["d"] = df_all_time.index
    df_all_time["isFuture"] = df_all_time["d"].apply(
        lambda x: x > InfoDates.get("dateMaxMW")
    )

    df_all_time = df_all_time.drop(columns=["d"])

    # Enlève données Temp manquantes à la fin du df
    df_all_time = df_all_time.loc[df_all_time.Temp.notna()]

    return df_all_time, FEATURES


def st_make_predictions(
    df: pd.DataFrame,
    model: xgb.XGBRegressor,
    FEATURES: list,
) -> pd.DataFrame:
    df["prediction"] = model.predict(
        X=df[FEATURES],
        iteration_range=(0, model.best_iteration + 1),
    )

    return df
