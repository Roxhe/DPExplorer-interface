import streamlit as st
from utils import fetch_user_data  # Import de la fonction

# Configuration de la page
st.set_page_config(page_title="DPExplorer - Prioriser vos travaux", page_icon="🛠️", layout="centered")

# Interface principale
def main():
    st.title("🖌️ DPExplorer - Prioriser vos travaux 🛠️")
    st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique.")

    # Entrée utilisateur
    n_dpe = st.text_input("📄 Entrez votre N°DPE :", "")
    e_dpe_cible = st.text_input("🎯 Entrez votre Étiquette DPE Cible :", "")

    # Bouton pour récupérer les données
    if st.button("🔍 Connaitre vos priorités de travaux !"):
        if n_dpe and e_dpe_cible:
            st.info("🔄 Récupération des priorités de travaux...")
            with st.spinner("Analyse en cours..."):
                # Appel à la fonction importée
                data_df = fetch_user_data(n_dpe)

                # Affichage des résultats
                if not data_df.empty:
                    st.subheader("🔍 Résultats trouvés :")
                    st.dataframe(data_df)

                    st.success(f"🎯 Votre objectif est d'atteindre l'étiquette : {e_dpe_cible}")
                else:
                    st.warning("Aucune donnée trouvée pour le N°DPE fourni.")
        else:
            st.warning("Veuillez remplir les deux champs pour continuer.")

if __name__ == "__main__":
    main()
