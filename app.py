import streamlit as st
from utils import fetch_user_data, api_final_process

# Initialisation de l'état de session pour la navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "DPExplorer"

# Fonction pour changer de page
def navigate_to(page):
    st.session_state["current_page"] = page

# Barre latérale avec des boutons pour changer de page
st.sidebar.title("Navigation")
if st.sidebar.button("Accéder à DPExplorer"):
    navigate_to("DPExplorer")
if st.sidebar.button("À propos"):
    navigate_to("À propos")

# Page "DPExplorer"
if st.session_state["current_page"] == "DPExplorer":
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

    def main():
        st.title("🖌️ DPExplorer 🛠️")
        st.write("Optimisez vos travaux pour atteindre une meilleure étiquette énergétique. (Valide uniquement pour les DPE établis après juillet 2021)")

        # Initialiser l'état pour gérer le N°DPE
        if "n_dpe_valid" not in st.session_state:
            st.session_state["n_dpe_valid"] = False
        if "etiquette_dpe" not in st.session_state:
            st.session_state["etiquette_dpe"] = None
        if "note_cible" not in st.session_state:
            st.session_state["note_cible"] = None

        # Étape 1 : Entrée utilisateur pour le N°DPE avec bouton de validation
        if not st.session_state["n_dpe_valid"]:
            n_dpe = st.text_input(
                "📄 Entrez votre N°DPE : (Exemple : 2494E3076086T)",
                key="n_dpe_input",
                placeholder="Exemple : 2494E3076086T"
            )
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
            selected_label = st.selectbox(
                "Choisissez une étiquette cible :",
                options=possible_labels,
                key="dpe_selectbox"
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
            st.write("**Vos infos:**")
            st.write(f"- **N°DPE :** {st.session_state['n_dpe']}")
            st.write(f"- **Note cible :** {st.session_state['note_cible']}")

            # Lancer le processus final
            if st.button("🛠️ Lancer le processus final"):
                with st.spinner("Traitement en cours..."):
                    results = api_final_process(st.session_state["n_dpe"], st.session_state["note_cible"])
                    st.success("🎉 Analyse terminée ! Voici vos résultats :")

                    # Section des résultats textuels
                    if results:
                        for result in results[:-1]:
                            st.markdown(
                                f"""
                                <div style='
                                    background-color: #f8f9fa;
                                    padding: 10px;
                                    border-left: 5px solid #007bff;
                                    margin-bottom: 10px;
                                    border-radius: 5px;
                                    '>
                                    <strong style="color: #007bff;">💡 {result}</strong>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        # Afficher l'étiquette atteinte (dernier élément de la liste)
                        label_reached = results[-1]
                        if label_reached in dpe_colors:
                            st.subheader("🔹 Étiquette atteinte :")
                            st.markdown(
                                f"<div class='dpe-button' style='background-color: {dpe_colors[label_reached]};'>{label_reached}</div>",
                                unsafe_allow_html=True
                            )

    main()

# Page "À propos"
elif st.session_state["current_page"] == "À propos":
    st.title("À propos")
    st.write("Bienvenue dans l'application DPExplorer !")
    st.markdown("""
# DPExplorer : Priorisez vos travaux pour un meilleur DPE

**DPExplorer** est un outil innovant qui aide à améliorer l'étiquette énergétique (DPE) d’un logement en identifiant les travaux d’isolation à prioriser.
Grâce à un modèle de Machine Learning **Random Forest**, il simule l’impact des rénovations potentielles et propose une priorisation intelligente basée sur les déperditions énergétiques des isolations actuelles.

---

## Données utilisées

**DPExplorer** fonctionne directement à partir de la base de données de l'ADEME et est utilisable sur tous les DPE fournis après juillet 2021.
Grâce au numéro de DPE, l'outil peut automatiquement collecter toutes les informations nécessaires sur le bâtiment, facilitant ainsi les simulations et l’évaluation des travaux à réaliser.

---

## À titre informatif

Il est important de noter que les travaux d'isolation, à eux seuls, ne suffisent généralement pas à faire passer un bâtiment d'une étiquette peu performante à une étiquette très performante.

**DPExplorer** est un outil conçu à titre informatif pour guider vos décisions sur les travaux d’amélioration énergétique.
Il ne remplace en aucun cas l’expertise et les conseils d’un professionnel qualifié, indispensable pour une évaluation complète et conforme aux normes en vigueur.

---

## Contexte du projet

Ce projet a été réalisé dans le cadre d’un projet de fin de bootcamp chez **Le Wagon**, par [Edouard Lenoir](https://www.linkedin.com/in/edouard-lenoir-/), [Alexandre Marmin](https://www.linkedin.com/in/alexandre-marmin/), [Léo Da Rocha](https://www.linkedin.com/in/léo-da-rocha-593695215/) et [Mehdi Plumaseau](https://www.linkedin.com/in/medhiplumasseau/).
Il illustre l’application des compétences en Machine Learning et en traitement de données pour répondre à un besoin concret.
    """)
