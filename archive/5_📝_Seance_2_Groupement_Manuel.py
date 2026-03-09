import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Séance 2 : Groupement Manuel", page_icon="📝")

# --- CONFIGURATION ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

st.title("📝 Séance 2 : Groupement Manuel")
st.markdown("""
**Objectif :** Comprendre comment on passe d'une liste de valeurs continues à un tableau de fréquences par intervalles.
""")

# --- 1. DÉFINITION DES SCÉNARIOS ---
SCENARIOS = {
    "notes": {
        "titre": "Les Mentions (Éducation)",
        "unit": "/20",
        "min": 10, "max": 20, "digits": 2,
        "bins": [10, 12, 14, 16, 18, 20.1],
        "labels": ["10 à <12", "12 à <14", "14 à <16", "16 à <18", "18 à 20"]
    },
    "revenus": {
        "titre": "Revenus Mensuels (Économie)",
        "unit": "€",
        "min": 1500, "max": 4000, "digits": 0,
        "bins": [1500, 2000, 2500, 3000, 3500, 4001],
        "labels": ["1500 à <2000", "2000 à <2500", "2500 à <3000", "3000 à <3500", "3500 à 4000"]
    },
    "age": {
        "titre": "Tranches d'Âge (Démographie)",
        "unit": "ans",
        "min": 20, "max": 70, "digits": 0,
        "bins": [20, 30, 40, 50, 60, 70.1],
        "labels": ["20 à <30", "30 à <40", "40 à <50", "50 à <60", "60 à 70"]
    }
}

# --- 2. GESTION DE L'ÉTAT ---
if 'man_group_data' not in st.session_state:
    # Choix du scénario
    scen_key = random.choice(list(SCENARIOS.keys()))
    scenario = SCENARIOS[scen_key]
    
    # Génération de 20 valeurs seulement
    n = 20
    raw_data = np.random.uniform(scenario["min"], scenario["max"], n)
    clean_data = np.round(raw_data, scenario["digits"])
    
    # Pour l'exercice manuel, on TRIE les données, c'est crucial pour aider l'étudiant
    clean_data.sort()
    
    df = pd.DataFrame(clean_data, columns=["Valeur"])
    
    # Création du template de réponse vide
    df_input = pd.DataFrame({
        "Intervalle": scenario["labels"],
        "Effectif (ni)": [0] * len(scenario["labels"])
    })
    
    st.session_state.man_group_data = df
    st.session_state.man_group_scen = scenario
    st.session_state.man_group_input = df_input
    st.session_state.man_check = False

# Bouton Reset
if st.button("🔄 Nouvel Exercice"):
    keys = ['man_group_data', 'man_group_scen', 'man_group_input', 'man_check']
    for k in keys:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

# Récupération
df = st.session_state.man_group_data
scen = st.session_state.man_group_scen
df_input_template = st.session_state.man_group_input

# --- 3. INTERFACE ---
st.subheader(f"Exercice : {scen['titre']}")
st.info(f"""
Voici une série de **20 valeurs** triées par ordre croissant.
Regroupez-les dans le tableau de droite en comptant combien de valeurs tombent dans chaque intervalle.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### Données ({scen['unit']})")
    # On affiche les données en mode "Tableau propre"
    st.dataframe(df, height=600, hide_index=True)

with col2:
    st.markdown("### Votre Distribution")
    
    # TABLEAU ÉDITABLE
    edited_df = st.data_editor(
        df_input_template,
        column_config={
            "Intervalle": st.column_config.TextColumn(disabled=True),
            "Effectif (ni)": st.column_config.NumberColumn(
                min_value=0, max_value=20, step=1, required=True
            )
        },
        hide_index=True,
        key="editor_group_manual"
    )
    
    # --- 4. CORRECTION ---
    if st.button("✅ Vérifier"):
        st.session_state.man_check = True

    if st.session_state.man_check:
        st.divider()
        
        # Calcul de la solution
        # pd.cut fait le travail de groupement automatiquement
        solution = pd.cut(df['Valeur'], bins=scen["bins"], labels=scen["labels"], right=False)
        true_counts = solution.value_counts().sort_index()
        
        score = 0
        
        # Vérification ligne par ligne
        for index, row in edited_df.iterrows():
            label = row["Intervalle"]
            user_val = row["Effectif (ni)"]
            true_val = true_counts.get(label, 0)
            
            if user_val == true_val:
                st.success(f"✅ **{label}** : {user_val} (Correct)")
                score += 1
            else:
                st.error(f"❌ **{label}** : Vous avez mis **{user_val}**, la réponse est **{true_val}**.")
        
        # Vérification Total
        user_total = edited_df["Effectif (ni)"].sum()
        if user_total == 20:
            st.info(f"Total : {user_total} / 20 (Compte juste)")
        else:
            st.warning(f"⚠️ Votre total est de **{user_total}**, il devrait être de **20**. Vous avez oublié ou compté en double des valeurs.")
            
        if score == len(scen["labels"]):
            st.balloons()
            st.markdown("### 👏 Bravo ! Groupement réussi.")

# --- 5. AIDE ---
with st.sidebar:
    st.header("Règle des intervalles")
    st.markdown(f"""
    **Intervalle [a, b[** :
    * On inclut la valeur **a** (si la donnée est égale à a, on la compte).
    * On exclut la valeur **b** (si la donnée est égale à b, elle va dans l'intervalle suivant).
    
    *Exemple :*
    Si l'intervalle est **10 à <12** :
    * 10 est dedans.
    * 11.9 est dedans.
    * 12 va dans la case suivante (12 à <14).
    
    📄 <a href="{URL_SLIDES}" target="_blank">Voir le cours</a>
    """, unsafe_allow_html=True)