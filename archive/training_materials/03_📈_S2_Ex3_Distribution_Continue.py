import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="S2 | Ex3 : Groupement", page_icon="📈", layout="wide")

st.title("📈 S2 | Ex. 3 : Groupement (Variable Continue)")

# NEW CONTEXT SECTION
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Transformer une variable quantitative continue (Salaire, Note, Âge) en classes d'intervalles (Discrétisation).

    ### 📖 Le sens de l'exercice
    Contrairement aux catégories, les variables continues ont une infinité de valeurs (personne n'a exactement le même salaire au centime près). Un simple comptage rendrait le tableau illisible.
    
    Il faut donc **créer des "tiroirs" (intervalles)**. 
    * *Exemple :* On ne compte pas les gens qui gagnent 1500,02€, mais ceux qui sont dans **$[1500 ; 2000[$**.
    * C'est un compromis : on perd en précision (valeur exacte) pour gagner en **synthèse** (vision globale).
    """)

# HARMONIZATION: Standardized Tab Names
tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])


URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

SCENARIOS = {
    "notes": {
        "tag": "Notes", "titre": "Mentions (Éducation)", "unit": "/20",
        "min": 10, "max": 20, "mean": 14.5, "std": 2.5, "digits": 2, "step": 2,
        "bins": [10, 12, 14, 16, 18, 20.1],
        "labels": ["10 à <12", "12 à <14", "14 à <16", "16 à <18", "18 à 20"]
    },
    "revenus": {
        "tag": "Revenus", "titre": "Salaires (Économie)", "unit": "€",
        "min": 1500, "max": 4000, "mean": 2600, "std": 600, "digits": 0, "step": 500,
        "bins": [1500, 2000, 2500, 3000, 3500, 4001],
        "labels": ["1500 à <2000", "2000 à <2500", "2500 à <3000", "3000 à <3500", "3500 à 4000"]
    },
    "age": {
        "tag": "Age", "titre": "Pyramide des Âges", "unit": "ans",
        "min": 20, "max": 70, "mean": 45, "std": 15, "digits": 0, "step": 10,
        "bins": [20, 30, 40, 50, 60, 70.1],
        "labels": ["20 à <30", "30 à <40", "40 à <50", "50 à <60", "60 à 70"]
    }
}


# ==============================================================================
# ONGLET 1 : MANUEL
# ==============================================================================
with tab_man:
    st.subheader("1. Calcul manuel")
    
    with st.sidebar:
        st.markdown("---")
        st.header("📝 Aide : Groupement")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **Intervalle [a, b[ :**
        * **a** inclus (compté).
        * **b** exclu (va dans la suite).
        * *Ex: 12 est dans [12, 14[, pas [10, 12[*
        """, unsafe_allow_html=True)

    if st.button("🔄 Nouveau Cas Manuel", key="btn_grp_man"):
        keys = ['gm_data', 'gm_scen', 'gm_input', 'gm_check']
        for k in keys:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

    if 'gm_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = 20
        # Données triées pour le manuel
        clean = np.round(np.random.uniform(scen["min"], scen["max"], n), scen["digits"])
        clean.sort()
        st.session_state.gm_data = pd.DataFrame(clean, columns=["Valeur"])
        st.session_state.gm_scen = scen
        st.session_state.gm_input = pd.DataFrame({"Intervalle": scen["labels"], "Effectif": [0]*len(scen["labels"])})
        st.session_state.gm_check = False

    df_m = st.session_state.gm_data
    scen_m = st.session_state.gm_scen

    st.info(f"Voici **20 valeurs triées**. Classez-les par pas de **{scen_m['step']} {scen_m['unit']}**.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(df_m, height=600, hide_index=True)
    with col2:
        edited_df = st.data_editor(
            st.session_state.gm_input,
            column_config={
                "Intervalle": st.column_config.TextColumn(disabled=True),
                "Effectif": st.column_config.NumberColumn(min_value=0, max_value=20, step=1)
            },
            hide_index=True,
            key="edit_grp_man"
        )
        if st.button("✅ Vérifier", key="chk_grp_man"):
            st.session_state.gm_check = True
        
        if st.session_state.gm_check:
            sol = pd.cut(df_m["Valeur"], bins=scen_m["bins"], labels=scen_m["labels"], right=False)
            true_counts = sol.value_counts().sort_index()
            score = 0
            st.divider()
            for idx, row in edited_df.iterrows():
                lbl = row["Intervalle"]
                val = row["Effectif"]
                true_val = true_counts.get(lbl, 0)
                if val == true_val:
                    st.success(f"✅ {lbl} : {val}")
                    score += 1
                else:
                    st.error(f"❌ {lbl} : Mis {val}, Attendu {true_val}")
            if score == len(scen_m["labels"]): st.balloons()

# ==============================================================================
# ONGLET 2 : EXCEL
# ==============================================================================
with tab_xl:
    st.subheader("2. Fonction Excel")
    
    with st.sidebar:
        st.header("📊 Aide : Excel")
        step_help = st.session_state.gx_scen['step'] if 'gx_scen' in st.session_state else "X"
        min_help = st.session_state.gx_scen['min'] if 'gx_scen' in st.session_state else "Min"
        max_help = st.session_state.gx_scen['max'] if 'gx_scen' in st.session_state else "Max"
        
        st.markdown(f"""
        **Procédure :**
        1. Faire le TCD.
        2. Clic Droit sur une valeur (gauche) > **Grouper**.
        3. Config :
            * Début: {min_help}
            * Fin: {max_help}
            * Par: {step_help}
        """)

    if st.button("🔄 Nouveau Cas Excel", key="btn_grp_xl"):
        if 'gx_data' in st.session_state: del st.session_state['gx_data']
        st.rerun()

    if 'gx_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = 300
        raw = np.random.normal(scen["mean"], scen["std"], n)
        clean = np.round(np.clip(raw, scen["min"], scen["max"]), scen["digits"])
        ids = random.sample(range(10000, 99999), n)
        st.session_state.gx_data = pd.DataFrame({"ID": ids, "Variable": clean})
        st.session_state.gx_scen = scen

    df_e = st.session_state.gx_data
    scen_e = st.session_state.gx_scen

    st.info(f"Fichier : **{len(df_e)} lignes**. Variable `{scen_e['titre']}`. Groupez par pas de **{scen_e['step']}**.")

    ts = datetime.now().strftime("%H%M")
    fn = f"MQ_S2_Ex3_{scen_e['tag']}_{ts}.xlsx"
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as w:
        df_e.to_excel(w, index=False)
    st.download_button(f"📥 Télécharger {fn}", out.getvalue(), fn)

    up = st.file_uploader("Déposez le TCD groupé", type=['xlsx'], key="up_grp_xl")
    if up:
        try:
            wb = openpyxl.load_workbook(up, data_only=True)
            nums = set()
            for s in wb.worksheets:
                for r in s.iter_rows(values_only=True):
                    for c in r:
                        if isinstance(c, (int, float)): nums.add(int(c))
            
            sol = pd.cut(df_e["Variable"], bins=scen_e["bins"], labels=scen_e["labels"], right=False)
            corr = sol.value_counts().sort_index()
            
            cols = st.columns(2)
            ok = True
            st.divider()
            for i, (lbl, cnt) in enumerate(corr.items()):
                with cols[i%2]:
                    if cnt in nums:
                        st.success(f"✅ {lbl} : {cnt}")
                    else:
                        st.error(f"❌ {lbl} : {cnt} manquant")
                        ok = False
            if ok: st.balloons()
        except Exception as e:
            st.error(f"Erreur : {e}")