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

    # Sélection des étiquettes via des cadres interactifs
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")

    # Initialiser l'état pour conserver l'étiquette sélectionnée
    if "selected_label" not in st.session_state:
        st.session_state["selected_label"] = None

    # Création des colonnes pour aligner les cadres
    cols = st.columns(len(dpe_colors))  # Une colonne par étiquette

    for i, (label, color) in enumerate(dpe_colors.items()):
        with cols[i]:
            # Positionnement absolu pour superposer les boutons invisibles
            st.markdown(
                f"""
                <div style="
                    position: relative;
                    width: 100%;
                    text-align: center;">
                    <div style="
                        background-color: {color};
                        color: white;
                        text-align: center;
                        font-size: 20px;
                        font-weight: bold;
                        border-radius: 10px;
                        padding: 15px;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
                        position: relative;">
                        {label}
                    </div>
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;">
                        <form action="" method="get">
                            <input type="submit" name="button_{label}" value="" style="
                                opacity: 0;
                                width: 100%;
                                height: 100%;
                                cursor: pointer;">
                        </form>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Détecter si le bouton a été cliqué
            if f"button_{label}" in st.query_params:
                st.session_state["selected_label"] = label

    # Afficher l'étiquette sélectionnée
    selected_label = st.session_state["selected_label"]
    if selected_label:
        st.success(f"✅ Vous avez sélectionné l'étiquette : {selected_label}")

    # Bouton pour confirmer et récupérer les priorités
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
