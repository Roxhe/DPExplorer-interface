import streamlit as st
import pandas as pd
from utils import fetch_user_data  # Import de ta fonction d'API

# Configuration de la page
st.set_page_config(page_title="DPExplorer - Prioriser vos travaux", page_icon="🛠️", layout="centered")

# Code couleur des étiquettes DPE
dpe_colors = {
    "A": "#319a31",  # Vert foncé
    "B": "#33cc33",  # Vert
    "C": "#ccff33",  # Vert Jaune
    "D": "#ffff00",  # Jaune
    "E": "#ffcc00",  # Orange Jaune
    "F": "#ff9a33",  # Orange
    "G": "#ff0000",  # Rouge foncé
}

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur pour le N°DPE
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")

    # Sélection d'une étiquette cible via cases colorées cliquables
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")

    # Colonne pour afficher les étiquettes
    selected_label = None
    cols = st.columns(len(dpe_colors))  # Création d'une colonne par étiquette

    for i, (label, color) in enumerate(dpe_colors.items()):
        with cols[i]:
            # Création de boutons visuels avec HTML et CSS
            button_clicked = st.markdown(
                f"""
                <div style='
                    display: inline-block;
                    background-color: {color};
                    color: white;
                    text-align: center;
                    border-radius: 10px;
                    padding: 15px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);'
                    onclick="window.location.href='?label={label}'">
                    {label}
                </div>
                """,
                unsafe_allow_html=True
            )

    # Affichage de l'étiquette sélectionnée
    selected_label = st.query_params.get("label")
    if selected_label:
        st.success(f"✅ Vous avez sélectionné l'étiquette : {selected_label}")

    # Bouton pour lancer la récupération
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
