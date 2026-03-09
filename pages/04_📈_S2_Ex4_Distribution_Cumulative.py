import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="S2 | Ex4 : Cumul", page_icon="📈", layout="wide")

st.title("📈 S2 | Ex. 4 : Distribution Cumulative")

# NEW CONTEXT SECTION
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Calculer les **Effectifs Cumulés ($N_i$)** pour situer les valeurs les unes par rapport aux autres.

    ### 📖 Le sens de l'exercice
    Savoir qu'il y a 20 personnes dans la tranche "Moyen" est utile, mais cela ne nous dit pas combien de personnes sont "au-dessus" ou "en-dessous".
    
    Le cumul est l'outil qui permet de **classer la population**. C'est une étape technique indispensable pour déterminer :
    1.  **La Médiane :** La valeur qui coupe la population en deux moitiés égales (50%).
    2.  **Les Quartiles :** Les valeurs qui séparent les 25% les plus modestes ou les 25% les plus riches.
    """)

# HARMONIZATION: Standardized Tab Names
tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- SCÉNARIOS ---
SCENARIOS = {
    "notes": {
        "tag": "Notes", "titre": "Mentions (Éducation)", "unit": "/20",
        "min": 0, "max": 20, "mean": 11, "std": 3.5, "digits": 2, "step": 2,
        "bins": [0, 8, 10, 12, 14, 16, 20.1],
        "labels": ["< 8", "8 à <10", "10 à <12", "12 à <14", "14 à <16", "16 à 20"]
    },
    "revenus": {
        "tag": "Revenus", "titre": "Salaires (Économie)", "unit": "€",
        "min": 1200, "max": 4000, "mean": 2100, "std": 500, "digits": 0, "step": 500,
        "bins": [1200, 1500, 2000, 2500, 3000, 4001],
        "labels": ["1200 à <1500", "1500 à <2000", "2000 à <2500", "2500 à <3000", "3000 à 4000"]
    },
    "age": {
        "tag": "Age", "titre": "Démographie", "unit": "ans",
        "min": 18, "max": 80, "mean": 40, "std": 15, "digits": 0, "step": 10,
        "bins": [18, 25, 35, 45, 60, 80.1],
        "labels": ["18 à <25", "25 à <35", "35 à <45", "45 à <60", "60 à 80"]
    }
}

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=19"

# ==============================================================================
# ONGLET 1 : MANUEL
# ==============================================================================
with tab_man:
    st.subheader("1. Calcul manuel")
    
    with st.sidebar:
        st.header("📝 Aide : Cumul")
        st.markdown(f"""
        📄 <a href="{URL_SLIDES}" target="_blank">Slides (PDF)</a>
        
        **Effectif Cumulé ($N_i$) :**
        C'est la somme de l'effectif de la ligne actuelle et de tous les précédents.
        
        *Exemple :*
        * Ligne 1 : $n_1$
        * Ligne 2 : $n_1 + n_2$
        * Ligne 3 : $n_1 + n_2 + n_3$
        """, unsafe_allow_html=True)

    if st.button("🔄 Nouveau Cas Manuel", key="btn_cum_man"):
        keys = ['cm_data', 'cm_scen', 'cm_input', 'cm_check']
        for k in keys:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

    if 'cm_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = 50 # Échantillon moyen
        
        # Génération des données brutes puis distribution
        raw = np.random.normal(scen["mean"], scen["std"], n)
        raw = np.clip(raw, scen["min"], scen["max"])
        df_raw = pd.DataFrame(raw, columns=["Val"])
        
        # Création de la table de distribution (L'exercice commence ICI)
        dist = pd.cut(df_raw["Val"], bins=scen["bins"], labels=scen["labels"], right=False).value_counts().sort_index()
        df_dist = pd.DataFrame({"Intervalle": dist.index, "Effectif": dist.values})
        
        # Ajout colonne vide pour réponse
        df_dist["Effectif Cumulé (Ni)"] = 0
        
        st.session_state.cm_data = df_dist
        st.session_state.cm_scen = scen
        st.session_state.cm_check = False

    df_m = st.session_state.cm_data
    scen_m = st.session_state.cm_scen

    st.info(f"""
    Voici la distribution des **{scen_m['titre']}**. 
    Complétez la colonne **Effectif Cumulé**.
    """)

    # Affichage Editeur
    edited_df = st.data_editor(
        df_m,
        column_config={
            "Intervalle": st.column_config.TextColumn(disabled=True),
            "Effectif": st.column_config.NumberColumn(disabled=True),
            "Effectif Cumulé (Ni)": st.column_config.NumberColumn(min_value=0, step=1, required=True)
        },
        hide_index=True,
        key="edit_cum_man",
        height=300
    )

    if st.button("✅ Vérifier", key="chk_cum_man"):
        st.session_state.cm_check = True

    if st.session_state.cm_check:
        # Calcul de la vérité : somme cumulée des effectifs
        true_cumsum = df_m["Effectif"].cumsum()
        user_vals = edited_df["Effectif Cumulé (Ni)"]
        
        score = 0
        st.divider()
        cols = st.columns(2)
        
        for i, (u_val, t_val) in enumerate(zip(user_vals, true_cumsum)):
            lbl = df_m.iloc[i]["Intervalle"]
            with cols[i % 2]:
                if u_val == t_val:
                    st.success(f"✅ {lbl} : {u_val}")
                    score += 1
                else:
                    st.error(f"❌ {lbl} : Mis {u_val}, Attendu {t_val}")
        
        if score == len(df_m):
            st.balloons()
            st.success("👏 Parfait ! Vous avez compris la logique du cumul.")

# ==============================================================================
# ONGLET 2 : EXCEL
# ==============================================================================
with tab_xl:
    st.subheader("2. Fonction Excel")

    with st.sidebar:
        st.markdown("---")
        st.header("📊 Aide : Excel")
        st.info("""
        **La Formule Magique :**
        Pour calculer un cumul, on fixe la première cellule de la plage avec des dollars ($).
        
        1. Dans la cellule C2, écrivez :
           `=SOMME($B$2:B2)`
        2. Tirez la poignée vers le bas.
        
        *Explication :*
        * Ligne 2 : `=SOMME($B$2:B2)` (Somme de B2 à B2)
        * Ligne 3 : `=SOMME($B$2:B3)` (Somme de B2 à B3)
        * etc.
        """)

    if st.button("🔄 Nouveau Cas Excel", key="btn_cum_xl"):
        if 'cx_data' in st.session_state: del st.session_state['cx_data']
        st.rerun()

    if 'cx_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        n = 200
        
        raw = np.random.normal(scen["mean"], scen["std"], n)
        raw = np.clip(raw, scen["min"], scen["max"])
        
        # On génère DIRECTEMENT le tableau de distribution pour l'exercice
        dist = pd.cut(raw, bins=scen["bins"], labels=scen["labels"], right=False).value_counts().sort_index()
        df_export = pd.DataFrame({"Intervalle": dist.index, "Effectif": dist.values})
        
        st.session_state.cx_data = df_export
        st.session_state.cx_scen = scen

    df_x = st.session_state.cx_data
    scen_x = st.session_state.cx_scen

    st.info(f"""
    **Contexte :** Vous disposez déjà du tableau de distribution pour *{scen_x['titre']}*.
    **Consigne :** 1. Téléchargez le fichier.
    2. Dans la colonne **C**, calculez les **Effectifs Cumulés**.
    3. ⚠️ **Impératif :** Utilisez la formule avec ancrage : `=SOMME($B$2:B2)` (ou `SUM` en anglais).
    """)

    # Download
    ts = datetime.now().strftime("%H%M")
    fn = f"MQ_S2_Ex4_{scen_x['tag']}_{ts}.xlsx"
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as w:
        df_x.to_excel(w, index=False, sheet_name='Distribution')
    st.download_button(f"📥 Télécharger le tableau ({fn})", out.getvalue(), fn)

    # Upload
    up = st.file_uploader("Déposez le fichier avec la colonne cumulée", type=['xlsx'], key="up_cum_xl")
    
    if up:
        try:
            # On lit avec data_only=True pour récupérer le résultat de la formule SOMME
            wb = openpyxl.load_workbook(up, data_only=True)
            ws = wb.active
            
            # On récupère les valeurs de la colonne C (Colonne 3)
            # On suppose que l'étudiant a écrit en C2, C3...
            student_vals = []
            for row in ws.iter_rows(min_row=2, min_col=3, max_col=3, values_only=True):
                if row[0] is not None:
                    student_vals.append(row[0])
            
            # Calcul vérité
            true_vals = df_x["Effectif"].cumsum().tolist()
            
            st.divider()
            
            # Vérification
            if not student_vals:
                st.warning("⚠️ Je ne trouve rien dans la colonne C. Avez-vous bien rempli la colonne juste à droite des effectifs ?")
            else:
                score = 0
                cols = st.columns(2)
                
                # On compare la longueur
                limit = min(len(true_vals), len(student_vals))
                
                for i in range(limit):
                    u_val = student_vals[i]
                    t_val = true_vals[i]
                    lbl = df_x.iloc[i]["Intervalle"]
                    
                    with cols[i%2]:
                        # Tolérance float/int
                        try:
                            is_correct = abs(float(u_val) - float(t_val)) < 0.1
                        except:
                            is_correct = False
                            
                        if is_correct:
                            st.success(f"✅ {lbl} : {int(u_val)}")
                            score += 1
                        else:
                            st.error(f"❌ {lbl} : Trouvé {u_val}, Attendu {t_val}")

                if score == len(true_vals):
                    st.balloons()
                    st.success("👏 Excellent ! Votre cumul est correct.")
                elif score > 0:
                    st.warning("Certaines valeurs sont fausses. Vérifiez votre formule : avez-vous bien mis le $ uniquement sur le premier B2 ? (`$B$2:B2`)")

        except Exception as e:
            st.error(f"Erreur de lecture : {e}")