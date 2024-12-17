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

    # Utilisation des colonnes pour aligner les boutons
    cols = st.columns(len(dpe_colors))  # Une colonne par bouton coloré

    # Création des boutons dynamiquement
    for i, (label, color) in enumerate(dpe_colors.items()):
        with cols[i]:
            if st.button(
                label,
                key=label,
                help=f"Sélectionnez l'étiquette {label}",
                use_container_width=True,
            ):
                st.session_state["selected_label"] = label  # Enregistrer l'étiquette sélectionnée
                selected_label = label

            # Afficher les couleurs de fond avec markdown pour style visuel
            st.markdown(
                f"""
                <style>
                div[data-testid="stButton"] > button {{
                    background-color: {color};
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 8px;
                    height: 50px;
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )

    # Confirmation de la sélection
    if selected_label:
        st.success(f"✅ Vous avez sélectionné l'étiquette : {selected_label}")

    # Bouton pour lancer la récupération des priorités
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
