import requests
import os


API_KEY = os.getenv("API_KEY")  # Clé d'authentification pour accéder à l'API
base_url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"  # URL de l'API
headers = {
    "Authorization": f"Bearer {API_KEY}"  # Inclusion de la clé API dans l'en-tête pour l'authentification
}

def fetch_user_data():
    n_dpe = str(input("Votre N°de DPE (d'après Juillet 2021) : "))

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


    user_df = pd.DataFrame(data)
    return user_df
