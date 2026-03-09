import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime

st.set_page_config(page_title="S4 | Ex. 9 : Tableaux Croisés", page_icon="📊", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_4.pdf" 
st.title("📊 S4 | Ex. 9 : Distribution à deux variables (Tableau Croisé)")

SCENARIOS = {
    "sondage": {
        "titre": "Intentions de vote par âge",
        "v1_name": "Catégorie d'Âge", "v1_cats": ["Jeune", "Senior"],
        "v2_name": "Intention de Vote", "v2_cats": ["Candidat A", "Candidat B"]
    },
    "entreprise": {
        "titre": "Satisfaction par département",
        "v1_name": "Département", "v1_cats": ["Tech", "Ventes"],
        "v2_name": "Satisfaction", "v2_cats": ["Satisfait", "Insatisfait"]
    },
    "sante": {
        "titre": "Efficacité d'un traitement",
        "v1_name": "Groupe", "v1_cats": ["Médicament", "Placebo"],
        "v2_name": "Guérison", "v2_cats": ["Oui", "Non"]
    }
}

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Comprendre et construire un tableau de contingence (tableau croisé) pour observer la relation entre deux variables qualitatives.

    ### 🧠 Le sens de l'exercice
    Au lieu de regarder une seule variable à la fois (ex: la moyenne des âges), on croise deux dimensions pour révéler des structures cachées :
    * Les *Jeunes* votent-ils différemment des *Seniors* ? 
    * Le *Médicament* guérit-il plus souvent que le *Placebo* ?
    
    💡 **Pourquoi c'est important pour la suite ? (Test du Khi-Deux)**
    Le tableau croisé est la base de l'analyse de dépendance entre variables catégorielles. En comparant les effectifs réels observés dans le tableau avec ce qu'on obtiendrait par pur hasard, on peut prouver statistiquement (avec le test du Khi-Deux, ou $\chi^2$) si deux variables sont liées.
    """)

if st.button("🔄 Nouveau Scénario"):
    for k in ['cross_man_data', 'cross_xl_data', 'cross_editor_key']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Comptage manuel pas à pas")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.info("**Concept :** Compter les co-occurrences.")
        st.markdown(f"""
        **Algorithme :**
        1. **Lecture :** Prenez chaque ligne (chaque individu) de la base de données.
        2. **Classification :** Identifiez sa catégorie pour la Variable 1 (Ligne) et la Variable 2 (Colonne).
        3. **Comptage :** Ajoutez +1 dans la case correspondante du tableau de contingence.
        4. **Marges :** Additionnez les lignes et les colonnes pour vérifier que le **Total Général** correspond bien au nombre total d'individus ($N$).
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        """, unsafe_allow_html=True)
    
    # Initialize Data (Small dataset for manual counting)
    if 'cross_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        # Create ~12 random rows
        N = random.randint(12, 15)
        v1_data = random.choices(scen["v1_cats"], k=N)
        v2_data = random.choices(scen["v2_cats"], k=N)
        
        st.session_state.cross_man_data = pd.DataFrame({
            scen["v1_name"]: v1_data,
            scen["v2_name"]: v2_data
        })
        st.session_state.cross_man_scen = scen
    
    if 'cross_editor_key' not in st.session_state:
        st.session_state.cross_editor_key = random.randint(0, 100000)

    df_m = st.session_state.cross_man_data
    scen = st.session_state.cross_man_scen
    n = len(df_m)

    st.info(f"""
    **Contexte :** Pour étudier *{scen['titre']}*, nous allons construire manuellement un tableau croisé.
    **Consigne :** 1. Observez la base de données brute ci-dessous ({n} observations).
    2. Comptez les effectifs croisés et remplissez le tableau récapitulatif (remplacez les zéros).
    3. N'oubliez pas de calculer les totaux marginaux (lignes et colonnes).
    """)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("#### Base de données brute")
        st.dataframe(df_m, use_container_width=True, hide_index=False)

    with col2:
        st.markdown("#### Tableau Croisé (à remplir)")
        
        v1_col = scen["v1_name"]
        v2_col = scen["v2_name"]
        v1_cats = scen["v1_cats"]
        v2_cats = scen["v2_cats"]
        
        # Setup the empty crosstab for the user
        index_col = f"{v1_col} \\ {v2_col}"
        empty_grid = {index_col: v1_cats + ["Total"]}
        for cat in v2_cats:
            empty_grid[cat] = [0] * (len(v1_cats) + 1)
        empty_grid["Total"] = [0] * (len(v1_cats) + 1)
        
        df_input = pd.DataFrame(empty_grid)
        
        # Configure columns for Data Editor
        col_config = {
            index_col: st.column_config.TextColumn(disabled=True)
        }
        for col in v2_cats + ["Total"]:
            col_config[col] = st.column_config.NumberColumn(
                col, required=True, step=1
            )
            
        edited_df = st.data_editor(
            df_input,
            column_config=col_config,
            hide_index=True,
            key=f"editor_cross_{st.session_state.cross_editor_key}"
        )
        
        if st.button("✅ Vérifier le tableau"):
            # Calculate True Crosstab
            true_ct = pd.crosstab(
                df_m[v1_col], 
                df_m[v2_col], 
                margins=True, 
                margins_name="Total"
            )
            
            # Reindex to ensure order matches the predefined categories even if a category has 0 count
            true_ct = true_ct.reindex(index=v1_cats + ["Total"], columns=v2_cats + ["Total"], fill_value=0)
            
            errors = []
            
            # Check user values against true values
            for idx_num, idx_name in enumerate(v1_cats + ["Total"]):
                for col_name in v2_cats + ["Total"]:
                    user_val = edited_df.loc[idx_num, col_name]
                    true_val = true_ct.loc[idx_name, col_name]
                    
                    if user_val != true_val:
                        if idx_name == "Total" or col_name == "Total":
                            errors.append(f"Erreur de marge : La case ({idx_name}, {col_name}) devrait être {true_val} (vous avez {user_val}).")
                        else:
                            errors.append(f"Erreur de comptage : La case croisant '{idx_name}' et '{col_name}' devrait être {true_val} (vous avez {user_val}).")
            
            if not errors:
                st.success(f"👏 Parfait ! Votre tableau croisé est correct (Total $N = {n}$).")
                st.balloons()
            else:
                st.error("⚠️ Des erreurs ont été détectées :")
                for err in errors[:5]: # Limit to 5 errors to avoid flooding
                    st.warning(err)
                if len(errors) > 5:
                    st.warning("... et d'autres erreurs. Revérifiez vos comptages et vos totaux.")

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonction Excel (Tableau Croisé Dynamique)")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown("""
        **Sur Excel :**
        1. Cliquez n'importe où dans vos données.
        2. Allez dans **Insertion** > **Tableau Croisé Dynamique**.
        3. Glissez la *Variable 1* dans **Lignes**.
        4. Glissez la *Variable 2* dans **Colonnes**.
        5. Glissez l'une des deux variables dans **Valeurs**. Assurez-vous que l'opération est bien sur "Nombre" (Count) et non "Somme".
        """)
    
    if 'cross_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        # Create ~250-300 rows with some weighted probabilities to make it realistic
        N_xl = random.randint(250, 300)
        
        # Simple generation
        v1_data = random.choices(scen["v1_cats"], weights=[0.4, 0.6], k=N_xl)
        
        # Make v2 dependent on v1 for realism
        v2_data = []
        for v1 in v1_data:
            if v1 == scen["v1_cats"][0]:
                v2_data.append(random.choices(scen["v2_cats"], weights=[0.7, 0.3], k=1)[0])
            else:
                v2_data.append(random.choices(scen["v2_cats"], weights=[0.3, 0.7], k=1)[0])
                
        st.session_state.cross_xl_data = pd.DataFrame({
            "ID_Observation": range(1, N_xl + 1),
            scen["v1_name"]: v1_data,
            scen["v2_name"]: v2_data
        })
        st.session_state.cross_xl_scen = scen
    
    df_x = st.session_state.cross_xl_data
    scen_x = st.session_state.cross_xl_scen
    
    st.info(f"""
    **Contexte :** Vous avez une large base de données concernant *{scen_x['titre'].lower()}* ({len(df_x)} lignes).
    **Consigne :** 1. Téléchargez le fichier Excel.
    2. Insérez un Tableau Croisé Dynamique (TCD).
    3. Retrouvez les valeurs spécifiques demandées ci-dessous pour vérifier votre TCD.
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S3_Ex9_TCD_{scen_x['titre'].replace(' ', '_')}_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger Données ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    # Pick specific categories to ask the user
    cat_L = scen_x["v1_cats"][0]
    cat_C = scen_x["v2_cats"][1]
    
    colA, colB, colC = st.columns(3)
    with colA:
        ans_total = st.number_input("Total Général (N) :", step=1)
    with colB:
        ans_intersec = st.number_input(f"Intersection [{cat_L}] et [{cat_C}] :", step=1)
    with colC:
        ans_margin = st.number_input(f"Total de la ligne [{cat_L}] :", step=1)
        
    if st.button("Correction Excel"):
        true_total = len(df_x)
        true_intersec = len(df_x[(df_x[scen_x["v1_name"]] == cat_L) & (df_x[scen_x["v2_name"]] == cat_C)])
        true_margin = len(df_x[df_x[scen_x["v1_name"]] == cat_L])
        
        errors = False
        if ans_total != true_total:
            st.error(f"❌ Total Général incorrect. Attendu : {true_total}")
            errors = True
        if ans_intersec != true_intersec:
            st.error(f"❌ Intersection incorrecte. Attendu : {true_intersec}")
            errors = True
        if ans_margin != true_margin:
            st.error(f"❌ Total marginal incorrect. Attendu : {true_margin}")
            errors = True
            
        if not errors:
            if ans_total == 0: # User hasn't typed anything yet (0 is default)
                st.warning("Veuillez entrer vos résultats pour lancer la vérification.")
            else:
                st.success("✅ Tout est correct ! Vous maîtrisez les TCD.")
                st.balloons()