import streamlit as st
import pandas as pd
from utils import fetch_user_data  # Import de ta fonction existante

# Configuration de la page
st.set_page_config(page_title="DPExplorer - Prioriser vos travaux", page_icon="🛠️", layout="centered")

# Code couleur des étiquettes DPE
dpe_colors = {
    "A": "#009933",  # Vert foncé
    "B": "#66cc33",  # Vert clair
    "C": "#ffcc00",  # Jaune
    "D": "#ff9933",  # Orange
    "E": "#ff6600",  # Orange foncé
    "F": "#cc3300",  # Rouge clair
    "G": "#990000",  # Rouge foncé
}

# Fonction pour afficher les étiquettes sous forme de tableau visuel
def display_dpe_table():
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")

    # Créer une ligne de colonnes pour afficher les étiquettes
    cols = st.columns(7)

    # Retourner la sélection de l'utilisateur
    selected_label = None
    for i, label in enumerate(dpe_colors.keys()):
        with cols[i]:
            st.markdown(
                f"<div style='background-color:{dpe_colors[label]};"
                f" color:white; border-radius:8px; text-align:center; padding:10px;'>"
                f"<b>{label}</b></div>",
                unsafe_allow_html=True
            )
            if st.button(f"🔘 {label}"):
                selected_label = label
    return selected_label

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur pour le N°DPE
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")

    # Afficher le tableau des étiquettes
    e_dpe_cible = display_dpe_table()

    # Bouton pour lancer la récupération
    if e_dpe_cible and n_dpe:
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
    elif not n_dpe:
        st.warning("Veuillez entrer votre N°DPE pour continuer.")
    elif not e_dpe_cible:
        st.info("Cliquez sur une étiquette pour la sélectionner.")

if __name__ == "__main__":
    main()
