import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime

st.set_page_config(page_title="S3 | Ex6 : Moyenne", page_icon="🎯", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=26"

st.title("🎯 S3 | Ex. 6 : La Moyenne Simple")

SCENARIOS = {
    "notes": {"titre": "Notes d'Étudiant", "unit": "/20", "min": 0, "max": 20, "digits": 1},
    "taille": {"titre": "Taille de Basketteur", "unit": "cm", "min": 180, "max": 215, "digits": 0},
    "ecran": {"titre": "Temps Écran", "unit": "h", "min": 1, "max": 12, "digits": 1},
    "co2": {"titre": "Empreinte Carbone (tCO2/hab)", "unit": "t", "min": 2, "max": 15, "digits": 1}
}

with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Calculer le point d'équilibre mathématique de la distribution.

    ### 🧠 Le sens de l'exercice
    La moyenne répond à la question : **"Si on mettait tout en commun et qu'on partageait équitablement, combien chacun aurait-il ?"**
    
    C'est le centre de gravité des données. Contrairement à la médiane, la moyenne prend en compte la valeur exacte de chaque individu (ce qui la rend sensible aux extrêmes).
    """)

if st.button("🔄 Nouveau Cas"):
    for k in ['mean_man_data', 'mean_man_scen', 'mean_xl_data', 'mean_xl_scen']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire (Manuel)")
        st.info("**Formule :** Somme totale divisée par le nombre d'individus.")
        st.latex(r"\bar{x} = \frac{\sum x_i}{N}")
        st.markdown(f"""
        **En français :**
        1. Additionner toutes les valeurs.
        2. Compter combien il y a de valeurs.
        3. Diviser (1) par (2).
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        """, unsafe_allow_html=True)
    
    if 'mean_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        vals = [round(random.uniform(scen["min"], scen["max"]), scen["digits"]) for _ in range(5)]
        st.session_state.mean_man_data = pd.DataFrame({f"Val ({scen['unit']})": vals})
        st.session_state.mean_man_scen = scen

    df_m = st.session_state.mean_man_data
    scen_m = st.session_state.mean_man_scen

    st.info(f"""
    **Contexte :** Voici 5 valeurs de *{scen_m['titre']}*. Nous cherchons le point d'équilibre.
    **Consigne :** 1. Additionnez toutes les valeurs pour obtenir le total.
    2. Divisez ce total par le nombre d'éléments (5).
    3. Arrondissez si nécessaire à 1 ou 2 décimales.
    **Attention :** N'oubliez aucune valeur dans l'addition !
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_m, height=230, hide_index=True)
    with col2:
        user_mean = st.number_input(f"Moyenne ({scen_m['unit']}) :", step=0.1)
        if st.button("Vérifier"):
            true_mean = df_m.iloc[:, 0].mean()
            if abs(user_mean - true_mean) < 0.05:
                st.success(f"✅ Bravo ! {true_mean:.2f}")
                st.balloons()
            else:
                st.error(f"❌ La moyenne est {true_mean:.2f}")

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonction Excel")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire (Excel)")
        st.info("**Excel :** Ne calculez rien, utilisez la fonction.")
        
        st.markdown("""
        **Syntaxe Excel :**
        * 🇫🇷 `=MOYENNE(Plage)`
        * 🇺🇸 `=AVERAGE(Range)`
        
        ⚠️ Ne sélectionnez pas les entêtes (textes), uniquement les cellules chiffrées.
        """)
    
    if 'mean_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        data = np.random.normal((scen["max"]+scen["min"])/2, (scen["max"]-scen["min"])/6, 200)
        data = np.clip(data, scen["min"], scen["max"])
        st.session_state.mean_xl_data = pd.DataFrame({"ID": range(1, 201), "Val": np.round(data, scen["digits"])})
        st.session_state.mean_xl_scen = scen
    
    df_x = st.session_state.mean_xl_data
    scen_x = st.session_state.mean_xl_scen

    st.info(f"""
    **Contexte :** Vous disposez d'un jeu de données de 200 lignes concernant *{scen_x['titre']}*.
    **Consigne :** 1. Téléchargez les données.
    2. Dans Excel, calculez la moyenne de la colonne B via `=MOYENNE(B2:B201)` (ou `=AVERAGE`).
    **Astuce :** Vérifiez que vous n'avez pas sélectionné l'entête (le texte) dans votre plage.
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S3_Ex6_Moyenne_Simple_{scen_x['titre']}_{ts}.xlsx"
    st.download_button(
    label=f"📥 Télécharger Données ({file_name})", 
    data=out.getvalue(), 
    file_name=file_name
    )

    u_val = st.number_input("Résultat Excel :", step=0.01)
    if st.button("Correction"):
        t_val = df_x.iloc[:, 1].mean()
        if abs(u_val - t_val) < 0.05:
            st.success(f"✅ Correct ! ({t_val:.2f})")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {t_val:.2f}")