import streamlit as st
import pandas as pd
from utils import fetch_user_data, final_process

# Configuration de la page
st.set_page_config(page_title="DPExplorer - Prioriser vos travaux", page_icon="🛠️", layout="wide")

# Code couleur des étiquettes DPE (ordre inversé pour G -> A)
dpe_colors = {
    "G": "#ff0000",  # Rouge foncé
    "F": "#ff9a33",  # Orange
    "E": "#ffcc00",  # Orange Jaune
    "D": "#ffff00",  # Jaune
    "C": "#ccff33",  # Vert Jaune
    "B": "#33cc33",  # Vert
    "A": "#319a31",  # Vert foncé
}

# Ordre des étiquettes pour comparaison (de G vers A)
dpe_order = list(dpe_colors.keys())

# CSS global pour les étiquettes stylisées
st.markdown(
    """
    <style>
        .dpe-button {
            color: beige;
            text-shadow: -1px -1px 0 #000,
                         1px -1px 0 #000,
                         -1px 1px 0 #000,
                         1px 1px 0 #000;  /* Bordure noire autour des lettres */
            font-size: 28px; /* Taille agrandie */
            font-weight: bold; /* Texte en gras */
            text-align: center;
            border-radius: 10px;
            padding: 15px;
            width: 100%;
            display: block;
            margin: 10px auto;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fonction principale
def main():
    st.title("🖌️ DPExplorer 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Initialiser l'état pour gérer le N°DPE
    if "n_dpe_valid" not in st.session_state:
        st.session_state["n_dpe_valid"] = False
    if "etiquette_dpe" not in st.session_state:
        st.session_state["etiquette_dpe"] = None
    if "note_cible" not in st.session_state:
        st.session_state["note_cible"] = None

    # Étape 1 : Entrée utilisateur pour le N°DPE avec bouton de validation
    if not st.session_state["n_dpe_valid"]:
        n_dpe = st.text_input("📄 Entrez votre N°DPE :", key="n_dpe_input")
        if st.button("✅ Valider le N°DPE"):
            if n_dpe:
                st.info(f"🔄 Récupération des informations pour le N°DPE {n_dpe}...")
                with st.spinner("Analyse en cours..."):
                    # Appel à la fonction pour récupérer les données
                    data_df = fetch_user_data(n_dpe)

                    if not data_df.empty:
                        # Récupérer l'étiquette actuelle
                        etiquette_dpe = data_df["Etiquette_DPE"].iloc[0] if "Etiquette_DPE" in data_df.columns else None

                        if etiquette_dpe in dpe_order:
                            st.session_state["n_dpe_valid"] = True
                            st.session_state["etiquette_dpe"] = etiquette_dpe
                            st.session_state["possible_labels"] = dpe_order[dpe_order.index(etiquette_dpe) + 1:]
                            st.session_state["n_dpe"] = n_dpe
                        else:
                            st.error("⚠️ L'étiquette DPE actuelle est invalide.")
                    else:
                        st.error("⚠️ Aucune donnée trouvée pour le N°DPE fourni.")
            else:
                st.warning("Veuillez entrer un N°DPE valide.")

    # Étape 2 : Afficher les étiquettes si N°DPE validé
    if st.session_state["n_dpe_valid"]:
        etiquette_dpe = st.session_state["etiquette_dpe"]
        possible_labels = st.session_state["possible_labels"]

        # Afficher l'étiquette actuelle
        st.subheader("📊 Votre étiquette actuelle :")
        st.markdown(
            f"<div class='dpe-button' style='background-color: {dpe_colors[etiquette_dpe]};'>{etiquette_dpe}</div>",
            unsafe_allow_html=True
        )

        # Sélection des étiquettes cibles
        st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")
        selected_label = st.radio(
            "Choisissez une étiquette cible :",
            options=possible_labels,
            horizontal=True,
            key="dpe_radio"
        )

        # Stocker la note cible dans l'état de session
        if selected_label:
            st.session_state["note_cible"] = selected_label
            st.markdown(
                f"<div class='dpe-button' style='background-color: {dpe_colors[selected_label]};'>{selected_label}</div>",
                unsafe_allow_html=True
            )
            st.success(f"🎯 Votre objectif est d'atteindre l'étiquette : {selected_label}")

        # Afficher les valeurs stockées pour confirmation
        st.write("**Données disponibles pour la suite :**")
        st.write(f"- **N°DPE :** {st.session_state['n_dpe']}")
        st.write(f"- **Note cible :** {st.session_state['note_cible']}")

        # Lancer le processus final
        if st.button("🛠️ Lancer le processus final"):
            with st.spinner("Traitement en cours..."):
                results = final_process(st.session_state["n_dpe"], st.session_state["note_cible"])
                st.success("🎉 Analyse terminée ! Voici vos résultats :")
                for result in results:
                    st.write(f"- {result}")

if __name__ == "__main__":
    main()
