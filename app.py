import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from utils import fetch_user_data  # Import de ta fonction d'API

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

# Fonction pour construire les données avec couleurs pour AgGrid
def build_dpe_table():
    data = [{"Étiquette": label, "Couleur": color} for label, color in dpe_colors.items()]
    return pd.DataFrame(data)

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur pour le N°DPE
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")

    # Initialiser l'état pour conserver l'étiquette sélectionnée
    if "selected_label" not in st.session_state:
        st.session_state["selected_label"] = None

    # Affichage des étiquettes DPE dans AgGrid
    st.subheader("🎯 Sélectionnez votre Étiquette DPE Cible")
    dpe_df = build_dpe_table()

    # Configuration des options AgGrid
    gb = GridOptionsBuilder.from_dataframe(dpe_df)
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_column("Étiquette", cellStyle=lambda params: f"background-color: {params.data['Couleur']}; color: white; text-align: center; font-size: 16px; font-weight: bold;")
    grid_options = gb.build()

    # Affichage de la grille interactive
    grid_response = AgGrid(
        dpe_df,
        gridOptions=grid_options,
        height=200,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,  # Permet le JavaScript pour styliser les cellules
        theme="streamlit",  # Utilise le thème Streamlit
    )

    # Capture de la sélection
    selected_rows = grid_response["selected_rows"]
    if selected_rows:
        st.session_state["selected_label"] = selected_rows[0]["Étiquette"]

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
