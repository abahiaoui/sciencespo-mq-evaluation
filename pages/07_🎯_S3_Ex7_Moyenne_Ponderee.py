import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime


st.set_page_config(page_title="S3 | Ex7 : Moyenne Pondérée", page_icon="🎯", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=27"

st.title("🎯 S3 | Ex. 7 : La Moyenne Pondérée")

SCENARIOS = {
    "academic": {
        "titre": "Note sur le semestre", "l_val": "Note", "l_w": "Coef",
        "items": ["Droit", "Eco", "Histoire", "Anglais"], "min": 8, "max": 18, "w": [6, 6, 4, 3]
    },
    "reviews": {
        "titre": "Avis Clients", 
        "l_val": "Note /5", 
        "l_w": "Nombre d'avis",
        "items": ["Google", "Trustpilot", "Site Web", "App Store"], 
        "min": 1, 
        "max": 5, 
        "w": [120, 500, 45, 800]
    },
    "chomage": {
        "titre": "Chômage National", 
        "l_val": "Taux Chômage (%)", 
        "l_w": "Pop. Active (M)",
        "items": ["Île-de-France", "Bretagne", "Hauts-de-France", "Corse"], 
        "min": 5, "max": 12, 
        "w": [60, 15, 25, 2] 
    },
    "payroll": {
        "titre": "Masse Salariale", "l_val": "Salaire", "l_w": "Effectif",
        "items": ["Ouvriers", "Employés", "Cadres", "Dirigeants"], 
        "min": 1500, "max": 5000, "w": [50, 100, 25, 5] 
    }
}

with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Calculer une moyenne quand les éléments n'ont pas la même importance (Poids/Coefficients/Effectifs).

    ### 🧠 Le sens de l'exercice
    Dans la réalité, 1 individu $\\neq$ 1 individu :
    * **Scolarité :** Un partiel (Coef 2) compte moins qu'un final (Coef 6).
    * **Sociologie :** Le salaire moyen d'une région (1M habitants) pèse plus que celui d'un village (100 habitants).
    * **Commerce :** Le prix moyen d'un panier dépend de la quantité achetée de chaque produit.
    """)

if st.button("🔄 Nouveau Cas"):
    for k in ['wm_man_data', 'wm_man_scen', 'wm_xl_data', 'wm_xl_scen']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire (Manuel)")
        st.info("**Principe :** Chaque valeur tire la moyenne vers elle avec une force proportionnelle à son poids.")
        st.latex(r"\bar{x} = \frac{\sum (x_i \times p_i)}{\sum p_i}")
        st.markdown(f"""
        **Algorithme :**
        1. Multiplier chaque Note par son Poids.
        2. Somme des résultats (Numérateur).
        3. Somme des Poids (Dénominateur).
        4. Diviser le tout.
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        """, unsafe_allow_html=True)
    
    if 'wm_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        vals = [random.randint(scen["min"], scen["max"]) for _ in scen["items"]]
        df = pd.DataFrame({"Item": scen["items"], scen["l_val"]: vals, scen["l_w"]: scen["w"]})
        st.session_state.wm_man_data = df
        st.session_state.wm_man_scen = scen

    scen = st.session_state.wm_man_scen
    df_m = st.session_state.wm_man_data

    st.info(f"""
    **Contexte :** Cas *{scen['titre']}*. Ici, chaque élément a une importance (poids) différente.
    **Consigne :** 1. Multipliez chaque *{scen['l_val']}* par son *{scen['l_w']}*.
    2. Faites la somme de ces produits.
    3. Divisez le tout par la somme totale des *{scen['l_w']}*.
    **Piège à éviter :** Ne divisez pas par le nombre d'items (4), mais bien par la somme des poids !
    """)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.dataframe(df_m, hide_index=True)
    with col2:
        u_res = st.number_input("Résultat :", step=0.1)
        if st.button("Vérifier"):
            num = sum(df_m.iloc[:, 1] * df_m.iloc[:, 2])
            den = sum(df_m.iloc[:, 2])
            res = num / den
            if abs(u_res - res) < 0.1:
                st.success(f"✅ Bravo ! {res:.2f}")
                st.balloons()
            else:
                st.error(f"❌ ({num} / {den}) = {res:.2f}")

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonction Excel")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire (Excel)")
        st.markdown("""
        **La fonction magique :**
        `=SOMMEPROD(Plage1; Plage2)`
        
        Cette fonction fait l'étape 1 et 2 d'un coup (Multiplication + Somme).
        
        **Formule complète :**
        ```excel
        = SOMMEPROD(Notes; Coefs) / SOMME(Coefs)
        ```
        """)
    
    if 'wm_xl_data' not in st.session_state:
        # USE THE SCENARIO INSTEAD OF HARDCODED LISTS
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        # Generate random data based on scenario limits
        vals = [random.randint(scen["min"], scen["max"]) for _ in scen["items"]]
        weights = [random.randint(10, 200) for _ in scen["items"]]
        
        st.session_state.wm_xl_data = pd.DataFrame({
            "Catégorie": scen["items"], 
            scen["l_w"]: weights, 
            scen["l_val"]: vals
        })
        st.session_state.wm_xl_scen = scen

    
    df_x = st.session_state.wm_xl_data
    scen_x = st.session_state.wm_xl_scen

    st.info(f"""
    **Contexte :** Calculer la moyenne pondérée manuellement sur Excel est long et propice aux erreurs.
    **Consigne :** 1. Utilisez la fonction magique : `=SOMMEPROD(Plage_Poids; Plage_Valeurs)`.
    2. Divisez le résultat par `=SOMME(Plage_Poids)`.
    **Syntaxe :** En anglais, c'est `=SUMPRODUCT(...) / SUM(...)`.
    """)

    
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S3_Ex7_Moyenne_Ponderee_{scen_x['titre']}_{ts}.xlsx"
    st.download_button(
    label=f"📥 Télécharger Données ({file_name})", 
    data=out.getvalue(), 
    file_name=file_name
    )    
    u_val = st.number_input("Salaire Moyen Global :", step=1.0)
    if st.button("Correction"):
        col_w = scen_x["l_w"]   # e.g., "Coef", "Qté", "Effectif"
        col_val = scen_x["l_val"] # e.g., "Note", "Prix", "Salaire"

        res = sum(df_x[col_w] * df_x[col_val]) / sum(df_x[col_w])
        if abs(u_val - res) < 1:
            st.success(f"✅ Correct ! ({res:.0f})")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {res:.0f}")