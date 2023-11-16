import os
import pandas as pd
import json
import httpx
import locale
from pathlib import Path

locale.setlocale(locale.LC_ALL, "fr_CA.UTF-8")

import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")
col_HQ = "#FF9B00"


def update_demande_quotidienne_HQ() -> pd.DataFrame:
    """Création d'un fichier parquet et un graphique, contenant les dernières demandes horaires d'électricité
       Import à partir du fichier quotidien d'HQ

    Returns:
        DataFrame: DataFrame avec la demande horaire ['date', 'MW']
    """
    url = "https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/demande.json"

    path_to_interim_data = os.path.join(Path(__file__).parents[2], "data/interim/")
    path_to_img = os.path.join(Path(__file__).parents[2], "reports/figures/")
    file_parquet = "quotidien_demande_HQ.parquet"
    file_image = "quotidien_demande_HQ.png"

    # Obtenir les données sur le site HQ
    r = httpx.get(url)
    data = json.loads(r.text)

    df = (
        pd.DataFrame.from_records(data["details"])
        .rename(columns={"valeurs": "MW"})
        .set_index("date")
    )
    df.index = pd.to_datetime(df.index)
    df["MW"] = df["MW"].apply(lambda x: x.get("demandeTotal"))
    df = df.dropna()

    # Enregistrer le graphique
    df.plot(
        style="-",
        ms=1.5,
        fontsize=16,
        figsize=(15, 5),
        xlabel="",
        ylabel="MW",
        legend=False,
        color=col_HQ,
    )

    plt.title(
        f"Demande électrique le {str(df.index.date[0].strftime('%d %B %Y'))} et le jour suivant",
        fontsize=24,
    )
    plt.tight_layout()
    plt.savefig(os.path.join(path_to_img, file_image), dpi=300)

    print(f"Sauvegardons le graphique : {os.path.join(path_to_img, file_image)}\n")

    # Regrouper par heure
    df["date_"] = df.index.date
    df["heure_"] = df.index.hour
    df["dh"] = df["date_"].astype(str) + " " + df["heure_"].astype(str) + ":00:00"
    df_grouped = pd.DataFrame(df.groupby(["dh"]).MW.mean())
    df_grouped.index = pd.to_datetime(df_grouped.index)
    df_grouped.sort_index(inplace=True)
    df_grouped = df_grouped.iloc[:-1]
    df_grouped.index.names = ["date"]

    # Lire les données existantes et combiner avec les nouvelles données
    nouveau_df = pd.read_parquet(
        path=os.path.join(path_to_interim_data, file_parquet),
        engine="pyarrow",
    ).combine_first(df_grouped)

    #  Enregistrer le nouveau fichier par dessus l'existant
    nouveau_df.to_parquet(
        path=os.path.join(path_to_interim_data, file_parquet),
        engine="pyarrow",
    )

    print(
        f"\nLe fichier de données quotidiennes de la demande électrique possède maintenant {nouveau_df.shape[0]} heures.\n"
    )

    return nouveau_df


if __name__ == "__main__":
    update_demande_quotidienne_HQ()
