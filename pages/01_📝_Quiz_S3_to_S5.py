import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd
import numpy as np

st.set_page_config(page_title="Quiz S3 à S5", page_icon="📝", layout="wide")

st.title("📝 Évaluation : Séances 3 à 5")
st.markdown("""
**Durée estimée : 30 minutes**

Veuillez répondre à toutes les questions avant de soumettre. Une fois soumis, vos réponses seront enregistrées définitivement.
""")

# 1. Setup connection securely
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

try:
    s_info = st.secrets["connections"]["gsheets"]
    credentials = Credentials.from_service_account_info(
        s_info,
        scopes=scopes,
    )
    client = gspread.authorize(credentials)
except Exception as e:
    st.error(f"Erreur de connexion à Google Sheets: {e}")
    st.stop()

# Helpers
def calculate_variance(data, is_sample=False):
    n = len(data)
    if n <= 1: return 0.0
    mean = sum(data) / n
    sq_diff = sum((x - mean) ** 2 for x in data)
    return sq_diff / (n - 1 if is_sample else n)

def get_client_ip():
    try:
        # Streamlit >= 1.35
        header_val = st.context.headers.get("X-Forwarded-For")
        if header_val:
            return header_val.split(",")[0].strip()
        return "Local/Unknown"
    except Exception:
        try:
            # Fallback for older Streamlit versions
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers()
            if "X-Forwarded-For" in headers:
                return headers["X-Forwarded-For"].split(",")[0].strip()
            return "Local/Unknown"
        except Exception:
            return "Unknown"

import hashlib
def string_to_seed(s):
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % (10**8)

# Step 1: Identification to lock the seed
if 'identified' not in st.session_state:
    st.header("Étape 1 : Identification")
    st.info("Veuillez saisir votre adresse email Sciences Po pour générer votre sujet d'examen unique.")
    email_input = st.text_input("Adresse e-mail (Sciences Po)")
    if st.button("Commencer l'examen"):
        if email_input and "@" in email_input:
            st.session_state['identified'] = True
            st.session_state['email_student'] = email_input.strip()
            st.rerun()
        else:
            st.error("Veuillez entrer une adresse e-mail valide.")
    st.stop() # Halt rendering until identified

# Once identified, seed numpy and generate dataset
email = st.session_state['email_student']
seed = string_to_seed(email)
np.random.seed(seed)

# Generate Random Variables for Q4 & Q5 (Dataset)
base_values = np.random.randint(10, 30, size=6)
remainder = sum(base_values) % 6
if remainder != 0:
    base_values[5] += (6 - remainder) # Ensure the sum is perfectly divisible by 6 for a clean integer mean
dataset_q4 = sorted([int(x) for x in base_values]) # List of 6 integers

# Calculate correct answers for Q4 & Q5 based on randomized dataset
# Median
def calc_median(data):
    n = len(data)
    if n % 2 == 0:
        return (data[n//2 - 1] + data[n//2]) / 2.0
    return float(data[n//2])

correct_q4_med = calc_median(dataset_q4)
correct_q4_mean = sum(dataset_q4) / len(dataset_q4)
correct_q5_var = calculate_variance(dataset_q4, is_sample=False)

# Generate Random Variables for Q6 (Public vs Private)
# Let's generate a 7-row table (3 Public, 4 Private)
salaries_public = [int(x) for x in np.random.randint(1800, 2600, size=3)]
salaries_prive = [int(x) for x in np.random.randint(2200, 4800, size=4)]

# Calculate correct answers for Q6
correct_q5_mean_public = sum(salaries_public) / len(salaries_public)
correct_q5_mean_prive = sum(salaries_prive) / len(salaries_prive)

with st.form("quiz_form"):
    st.header("Informations de l'étudiant")
    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom", key="prenom")
    with col2:
        nom = st.text_input("Nom", key="nom")
    st.text_input("Adresse e-mail", value=email, disabled=True)
    
    st.sidebar.markdown(f"**🟢 Étudiant connecté :**\n*{email}*")
    st.divider()
    
    # --- PART 1 ---
    st.header("Partie 1 : Fondations des données et Échantillonnage (S5) - 10 mins")
    
    q1_options = ["Données Administratives", "Données d'Enquête", "Données de Trace"]
    np.random.shuffle(q1_options)
    
    st.subheader("Question 1 (3 pts : 1 pt/proposition)")
    st.markdown("Associez les situations suivantes à leur type de source de données correct :")
    q1_a = st.radio("A. Les registres d'état civil recensant les naissances et les décès dans une commune.", options=["Sélectionner..."] + q1_options, key="q1_a")
    q1_b = st.radio("B. Les réponses à un sondage sur les intentions de vote aux prochaines élections.", options=["Sélectionner..."] + q1_options, key="q1_b")
    q1_c = st.radio("C. Les coordonnées GPS collectées par une application mobile pour suivre les déplacements.", options=["Sélectionner..."] + q1_options, key="q1_c")

    st.subheader("Question 2 (2 pts)")
    
    q2_opts = [
        "Échantillonnage aléatoire simple sur la liste totale", 
        "Échantillonnage de convenance à la sortie du restaurant", 
        "Échantillonnage stratifié en fonction du cycle d'études", 
        "Pas d'échantionnage, interroger tous les étudiants"
    ]
    np.random.shuffle(q2_opts)
    
    q2 = st.radio(
        "Une université souhaite interroger 500 de ses 10 000 étudiants sur la qualité des repas. Sachant que le budget, le temps disponible et les habitudes alimentaires varient fortement selon le cycle d'études (Licence, Master, Doctorat), quelle méthode d'échantillonnage garantira la meilleure représentativité avec un coût maîtrisé ?",
        options=["Sélectionner..."] + q2_opts,
        key="q2"
    )
    
    st.divider()

    # --- PART 2 ---
    st.header("Partie 2 : Statistiques Descriptives Univariées (S3) - 10 mins")
    
    st.markdown(f"Considérez la série de données suivante représentant l'âge de 6 personnes interrogées lors d'une enquête sociologique : `{dataset_q4}`")
    
    st.subheader("Question 3 (2 pts : 1 pt/mesure)")
    col_q3_1, col_q3_2 = st.columns(2)
    with col_q3_1:
        q3_median = st.number_input("Calculez la Médiane", value=0.0, step=0.5, format="%.2f", key="q3_median")
    with col_q3_2:
        q3_mean = st.number_input("Calculez la Moyenne Simple", value=0.0, step=0.5, format="%.2f", key="q3_mean")
        
    st.subheader("Question 4 (4 pts : 2 pts/mesure)")
    col_q4_1, col_q4_2 = st.columns(2)
    with col_q4_1:
        q4_variance = st.number_input("Calculez la Variance (considérez qu'il s'agit d'une population entière, c-a-d Sn)", value=0.0, step=0.1, format="%.2f", key="q4_variance")
    with col_q4_2:
        q4_std = st.number_input("Calculez l'Écart-type (Standard Deviation)", value=0.0, step=0.1, format="%.2f", key="q4_std")
    
    st.divider()

    # --- PART 3 ---
    st.header("Partie 3 : Analyse Bivariée (S4) - 10 mins")
    
    st.markdown(f"""
    Vous analysez l'impact du secteur d'activité sur la rémunération. Vous disposez du tableau suivant présentant des salaires mensuels :
    | Secteur d'activité | Salaire (€) |
    | :--- | :--- |
    | Public | {salaries_public[0]} |
    | Public | {salaries_public[1]} |
    | Public | {salaries_public[2]} |
    | Privé | {salaries_prive[0]} |
    | Privé | {salaries_prive[1]} |
    | Privé | {salaries_prive[2]} |
    | Privé | {salaries_prive[3]} |
    """)
    
    st.subheader("Question 5a (2 pts : 1 pt/secteur)")
    col_q5_1, col_q5_2 = st.columns(2)
    with col_q5_1:
        q5_mean_public = st.number_input("Calculez le salaire moyen pour le Secteur Public", value=0.0, step=100.0, format="%.2f", key="q5_public")
    with col_q5_2:
        q5_mean_prive = st.number_input("Calculez le salaire moyen pour le Secteur Privé", value=0.0, step=100.0, format="%.2f", key="q5_prive")
    
    st.subheader("Question 5b - Interprétation (2 pts)")
    q5b_opts = [
        "Le secteur d'activité détermine de manière certaine et causale le salaire des individus de la population globale.",
        "Le secteur d'activité n'a strictement aucune influence sur le salaire.",
        "On observe une différence de moyenne dans l'échantillon, suggérant un lien, mais des moyennes seules ne suffisent pas pour prouver l'influence au niveau d'une population (il faudrait des tests inférentiels)."
    ]
    np.random.shuffle(q5b_opts)
    q5b = st.radio(
        "Au vu des moyennes conditionnelles, que peut-on affirmer provisoirement concernant le salaire et le secteur d'activité ?",
        options=["Sélectionner..."] + q5b_opts,
        key="q5b"
    )

    st.subheader("Question 6 (2 pts)")
    q6_opts = [
        "Plus le taux de pauvreté est élevé, plus l'espérance de vie tend à augmenter.",
        "Plus le taux de pauvreté est élevé, plus l'espérance de vie tend à diminuer.",
        "Le taux de pauvreté n'a aucune influence linéaire sur l'espérance de vie.",
        "C'est impossible, une covariance ne peut pas être négative."
    ]
    np.random.shuffle(q6_opts)
    q6 = st.radio(
        "Si la covariance entre le taux de pauvreté (variable X) et l'espérance de vie (variable Y) d'une région est fortement négative, qu'est-ce que cela indique ?",
        options=["Sélectionner..."] + q6_opts,
        key="q6"
    )

    st.subheader("Question 7 (1.5 pts)")
    q7_opts = [
        "La somme des (X - moyenne(X))² divisée par le nombre d'observations",
        "La moyenne des produits croisés : somme des ((X - moyenne(X)) * (Y - moyenne(Y))) divisée par le nombre d'observations",
        "La somme des produits des moyennes de X et de Y",
        "Le produit de l'écart-type de X par l'écart-type de Y"
    ]
    np.random.shuffle(q7_opts)
    q7 = st.radio(
        "Quelle est la formule correcte pour calculer manuellement la covariance entre deux variables X et Y ?",
        options=["Sélectionner..."] + q7_opts,
        key="q7"
    )

    st.subheader("Question 8 (1.5 pts)")
    q8_opts = [
        "=COVAR.P() (ou =COVARIANCE.PE())", 
        "=COVAR.S() (ou =COVARIANCE.STANDARD())", 
        "=CORREL()", 
        "=ECARTYPE.PE()"
    ]
    np.random.shuffle(q8_opts)
    q8 = st.radio(
        "Quelle est la formule Excel qui calcule la covariance d'une population (et non d'un échantillon) ?",
        options=["Sélectionner..."] + q8_opts,
        key="q8"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    submitted = st.form_submit_button("S'assurer d'avoir tout rempli, puis Soumettre ! 🚀", use_container_width=True)

    if submitted:
        # 1. Validation de base
        missing_fields = []
        if not prenom or not nom or not email:
            missing_fields.append("Informations de l'étudiant (Nom, Prénom, Email)")
        if q1_a == "Sélectionner..." or q1_b == "Sélectionner..." or q1_c == "Sélectionner...":
            missing_fields.append("Question 1")
        if q2 == "Sélectionner...": missing_fields.append("Question 2")
        if q3_median == 0.0 or q3_mean == 0.0: missing_fields.append("Question 3 (Valeur nulle non acceptée)")
        if q4_variance == 0.0 or q4_std == 0.0: missing_fields.append("Question 4 (Valeur nulle non acceptée)")
        if q5_mean_public == 0.0 or q5_mean_prive == 0.0: missing_fields.append("Question 5a (Valeur nulle non acceptée)")
        if q5b == "Sélectionner...": missing_fields.append("Question 5b")
        if q6 == "Sélectionner...": missing_fields.append("Question 6")
        if q7 == "Sélectionner...": missing_fields.append("Question 7")
        if q8 == "Sélectionner...": missing_fields.append("Question 8")
        
        # Pour les inputs numériques, la valeur 0.0 par défaut complique la validation de "rempli/pas rempli",
        # mais on laisse passer car 0 pourrait théoriquement être une réponse tapée.
        
        if missing_fields:
            st.error(f"Veuillez remplir les champs suivants avant de soumettre : {', '.join(missing_fields)}")
        else:
            with st.spinner("Enregistrement sécurisé de vos réponses..."):
                try:
                    # CALCULATE MISSING VARS
                    correct_q5_std = correct_q5_var ** 0.5
                    
                    # SCORING LOGIC
                    score = 0
                    max_score = 20 # Total points (adjusted)
                    
                    # Store booleans for HTML color formatting
                    q1a_ok = q1_a == "Données Administratives"
                    q1b_ok = q1_b == "Données d'Enquête"
                    q1c_ok = q1_c == "Données de Trace"
                    q2_ok = q2 == "Échantillonnage stratifié en fonction du cycle d'études"
                    q3_med_ok = abs(q3_median - correct_q4_med) < 0.01
                    q3_mean_ok = abs(q3_mean - correct_q4_mean) < 0.01
                    q4_var_ok = abs(q4_variance - correct_q5_var) < 0.1
                    q4_std_ok = abs(q4_std - correct_q5_std) < 0.1
                    q5_public_ok = abs(q5_mean_public - correct_q5_mean_public) < 0.01
                    q5_prive_ok = abs(q5_mean_prive - correct_q5_mean_prive) < 0.01
                    q5b_ok = q5b.startswith("On observe une différence de moyenne")
                    q6_ok = q6 == "Plus le taux de pauvreté est élevé, plus l'espérance de vie tend à diminuer."
                    q7_ok = q7.startswith("La moyenne des produits croisés")
                    q8_ok = q8.startswith("=COVAR.P")
                    
                    # Tally Score out of 20
                    if q1a_ok: score += 1
                    if q1b_ok: score += 1
                    if q1c_ok: score += 1
                    if q2_ok: score += 2
                    if q3_med_ok: score += 1
                    if q3_mean_ok: score += 1
                    if q4_var_ok: score += 2
                    if q4_std_ok: score += 2
                    if q5_public_ok: score += 1
                    if q5_prive_ok: score += 1
                    if q5b_ok: score += 2
                    if q6_ok: score += 2
                    if q7_ok: score += 1.5
                    if q8_ok: score += 1.5
                    

                    # Google Sheets Save
                    sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
                    spreadsheet = client.open_by_url(sheet_url)
                    worksheet = spreadsheet.sheet1
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Format randomized data as strings
                    dataset_q4_str = str(dataset_q4)
                    salaries_public_str = str(salaries_public)
                    salaries_prive_str = str(salaries_prive)
                    
                    ip_address = get_client_ip()
                    
                    # Helper for HTML formatting
                    def fmt_ans(ans, is_correct):
                        cls = "ans-right" if is_correct else "ans-wrong"
                        return f'<span class="{cls}">{ans}</span>'
                    
                    # Generate HTML response summary for Download
                    html_content = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                            .correct {{ color: green; font-weight: bold; }}
                            .incorrect {{ color: red; font-weight: bold; text-decoration: line-through; }}
                            .correction {{ color: blue; font-weight: bold; margin-left: 10px; }}
                            h3 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
                            p {{ margin-bottom: 15px; background: #f9f9f9; padding: 10px; border-radius: 5px; }}
                        </style>
                    </head>
                    <body>
                        <h2>Receipt de Soumission : {prenom} {nom}</h2>
                        <h3>Partie 1 : Fondations des données et Échantillonnage</h3>
                        <p><strong>[Q1] Associez les situations suivantes à leur type de source de données correct ({sum([1 if q1a_ok else 0, 1 if q1b_ok else 0, 1 if q1c_ok else 0])}/3):</strong><br>
                        - <em>Les registres d'état civil :</em> {fmt_ans(q1_a, q1a_ok)} <br>Correction : <span class="correction">Données Administratives</span><br>
                        - <em>Les réponses à un sondage :</em> {fmt_ans(q1_b, q1b_ok)} <br>Correction : <span class="correction">Données d'Enquête</span><br>
                        - <em>Les coordonnées GPS mobiles :</em> {fmt_ans(q1_c, q1c_ok)} <br>Correction : <span class="correction">Données de Trace</span></p>
                        
                        <p><strong>[Q2] Échantillonnage représentatif pour enquête universitaire à coûts maîtrisés ({"2/2" if q2_ok else "0/2"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q2, q2_ok)} <br>Correction : <span class="correction">Échantillonnage stratifié en fonction du cycle d'études</span></p>

                        <h3>Partie 2 : Statistiques Descriptives Univariées</h3>
                        <p><strong>Dataset (âges) :</strong> <code>{dataset_q4_str}</code></p>
                        
                        <p><strong>[Q3] Calculez la Médiane ({"1/1" if q3_med_ok else "0/1"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q3_median, q3_med_ok)} <br>Correction : <span class="correction">{correct_q4_med}</span></p>
                        
                        <p><strong>Calculez la Moyenne Simple (entière) ({"1/1" if q3_mean_ok else "0/1"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q3_mean, q3_mean_ok)} <br>Correction : <span class="correction">{correct_q4_mean}</span></p>
                        
                        <p><strong>[Q4] Calculez la Variance ({"2/2" if q4_var_ok else "0/2"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q4_variance, q4_var_ok)} <br>Correction : <span class="correction">~{correct_q5_var:.2f}</span></p>
                        
                        <p><strong>Calculez l'Écart-type ({"2/2" if q4_std_ok else "0/2"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q4_std, q4_std_ok)} <br>Correction : <span class="correction">~{correct_q5_std:.2f}</span></p>

                        <h3>Partie 3 : Analyse Bivariée</h3>
                        <p><strong>Salaires Secteur Public :</strong> <code>{salaries_public_str}</code> | <strong>Secteur Privé :</strong> <code>{salaries_prive_str}</code></p>
                        
                        <p><strong>[Q5a] Moyenne Secteur Public ({"1/1" if q5_public_ok else "0/1"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q5_mean_public, q5_public_ok)} <br>Correction : <span class="correction">{correct_q5_mean_public:.2f}</span></p>

                        <p><strong>[Q5a] Moyenne Secteur Privé ({"1/1" if q5_prive_ok else "0/1"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q5_mean_prive, q5_prive_ok)} <br>Correction : <span class="correction">{correct_q5_mean_prive:.2f}</span></p>
                        
                        <p><strong>[Q5b] Interprétation (Influence du secteur sur salaire) ({"2/2" if q5b_ok else "0/2"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q5b, q5b_ok)} <br>Correction : <span class="correction">On observe une différence de moyenne dans l'échantillon, suggérant un lien, mais des moyennes seules ne suffisent pas pour prouver l'influence au niveau d'une population (il faudrait des tests inférentiels).</span></p>
                        
                        <p><strong>[Q6] Covariance fortement négative (pauvreté vs espérance de vie) ({"2/2" if q6_ok else "0/2"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q6, q6_ok)} <br>Correction : <span class="correction">Plus le taux de pauvreté est élevé, plus l'espérance de vie tend à diminuer.</span></p>
                        
                        <p><strong>[Q7] Formule manuelle Covariance ({"1.5/1.5" if q7_ok else "0/1.5"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q7, q7_ok)} <br>Correction : <span class="correction">La moyenne des produits croisés...</span></p>
                        
                        <p><strong>[Q8] Formule Excel Covariance (Population) ({"1.5/1.5" if q8_ok else "0/1.5"}) :</strong><br> 
                        Réponse de l'étudiant : {fmt_ans(q8, q8_ok)} <br>Correction : <span class="correction">=COVAR.P() (ou =COVARIANCE.PE())</span></p>
                        
                    </body>
                    </html>
                    """
                    
                    # Minify the HTML significantly so it fits cleanly into a single Google Sheets cell without massive row height
                    minified_html = html_content.replace('\n', '').replace('    ', ' ')
                    
                    # row format: Timestamp, Prenom, Nom, Email, IP_Address, Score, Dataset_Q4, Dataset_Q5_Public, Dataset_Q5_Prive, Q1a, Q1b, Q1c, Q2, Q3_med, Q3_mean, Q4_var, Q4_std, Q5_Public, Q5_Prive, Q5b, Q6, Q7, Q8, HTML
                    row_data = [
                        timestamp, prenom, nom, email, ip_address, f"{score}/{max_score}",
                        dataset_q4_str, salaries_public_str, salaries_prive_str, # Store the specific random questions
                        q1_a, q1_b, q1_c, q2,
                        float(q3_median), float(q3_mean), float(q4_variance), float(q4_std), float(q5_mean_public), float(q5_mean_prive),
                        q5b, q6, q7, q8, minified_html
                    ]
                    
                    worksheet.append_row(row_data)
                    
                    st.session_state['quiz_submitted'] = True
                    st.session_state['success_msg'] = "✅ Vos réponses ont été bien enregistrées. Vous pouvez maintenant fermer cette page."
                    
                except Exception as e:
                    st.error(f"Une erreur s'est produite lors de l'enregistrement. Détails pour le professeur: {e}")

if st.session_state.get('quiz_submitted', False):
    st.success(st.session_state.get('success_msg', '✅ Enregistré !'))
    st.info("Vos réponses et votre énoncé unique ont bien été enregistrés sur le serveur. Vous pouvez fermer cette page.")
