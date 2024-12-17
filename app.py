import streamlit as st
import requests

st.title("🖌️DPExplorer - Prioriser vos travaux 🛠️")

n_dpe = st.text_input("📄Entrez votre N°DPE : ")
E_dpe_cible = st.text_input("🎯Entrez votre Etiquette DPE Cible : ")


if st.button("Connaitre vos priorités de travaux !"):
    params = {
        "n_dpe": n_dpe,
    }
