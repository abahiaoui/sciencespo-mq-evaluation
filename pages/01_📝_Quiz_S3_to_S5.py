import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime
import pandas as pd
import numpy as np

st.set_page_config(page_title="Quiz S3 à S5", page_icon="📝", layout="wide")

st.title("📝 Évaluation : Séances 3 à 5")
st.markdown("""
**Durée estimée : 30 minutes**

Veuillez répondre à toutes les questions avant de soumettre. Une fois soumis, vos réponses seront enregistrées définitivement.
""")

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
import json

# Define the scopes required
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# We need to load client secrets for OAuth2 from Streamlit secrets or a file
# For local ease, we'll assume the user has placed 'client_secret.json' in the repo root,
# or we can read it from st.secrets if configured.
CLIENT_SECRETS_FILE = "client_secret.json"

st.sidebar.header("🔐 Authentification Professeur")
credentials = None

if os.path.exists("token.json"):
    try:
        with open("token.json", "r") as token_file:
            token_data = json.load(token_file)
            credentials = Credentials.from_authorized_user_info(token_data, SCOPES)
    except Exception as e:
        st.sidebar.error(f"Erreur de lecture du token : {e}")

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            # Save the refreshed credentials
            with open("token.json", "w") as token_file:
                token_file.write(credentials.to_json())
        except Exception as e:
            st.sidebar.warning("Le token a expiré et n'a pas pu être rafraîchi. Veuillez vous reconnecter.")
            credentials = None
    
    if not credentials:
        st.sidebar.warning("L'application doit être autorisée avec votre compte Google personnel pour uploader les fichiers sur votre Drive.")
        if not os.path.exists(CLIENT_SECRETS_FILE):
             st.sidebar.error(f"⚠️ Fichier `{CLIENT_SECRETS_FILE}` introuvable ! Vous devez télécharger vos identifiants OAuth depuis Google Cloud Console et les placer à la racine du projet.")
        else:
             flow = Flow.from_client_secrets_file(
                 CLIENT_SECRETS_FILE,
                 scopes=SCOPES,
                 redirect_uri='urn:ietf:wg:oauth:2.0:oob' # Desktop flow out-of-band
             )
             
             auth_url, _ = flow.authorization_url(prompt='consent')
             st.sidebar.markdown(f"[Cliquez ici pour autoriser l'application]({auth_url})")
             
             auth_code = st.sidebar.text_input("Collez le code d'autorisation ici :")
             if st.sidebar.button("Valider le code"):
                 try:
                     flow.fetch_token(code=auth_code)
                     credentials = flow.credentials
                     # Save the credentials for the next run
                     with open("token.json", "w") as token_file:
                         token_file.write(credentials.to_json())
                     st.sidebar.success("✅ Authentification réussie ! L'application est prête.")
                     st.rerun()
                 except Exception as e:
                     st.sidebar.error(f"Échec de l'authentification : {e}")

if not credentials or not credentials.valid:
    st.info("⚠️ En attente de l'authentification du professeur. Les étudiants ne peuvent pas encore soumettre.")
    st.stop()

# If we get here, credentials are valid!
try:
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

with st.form("quiz_form"):
    st.header("Informations de l'étudiant")
    col1, col2 = st.columns(2)
    with col1:
        prenom = st.text_input("Prénom", key="prenom")
    with col2:
        nom = st.text_input("Nom", key="nom")
    email = st.text_input("Adresse e-mail (Sciences Po)", key="email")
    
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
    
    st.markdown("Considérez la série de données suivante représentant le temps (en minutes) passé par 6 étudiants à résoudre un problème : `[12, 15, 15, 18, 22, 26]`")
    
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
    
    st.markdown("""
    Vous disposez du tableau suivant présentant des salaires selon la catégorie :
    | Catégorie | Salaire (€) |
    | :--- | :--- |
    | A | 2000 |
    | A | 2200 |
    | B | 3000 |
    | B | 3500 |
    | B | 4000 |
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
                    
                    # Q3 (1.5 pts) -> La variance échantillon Sn-1 divise par n-1, donc elle est mathématiquement PLUS GRANDE que la variance population Sn (qui divise par n). Donc l'énoncé est Faux.
                    if q3 == "Faux": score += 1.5
                    
                    # Q4 (1 pt chaque)
                    # Median of 12, 15, 15, 18, 22, 26 is (15+18)/2 = 16.5
                    if abs(q4_median - 16.5) < 0.01: score += 1
                    # Mean is (12+15+15+18+22+26)/6 = 108/6 = 18.0
                    if abs(q4_mean - 18.0) < 0.01: score += 1
                    
                    # Q5 (1 pt)
                    # pop variance of [12, 15, 15, 18, 22, 26]. Mean=18. 
                    # ssq = (12-18)^2 + 2*(15-18)^2 + (18-18)^2 + (22-18)^2 + (26-18)^2
                    # ssq = 36 + 2*9 + 0 + 16 + 64 = 134
                    # var = 134 / 6 = 22.3333...
                    if abs(q5_variance - 22.33) < 0.1: score += 1
                    
                    # Q6 (1 pt)
                    # Mean B = (3000+3500+4000)/3 = 3500
                    if abs(q6_mean_catB - 3500.0) < 0.01: score += 1
                    
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
                    
                    # row format: Timestamp, Prenom, Nom, Email, Q1a, Q1b, Q1c, Q2, Q3, Q4_med, Q4_mean, Q5, Q6, Q7, Q8, Q9, Score
                    row_data = [
                        timestamp, prenom, nom, email,
                        q1_a, q1_b, q1_c, q2, q3,
                        float(q4_median), float(q4_mean), float(q5_variance), float(q6_mean_catB),
                        q7, q8, q9, f"{score}/{max_score}"
                    ]
                    
                    worksheet.append_row(row_data)
                    
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
                        <p><strong>Médiane de [12, 15, 15, 18, 22, 26] :</strong> Vous avez répondu <span class="student-ans">{q4_median}</span>. Correction : <span class="correct">16.5</span> (Moyenne des deux valeurs centrales 15 et 18)</p>
                        <p><strong>Moyenne de [12, 15, 15, 18, 22, 26] :</strong> Vous avez répondu <span class="student-ans">{q4_mean}</span>. Correction : <span class="correct">18.0</span></p>
                        <p><strong>Variance de la population :</strong> Vous avez répondu <span class="student-ans">{q5_variance}</span>. Correction : <span class="correct">~22.33</span> (134 / 6)</p>

                        <h3>Partie 3</h3>
                        <p><strong>Moyenne Catégorie B :</strong> Vous avez répondu <span class="student-ans">{q6_mean_catB}</span>. Correction : <span class="correct">3500.0</span></p>
                        <p><strong>Covariance Négative :</strong> Vous avez répondu <span class="student-ans">{q7}</span>. Correction : <span class="correct">Plus un étudiant révise, plus sa note tend à diminuer.</span></p>
                        <p><strong>Formule manuelle Covariance :</strong> Vous avez répondu <span class="student-ans">{q8}</span>. Correction : <span class="correct">La moyenne des produits croisés...</span></p>
                        <p><strong>Formule Excel Covariance (Population) :</strong> Vous avez répondu <span class="student-ans">{q9}</span>. Correction : <span class="correct">=COVAR.P() (ou =COVARIANCE.PE())</span></p>
                        
                    </body>
                    </html>
                    """
                    
                    b64_html = html_content.encode('utf-8')
                    st.session_state['quiz_submitted'] = True
                    st.session_state['download_data'] = b64_html
                    st.session_state['download_filename'] = f"Correction_{nom}_{prenom}.html"
                    st.session_state['success_msg'] = f"✅ Ouf ! Vos réponses ont été bien enregistrées. Note : {score}/{max_score}"
                    
                    # Upload the html_content directly to Google Drive
                    from io import BytesIO
                    import io
                    
                    # Ensure Drive API access is established
                    drive_service = build('drive', 'v3', credentials=credentials)
                    
                    file_metadata = {
                        'name': f"Correction_{nom}_{prenom}_{timestamp}.html",
                        'parents': ['1JR9EPNbOKyQ4F8WEoJ-G97I2Y1WKj4G0'] # target folder provided by user
                    }
                    
                    # Upload in-memory bytes
                    fh = io.BytesIO(b64_html)
                    media = MediaIoBaseUpload(fh, mimetype='text/html', resumable=True)
                    
                    try:
                        file = drive_service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True
                        ).execute()
                        st.session_state['drive_msg'] = f"Une copie a également été enregistrée automatiquement de manière sécurisée (ID: {file.get('id')})."
                    except Exception as e:
                        if "storageQuotaExceeded" in str(e):
                            st.session_state['drive_msg'] = "⚠️ Le fichier HTML n'a pas pu être uploadé sur Google Drive car le Service Account n'a pas de quota de stockage. Solution : Pensez à convertir ce dossier en \"Drive Partagé\" (Shared Drive) dans vos paramètres Workspace."
                        else:
                            raise e

                except Exception as e:
                    st.error(f"Une erreur s'est produite lors de l'enregistrement. Détails pour le professeur: {e}")

if st.session_state.get('quiz_submitted', False):
    st.success(st.session_state.get('success_msg', '✅ Enregistré !'))
    if 'drive_msg' in st.session_state:
        st.info(st.session_state['drive_msg'])
    st.download_button(
        label="📄 Télécharger votre copie et la correction",
        data=st.session_state.get('download_data', b''),
        file_name=st.session_state.get('download_filename', 'correction.html'),
        mime="text/html",
        type="primary"
    )
