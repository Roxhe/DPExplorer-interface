import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Mon Application Streamlit",
    page_icon="📊",
    layout="wide",
)

# Fonction principale
def main():
    # Titre et description
    st.title("Mon Application Streamlit")
    st.write("Bienvenue dans cette application Streamlit. Voici une démonstration simple.")

    # Barre latérale
    st.sidebar.header("Navigation")
    menu = st.sidebar.radio(
        "Choisissez une section :",
        ["Accueil", "Visualisation", "À propos"]
    )

    # Logique des pages
    if menu == "Accueil":
        st.subheader("Accueil")
        st.write("Cette section présente l'accueil de l'application.")
        st.image("https://source.unsplash.com/random/800x400", caption="Exemple d'image")

    elif menu == "Visualisation":
        st.subheader("Visualisation des données")
        st.write("Affichez des graphiques ou des tableaux de données ici.")

        # Exemple de graphique
        import pandas as pd
        import matplotlib.pyplot as plt

        # Exemple de données
        data = pd.DataFrame({
            'x': range(1, 11),
            'y': [x**2 for x in range(1, 11)]
        })

        st.write("Voici un exemple de graphique :")
        fig, ax = plt.subplots()
        ax.plot(data['x'], data['y'], marker='o', linestyle='-')
        ax.set_title("Exemple de graphique")
        ax.set_xlabel("Axe X")
        ax.set_ylabel("Axe Y")
        st.pyplot(fig)

    elif menu == "À propos":
        st.subheader("À propos")
        st.write("""
        Cette application Streamlit a été créée pour démontrer les fonctionnalités de base.
        """)
        st.info("Auteur : Votre Nom")

# Point d'entrée
if __name__ == "__main__":
    main()
