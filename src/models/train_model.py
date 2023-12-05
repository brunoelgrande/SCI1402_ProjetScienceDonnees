import pandas as pd
import numpy as np
import locale
from rich import print
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse

import warnings

warnings.filterwarnings(action="ignore")

pd.options.mode.chained_assignment = None

locale.setlocale(category=locale.LC_ALL, locale="fr_CA.UTF-8")


def calcul_erreurs(df: pd.DataFrame, nomColPrediction: str, nomColReel: str) -> dict:
    """Calcul et impressions d'erreurs sur un dataframe contenant les prédictions du modèle:
        - MSE : Mean Square Error
        - RMSE : Root Mean Square Error
        - MAE : Mean Average Error

    Args:
        df (pd.DataFrame): df contenant les prédictions et valeurs réelles
        nomColPrediction (str): nom de variable contenant les prédictions
        nomColReel (str): nom de variable contenant les données réelles

    Returns:
        dict: Calcul des 3 valeurs d'erreurs calculées.
    """
    Y = df[[nomColPrediction, nomColReel]].dropna()

    Y_true = Y[nomColReel].values
    Y_pred = Y[nomColPrediction].values

    MSE = mse(Y_true, Y_pred)
    RMSE = np.sqrt(MSE)
    MAE = mae(Y_true, Y_pred)

    print(
        f"Le MSE est de {MSE:0.1f}, le RMSE est de {RMSE:0.1f} et le MAE de {MAE:0.1f} pour un calcul sur {len(Y_true)} valeurs."
    )

    return {
        "MSE": MSE,
        "RMSE": RMSE,
        "MAE": MAE,
    }
