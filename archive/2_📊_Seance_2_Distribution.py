import streamlit as st
import pandas as pd
import numpy as np
import io
import random
import openpyxl
from datetime import datetime

st.set_page_config(page_title="Séance 2 : Distributions", page_icon="📊")

# --- CONFIGURATION ---
URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=15"

st.title("📊 Séance 2 : Distributions et TCD")
st.markdown("""
**Objectif :** Utiliser un Tableau Croisé Dynamique (Pivot Table) pour transformer une liste d'individus en tableau de distribution.
""")

# --- 1. CONFIGURATION DES SCÉNARIOS ---
SCENARIOS = {
    "education": {
        "tag": "Education",
        "titre": "Niveau d'Étude (Sociologie)",
        "col_id": "ID_Individu",
        "col_var": "Diplome",
        "categories": ["1. Sans Bac", "2. Bac", "3. Licence", "4. Master", "5. Doctorat"],
        "weights": [0.15, 0.30, 0.30, 0.20, 0.05]
    },
    "satisfaction": {
        "tag": "Satisfaction",
        "titre": "Enquête Satisfaction (Marketing)",
        "col_id": "Ref_Client",
        "col_var": "Avis_Service",
        "categories": ["1. Très Insatisfait", "2. Insatisfait", "3. Neutre", "4. Satisfait", "5. Très Satisfait"],
        "weights": [0.10, 0.15, 0.20, 0.40, 0.15]
    },
    "transport": {
        "tag": "Transport",
        "titre": "Mode de Transport (Urbanisme)",
        "col_id": "Matricule_Usager",
        "col_var": "Transport_Principal",
        "categories": ["1. Voiture", "2. Transports en commun", "3. Vélo", "4. Marche", "5. Deux-roues"],
        "weights": [0.35, 0.40, 0.10, 0.10, 0.05]
    },
    "politique": {
        "tag": "Politique",
        "titre": "Sondage Politique (Science Po)",
        "col_id": "Code_Electeur",
        "col_var": "Intention_Vote",
        "categories": ["1. Candidat A", "2. Candidat B", "3. Candidat C", "4. Abstention", "5. Blanc/Nul"],
        "weights": [0.25, 0.22, 0.18, 0.25, 0.10]
    }
}

# --- 2. BOUTON "NOUVEL EXERCICE" ---
if st.button("🔄 Générer un nouveau jeu de données"):
    keys_to_clear = ['dist_data', 'current_scenario']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# --- 3. GÉNÉRATION DES DONNÉES ---
if 'dist_data' not in st.session_state:
    scenario_key = random.choice(list(SCENARIOS.keys()))
    scenario = SCENARIOS[scenario_key]
    
    n = random.randint(180, 250)
    variable_data = random.choices(scenario["categories"], weights=scenario["weights"], k=n)
    ids = random.sample(range(10000, 99999), n)
    
    df = pd.DataFrame({
        scenario["col_id"]: ids,
        scenario["col_var"]: variable_data
    })
    
    st.session_state.dist_data = df
    st.session_state.current_scenario = scenario

current_scen = st.session_state.current_scenario
df_current = st.session_state.dist_data

# --- 4. AFFICHAGE ET TÉLÉCHARGEMENT ---
st.subheader(f"1. L'Exercice : {current_scen['titre']}")

# --- AIDE DANS LA SIDEBAR ---
with st.sidebar:
    st.header("💡 Aide Mémoire")
    
    st.markdown(f"""
    **Besoin de revoir le cours ?**
    📄 <a href="{URL_SLIDES}" target="_blank">Ouvrir les slides (PDF)</a>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown(f"""
    **Comment faire un TCD ?**
    
    1. Sélectionnez tout votre tableau (**Ctrl+A**).
    2. Allez dans **Insertion** > **Tableau Croisé Dynamique**.
    3. Glissez la variable *{current_scen['col_var']}* dans la zone **LIGNES**.
    4. Glissez la même variable dans la zone **VALEURS**.
    
    ⚠️ *Si Excel affiche une somme au lieu d'un comptage :*
    * Cliquez sur le champ dans VALEURS.
    * Allez dans **Paramètres des champs de valeur**.
    * Choisissez **Nombre** (ou "Compte").
    """)

# --- CONSIGNES PRINCIPALES ---
st.info(f"""
**Contexte :** Vous analysez un fichier de **{len(df_current)} lignes**.
Chaque ligne est identifiée par `{current_scen['col_id']}`.

**Consignes :**
1. Téléchargez le fichier Excel ci-dessous.
2. Créez un **Tableau Croisé Dynamique**.
3. Analysez la variable **`{current_scen['col_var']}`** pour afficher :
    * **La distribution des effectifs par catégorie**.
""")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name_clean = f"MQ_Ex2_{current_scen['tag']}_{timestamp}.xlsx"

output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_current.to_excel(writer, index=False, sheet_name='Donnees_Brutes')

st.download_button(
    label=f"📥 Télécharger le fichier ({file_name_clean})",
    data=output.getvalue(),
    file_name=file_name_clean,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- 5. CORRECTION AUTOMATIQUE ---
st.subheader("2. Correction Automatique")
uploaded_file = st.file_uploader("Déposez votre fichier (.xlsx) complété ici", type=['xlsx'])

if uploaded_file:
    try:
        correction = df_current[current_scen["col_var"]].value_counts().sort_index()
        total_ref = len(df_current)
        
        wb = openpyxl.load_workbook(uploaded_file, data_only=True)
        
        found_text = set()
        found_numbers = set()
        sheet_names_scanned = []

        for sheet in wb.worksheets:
            sheet_names_scanned.append(sheet.title)
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if cell is not None:
                        val_str = str(cell).strip().lower()
                        found_text.add(val_str)
                        try:
                            val_float = float(cell)
                            found_numbers.add(val_float)
                            found_numbers.add(int(val_float)) 
                        except ValueError:
                            pass
        
        st.write(f"🔍 Analyse des feuilles : *{', '.join(sheet_names_scanned)}*")
        
        var_name_lower = current_scen["col_var"].lower()
        if not any(var_name_lower in txt for txt in found_text):
            st.warning(f"⚠️ Attention : Je ne trouve pas la variable **{current_scen['col_var']}** dans votre fichier.")
        
        found_all = True
        st.divider()
        cols = st.columns(2)
        
        for i, (cat, count_attendu) in enumerate(correction.items()):
            label_clean = cat.lower()
            label_text_only = cat.split(". ")[-1].lower() if ". " in cat else cat.lower()
            
            with cols[i % 2]:
                label_found = any((label_clean in txt) or (label_text_only in txt) for txt in found_text)
                if not label_found:
                    st.warning(f"⚠️ Label introuvable : **{cat}**")
                
                if count_attendu in found_numbers:
                    st.success(f"✅ **{cat}** : {count_attendu}")
                else:
                    st.error(f"❌ **{cat}** : Attendu {count_attendu}, pas trouvé.")
                    found_all = False

        if total_ref in found_numbers:
            st.success(f"✅ **Total Général** ({total_ref}) correct.")
        else:
            st.warning(f"⚠️ Total général ({total_ref}) introuvable.")

        if found_all:
            st.balloons()
            st.success(f"👏 Bravo ! Exercice '{current_scen['titre']}' validé.")

    except Exception as e:
        st.error(f"Erreur technique : {e}")