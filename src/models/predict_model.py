import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
import os

from pathlib import Path

from src import *
from references import *
from rich import print

################################################################################

# Fichiers : modèle et graphiques
path_to_models = os.path.join(Path(__file__).parents[2], "models")
file_model = "optuna_best_model.json"
path_file_model = os.path.join(path_to_models, file_model)

path_to_img = os.path.join(Path(__file__).parents[2], "reports/figures")
file_image = "predictions.png"
path_file_image = os.path.join(path_to_img, file_image)

################################################################################


def save_graph_prediction(
    df: pd.DataFrame,
    path_file_image=path_file_image,
    startDate: list() = [2023, 11, 12],
    onlyFuture: bool = False,
    pltShow: bool = False,
    pltSave: bool = True,
):
    if onlyFuture:
        date_debut = df.index.date[0]
        startDate = [date_debut.year, date_debut.month, date_debut.day]

    list_mois = mois_cat_type.categories
    mois = (list_mois[startDate[1] - 1]).lower()

    # Visualisation
    ax = df["pred"].plot(
        figsize=(15, 5),
        ms=1,
        lw=1,
        title=f"Prédiction de la demande électrique à partir du {startDate[2]} {mois} {startDate[0]}",
        label="Prédiction",
        ls="--",
        xlabel="",
        ylabel="MW",
        color=col_demande_predite,
    )

    df["MW"].plot(
        ax=ax,
        ms=1,
        lw=1,
        label="Demande réelle",
        xlabel="",
        color=col_demande_relle,
    )

    ax.axvline(
        datetime.now().date(),
        color="black",
        ls="--",
        linewidth=2,
        alpha=0.7,
    )

    ax.legend()

    plt.tight_layout()

    if pltSave:
        plt.savefig(path_file_image, dpi=300)
        print(f"Graphique prédiction enregistré : {path_file_image}")

    if pltShow:
        plt.show()


def make_predictions(
    onlyFuture: bool = False,
    startDate=[2023, 11, 12],
    path_file_model=path_file_model,
) -> pd.DataFrame:
    # Charger le modèle
    loaded_reg = xgb.XGBRegressor()
    loaded_reg.load_model(path_file_model)

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

    ## Pour avoir de la demande à comparer avec prédictions (version temporaire)
    df_all_time["isFuture_but_MW_History"] = df_all_time["d"].apply(
        lambda x: x
        > datetime(year=startDate[0], month=startDate[1], day=startDate[2], hour=12)
    )

    df_all_time = df_all_time.drop(columns=["d"])

    # Enlève données Temp manquantes à la fin du df
    df_all_time = df_all_time.loc[df_all_time.Temp.notna()]

    if onlyFuture:
        future_w_features = df_all_time.query("isFuture").copy()
    else:
        future_w_features = df_all_time.query("isFuture_but_MW_History").copy()

    # Réalisons les prédictions sur les données "futures"
    future_w_features["pred"] = loaded_reg.predict(future_w_features[FEATURES])

    return future_w_features


if __name__ == "__main__":
    # Date de début des prédictions
    startDate = [2023, 11, 12]
    ## ou True :
    onlyFuture = False

    df = make_predictions(
        onlyFuture=onlyFuture,
        startDate=startDate,
        path_file_model=path_file_model,
    )

    # Sauvegarder graphique
    save_graph_prediction(
        df=df,
        path_file_image=path_file_image,
        startDate=startDate,
        onlyFuture=onlyFuture,
        pltSave=True,
        pltShow=False,
    )
