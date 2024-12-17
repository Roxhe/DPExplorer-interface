import streamlit as st
import pandas as pd
from utils import fetch_user_data  # Import de ta fonction existante

# Configuration de la page
st.set_page_config(page_title="DPExplorer - Prioriser vos travaux", page_icon="🛠️", layout="centered")

# Couleurs DPE pour les étiquettes
dpe_colors = {
    "A": "#009933",  # Vert foncé
    "B": "#66cc33",  # Vert clair
    "C": "#ffcc00",  # Jaune
    "D": "#ff9933",  # Orange
    "E": "#ff6600",  # Orange foncé
    "F": "#cc3300",  # Rouge clair
    "G": "#990000",  # Rouge foncé
}

# Fonction pour créer le tableau des étiquettes DPE
def create_dpe_table():
    dpe_data = pd.DataFrame({
        "Étiquette": ["G", "F", "E", "D", "C", "B", "A"],
        "Description": [
            "Très mauvaise performance",
            "Mauvaise performance",
            "Performance médiocre",
            "Performance moyenne",
            "Bonne performance",
            "Très bonne performance",
            "Excellente performance"
        ]
    })
    return dpe_data

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur pour le N°DPE
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")

    # Sélection de l'étiquette cible via tableau interactif
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")
    dpe_table = create_dpe_table()

    # Affichage du tableau avec un style
    styled_table = dpe_table.style.applymap(lambda _: "color: white;", subset="Étiquette")
    for label, color in dpe_colors.items():
        styled_table = styled_table.applymap(
            lambda v: f"background-color: {color}; color: white;" if v == label else "",
            subset="Étiquette"
        )

    # Sélecteur d'étiquette (dans une liste)
    e_dpe_cible = st.radio("Choisissez une étiquette cible :", options=dpe_table["Étiquette"])

    # Bouton pour lancer la récupération
    if st.button("🔍 Connaitre vos priorités de travaux !"):
        if n_dpe and e_dpe_cible:
            st.info(f"🔄 Récupération des priorités de travaux pour N°DPE {n_dpe}...")
            with st.spinner("Analyse en cours..."):
                # Appel à la fonction pour récupérer les données
                data_df = fetch_user_data(n_dpe)

                # Affichage des résultats
                if not data_df.empty:
                    st.subheader("🔍 Résultats trouvés :")
                    st.dataframe(data_df)
                    st.success(f"🎯 Votre objectif est d'atteindre l'étiquette : {e_dpe_cible}")
                else:
                    st.warning("Aucune donnée trouvée pour le N°DPE fourni.")
        else:
            st.warning("Veuillez remplir le N°DPE et sélectionner une étiquette cible.")

if __name__ == "__main__":
    main()
