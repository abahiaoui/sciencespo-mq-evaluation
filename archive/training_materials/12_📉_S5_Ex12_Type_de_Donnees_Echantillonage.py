import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(page_title="S5 | Ex. 12 : Sources & Échantillonnage", page_icon="🎲", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_5.pdf"

st.title("🎲 S5 | Ex. 12 : Sources de Données & Échantillonnage")

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Comprendre d'où viennent les données et comment construire un échantillon fiable.

    ### 🧠 Le sens de l'exercice
    Les données sociales proviennent de trois grandes sources : Administratives, Enquêtes, et Traces. 
    Même avec une source fiable, si l'on ne capture pas l'information sur toute la population (exhaustivité), il faut créer un échantillon. 
    L'erreur historique du *Literary Digest* en 1936 nous rappelle qu'un échantillon non représentatif mène à des conclusions erronées, indépendamment de sa taille.
    """)

if st.button("🔄 Réinitialiser la session"):
    # Clear cache variables
    for k in ['quiz_submitted']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_sources, tab_echantillon = st.tabs(["🕵️ 1. Sources (Concepts)", "📊 2. Échantillonnage (Pratique)"])

# --- TAB 1 : SOURCES ---
with tab_sources:
    st.subheader("Identifier les 3 grands types de sources")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown(f'''
        * **Administratives :** Fiables, exhaustives, peu flexibles.
        * **Enquêtes :** Sondages ou interviews, riches, non-exhaustives.
        * **Traces :** Captées sans intention première, soulèvent des préoccupations liées à l'éthique.
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        ''', unsafe_allow_html=True)

    st.info("Associez chaque exemple pratique au bon type de source de données.")
    
    with st.form("quiz_sources"):
        q1 = st.radio("1. Les déclarations de revenus centralisées par le Ministère de l'Économie :", 
                      ["Données d'enquêtes", "Données administratives", "Données issues de traces"], index=None)
        q2 = st.radio("2. Le nombre de 'J'aime' et l'historique de navigation sur un réseau social :", 
                      ["Données d'enquêtes", "Données administratives", "Données issues de traces"], index=None)
        q3 = st.radio("3. Un questionnaire rempli par 1000 étudiants sur leurs conditions de vie :", 
                      ["Données d'enquêtes", "Données administratives", "Données issues de traces"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "Données administratives":
                st.success("Q1 : Correct ! Ces données sont produites par les administrations et sont généralement exhaustives.")
            else:
                st.error("Q1 : Faux. C'est une donnée administrative.")
                errors += 1
                
            if q2 == "Données issues de traces":
                st.success("Q2 : Correct ! Ces volumes importants sont générés par l'usage quotidien sans but scientifique initial.")
            else:
                st.error("Q2 : Faux. C'est une trace numérique.")
                errors += 1
                
            if q3 == "Données d'enquêtes":
                st.success("Q3 : Correct ! La donnée est restreinte à un échantillon sondé.")
            else:
                st.error("Q3 : Faux. C'est une enquête.")
                errors += 1
                
            if errors == 0:
                st.balloons()

# --- TAB 2 : ECHANTILLONNAGE ---
with tab_echantillon:
    st.subheader("Construire un échantillon représentatif")
    
    st.info("L'échantillonnage est crucial pour garantir que les conclusions tirées d'un sous-ensemble de données soient valides pour l'ensemble de la population.")
    
    with st.form("quiz_echantillon"):
        q1 = st.radio("1. Quel est le risque principal d'un échantillon non représentatif ?", 
                      ["Biais de sélection", "Erreur de mesure", "Variance élevée"], index=None)
        q2 = st.radio("2. Quelle technique d'échantillonnage garantit que chaque individu a une chance égale d'être sélectionné ?", 
                      ["Échantillonnage aléatoire simple", "Échantillonnage stratifié", "Échantillonnage par grappes"], index=None)
        q3 = st.radio("3. Quel est l'avantage principal de l'échantillonnage stratifié ?", 
                      ["Réduction du biais de sélection", "Meilleure précision des estimations pour les sous-groupes", "Simplicité de mise en œuvre"], index=None)
        
        submitted = st.form_submit_button("✅ Vérifier mes réponses")
        
        if submitted:
            errors = 0
            if q1 == "Biais de sélection":
                st.success("Q1 : Correct ! Un échantillon non représentatif peut introduire un biais de sélection, faussant les résultats.")
            else:
                st.error("Q1 : Faux. Le risque principal est le biais de sélection.")
                errors += 1
                
            if q2 == "Échantillonnage aléatoire simple":
                st.success("Q2 : Correct ! Cette technique garantit une chance égale pour chaque individu.")
            else:
                st.error("Q2 : Faux. C'est l'échantillonnage aléatoire simple.")
                errors += 1
                
            if q3 == "Meilleure précision des estimations pour les sous-groupes":
                st.success("Q3 : Correct ! L'échantillonnage stratifié permet d'obtenir des estimations plus précises pour les sous-groupes spécifiques.")
            else:
                st.error("Q3 : Faux. L'avantage principal est la meilleure précision pour les sous-groupes.")
                errors += 1
                
            if errors == 0:
                st.balloons()