import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime

st.set_page_config(page_title="S4 | Ex. 10 : Covariance", page_icon="📉", layout="wide")

URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_4.pdf" # Remplacez par le bon lien

st.title("📉 S4 | Ex. 10 : Covariance")

SCENARIOS = {
    "glaces": {
        "titre": "Température & Ventes de Glaces", 
        "var_x": "Température (°C)", "var_y": "Ventes (K€)",
        "vals_x": [20, 25, 30, 22, 28], # Moyenne X = 25
        "vals_y": [2, 5, 8, 3, 7],      # Moyenne Y = 5
        "mean_x": 25, "mean_y": 5,
        "relation": "positive"
    },
    "voiture": {
        "titre": "Vitesse & Temps de Trajet", 
        "var_x": "Vitesse (km/h)", "var_y": "Temps (min)",
        "vals_x": [30, 50, 70, 40, 60], # Moyenne X = 50
        "vals_y": [60, 40, 20, 50, 30], # Moyenne Y = 40
        "mean_x": 50, "mean_y": 40,
        "relation": "négative"
    },
    "etude": {
        "titre": "Heures de Révision & Note à l'Examen", 
        "var_x": "Révisions (h)", "var_y": "Note (/20)",
        "vals_x": [2, 4, 6, 3, 5],      # Moyenne X = 4
        "vals_y": [8, 12, 16, 10, 14],  # Moyenne Y = 12
        "mean_x": 4, "mean_y": 12,
        "relation": "positive"
    }
}

# --- CONTEXTE ---
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Mesurer comment deux variables évoluent ensemble (co-varient). 

    ### 🧠 Le sens de l'exercice
    La covariance nous indique la **direction** de la relation entre deux variables $X$ et $Y$ :
    * **Covariance Positive (> 0) :** Quand $X$ augmente, $Y$ a tendance à augmenter aussi (ex: Température et Ventes de glaces).
    * **Covariance Négative (< 0) :** Quand $X$ augmente, $Y$ a tendance à diminuer (ex: Vitesse et Temps de trajet).
    * **Covariance proche de 0 :** Il n'y a pas de relation linéaire évidente.
    
    💡 **Pourquoi c'est important pour la suite ?**
    La covariance est la brique de base pour calculer la **Corrélation**. Elle dépend des unités choisies (des K€, des km/h), ce qui la rend difficile à interpréter seule. La corrélation viendra standardiser ce résultat entre -1 et 1.
    """)

if st.button("🔄 Nouveau Scénario"):
    # Clear all session state related to this page
    for k in ['cov_man_data', 'cov_xl_data', 'editor_key_cov']:
        if k in st.session_state: del st.session_state[k]
    st.rerun()

tab_man, tab_xl = st.tabs(["📝 Mode Manuel (Comprendre)", "📊 Mode Excel (Pratiquer)"])

# --- MANUEL ---
with tab_man:
    st.subheader("1. Calcul manuel pas à pas")
    
    with st.sidebar:
        st.header("📝 Aide Mémoire")
        st.info("**Concept :** C'est la moyenne des produits des écarts.")
        st.latex(r"Cov(X,Y) = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{N}")
        st.markdown(f"""
        **Algorithme :**
        1. **Ecarts X :** Distance de $X$ à sa moyenne.
        2. **Ecarts Y :** Distance de $Y$ à sa moyenne.
        3. **Produit :** On multiplie les deux écarts ligne par ligne.
        4. **Somme :** On additionne tous les produits.
        5. **Covariance :** On divise la somme par $N$ (le nombre d'observations).
                    
        **Signe du produit :**
        * Si $X$ et $Y$ sont tous deux au-dessus (ou en dessous) de leur moyenne, le produit est **positif**.
        * Si l'un est au-dessus et l'autre en dessous, le produit est **négatif**.
        
        📄 <a href="{URL_SLIDES}" target="_blank">Voir les Slides</a>
        """, unsafe_allow_html=True)
    
    # Initialize Data
    if 'cov_man_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        st.session_state.cov_man_data = pd.DataFrame({
            scen["var_x"]: scen["vals_x"],
            scen["var_y"]: scen["vals_y"]
        })
        st.session_state.cov_man_scen = scen
    
    if 'editor_key_cov' not in st.session_state:
        st.session_state.editor_key_cov = random.randint(0, 100000)

    df_m = st.session_state.cov_man_data
    scen = st.session_state.cov_man_scen
    mean_x = scen["mean_x"]
    mean_y = scen["mean_y"]
    n = len(df_m)

    st.info(f"""
    **Contexte :** Étudions la relation entre *{scen['titre']}*. 
    **Consigne :** 1. Calculez les écarts à la moyenne pour $X$ et pour $Y$.
    2. Multipliez ces écarts dans la dernière colonne.
    **Note :** La moyenne de X ($\mu_X$) est de {mean_x} et la moyenne de Y ($\mu_Y$) est de {mean_y}.
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### 1. Remplissez le tableau")
        st.caption("Calculez les écarts pour X et Y, puis leur produit.")
        
        # Prepare the DataFrame for the editor
        df_input = pd.DataFrame()
        df_input[f"X ({scen['var_x']})"] = df_m[scen['var_x']]
        df_input[f"Y ({scen['var_y']})"] = df_m[scen['var_y']]
        df_input["Ecart X (x - μx)"] = [None] * n
        df_input["Ecart Y (y - μy)"] = [None] * n
        df_input["Produit des écarts"] = [None] * n
        
        # Display Data Editor
        edited_df = st.data_editor(
            df_input,
            column_config={
                f"X ({scen['var_x']})": st.column_config.NumberColumn(disabled=True),
                f"Y ({scen['var_y']})": st.column_config.NumberColumn(disabled=True),
                "Ecart X (x - μx)": st.column_config.NumberColumn(required=True, step=0.1),
                "Ecart Y (y - μy)": st.column_config.NumberColumn(required=True, step=0.1),
                "Produit des écarts": st.column_config.NumberColumn(
                    help="Ecart X multiplié par Ecart Y", required=True, step=0.1
                )
            },
            hide_index=True,
            key=f"editor_cov_{st.session_state.editor_key_cov}" 
        )

    with col2:
        st.markdown("#### 2. Finalisation")
        
        # Step 1: Sum of products
        u_somme = st.number_input("A. Somme des Produits (Total dernière colonne) :", step=1.0)
        
        # Step 2: Covariance
        u_cov = st.number_input(f"B. Covariance (Somme / {n}) :", step=0.1)
        
        if st.button("✅ Vérifier les calculs"):
            row_errors = []
            
            # Recalculate Truth
            true_diffs_x = df_m[scen['var_x']] - mean_x
            true_diffs_y = df_m[scen['var_y']] - mean_y
            true_prods = true_diffs_x * true_diffs_y
            
            # Check User Inputs
            try:
                user_diffs_x = edited_df["Ecart X (x - μx)"].fillna(0)
                user_diffs_y = edited_df["Ecart Y (y - μy)"].fillna(0)
                user_prods = edited_df["Produit des écarts"].fillna(0)
                
                for i in range(n):
                    if abs(user_diffs_x.iloc[i] - true_diffs_x.iloc[i]) > 0.01:
                        row_errors.append(f"Ligne {i+1} : Ecart X incorrect (mis {user_diffs_x.iloc[i]}, attendu {true_diffs_x.iloc[i]})")
                    elif abs(user_diffs_y.iloc[i] - true_diffs_y.iloc[i]) > 0.01:
                        row_errors.append(f"Ligne {i+1} : Ecart Y incorrect (mis {user_diffs_y.iloc[i]}, attendu {true_diffs_y.iloc[i]})")
                    elif abs(user_prods.iloc[i] - true_prods.iloc[i]) > 0.01:
                        row_errors.append(f"Ligne {i+1} : Produit incorrect (mis {user_prods.iloc[i]}, attendu {true_prods.iloc[i]})")
            except Exception as e:
                row_errors.append("Veuillez remplir toutes les cases du tableau.")

            # Verify Final Stats
            real_somme = true_prods.sum()
            real_cov = real_somme / n
            
            stats_errors = []
            if abs(u_somme - real_somme) > 0.1:
                stats_errors.append(f"❌ Erreur Somme : {u_somme} ≠ {real_somme}")
            if abs(u_cov - real_cov) > 0.1:
                stats_errors.append(f"❌ Erreur Covariance : {u_cov} ≠ {real_cov:.2f}")

            # Display Results
            if not row_errors and not stats_errors:
                st.success(f"👏 Bravo ! Tableau et calculs parfaits. La covariance est de {real_cov:.2f}.")
                st.balloons()
            else:
                if row_errors:
                    st.error("⚠️ Erreurs dans le tableau :")
                    for err in row_errors[:3]:
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
        **Fonction Excel (Population) :**
        
        Comme pour la variance, nous travaillons ici sur des données complètes.
        
        * **Covariance :**
            `=COVARIANCE.P(Matrice1; Matrice2)`
            
        *(Le suffixe **.P** est crucial. Sans lui, Excel utilise `.S` qui divise par N-1).*
        """)
    
    if 'cov_xl_data' not in st.session_state:
        s_key = random.choice(list(SCENARIOS.keys()))
        scen = SCENARIOS[s_key]
        
        # Generate correlated data based on scenario
        x_data = np.random.normal(scen["mean_x"], 10, 100)
        if scen["relation"] == "positive":
            y_data = x_data * 1.5 + np.random.normal(0, 5, 100)
        else:
            y_data = x_data * -1.5 + np.random.normal(0, 5, 100)
            
        st.session_state.cov_xl_data = pd.DataFrame({
            scen["var_x"]: np.round(x_data, 1), 
            scen["var_y"]: np.round(y_data, 1)
        })
        st.session_state.cov_xl_scen = scen
    
    df_x = st.session_state.cov_xl_data
    scen_x = st.session_state.cov_xl_scen
    
    st.info(f"""
    **Contexte :** Vous avez une base de données contenant 100 observations de *{scen_x['var_x']}* et *{scen_x['var_y']}*.
    **Consigne :** Calculez la covariance entre ces deux variables.
    **Important :** Utilisez bien la fonction `=COVARIANCE.P(Plage1; Plage2)` pour calculer sur l'ensemble de la population.
    """)

    out = io.BytesIO()
    with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
        df_x.to_excel(writer, index=False)
        
    ts = datetime.now().strftime("%H%M")
    file_name = f"MQ_S3_Ex9_Covariance_{ts}.xlsx"
    
    st.download_button(
        label=f"📥 Télécharger Données ({file_name})", 
        data=out.getvalue(), 
        file_name=file_name
    )
    
    colA, _ = st.columns(2)
    with colA:
        u_cov_xl = st.number_input("Covariance calculée dans Excel :", step=0.1)
        
    if st.button("Correction Excel"):
        # np.cov calculates sample covariance by default. bias=True calculates population covariance (divides by N)
        true_cov = np.cov(df_x[scen_x['var_x']], df_x[scen_x['var_y']], bias=True)[0, 1]
        
        if abs(u_cov_xl - true_cov) < 0.5:
            st.success("✅ Correct !")
            st.balloons()
        else:
            st.error(f"❌ Attendu : {true_cov:.2f}")