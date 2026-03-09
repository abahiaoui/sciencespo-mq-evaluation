import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Séance 2 : Calcul Manuel", page_icon="📝")

# --- CONFIGURATION ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

st.title("📝 Séance 2 : Construction de distribution (Manuel)")
st.markdown("""
**Objectif :** Comprendre la mécanique de la distribution en comptant "à la main" un petit échantillon.
""")

# --- 1. SCÉNARIOS (Mêmes thèmes, mais on garde la cohérence) ---
SCENARIOS = {
    "education": {
        "titre": "Niveau d'Étude",
        "col_id": "ID",
        "col_var": "Diplome",
        "categories": ["Sans Bac", "Bac", "Licence", "Master", "Doctorat"],
        "weights": [0.1, 0.3, 0.3, 0.2, 0.1]
    },
    "satisfaction": {
        "titre": "Satisfaction Client",
        "col_id": "Client",
        "col_var": "Avis",
        "categories": ["Très Insatisfait", "Insatisfait", "Neutre", "Satisfait", "Très Satisfait"],
        "weights": [0.1, 0.2, 0.2, 0.4, 0.1]
    },
    "transport": {
        "titre": "Mode de Transport",
        "col_id": "Usager",
        "col_var": "Transport",
        "categories": ["Voiture", "Bus/Métro", "Vélo", "Marche", "Scooter"],
        "weights": [0.3, 0.4, 0.1, 0.15, 0.05]
    }
}

# --- 2. GESTION DE L'ÉTAT (Génération des données) ---
if 'manual_data' not in st.session_state:
    # On choisit un scénario
    scenario_key = random.choice(list(SCENARIOS.keys()))
    scenario = SCENARIOS[scenario_key]
    
    # Petit échantillon pour que ce soit faisable à l'oeil (N=15)
    n = 15
    variable_data = random.choices(scenario["categories"], weights=scenario["weights"], k=n)
    ids = random.sample(range(100, 999), n)
    
    # DataFrame Brut (Liste)
    df = pd.DataFrame({
        scenario["col_id"]: ids,
        scenario["col_var"]: variable_data
    })
    
    # On trie par ID pour mélanger les catégories (rend le comptage plus réaliste)
    df = df.sort_values(by=scenario["col_id"]).reset_index(drop=True)
    
    # Initialisation de la grille de réponse (Tableau vide à remplir)
    # On pré-remplit les catégories pour guider l'étudiant
    df_input = pd.DataFrame({
        "Catégorie": scenario["categories"],
        "Effectif (ni)": [0] * len(scenario["categories"]) # Colonne de zéros
    })
    
    st.session_state.manual_data = df
    st.session_state.manual_scenario = scenario
    st.session_state.manual_input = df_input
    st.session_state.manual_check = False

# Bouton Reset
if st.button("🔄 Nouvel Exercice"):
    del st.session_state['manual_data']
    st.session_state.manual_check = False
    st.rerun()

# Récupération des données actuelles
df = st.session_state.manual_data
scenario = st.session_state.manual_scenario
df_input_template = st.session_state.manual_input

# --- 3. INTERFACE DE TRAVAIL ---
st.subheader(f"Exercice : {scenario['titre']}")
st.info(f"Voici une liste de **{len(df)} individus**. Comptez les effectifs pour chaque catégorie et remplissez le tableau de droite.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 1. Données Brutes")
    # Affichage de la liste brute
    st.dataframe(df, height=600, hide_index=True)

with col2:
    st.markdown("### 2. Votre Tableau de Distribution")
    st.write("Double-cliquez sur les cases de la colonne **Effectif** pour entrer vos valeurs.")
    
    # TABLEAU ÉDITABLE (Data Editor)
    # key='user_grid' permet de récupérer les modifs
    edited_df = st.data_editor(
        df_input_template,
        column_config={
            "Catégorie": st.column_config.TextColumn(disabled=True), # On empêche de modifier les noms
            "Effectif (ni)": st.column_config.NumberColumn(
                "Effectif (ni)",
                min_value=0,
                max_value=len(df),
                step=1,
                required=True
            )
        },
        hide_index=True,
        key="editor_manual"
    )

    # --- 4. CORRECTION ---
    if st.button("✅ Vérifier mes calculs"):
        st.session_state.manual_check = True

    if st.session_state.manual_check:
        st.divider()
        st.markdown("### 🔍 Résultats")
        
        # 1. Calcul de la vraie solution
        # On compte les valeurs réelles dans la liste brute
        true_counts = df[scenario["col_var"]].value_counts()
        
        # 2. Comparaison ligne par ligne
        score = 0
        total_items = len(edited_df)
        
        for index, row in edited_df.iterrows():
            cat = row["Catégorie"]
            user_val = row["Effectif (ni)"]
            
            # On récupère la vraie valeur (0 si la catégorie n'est pas dans la liste)
            true_val = true_counts.get(cat, 0)
            
            if user_val == true_val:
                st.success(f"✅ **{cat}** : {user_val} (Correct)")
                score += 1
            else:
                st.error(f"❌ **{cat}** : Vous avez mis **{user_val}**, mais il y en a **{true_val}**.")
        
        # Vérification du total
        user_total = edited_df["Effectif (ni)"].sum()
        true_total = len(df)
        
        if user_total == true_total:
            st.info(f"Votre Total : **{user_total}** (Bon compte global)")
        else:
            st.warning(f"⚠️ Votre somme totale est **{user_total}**, alors qu'il y a **{true_total}** individus. Vous avez oublié ou compté en double quelqu'un.")

        if score == total_items:
            st.balloons()
            st.markdown("### 👏 Bravo ! Distribution parfaite.")

# --- 5. AIDE ---
with st.sidebar:
    st.header("Aide Mémoire")
    st.markdown(f"""
    **Méthode de comptage :**
    Pour éviter les erreurs, parcourez la liste de gauche et faites des bâtons sur une feuille de papier brouillon pour chaque catégorie.
    
    **Effectif ($n_i$) :**
    C'est le nombre d'individus appartenant à une catégorie donnée.
    
    📄 <a href="{URL_SLIDES}" target="_blank">Voir le cours (PDF)</a>
    """, unsafe_allow_html=True)