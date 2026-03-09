import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="Séance 2 : Groupement", page_icon="📈")

# --- CONFIGURATION ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

st.title("📈 Séance 2 : Groupement par intervalles")
st.markdown("""
**Objectif :** Transformer une variable quantitative continue en classes d'amplitudes égales via la fonction **Grouper** d'Excel.
""")

# --- 1. DÉFINITION DES SCÉNARIOS (Adaptés SHS) ---
SCENARIOS = {
    "notes": {
        "tag": "Notes",
        "titre": "Les Mentions (Sociologie de l'Éducation)",
        "col_id": "Matricule",
        "col_var": "Note_Finale",
        "unit": "/20",
        # Génération : 10 à 20
        "min": 10, "max": 20, "mean": 14.5, "std": 2.5, "digits": 2,
        # Groupement : Pas de 2
        "step": 2,
        "bins": [10, 12, 14, 16, 18, 20.1],
        "labels": ["10 - 12", "12 - 14", "14 - 16", "16 - 18", "18 - 20"]
    },
    "revenus": {
        "tag": "Revenus",
        "titre": "Inégalités de Revenus (Socio-Économie)",
        "col_id": "ID_Menage",
        "col_var": "Revenu_Mensuel",
        "unit": "€",
        # Génération : 1500 à 4500
        "min": 1500, "max": 4500, "mean": 2600, "std": 800, "digits": 0,
        # Groupement : Pas de 500 euros
        "step": 500,
        "bins": [1500, 2000, 2500, 3000, 3500, 4000, 4501],
        "labels": ["1500 - 2000", "2000 - 2500", "2500 - 3000", "3000 - 3500", "3500 - 4000", "4000 - 4500"]
    },
    "age": {
        "tag": "Age",
        "titre": "Pyramide des Âges (Démographie)",
        "col_id": "ID_Repondant",
        "col_var": "Age",
        "unit": "ans",
        # Génération : 20 à 80 ans
        "min": 20, "max": 80, "mean": 45, "std": 15, "digits": 0,
        # Groupement : Pas de 10 ans (Décennies)
        "step": 10,
        "bins": [20, 30, 40, 50, 60, 70, 80.1],
        "labels": ["20 - 30", "30 - 40", "40 - 50", "50 - 60", "60 - 70", "70 - 80"]
    }
}

# --- 2. BOUTON RESET ---
if st.button("🔄 Générer un nouvel exercice"):
    keys_to_del = ['group_data', 'group_scenario']
    for k in keys_to_del:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

# --- 3. GÉNÉRATION DES DONNÉES ---
if 'group_data' not in st.session_state:
    # Choix aléatoire
    scen_key = random.choice(list(SCENARIOS.keys()))
    scenario = SCENARIOS[scen_key]
    
    n = 300
    ids = random.sample(range(50000, 59999), n)
    
    # Génération Normale bornée
    raw_data = np.random.normal(loc=scenario["mean"], scale=scenario["std"], size=n)
    clean_data = np.clip(raw_data, scenario["min"], scenario["max"])
    clean_data = np.round(clean_data, scenario["digits"])
    
    df = pd.DataFrame({
        scenario["col_id"]: ids,
        scenario["col_var"]: clean_data
    })
    
    st.session_state.group_data = df
    st.session_state.group_scenario = scenario

# Récupération contextuelle
df_current = st.session_state.group_data
scen = st.session_state.group_scenario

# Calcul de la solution (Vérité Terrain)
solution = pd.cut(df_current[scen["col_var"]], bins=scen["bins"], labels=scen["labels"], right=False)
solution_counts = solution.value_counts().sort_index()

# --- 4. AFFICHAGE ET TÉLÉCHARGEMENT ---
st.subheader(f"1. L'Exercice : {scen['titre']}")

# --- AIDE DANS LA SIDEBAR ---
with st.sidebar:
    st.header(f"💡 Aide : Pas de {scen['step']}")
    st.markdown(f"""
    **Le problème :** La variable *{scen['col_var']}* est continue (ex: {df_current[scen['col_var']].iloc[0]} {scen['unit']}). Il faut créer des classes.
    
    **La méthode Excel :**
    1. Faites votre TCD ({scen['col_var']} en **Lignes**, {scen['col_id']} en **Valeurs**).
    2. Cliquez droit sur n'importe quel chiffre dans la colonne de gauche > **Grouper...**
    3. Configurez la fenêtre :
        * **Début :** {scen['min']}
        * **Fin :** {scen['max']}
        * **Par :** {scen['step']}
    4. Validez. Excel crée les tranches automatiquement.
    
    📄 <a href="{URL_SLIDES}" target="_blank">Voir le slide du cours</a>
    """, unsafe_allow_html=True)
    
st.info(f"""
**Contexte :** Vous analysez un fichier de **{len(df_current)} individus**.
Les valeurs vont de **{scen['min']}** à **{scen['max']} {scen['unit']}**.

**Consignes :**
1. Téléchargez le fichier Excel.
2. Créez un TCD et **Groupez** la variable `{scen['col_var']}`.
3. Utilisez un **PAS de {scen['step']}**.
   *(Exemple de classes attendues : {scen['labels'][0]}, {scen['labels'][1]}...)*
4. Affichez les effectifs ($n_i$).
""")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"MQ_Ex3_{scen['tag']}_{timestamp}.xlsx"

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_current.to_excel(writer, index=False, sheet_name='Donnees')

st.download_button(
    label=f"📥 Télécharger le fichier ({file_name})",
    data=output.getvalue(),
    file_name=file_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- 5. CORRECTION AUTOMATIQUE ---
st.subheader("2. Correction Automatique")
uploaded_file = st.file_uploader("Déposez votre fichier (.xlsx) complété ici", type=['xlsx'])

if uploaded_file:
    try:
        wb = openpyxl.load_workbook(uploaded_file, data_only=True)
        
        found_numbers = set()
        
        # Scan global
        for sheet in wb.worksheets:
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if isinstance(cell, (int, float)):
                        found_numbers.add(cell)
                        found_numbers.add(int(cell))
        
        st.write("---")
        st.write("#### 🔍 Vérification des Effectifs")
        
        cols = st.columns(2)
        found_all = True
        
        for i, (label, count_attendu) in enumerate(solution_counts.items()):
            with cols[i % 2]:
                # On tolère que l'étudiant ait trouvé le bon compte
                if count_attendu in found_numbers:
                    st.success(f"✅ **Tranche {label}** : {count_attendu}")
                else:
                    st.error(f"❌ **Tranche {label}** : Attendu {count_attendu}, pas trouvé.")
                    found_all = False
        
        total_ref = len(df_current)
        if total_ref in found_numbers:
            st.success(f"✅ **Total Général** ({total_ref}) correct.")
        else:
            st.warning(f"⚠️ Total général ({total_ref}) introuvable.")

        if found_all:
            st.balloons()
            st.success(f"👏 Parfait ! Vous maîtrisez le groupement sur le thème '{scen['tag']}'.")

    except Exception as e:
        st.error(f"Erreur de lecture : {e}")