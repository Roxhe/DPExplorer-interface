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

    # Afficher les étiquettes sous forme de boutons colorés
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")

    selected_label = st.session_state.get("selected_label", None)

    # Utilisation des colonnes pour afficher les boutons colorés
    cols = st.columns(len(dpe_colors))  # Une colonne par étiquette

    for i, (label, color) in enumerate(dpe_colors.items()):
        # Bouton avec un style appliqué
        with cols[i]:
            button_html = f"""
            <style>
            div[data-testid="stButton"] > button {{
                background-color: {color} !important;
                color: white !important;
                font-size: 18px !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                height: 50px !important;
                width: 100% !important;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.3) !important;
            }}
            </style>
            """
            st.markdown(button_html, unsafe_allow_html=True)

            if st.button(label, key=label):
                st.session_state["selected_label"] = label
                selected_label = label

    # Confirmation de la sélection
    if selected_label:
        st.success(f"✅ Vous avez sélectionné l'étiquette : {selected_label}")

    # Bouton de confirmation pour lancer la récupération
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
