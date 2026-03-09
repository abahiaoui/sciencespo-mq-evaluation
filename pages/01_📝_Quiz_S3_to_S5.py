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

# Generate Random Variables for Q6 (Categories B and A)
# Let's generate a 5-row table
salaries_A = [int(x) for x in np.random.randint(1500, 2500, size=2)]
salaries_B = [int(x) for x in np.random.randint(2800, 4500, size=3)]

# Calculate correct answer for Q6
correct_q6_mean_catB = sum(salaries_B) / len(salaries_B)

with st.form("quiz_form"):
    st.header("Informations de l'étudiant")
    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom", key="prenom")
    with col2:
        nom = st.text_input("Nom", key="nom")
    st.text_input("Adresse e-mail", value=email, disabled=True)
    
    st.divider()
    
    # --- PART 1 ---
    st.header("Partie 1 : Fondations des données et Échantillonnage (S5) - 10 mins")
    
    q1_options = ["Nominale", "Ordinale", "Intervalle", "Ratio"]
    st.subheader("Question 1")
    st.markdown("Associez les variables suivantes à leur type de donnée correct :")
    q1_a = st.selectbox("A. La température en degrés Celsius", options=["Sélectionner..."] + q1_options, key="q1_a")
    q1_b = st.selectbox("B. Le niveau d'études (Licence, Master, Doctorat)", options=["Sélectionner..."] + q1_options, key="q1_b")
    q1_c = st.selectbox("C. Le salaire mensuel en euros", options=["Sélectionner..."] + q1_options, key="q1_c")

    st.subheader("Question 2")
    q2 = st.radio(
        "Un chercheur sélectionne les participants de son étude en choisissant une personne sur 5 dans une liste alphabétique. Quel type d'échantillonnage utilise-t-il ?",
        options=["Sélectionner...", "Échantillonnage aléatoire simple", "Échantillonnage systématique", "Échantillonnage stratifié", "Échantillonnage en grappes"],
        key="q2"
    )

    st.subheader("Question 3")
    q3 = st.radio(
        "Vrai ou Faux : La variance d'un échantillon (Sn-1) sera toujours mathématiquement plus petite que la variance de la population totale (Sn) calculée sur le même jeu de données exact.",
        options=["Sélectionner...", "Vrai", "Faux"],
        key="q3"
    )
    
    st.divider()

    # --- PART 2 ---
    st.header("Partie 2 : Statistiques Descriptives Univariées (S3) - 10 mins")
    
    st.markdown(f"Considérez la série de données suivante représentant le temps (en minutes) passé par 6 étudiants à résoudre un problème : `{dataset_q4}`")
    
    st.subheader("Question 4")
    col_q4_1, col_q4_2 = st.columns(2)
    with col_q4_1:
        q4_median = st.number_input("Calculez la Médiane", value=0.0, step=0.5, format="%.2f", key="q4_median")
    with col_q4_2:
        q4_mean = st.number_input("Calculez la Moyenne Simple", value=0.0, step=0.5, format="%.2f", key="q4_mean")
        
    st.subheader("Question 5")
    q5_variance = st.number_input("Calculez la Variance (considérez qu'il s'agit d'une population entière, c-a-d Sn)", value=0.0, step=0.1, format="%.2f", key="q5_variance")
    
    st.divider()

    # --- PART 3 ---
    st.header("Partie 3 : Analyse Bivariée (S4) - 10 mins")
    
    st.markdown(f"""
    Vous disposez du tableau suivant présentant des salaires selon la catégorie :
    | Catégorie | Salaire (€) |
    | :--- | :--- |
    | A | {salaries_A[0]} |
    | A | {salaries_A[1]} |
    | B | {salaries_B[0]} |
    | B | {salaries_B[1]} |
    | B | {salaries_B[2]} |
    """)
    
    st.subheader("Question 6")
    q6_mean_catB = st.number_input("Calculez le salaire moyen conditionnel pour la catégorie B", value=0.0, step=100.0, format="%.2f", key="q6")
    
    st.subheader("Question 7")
    q7 = st.radio(
        "Si la covariance entre la variable X (heures de révision) et la variable Y (note à l'examen) est fortement négative, qu'est-ce que cela indique ?",
        options=[
            "Sélectionner...",
            "Plus un étudiant révise, plus sa note tend à augmenter.",
            "Plus un étudiant révise, plus sa note tend à diminuer.",
            "Le temps de révision n'a aucune influence linéaire sur la note.",
            "C'est impossible, une covariance ne peut pas être négative."
        ],
        key="q7"
    )

    st.subheader("Question 8")
    q8 = st.radio(
        "Quelle est la formule correcte pour calculer manuellement la covariance entre deux variables X et Y ?",
        options=[
            "Sélectionner...",
            "La somme des (X - moyenne(X))² divisée par le nombre d'observations",
            "La moyenne des produits croisés : somme des ((X - moyenne(X)) * (Y - moyenne(Y))) divisée par le nombre d'observations",
            "La somme des produits des moyennes de X et de Y",
            "Le produit de l'écart-type de X par l'écart-type de Y"
        ],
        key="q8"
    )

    st.subheader("Question 9")
    q9 = st.radio(
        "Quelle est la formule Excel qui calcule la covariance d'une population (et non d'un échantillon) ?",
        options=["Sélectionner...", "=COVAR.P() (ou =COVARIANCE.PE())", "=COVAR.S() (ou =COVARIANCE.STANDARD())", "=CORREL()", "=ECARTYPE.PE()"],
        key="q9"
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
        if q3 == "Sélectionner...": missing_fields.append("Question 3")
        if q7 == "Sélectionner...": missing_fields.append("Question 7")
        if q8 == "Sélectionner...": missing_fields.append("Question 8")
        if q9 == "Sélectionner...": missing_fields.append("Question 9")
        
        # Pour les inputs numériques, la valeur 0.0 par défaut complique la validation de "rempli/pas rempli",
        # mais on laisse passer car 0 pourrait théoriquement être une réponse tapée.
        
        if missing_fields:
            st.error(f"Veuillez remplir les champs suivants avant de soumettre : {', '.join(missing_fields)}")
        else:
            with st.spinner("Enregistrement sécurisé de vos réponses..."):
                try:
                    # SCORING LOGIC
                    score = 0
                    max_score = 11 # Total points
                    
                    # Q1 (1 pt par sous-question)
                    if q1_a == "Intervalle": score += 1
                    if q1_b == "Ordinale": score += 1
                    if q1_c == "Ratio": score += 1
                    
                    # Q2 (1.5 pts)
                    if q2 == "Échantillonnage systématique": score += 1.5
                    
                    # Q3 (1.5 pts)
                    if q3 == "Faux": score += 1.5
                    
                    # Q4 (1 pt chaque)
                    if abs(q4_median - correct_q4_med) < 0.01: score += 1
                    if abs(q4_mean - correct_q4_mean) < 0.01: score += 1
                    
                    # Q5 (1 pt)
                    if abs(q5_variance - correct_q5_var) < 0.1: score += 1
                    
                    # Q6 (1 pt)
                    if abs(q6_mean_catB - correct_q6_mean_catB) < 0.01: score += 1
                    
                    # Q7 (1 pt)
                    if q7 == "Plus un étudiant révise, plus sa note tend à diminuer.": score += 1
                    
                    # Q8 (0.5 pt)
                    if q8.startswith("La moyenne des produits croisés"): score += 0.5
                    
                    # Q9 (0.5 pt)
                    if q9.startswith("=COVAR.P"): score += 0.5
                    

                    # Google Sheets Save
                    sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
                    spreadsheet = client.open_by_url(sheet_url)
                    worksheet = spreadsheet.sheet1
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Format randomized data as strings
                    dataset_q4_str = str(dataset_q4)
                    salaries_B_str = str(salaries_B)
                    
                    ip_address = get_client_ip()
                    
                    # Generate HTML response summary for Download
                    html_content = f"""
                    <html>
                    <head><meta charset="UTF-8"><style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                        h1, h2 {{ color: #2c3e50; }}
                        .correct {{ color: green; font-weight: bold; }}
                        .student-ans {{ color: #34495e; font-style: italic; }}
                        .score {{ font-size: 1.2em; font-weight: bold; border: 2px solid #3498db; padding: 10px; display: inline-block; }}
                    </style></head>
                    <body>
                        <h1>Reçu de soumission - Évaluation de Méthodes Quantitatives</h1>
                        <p><strong>Étudiant(e) :</strong> {prenom} {nom} ({email})</p>
                        <p><strong>Date de soumission :</strong> {timestamp}</p>
                        <div class="score">Score Final : {score} / {max_score}</div>
                        
                        <h2>Récapitulatif et Correction</h2>
                        
                        <h3>Partie 1</h3>
                        <p><strong>Type de données :</strong><br>
                        Température : Vous avez répondu <span class="student-ans">{q1_a}</span>. Correction : <span class="correct">Intervalle</span><br>
                        Niveau d'études : Vous avez répondu <span class="student-ans">{q1_b}</span>. Correction : <span class="correct">Ordinale</span><br>
                        Salaire : Vous avez répondu <span class="student-ans">{q1_c}</span>. Correction : <span class="correct">Ratio</span></p>
                        
                        <p><strong>Échantillonnage (1 par 5) :</strong> Vous avez répondu <span class="student-ans">{q2}</span>. Correction : <span class="correct">Échantillonnage systématique</span></p>
                        <p><strong>Variance échantillon vs population :</strong> Vous avez répondu <span class="student-ans">{q3}</span>. Correction : <span class="correct">Faux</span> (Sn-1 divise par n-1, donc le résultat est plus grand que Sn qui divise par n)</p>

                        <h3>Partie 2</h3>
                        <p>Dataset de l'étudiant : {dataset_q4_str}</p>
                        <p><strong>Médiane :</strong> Vous avez répondu <span class="student-ans">{q4_median}</span>. Correction : <span class="correct">{correct_q4_med}</span></p>
                        <p><strong>Moyenne :</strong> Vous avez répondu <span class="student-ans">{q4_mean}</span>. Correction : <span class="correct">{correct_q4_mean}</span></p>
                        <p><strong>Variance de la population :</strong> Vous avez répondu <span class="student-ans">{q5_variance}</span>. Correction : <span class="correct">~{correct_q5_var:.2f}</span></p>

                        <h3>Partie 3</h3>
                        <p>Salaires Catégorie A : {str(salaries_A)} | Salaires Catégorie B : {salaries_B_str}</p>
                        <p><strong>Moyenne Catégorie B :</strong> Vous avez répondu <span class="student-ans">{q6_mean_catB}</span>. Correction : <span class="correct">{correct_q6_mean_catB:2f}</span></p>
                        <p><strong>Covariance Négative :</strong> Vous avez répondu <span class="student-ans">{q7}</span>. Correction : <span class="correct">Plus un étudiant révise, plus sa note tend à diminuer.</span></p>
                        <p><strong>Formule manuelle Covariance :</strong> Vous avez répondu <span class="student-ans">{q8}</span>. Correction : <span class="correct">La moyenne des produits croisés...</span></p>
                        <p><strong>Formule Excel Covariance (Population) :</strong> Vous avez répondu <span class="student-ans">{q9}</span>. Correction : <span class="correct">=COVAR.P() (ou =COVARIANCE.PE())</span></p>
                        
                    </body>
                    </html>
                    """
                    
                    # row format: Timestamp, Prenom, Nom, Email, IP_Address, Score, Dataset_Q4, Dataset_Q6_CatB, Q1a, Q1b, Q1c, Q2, Q3, Q4_med, Q4_mean, Q5, Q6, Q7, Q8, Q9, HTML
                    row_data = [
                        timestamp, prenom, nom, email, ip_address, f"{score}/{max_score}",
                        dataset_q4_str, salaries_B_str, # Store the specific random questions
                        q1_a, q1_b, q1_c, q2, q3,
                        float(q4_median), float(q4_mean), float(q5_variance), float(q6_mean_catB),
                        q7, q8, q9, html_content
                    ]
                    
                    worksheet.append_row(row_data)
                    
                    st.session_state['quiz_submitted'] = True
                    st.session_state['success_msg'] = "✅ Vos réponses ont été bien enregistrées. Vous pouvez maintenant fermer cette page."
                    
                except Exception as e:
                    st.error(f"Une erreur s'est produite lors de l'enregistrement. Détails pour le professeur: {e}")

if st.session_state.get('quiz_submitted', False):
    st.success(st.session_state.get('success_msg', '✅ Enregistré !'))
    st.info("Vos réponses et votre énoncé unique ont bien été enregistrés sur le serveur. Vous pouvez fermer cette page.")
