import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import os
import optuna
import warnings
from rich import print
from datetime import date
from references import *
from src import *

from pathlib import Path
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse

warnings.filterwarnings(action="ignore")


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


def objective(trial):
    base_score = trial.suggest_float("base_score", 0.3, 0.7)
    n_estimators = trial.suggest_int("n_estimators", 1000, 3000)
    max_depth = trial.suggest_int("max_depth", 3, 6)  # defaut 6, typique 3-10,
    learning_rate = trial.suggest_float(
        "learning_rate",
        0.005,
        0.2,
        log=True,
    )  # Typical final values : 0.01-0.2, alias eta
    gamma = trial.suggest_float(
        "gamma", 0, 5
    )  # defaut 0, range 0-inf, alias min_split_loss
    min_child_weight = trial.suggest_int(
        "min_child_weight", 3, 7
    )  # defaut 1, range 0-inf
    max_delta_step = trial.suggest_int(
        "max_delta_step", 0, 2
    )  # defaut 0, range 0-inf, typ 1-10
    subsample = trial.suggest_float(
        "subsample", 0.5, 1
    )  # defaut 1, typ 0.5-1, range 0-1
    reg_lambda = trial.suggest_float("reg_lambda", 6, 8)  # defaut 1, , typ 1+
    alpha = trial.suggest_float("alpha", 6, 10)  # def 0, typ 0+

    booster = "gbtree"

    reg = xgb.XGBRegressor(
        objective="reg:squarederror",
        booster=booster,
        tree_method="auto",
        predictor="cpu_predictor",
        early_stopping_rounds=50,
        base_score=base_score,
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        gamma=gamma,
        min_child_weight=min_child_weight,
        max_delta_step=max_delta_step,
        subsample=subsample,
        reg_lambda=reg_lambda,
        alpha=alpha,
    )

    reg.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=False,
    )

    return reg.best_score


if __name__ == "__main__":
    path_to_models = os.path.join(Path(__file__).parents[2], "models")
    file_model = "optuna_best_model.json"
    path = os.path.join(path_to_models, file_model)

    n_trials = 10

    (
        df,
        InfoDates,
    ) = import_and_create_features_no_categorical(
        fenetres=[1, 2, 3, 4, 6, 8, 12, 16, 24],
        fin="20221231",
        getInfoDate=True,
    )

    df = df.dropna()

    FEATURES = df.columns.to_list()[1:]  # Enlevons MW en première colonne
    TARGET = "MW"

    print(
        f"Nous avons {len(FEATURES)} caractéristiques dans le modèle après la création de celles-ci."
    )

    date_split = "2022-01-01"

    train = df.iloc[df.index < date_split]
    test = df.iloc[df.index >= date_split]

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]

    print("\n*************** Début de l'étude ***************\n")

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    best_value = study.best_value

    print("\n*************** Fin de l'étude ***************\n")
    print(
        f"La meilleur valeur obtenue est {best_value:0.2f} avec les paramètres suivants : "
    )
    print(best_params)

    print(
        "################################################################################ "
    )

    reg_best = xgb.XGBRegressor(
        **best_params,
        booster="gbtree",
        objective="reg:squarederror",
        tree_method="auto",
        predictor="cpu_predictor",
    )

    reg_best.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=250,
    )

    reg_best.save_model(path)
