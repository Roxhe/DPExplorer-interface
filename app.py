import streamlit as st
import pandas as pd
from utils import fetch_user_data  # Import de la fonction d'API

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

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur pour le N°DPE
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")

    # Tableau visuel interactif pour sélectionner l'étiquette cible
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")

    # Création des options avec radio
    selected_label = st.radio(
        "Cliquez sur une case pour sélectionner une étiquette :",
        options=list(dpe_colors.keys()),
        format_func=lambda x: f"Étiquette {x}",  # Option de format
        horizontal=True
    )

    # Affichage des étiquettes sous forme de cases colorées avec HTML
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; gap: 10px;">
            {"".join([
                f"<div style='background-color:{dpe_colors[label]}; color:white; padding:15px; text-align:center; width:50px; border-radius:8px; "
                f"font-weight:bold; cursor:pointer; border: 3px solid { '#FFFFFF' if selected_label != label else '#000000'};'>"
                f"{label}</div>"
                for label in dpe_colors.keys()
            ])}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Bouton de confirmation pour lancer l'analyse
    if st.button("🔍 Connaitre vos priorités de travaux !"):
        if n_dpe and selected_label:
            st.info(f"🔄 Récupération des priorités de travaux pour N°DPE {n_dpe}...")
            with st.spinner("Analyse en cours..."):
                # Appel à la fonction pour récupérer les données
                data_df = fetch_user_data(n_dpe)

                # Affichage des résultats
                if not data_df.empty:
                    st.subheader("🔍 Résultats trouvés :")
                    st.dataframe(data_df)
                    st.success(f"🎯 Votre objectif est d'atteindre l'étiquette : {selected_label}")
                else:
                    st.warning("Aucune donnée trouvée pour le N°DPE fourni.")
        else:
            st.warning("Veuillez entrer votre N°DPE et sélectionner une étiquette cible.")

if __name__ == "__main__":
    main()
