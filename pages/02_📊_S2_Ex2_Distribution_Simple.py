import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="S2 | Ex2 : Distribution Simple", page_icon="📊", layout="wide")

st.title("📊 S2 | Ex. 2 : Distribution (Variable Catégorielle)")

# NEW CONTEXT SECTION
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Maîtriser le passage des données brutes (liste d'individus) au tableau de distribution (tableau d'effectifs).

    ### 📖 Le sens de l'exercice
    Face à une base de données de 10 000 lignes, le cerveau humain est aveugle. 
    L'analyste doit **réduire l'information** pour la rendre intelligible. Pour une variable qualitative (ex: Diplôme, Avis), cela consiste à compter les occurrences de chaque catégorie.
    
    * **Mode Manuel :** On apprend à "dépouiller" les données (faire des bâtons) pour comprendre la logique d'agrégation.
    * **Mode Excel :** On utilise le **Tableau Croisé Dynamique (TCD)**, l'outil roi en entreprise pour automatiser ce comptage instantanément.
    """)

# HARMONIZATION: Standardized Tab Names
tab_manual, tab_excel = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"


# --- SCÉNARIOS ---
SCENARIOS = {
    "education": {
        "tag": "Education", "titre": "Niveau d'Étude (Sociologie)", "col_id": "ID_Individu", "col_var": "Diplome",
        "categories": ["1. Sans Bac", "2. Bac", "3. Licence", "4. Master", "5. Doctorat"],
        "weights": [0.15, 0.30, 0.30, 0.20, 0.05]
    },
    "satisfaction": {
        "tag": "Satisfaction", "titre": "Enquête Satisfaction (Marketing)", "col_id": "Ref_Client", "col_var": "Avis_Service",
        "categories": ["1. Très Insatisfait", "2. Insatisfait", "3. Neutre", "4. Satisfait", "5. Très Satisfait"],
        "weights": [0.10, 0.15, 0.20, 0.40, 0.15]
    },
    "transport": {
        "tag": "Transport", "titre": "Mode de Transport (Urbanisme)", "col_id": "Matricule_Usager", "col_var": "Transport_Principal",
        "categories": ["1. Voiture", "2. Transports en commun", "3. Vélo", "4. Marche", "5. Deux-roues"],
        "weights": [0.35, 0.40, 0.10, 0.10, 0.05]
    },
    "politique": {
        "tag": "Politique", "titre": "Sondage Politique (Science Po)", "col_id": "Code_Electeur", "col_var": "Intention_Vote",
        "categories": ["1. Candidat A", "2. Candidat B", "3. Candidat C", "4. Abstention", "5. Blanc/Nul"],
        "weights": [0.25, 0.22, 0.18, 0.25, 0.10]
    }
}


# ==============================================================================
# ONGLET 1 : MODE MANUEL
# ==============================================================================
with tab_manual:
    st.subheader("1. Calcul manuel")
    
    with st.sidebar:
        st.markdown("---")
        st.header("📝 Aide : Mode Manuel")
        st.markdown("""
        **Méthode :**
        1. Prenez une feuille de brouillon.
        2. Parcourez la liste ligne par ligne.
        3. Faites un trait pour chaque catégorie rencontrée.
        4. Comptez le total.
        """)

    if st.button("🔄 Nouveau Cas Manuel", key="btn_manual"):
        keys = ['manual_data', 'manual_scen', 'manual_input', 'manual_check']
        for k in keys:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

    if 'manual_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = 25 # Petit échantillon
        data = random.choices(scen["categories"], weights=scen["weights"], k=n)
        ids = random.sample(range(100, 999), n)
        df = pd.DataFrame({scen["col_id"]: ids, scen["col_var"]: data}).sort_values(by=scen["col_id"])
        
        st.session_state.manual_data = df
        st.session_state.manual_scen = scen
        st.session_state.manual_input = pd.DataFrame({
            "Catégorie": scen["categories"], 
            "Effectif (ni)": [0]*len(scen["categories"])
        })
        st.session_state.manual_check = False

    df_m = st.session_state.manual_data
    scen_m = st.session_state.manual_scen

    st.info(f"Fichier : **{len(df_m)} individus** ({scen_m['titre']}). Comptez les effectifs.")

    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.dataframe(df_m, height=500, hide_index=True)
    with col2:
        edited_df = st.data_editor(
            st.session_state.manual_input,
            column_config={
                "Catégorie": st.column_config.TextColumn(disabled=True),
                "Effectif (ni)": st.column_config.NumberColumn(min_value=0, max_value=25, step=1)
            },
            hide_index=True,
            key="edit_man"
        )
        if st.button("✅ Vérifier", key="chk_man"):
            st.session_state.manual_check = True

        if st.session_state.manual_check:
            true_counts = df_m[scen_m["col_var"]].value_counts()
            score = 0
            st.divider()
            for idx, row in edited_df.iterrows():
                cat = row["Catégorie"]
                val = row["Effectif (ni)"]
                true_val = true_counts.get(cat, 0)
                if val == true_val:
                    st.success(f"✅ {cat} : {val}")
                    score += 1
                else:
                    st.error(f"❌ {cat} : Mis {val}, Attendu {true_val}")
            if score == len(scen_m["categories"]): st.balloons()

# ==============================================================================
# ONGLET 2 : MODE EXCEL
# ==============================================================================
with tab_excel:
    st.subheader("2. Fonction Excel")
    
    with st.sidebar:
        st.header("📊 Aide : Mode Excel")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **TCD Rapide :**
        1. **Insertion** > **Tableau Croisé Dynamique**.
        2. Variable -> **LIGNES**.
        3. Variable -> **VALEURS** (Vérifiez que c'est "Nombre" et pas "Somme").
        """, unsafe_allow_html=True)

    if st.button("🔄 Nouveau Cas Excel", key="btn_excel"):
        if 'excel_data' in st.session_state: del st.session_state['excel_data']
        st.rerun()

    if 'excel_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = random.randint(180, 250)
        data = random.choices(scen["categories"], weights=scen["weights"], k=n)
        ids = random.sample(range(10000, 99999), n)
        st.session_state.excel_data = pd.DataFrame({scen["col_id"]: ids, scen["col_var"]: data})
        st.session_state.excel_scen = scen

    df_e = st.session_state.excel_data
    scen_e = st.session_state.excel_scen

    st.info(f"Fichier : **{len(df_e)} lignes**. Variable : **{scen_e['col_var']}**.")

    ts = datetime.now().strftime("%H%M")
    fn = f"MQ_S2_Ex2_{scen_e['tag']}_{ts}.xlsx"
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_e.to_excel(writer, index=False)
    
    st.download_button(f"📥 Télécharger {fn}", out.getvalue(), fn)

    up = st.file_uploader("Déposez votre TCD", type=['xlsx'], key="up_ex2")
    if up:
        try:
            wb = openpyxl.load_workbook(up, data_only=True)
            found_all = set()
            for s in wb.worksheets:
                for r in s.iter_rows(values_only=True):
                    for c in r:
                        if isinstance(c, (int, float)): found_all.add(int(c))
                        if c: found_all.add(str(c).lower().strip())
            
            corr = df_e[scen_e["col_var"]].value_counts()
            
            cols = st.columns(2)
            ok = True
            st.divider()
            for i, (cat, cnt) in enumerate(corr.items()):
                with cols[i%2]:
                    # Check Label (approx)
                    cat_clean = cat.lower()
                    cat_short = cat.split(". ")[-1].lower() if ". " in cat else cat.lower()
                    if not any((cat_clean in t or cat_short in t) for t in found_all if isinstance(t, str)):
                        st.warning(f"Label '{cat}' introuvable")
                    
                    # Check Count
                    if cnt in found_all:
                        st.success(f"✅ {cat} : {cnt}")
                    else:
                        st.error(f"❌ {cat} : {cnt} manquant")
                        ok = False
            if ok: st.balloons()
        except Exception as e:
            st.error(f"Erreur : {e}")