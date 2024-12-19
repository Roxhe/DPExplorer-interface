import requests
import pandas as pd

from api_params import *

base_url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines"  # URL de l'API

import pandas as pd
import numpy as np
from joblib import load
from packages.preprocessing import clean_user_data, qualitative_to_quantitative_user, preprocess_user_data
from interface.api_params import seuils_performance

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
        "q": n_dpe,  # Valeur du filtre
        "select": ",".join(columns_to_encode)  # Colonnes à récupérer
    }

    custom_request = requests.Request("GET", base_url, params=params).prepare()
    with requests.Session() as session:
        response = session.send(custom_request)

    if response.status_code == 200:
        print(f"Récupération réussie pour N°DPE - {n_dpe}")
        data = response.json().get("results", [])
        if data:  # Si des données sont présentes
            return pd.DataFrame(data)  # Retourne un DataFrame
        else:
            print("Aucune donnée trouvée pour ce N°DPE.")
            return pd.DataFrame()  # Retourne un DataFrame vide
    else:
        print(f"Erreur {response.status_code} pour N°DPE - {n_dpe}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur


def calculer_deperdition(row):
    total_deperdition_m2 = 0
    row = row.drop(columns=['Qualité_isolation_enveloppe'])
    toits = [
        "Qualité_isolation_plancher_haut_comble_perdu",
        "Qualité_isolation_plancher_haut_comble_aménagé",
        "Qualité_isolation_plancher_haut_toit_terrase"
    ]
    somme_toit = 0
    compteur_toit = 0
    for toit in toits:
        if toit in row:
            niveau_toit = row[toit].values[0]
            if isinstance(niveau_toit, (int, float)):
                somme_toit += niveau_toit
                compteur_toit += 1
    if compteur_toit > 0:
        moyenne_toit = somme_toit / compteur_toit
        total_deperdition_m2 += moyenne_toit
    for colonne, niveaux in seuils_performance.items():
        if colonne not in toits and colonne in row:
            niveau = row[colonne].values[0]
            if isinstance(niveau, (int, float)):
                total_deperdition_m2 += niveau
    total_deperdition_m2 = round(total_deperdition_m2, 3)
    return total_deperdition_m2


def attribuer_etiquette(deperdition):
    if deperdition < 1.821:
        return 'A'
    elif deperdition < 2.418:
        return 'B'
    elif deperdition < 3.076:
        return 'C'
    elif deperdition < 3.384:
        return 'D'
    else:
        return "Vos travaux d'isolations sont insuffisants."


def deperdition_par_etiquette(note_cible):
    if note_cible == 'A':
        return 1.821
    elif note_cible == 'B':
        return 2.418
    elif note_cible == 'C':
        return 3.076
    elif note_cible == 'D':
        return 3.384


def get_qualite_label(value, seuils):
    for label, seuil in seuils.items():
        if value == seuil:
            return label
    return "Unknown"


def final_process(n_dpe, note_cible):
    results = []
    data = fetch_user_data(n_dpe)
    data_cleaned = clean_user_data(data)
    data_converted = qualitative_to_quantitative_user(data_cleaned, mapping=seuils_performance)

    iterations = 0
    total_deperdition_m2 = calculer_deperdition(data_converted)
    deperdition_initial = total_deperdition_m2
    init_note_cible = note_cible
    note_cible = deperdition_par_etiquette(note_cible=note_cible)
    initial_qualities = data_converted.iloc[0].to_dict()

    while total_deperdition_m2 > note_cible:
        amelioration_effectuee = False
        for colonne, niveaux in seuils_performance.items():
            if colonne in data_converted.columns:
                current_value = data_converted.at[0, colonne]
                niveaux_tries = sorted(list(niveaux.values()), reverse=True)
                for i, niveau in enumerate(niveaux_tries):
                    if niveau < current_value:
                        data_converted.at[0, colonne] = niveau
                        total_deperdition_m2 = calculer_deperdition(data_converted)
                        iterations += 1
                        amelioration_effectuee = True
                        break
                if amelioration_effectuee:
                    break
        if not amelioration_effectuee:
            print("Aucune amélioration possible, vérifiez les seuils de performance.")
            break

    def format_colonne(nom_colonne):
        return nom_colonne.replace("Qualité_isolation_", "").replace("_", " ").capitalize()

    final_qualities = data_converted.iloc[0].to_dict()

    for colonne in seuils_performance.keys():
        formatted_colonne = format_colonne(colonne)

        initial_label = get_qualite_label(initial_qualities.get(colonne, None), seuils_performance[colonne])
        final_label = get_qualite_label(final_qualities.get(colonne, None), seuils_performance[colonne])

        if initial_label == final_label:
            continue
        elif final_label == "moyenne":
            results.append(f"{formatted_colonne}: L'isolation est satisfaisante, mais une optimisation supplémentaire serait bénéfique.")
        elif final_label == "bonne":
            results.append(f"{formatted_colonne}: L'isolation nécessite des révisions pour améliorer la performance thermique.")
        elif final_label == "très bonne":
            results.append(f"{formatted_colonne}: L'isolation doit être assidûment rénovée pour une performance optimale.")
    ratio = (total_deperdition_m2 - deperdition_initial) / deperdition_initial
    data_converted['Besoin_chauffage'] = data_converted['Besoin_chauffage'] + data_converted['Besoin_chauffage'] * ratio
    data_converted['Besoin_ECS'] = data_converted['Besoin_ECS'] + data_converted['Besoin_ECS'] * ratio
    data_converted['Conso_5_usages/m²_é_finale'] = data_converted['Conso_5_usages/m²_é_finale'] + data_converted['Conso_5_usages/m²_é_finale'] * ratio
    data_converted['Conso_5_usages_é_finale'] = data_converted['Conso_5_usages_é_finale'] + data_converted['Conso_5_usages_é_finale'] * ratio
    data_converted['Emission_GES_5_usages_par_m²'] = data_converted['Emission_GES_5_usages_par_m²'] + data_converted['Emission_GES_5_usages_par_m²'] * ratio
    data_converted['Emission_GES_5_usages'] = data_converted['Emission_GES_5_usages'] + data_converted['Emission_GES_5_usages'] * ratio

    X_user = preprocess_user_data(data_converted)
    loaded_model = load('pkl_file/model.pkl')
    pred_w_new_deperditions = loaded_model.predict(X_user)

    def convert_to_letters(array):
        mapping = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G'}
        return [mapping.get(value, '?') for value in array]

    if pred_w_new_deperditions != init_note_cible:
        results.append(
            "Changer les isolations n'est pas suffisant pour atteindre la note cible, "
            "mais cela peut tout de même améliorer l'étiquette."
        )

    pred_w_new_deperditions = convert_to_letters(pred_w_new_deperditions)
    results.append(pred_w_new_deperditions)
    return results
