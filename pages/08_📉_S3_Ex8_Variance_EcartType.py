import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime

st.set_page_config(page_title="S3 | Ex. 8 : Dispersion", page_icon="📉", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_2_3.pdf#page=40"

st.title("📉 S3 | Ex. 8 : Variance & Écart-Type")

SCENARIOS = {
    "education": {
        "titre": "Inégalités de niveau scolaire", 
        "unit": "/20",
        "vals_a": [11, 12, 12, 13, 12], # Classe Homogène (Niveau standard)
        "vals_b": [4, 19, 5, 20, 12],   # Classe Hétérogène (Excellence vs Échec)
        "mean": 12, 
        "sigma_low": 1.5, 
        "sigma_high": 7
    },
    "meteo": {
        "titre": "Stabilité des températures", "unit": "°C",
        "vals_a": [20, 21, 19, 20, 20], "vals_b": [10, 30, 5, 35, 20], 
        "mean": 20, "sigma_low": 3, "sigma_high": 10
    },
    "machine": {
        "titre": "Précision d'une Machine", "unit": "g",
        "vals_a": [499, 500, 501, 500, 500], "vals_b": [450, 550, 480, 520, 500], 
        "mean": 500, "sigma_low": 5, "sigma_high": 30
    },
    "sante": {
        "titre": "Temps d'Attente en Urgences", "unit": "min",
        "vals_a": [115, 120, 125, 120, 120], # Hôpital A (Fiable)
        "vals_b": [60, 180, 50, 190, 120],   # Hôpital B (Chaotique)
        "mean": 120, 
        "sigma_low": 5, 
        "sigma_high": 60
    }
}

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Mesurer si les données sont serrées (homogènes) ou étalées (hétérogènes) autour de la moyenne.

    ### 🧠 Le sens de l'exercice
    Deux groupes peuvent avoir la même moyenne (ex: 12/20), mais des profils opposés :
    * **Groupe A (Stable) :** Tout le monde a entre 11 et 13. C'est fiable, prévisible.
    * **Groupe B (Dispersé) :** Les notes vont de 2 à 20. C'est risqué, instable.
    
    💡 **Pourquoi c'est important pour la suite ? (Tests d'Hypothèses)**
    En statistiques, la dispersion est le **"Bruit"** et la différence de moyenne est le **"Signal"**. 
    Pour prouver qu'un résultat est significatif (ex: un médicament fonctionne), il faut un Signal fort ou un Bruit faible. Plus la dispersion est grande, plus il est difficile de prouver quoi que ce soit.
    """)

if st.button("🔄 Nouveau Scénario"):
    # Clear all session state related to this page
    for k in ['var_man_data', 'var_xl_data', 'editor_key']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:



        
    st.subheader("1. Calcul manuel pas à pas")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.info("**Concept :** C'est la moyenne des écarts au carré.")
        st.latex(r"V = \frac{\sum (x_i - \bar{x})^2}{N}")
        st.markdown(f"""
        **Algorithme :**
        1. **Ecarts :** Distance à la moyenne.
        2. **Carrés :** On met au carré (pour avoir du positif).
        3. **Somme (SCE) :** On additionne tout.
        4. **Variance :** On divise par N (Moyenne des carrés).
        5. **Ecart-Type :** Racine carrée.
                    
        **Pourquoi le carré ?**
        Pour éviter que les écarts positifs (+2) et négatifs (-2) ne s'annulent. Cela transforme tout en positif.
        
        **L'Écart-Type ($\sigma$) :**
        C'est simplement la racine carrée de la Variance pour revenir à l'unité d'origine (des notes, des euros...).
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        """, unsafe_allow_html=True)
    
    # Initialize Data
    if 'var_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        vals = random.choice([scen["vals_a"], scen["vals_b"]])
        st.session_state.var_man_data = pd.DataFrame({"Note": vals})
        st.session_state.var_man_scen = scen
    
    # FIX: Initialize key separately to ensure it always exists
    if 'editor_key' not in st.session_state:
        st.session_state.editor_key = random.randint(0, 100000)

    df_m = st.session_state.var_man_data
    scen = st.session_state.var_man_scen
    mean_val = st.session_state.var_man_scen["mean"]
    n = len(df_m)

    st.info(f"""
    **Contexte :** Pour comprendre la volatilité de *{scen['titre']}*, nous allons décomposer le calcul de la variance.
    **Consigne :** 1. Remplissez la colonne **Ecart** (Valeur - Moyenne).
    2. Remplissez la colonne **Carré** (résultat précédent × lui-même).
    3. Validez pour vérifier si vous avez compris la mécanique interne de l'écart-type.
    **Note :** La moyenne (μ) est fixée à {mean_val}.
    """)

    col1, col2 = st.columns([1.5, 1])



    

    with col1:
        st.markdown("#### 1. Remplissez le tableau")
        st.caption("Calculez l'écart pour chaque ligne, puis son carré.")
        
        # Prepare the DataFrame for the editor
        df_input = df_m.copy()
        df_input.columns = ["Valeur (x)"]
        df_input["Moyenne (μ)"] = mean_val
        df_input["Ecart (x - μ)"] = [None] * n  # Empty for user to fill
        df_input["Carré (x - μ)²"] = [None] * n # Empty for user to fill
        
        # Display Data Editor
        edited_df = st.data_editor(
            df_input,
            column_config={
                "Valeur (x)": st.column_config.NumberColumn(disabled=True),
                "Moyenne (μ)": st.column_config.NumberColumn(disabled=True),
                "Ecart (x - μ)": st.column_config.NumberColumn(
                    "Ecart (x - μ)", 
                    help="Valeur - Moyenne", 
                    required=True,
                    step=0.1
                ),
                "Carré (x - μ)²": st.column_config.NumberColumn(
                    "Carré (x - μ)²", 
                    help="Le résultat de l'écart multiplié par lui-même", 
                    required=True,
                    step=0.1
                )
            },
            hide_index=True,
            key=f"editor_{st.session_state.editor_key}" # Unique key ensures reset
        )

    with col2:
        st.markdown("#### 2. Finalisation")
        
        # Step 1: SCE
        u_sce = st.number_input("A. Somme des Carrés (Total colonne 4) :", step=1.0)
        
        # Step 2: Variance
        u_var = st.number_input(f"B. Variance (Somme / {n}) :", step=0.1)
        
        # Step 3: Std Dev
        u_std = st.number_input("C. Écart-Type (Racine de B) :", step=0.1)
        
        if st.button("✅ Vérifier les calculs"):
            # 1. Verify Table Rows
            row_errors = []
            
            # Recalculate Truth
            true_diffs = df_m["Note"] - mean_val
            true_sqs = true_diffs ** 2
            
            # Check User Inputs (Handle None/NaN)
            try:
                user_diffs = edited_df["Ecart (x - μ)"].fillna(0)
                user_sqs = edited_df["Carré (x - μ)²"].fillna(0)
                
                for i in range(n):
                    # Check Difference
                    if abs(user_diffs.iloc[i] - true_diffs.iloc[i]) > 0.01:
                        row_errors.append(f"Ligne {i+1} : Ecart incorrect (Vous avez mis {user_diffs.iloc[i]}, attendu {true_diffs.iloc[i]})")
                    # Check Square
                    elif abs(user_sqs.iloc[i] - true_sqs.iloc[i]) > 0.01:
                        row_errors.append(f"Ligne {i+1} : Carré incorrect (Vous avez mis {user_sqs.iloc[i]}, attendu {true_sqs.iloc[i]})")
            except Exception as e:
                row_errors.append("Veuillez remplir toutes les cases du tableau.")

            # 2. Verify Final Stats
            real_sce = true_sqs.sum()
            real_var = real_sce / n
            real_std = np.sqrt(real_var)
            
            stats_errors = []
            if abs(u_sce - real_sce) > 0.1:
                stats_errors.append(f"❌ Erreur Somme (SCE) : {u_sce} ≠ {real_sce}")
            if abs(u_var - real_var) > 0.1:
                stats_errors.append(f"❌ Erreur Variance : {u_var} ≠ {real_var:.2f}")
            if abs(u_std - real_std) > 0.1:
                stats_errors.append(f"❌ Erreur Ecart-Type : {u_std} ≠ {real_std:.2f}")

            # Display Results
            if not row_errors and not stats_errors:
                st.success(f"👏 Bravo ! Tableau et calculs parfaits. (σ = {real_std:.2f})")
                st.balloons()
            else:
                if row_errors:
                    st.error("⚠️ Erreurs dans le tableau :")
                    for err in row_errors[:3]: # Show max 3 errors to save space
                        st.warning(err)
                    if len(row_errors) > 3: st.warning("...")
                
                if stats_errors:
                    st.error("⚠️ Erreurs dans les résultats finaux :")
                    for err in stats_errors:
                        st.write(err)

# --- EXCEL ---
with tab_xl:
    st.subheader("2. Fonction Excel")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.markdown("""
        **Fonctions Excel (Population) :**
        
        Pour ce cours, nous travaillons sur des données complètes (Population), pas des échantillons (Séance 7 et 8).
        
        * **Variance :**
            `=VAR.P(Plage)`
        * **Écart-Type :**
            `=ECARTYPE.P(Plage)`
            
        *(Le suffixe **.P** est crucial. Sans lui, Excel divise par N-1, ce qui est faux ici).*
        """)
    
    if 'var_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        stable = np.random.normal(scen["mean"], scen["sigma_low"], 100)
        dispersed = np.random.normal(scen["mean"], scen["sigma_high"], 100)
        
        st.session_state.var_xl_data = pd.DataFrame({
            "Stable": np.round(stable, 1), 
            "Dispersé": np.round(dispersed, 1)
        })
        st.session_state.var_xl_scen = scen
    
    df_x = st.session_state.var_xl_data
    scen_x = st.session_state.get('var_xl_scen', SCENARIOS['education']) # Fallback in case scenario is missing
    
    st.info(f"""
    **Contexte :** Vous avez deux séries de données : "Stable" et "Dispersé".
    **Consigne :** 1. Calculez l'écart-type de chaque colonne pour comparer leur volatilité.
    2. Utilisez la fonction `=ECARTYPE.P(Plage)` (ou `=STDEV.P` en anglais).
    **Important :** N'oubliez pas le **.P** (Population). Si vous utilisez `.S` ou sans suffixe, le résultat sera faux (division par N-1).
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S3_Ex8_Variance_{scen_x['titre']}_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger Données ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    colA, colB = st.columns(2)
    with colA:
        std_A = st.number_input("Écart-type Stable :", step=0.1)
    with colB:
        std_B = st.number_input("Écart-type Dispersé :", step=0.1)
        
    if st.button("Correction Excel"):
        tA = np.std(df_x["Stable"]) 
        tB = np.std(df_x["Dispersé"])
        
        if abs(std_A - tA) < 0.2 and abs(std_B - tB) < 0.2:
            st.success("✅ Correct !")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {tA:.2f} et {tB:.2f}")