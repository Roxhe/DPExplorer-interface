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

# Fonction pour générer des boutons colorés cliquables
def colored_buttons():
    selected_label = st.session_state.get("selected_label", None)
    cols = st.columns(len(dpe_colors))  # Une colonne par étiquette

    for i, (label, color) in enumerate(dpe_colors.items()):
        # Génération d'un bouton stylisé via Markdown
        button_html = f"""
            <button style="
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 10px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            ">{label}</button>
        """

        # Injecter le bouton avec Markdown
        with cols[i]:
            if st.markdown(
                f'<a href="?selected_label={label}" target="_self">{button_html}</a>',
                unsafe_allow_html=True,
            ):
                st.session_state["selected_label"] = label

    # Retourner l'étiquette sélectionnée
    return st.session_state.get("selected_label", None)

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur pour le N°DPE
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")

    # Afficher les boutons colorés pour la sélection d'étiquette
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")
    selected_label = colored_buttons()

    # Afficher l'étiquette sélectionnée
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
