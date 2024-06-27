# -*- coding: utf-8 -*-

# Référence : B_b_1 : Obtenir les données - Historique demande d'électricité HQ
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
from datetime import timedelta
from pathlib import Path

from references import colors_pal

plt.style.use(style="fivethirtyeight")

################################################################################


def creation_grap_hist_HQ_import(dfs, **kwargs) -> None:
    """
    Création de graphiques montrant la variation de la demande par année
    """
    # Nous voulons 2 colonnes par nb_rangees
    nb_rangees = math.ceil(len(dfs) / 2)

    fig, axs = plt.subplots(ncols=2, nrows=nb_rangees, figsize=(16, 4* nb_rangees))

    index_dfs = 0

    for row in range(nb_rangees):
        for col in range(2):
            if index_dfs < len(dfs):
                axs[row, col].plot(
                    dfs[index_dfs],
                    color=colors_pal[index_dfs % len(colors_pal)],
                    linewidth=0.5,
                    linestyle="-",
                    alpha=0.75,
                )
                axs[row, col].set_title(
                    f"Demande Électricité HQ - {dfs[index_dfs].index[0].year}", fontsize=14
                )
                axs[row, col].set_xlabel("")
                axs[row, col].set_ylabel("MW", fontsize=14)
            index_dfs += 1

    fig.suptitle(
        "Demande en électricité au Québec - Importation des fichiers", fontsize=24
    )

    # Si nous voulons sauver le graph

    if file_to_save := kwargs.get("file_to_save", False):
        print(f"Sauvegardons le graphique : {file_to_save}\n")
        plt.savefig(fname=file_to_save, dpi=300)

    else:
        plt.show()


def correction_donnes_hist_HQ_import(dfs) -> None:
    """
    Vérification et corrections des données importées :
    - Vérification s'il n'y a pas plus d'heure entre les données dans la colonne Date
    """
    index_dfs = 0

    for df in dfs:
        for i in range(df.shape[0] - 1):
            v = (df.index[i + 1] - df.index[i]) > timedelta(
                hours=2
            )  # on ne veut pas inclure les changements d'heures où delta = 2
            if v:
                print("Problème : ")
                print(df.index[i], df.index[i + 1], sep="\n")
                print("#" * 20)

                # Correction : on ajoute 1h au temps précédent
                as_list = df.index.tolist()
                as_list[i + 1] = df.index[i] + timedelta(hours=1)
                df.index = as_list

                print("Après Correction : ")
                print(df.index[i], df.index[i + 1], sep="\n")
                print("#" * 20, "\n")

                dfs[index_dfs] = df.copy()

        index_dfs += 1


################################################################################


def import_complet_donnees_historiques_HQ() -> None:
    """
    Dans le but d'automatiser l'importation des données, nous allons transformer en fonctions les différentes étapes principales, que nous pourrons enchaîner et automatiser, de même que de réutiliser dans d'autres processus.
        - Importer tous les fichiers dans dossiers `data/raw/hq`
        - Corriger les données
        - Créer une visualisation des données importées, par année (donc par fichier)
        - Concaténer tous les df
        - Exporter vers un df en format parquet dans `data/interim` pour utilisation subséquente
    """

    data_path = os.path.join(Path(__file__).parents[2], "data/raw/hq")
    img_path = os.path.join(Path(__file__).parents[2], "reports/figures")
    path_to_interim_data = os.path.join(Path(__file__).parents[2], "data/interim")

    file_parquet = "historique_demande_HQ.parquet"
    file_image = "historique_demande_HQ.png"

    dfs = list()

    files = sorted([f for f in os.listdir(data_path) if f.endswith(".xlsx")])

    for file in files:
        if file.endswith(".xlsx"):
            df = (
                pd.read_excel(os.path.join(data_path, file), engine="openpyxl")
                .rename(columns={"Date": "date", "Moyenne (MW)": "MW"})
                .set_index("date")
            )

            dfs.append(df)

    correction_donnes_hist_HQ_import(dfs)

    creation_grap_hist_HQ_import(dfs, file_to_save=os.path.join(img_path, file_image))

    demande = pd.concat(dfs)
    demande.index.name = "date"

    demande.to_parquet(
        path=os.path.join(path_to_interim_data, file_parquet), engine="pyarrow"
    )

    print(
        f"\nImport de {len(dfs)} fichier de données de demande d'életricité d'HQ terminé.\n"
    )


if __name__ == "__main__":
    import_complet_donnees_historiques_HQ()
