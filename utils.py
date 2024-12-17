import requests
import pandas as pd

from api_params import *

base_url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"  # URL de l'API



def get_columns_to_encode():

    params = {"size": 750}  # Paramètre fixe pour la requête

    # Préparation de la requête
    custom_request = requests.Request("GET", base_url, params=params).prepare()

    # Envoi de la requête et traitement de la réponse
    with requests.Session() as session:
        response = session.send(custom_request)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            df = pd.DataFrame(results)
            columns_to_encode = [
                col for col in df.columns
                if any(keyword in col for keyword in keywords_flex) or col in keywords_strict
            ]
            return columns_to_encode
        else:
            print("Aucune donnée trouvée dans les résultats.")
            return []
    else:
        raise Exception(f"Erreur {response.status_code} lors de la requête à l'API.")


# Sélection des colonnes
columns_to_encode = get_columns_to_encode()


def fetch_user_data(n_dpe):

    params = {
            "size": 1,  # Nombre de lignes à récupérer
            "q_fields": "N°DPE",  # Champ sur lequel filtrer
            "q": n_dpe,  # Valeur du filtre ()
            "select": ",".join(columns_to_encode)  # Colonnes à récupérer
        }


    custom_request = requests.Request("GET", base_url, params=params).prepare()
    with requests.Session() as session:
            response = session.send(custom_request)

    if response.status_code == 200:
        print(f"Récupération réussie pour N°DPE - {n_dpe}")
        data = response.json()
        data = data.get("results", [])
    else:
        print(f"Erreur {response.status_code} pour N°DPE - {n_dpe}")

    return data
