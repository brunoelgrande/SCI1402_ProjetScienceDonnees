import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
import os
import warnings

from src import *
from pathlib import Path
from rich import print

warnings.filterwarnings(action="ignore")

# Charger le modèle
path_to_models = os.path.join(Path(__file__).parents[2], "models")
file_model = "optuna_best_model.json"
path = os.path.join(path_to_models, file_model)

loaded_reg = xgb.XGBRegressor()
loaded_reg.load_model(path)

print(loaded_reg.base_score)

# DF avec données historiques + 16 jours de prédictions de températures
(df_all_time, InfoDates) = import_and_create_features_no_categorical(getInfoDate=True)

FEATURES = df_all_time.columns.to_list()[1:]  # Enlevons MW en première colonne
TARGET = "MW"

df_all_time["d"] = df_all_time.index
df_all_time["isFuture"] = df_all_time["d"].apply(
    lambda x: x > InfoDates.get("dateMaxMW")
)

## Pour avoir de la demande à comparer avec prédictions
df_all_time["isFuture_but_MW_History"] = df_all_time["d"].apply(
    lambda x: x > datetime(2023, 11, 12)
)

df_all_time = df_all_time.drop(columns=["d"])

# Enlève données Temp manquantes à la fin du df
df_all_time = df_all_time.loc[df_all_time.Temp.notna()]

# Gardons les dates futures (ou dans ce cas, les dates d'historique de demande - 12 nov 2023)
future_w_features = df_all_time.query("isFuture_but_MW_History").copy()

# Réalisons les prédictions sur les données "futures"
future_w_features["pred"] = loaded_reg.predict(future_w_features[FEATURES])

# Visualisation
ax = future_w_features["pred"].plot(
    figsize=(15, 5),
    ms=1,
    lw=1,
    title="Prédiction de la demande à partir du 12 novembre 2023 \nDébut de la récolte des données de demande électrique",
    label="Prédictions",
    ls="--",
    xlabel="",
    ylabel="MW",
)

future_w_features["MW"].plot(
    ax=ax,
    ms=1,
    lw=1,
    label="Demande réelle",
    xlabel="",
)

ax.axvline(
    datetime.now().date(),
    color="black",
    ls="--",
    linewidth=2,
)

ax.legend()
plt.tight_layout()
plt.show()
