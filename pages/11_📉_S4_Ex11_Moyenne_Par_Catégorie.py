import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime

st.set_page_config(page_title="S4 | Ex. 11 : Moyenne par Catégorie", page_icon="📊", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_4.pdf" 
st.title("📊 S4 | Ex. 11 : Moyenne par Catégorie")

SCENARIOS = {
    "salaires": {
        "titre": "Salaires par Département", 
        "var_cat": "Département", "var_num": "Salaire (K€)",
        "categories": ["IT", "RH", "Ventes"],
        "data": [
            {"cat": "IT", "val": 42}, {"cat": "IT", "val": 48}, {"cat": "IT", "val": 45},
            {"cat": "RH", "val": 35}, {"cat": "RH", "val": 39},
            {"cat": "Ventes", "val": 30}, {"cat": "Ventes", "val": 40}, {"cat": "Ventes", "val": 56}
        ]
    },
    "loyers": {
        "titre": "Loyers par Type d'Appartement", 
        "var_cat": "Type", "var_num": "Loyer (€)",
        "categories": ["Studio", "T2", "T3"],
        "data": [
            {"cat": "Studio", "val": 500}, {"cat": "Studio", "val": 550}, {"cat": "Studio", "val": 600},
            {"cat": "T2", "val": 800}, {"cat": "T2", "val": 850},
            {"cat": "T3", "val": 1100}, {"cat": "T3", "val": 1200}, {"cat": "T3", "val": 1150}
        ]
    },
    "notes": {
        "titre": "Notes selon la Méthode de Révision", 
        "var_cat": "Méthode", "var_num": "Note (/20)",
        "categories": ["Visuelle", "Auditive", "Pratique"],
        "data": [
            {"cat": "Visuelle", "val": 12}, {"cat": "Visuelle", "val": 14},
            {"cat": "Auditive", "val": 11}, {"cat": "Auditive", "val": 13}, {"cat": "Auditive", "val": 15},
            {"cat": "Pratique", "val": 16}, {"cat": "Pratique", "val": 18}, {"cat": "Pratique", "val": 17}
        ]
    }
}

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Apprendre à résumer une variable numérique en fonction d'une variable catégorielle (groupes). 
    ### 🧠 Le sens de l'exercice
    Calculer la moyenne globale d'un jeu de données est utile, mais souvent insuffisant. Pour comparer des populations, on calcule la **moyenne conditionnelle** (ou moyenne par groupe) :
    * **Identifier les différences :** Est-ce que le département IT gagne en moyenne plus que les RH ?
    * **Préparer l'analyse de variance :** C'est la première étape avant de vérifier si ces différences sont statistiquement significatives (concept que l'on verra plus tard).
    
    💡 **Comment faire ?**
    Il suffit d'isoler les données d'un seul groupe (par exemple, uniquement les "Studios"), de faire la somme de leurs valeurs, puis de diviser par le nombre d'observations *dans ce groupe spécifique*.
    """)

if st.button("🔄 Nouveau Scénario"):
    for k in ['moy_man_data', 'moy_xl_data', 'editor_key_moy']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel pas à pas")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.info("**Concept :** Isoler, Sommer, Diviser.")
        st.latex(r"\bar{x}_k = \frac{\sum_{i=1}^{n_k} x_{i,k}}{n_k}")
        st.markdown(f"""
        **Où :**
        * $k$ représente une catégorie spécifique.
        * $n_k$ est le nombre d'observations dans cette catégorie.
        * $x_{{i,k}}$ sont les valeurs appartenant à la catégorie $k$.

        **Algorithme :**
        1. **Regrouper :** Identifiez toutes les lignes appartenant à la même catégorie.
        2. **Sommer :** Additionnez les valeurs de ces lignes.
        3. **Compter :** Comptez combien il y a de lignes dans ce groupe.
        4. **Diviser :** Somme / Nombre de lignes.
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        """, unsafe_allow_html=True)
    
    # Initialize Data
    if 'moy_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        # Shuffle the data so it's not perfectly grouped initially
        data_dicts = scen["data"].copy()
        random.shuffle(data_dicts)
        
        st.session_state.moy_man_data = pd.DataFrame(data_dicts)
        st.session_state.moy_man_scen = scen
    
    if 'editor_key_moy' not in st.session_state:
        st.session_state.editor_key_moy = random.randint(0, 100000)

    df_m = st.session_state.moy_man_data
    scen = st.session_state.moy_man_scen
    categories = scen["categories"]

    st.info(f"""
    **Contexte :** Étudions la base de données brute des *{scen['titre']}*. 
    **Consigne :** Remplissez le tableau récapitulatif en calculant la somme, l'effectif (nombre de lignes) et la moyenne pour **chaque** catégorie.
    """)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Données Brutes")
        # Rename columns for display
        df_display = df_m.rename(columns={"cat": scen['var_cat'], "val": scen['var_num']})
        st.dataframe(df_display, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("#### Tableau Récapitulatif à compléter")
        
        # Prepare the DataFrame for the editor
        df_input = pd.DataFrame()
        df_input[scen['var_cat']] = categories
        df_input["Somme des valeurs"] = [None] * len(categories)
        df_input["Effectif (N)"] = [None] * len(categories)
        df_input["Moyenne du groupe"] = [None] * len(categories)
        
        # Display Data Editor
        edited_df = st.data_editor(
            df_input,
            column_config={
                scen['var_cat']: st.column_config.TextColumn(disabled=True),
                "Somme des valeurs": st.column_config.NumberColumn(required=True, step=1.0),
                "Effectif (N)": st.column_config.NumberColumn(required=True, step=1.0),
                "Moyenne du groupe": st.column_config.NumberColumn(required=True, step=0.1)
            },
            hide_index=True,
            key=f"editor_moy_{st.session_state.editor_key_moy}",
            use_container_width=True
        )
        
        if st.button("✅ Vérifier les calculs"):
            row_errors = []
            
            # Recalculate Truth
            true_stats = df_m.groupby('cat')['val'].agg(['sum', 'count', 'mean']).reset_index()
            
            # Check User Inputs
            try:
                for idx, row in edited_df.iterrows():
                    cat_name = row[scen['var_cat']]
                    user_sum = float(row["Somme des valeurs"]) if pd.notnull(row["Somme des valeurs"]) else 0
                    user_count = float(row["Effectif (N)"]) if pd.notnull(row["Effectif (N)"]) else 0
                    user_mean = float(row["Moyenne du groupe"]) if pd.notnull(row["Moyenne du groupe"]) else 0
                    
                    true_row = true_stats[true_stats['cat'] == cat_name].iloc[0]
                    t_sum, t_count, t_mean = true_row['sum'], true_row['count'], true_row['mean']
                    
                    if abs(user_sum - t_sum) > 0.01:
                        row_errors.append(f"Catégorie '{cat_name}' : Somme incorrecte.")
                    elif abs(user_count - t_count) > 0.01:
                        row_errors.append(f"Catégorie '{cat_name}' : Effectif incorrect.")
                    elif abs(user_mean - t_mean) > 0.1:
                        row_errors.append(f"Catégorie '{cat_name}' : Moyenne incorrecte (Attendu : {t_mean:.2f}).")
            except Exception as e:
                row_errors.append("Veuillez remplir toutes les cases du tableau avec des nombres.")

            # Display Results
            if not row_errors:
                st.success("👏 Bravo ! Les agrégations par groupe sont parfaitement calculées.")
                st.balloons()
            else:
                st.error("⚠️ Erreurs trouvées :")
                for err in row_errors:
                    st.warning(err)

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonctions et Outils Excel")     
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown("""
        **Deux méthodes dans Excel :**
        
        **Méthode 1 : La fonction MOYENNE.SI**
        `=MOYENNE.SI(Plage_Critères; "LeCritère"; Plage_Moyenne)`
        * *Plage_Critères* : La colonne contenant les catégories.
        * *"LeCritère"* : Le nom de la catégorie (ex: "IT").
        * *Plage_Moyenne* : La colonne contenant les nombres à moyenner.
        
        **Méthode 2 : Le Tableau Croisé Dynamique (TCD)**
        1. Sélectionnez vos données > *Insertion* > *Tableau Croisé Dynamique*.
        2. Glissez la catégorie dans **Lignes**.
        3. Glissez la variable numérique dans **Valeurs**.
        4. Cliquez sur la flèche dans Valeurs > *Paramètres des champs de valeurs* > Choisissez **Moyenne**.
        """)
    
    if 'moy_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        cats = scen["categories"]
        
        # Generate 100 random rows
        n_rows = 150
        cat_col = np.random.choice(cats, n_rows)
        val_col = []
        
        # Add varied distributions to make means distinct
        for c in cat_col:
            if c == cats[0]: val_col.append(np.random.normal(50, 10))
            elif c == cats[1]: val_col.append(np.random.normal(85, 15))
            else: val_col.append(np.random.normal(30, 8))
            
        st.session_state.moy_xl_data = pd.DataFrame({
            scen["var_cat"]: cat_col,
            scen["var_num"]: np.round(val_col, 1)
        })
        st.session_state.moy_xl_scen = scen
        st.session_state.moy_xl_target_cat = random.choice(cats)
    
    df_x = st.session_state.moy_xl_data
    scen_x = st.session_state.moy_xl_scen
    target_cat = st.session_state.moy_xl_target_cat
    
    st.info(f"""
    **Contexte :** Vous avez une base de données contenant 150 observations.
    **Consigne :** Téléchargez le fichier et calculez la moyenne de *{scen_x['var_num']}* spécifiquement pour la catégorie **"{target_cat}"**.
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S4_Ex10_MoyenneCategorie_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger Données ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    colA, _ = st.columns(2)
    with colA:
        u_moy_xl = st.number_input(f"Moyenne calculée pour la catégorie '{target_cat}' :", step=0.1)
        
    if st.button("Correction Excel"):
        # Calculate the true mean for the target category
        true_mean = df_x[df_x[scen_x['var_cat']] == target_cat][scen_x['var_num']].mean()
        
        if abs(u_moy_xl - true_mean) < 0.2:
            st.success("✅ Correct !")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {true_mean:.1f}")