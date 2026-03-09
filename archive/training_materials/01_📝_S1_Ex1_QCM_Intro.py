import streamlit as st
import random

# HARMONIZATION: Use wide layout for consistency
st.set_page_config(page_title="S1 | Ex1 : Introduction", page_icon="📝", layout="wide")

st.title("📝 S1 | Ex. 1 : Introduction & Enjeux")

# NEW CONTEXT SECTION
with st.expander("📖 Contexte & Objectifs", expanded=True):
    st.markdown("""
    ### 🎯 Objectif
    Maîtriser les définitions et l'histoire de la quantification pour ne pas voir les chiffres comme de simples vérités mathématiques.

    ### 📖 Pourquoi ce quiz ?
    Comme vu en cours (*Slides Séance 1*), la statistique est **"la science de la collecte, description, analyse et interprétation"**. 
    
    Mais elle est aussi un outil de **pouvoir**. Du recensement antique (pour lever l'impôt) à l'arithmétique politique de William Petty, le chiffre ne se contente pas de décrire le monde : **il construit une réalité**. Ce quiz vérifie votre compréhension de ces enjeux critiques : biais, objectivité et argumentation.
    """)

st.markdown("---")
st.markdown("**Consigne :** Répondez à toutes les questions puis cliquez sur **Valider**.")

# --- CONFIGURATION DES LIENS ---
# Lien vers vos slides (Format PDF RAW)
BASE_URL_SLIDES = "https://raw.githubusercontent.com/abahiaoui/sciencespo-mq-training/main/slides/séance_1.pdf"

# --- GESTION DE L'ÉTAT ---
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False

if 'shuffled_questions' not in st.session_state:
    raw_questions = [
        {
            "question": "1. Comment le cours définit-il la statistique ?",
            "correct_text": "La science de la collecte, de la description, de l'analyse et de l'interprétation de données.",
            "options": [
                "L'art de manipuler des chiffres pour prouver une opinion personnelle.",
                "La science de la collecte, de la description, de l'analyse et de l'interprétation de données.",
                "Une branche des mathématiques uniquement dédiée au calcul de probabilités.",
                "Un outil informatique servant exclusivement à créer des graphiques."
            ],
            "explanation": "La statistique couvre tout le cycle de vie de la donnée : collecte, description, analyse et interprétation.",
            "slide_page": 63 
        },
        {
            "question": "2. Pourquoi la quantification est-elle considérée comme une 'construction' ?",
            "correct_text": "Parce que le processus crée une réalité qui reflète la volonté du producteur du chiffre.",
            "options": [
                "Parce que les chiffres sont des objets physiques que l'on assemble.",
                "Parce que le processus crée une réalité qui reflète la volonté du producteur du chiffre.",
                "Parce qu'il faut construire des ordinateurs puissants pour les calculer.",
                "Parce que les statistiques ne reposent sur aucune base réelle."
            ],
            "explanation": "Le processus de quantification crée une réalité qui reflète la volonté du producteur de la statistique.",
            "slide_page": 65
        },
        {
            "question": "3. Selon les 'Lamentations d'Ipou-our' (Égypte, 1750 av. J.-C.), que se passe-t-il quand les registres administratifs sont détruits ?",
            "correct_text": "Le grain devient un bien commun et l'ordre social s'effondre.",
            "options": [
                "L'armée prend le contrôle immédiat des récoltes pour éviter la famine.",
                "Le grain devient un bien commun et l'ordre social s'effondre.",
                "Les scribes sont condamnés à l'exil par le Pharaon.",
                "La population cesse de payer l'impôt mais continue de respecter les propriétés."
            ],
            "explanation": "Sans registres, 'le grain d'Égypte est un bien commun' et celui qui n'avait rien devient propriétaire, marquant l'effondrement de l'ordre.",
            "slide_page": 26
        },
        {
            "question": "4. Dans la Mésopotamie antique, quel était l'usage principal des tablettes d'argile ?",
            "correct_text": "Enregistrer la distribution de rations et le paiement d'impôts.",
            "options": [
                "Écrire des textes de loi pour les tribunaux.",
                "Enregistrer la distribution de rations et le paiement d'impôts.",
                "Cartographier les territoires conquis.",
                "Lister les généalogies des familles royales."
            ],
            "explanation": "Les tablettes servaient à comptabiliser la distribution de rations d'orge ou le paiement de l'impôt.",
            "slide_page": 24
        },
        {
            "question": "5. Que décrit le document rédigé par Auguste pour Tibère à Rome ?",
            "correct_text": "Les ressources de l'État, le nombre de citoyens en armes, les flottes et les impôts.",
            "options": [
                "Un traité de paix avec les peuples alliés.",
                "Les ressources de l'État, le nombre de citoyens en armes, les flottes et les impôts.",
                "Une liste de conseils philosophiques pour gouverner.",
                "Le calendrier des fêtes religieuses de l'Empire."
            ],
            "explanation": "Ce document détaillait les ressources de l'État, les citoyens sous les armes, les flottes et les impôts.",
            "slide_page": 27
        },
        {
            "question": "6. D'où vient étymologiquement le terme 'Statistique' (Statistik) ?",
            "correct_text": "De l'allemand, désignant la science de la description de l'État.",
            "options": [
                "Du latin 'Status', désignant simplement l'état des choses.",
                "De l'allemand, désignant la science de la description de l'État.",
                "Du grec 'Stater', une ancienne unité de mesure de poids.",
                "De l'anglais 'State-istics', l'art de gouverner."
            ],
            "explanation": "L'approche allemande (Statistik) se définissait comme la science de la description de l'État.",
            "slide_page": 41
        },
        {
            "question": "7. Quel contexte économique du XVIe siècle a favorisé le renouveau de la pensée quantitative ?",
            "correct_text": "L'arrivée des métaux précieux du Nouveau Monde et la rivalité entre les États européens.",
            "options": [
                "La découverte de l'imprimerie qui a facilité la diffusion des livres de comptes.",
                "L'arrivée des métaux précieux du Nouveau Monde et la rivalité entre les États européens.",
                "La fin de la guerre de Cent Ans qui a permis de lever de nouvelles armées.",
                "L'invention de la comptabilité en partie double par les Italiens."
            ],
            "explanation": "L'arrivée des métaux précieux et la compétition économique entre pays européens ont stimulé le besoin de mesures.",
            "slide_page": 34
        },
        {
            "question": "8. Qu'est-ce que l'Arithmétique Politique de William Petty (1676) ?",
            "correct_text": "Une méthode s'exprimant par le nombre, le poids ou la mesure plutôt que par des mots superlatifs.",
            "options": [
                "Un manuel de comptabilité pour les marchands de Londres.",
                "Une méthode s'exprimant par le nombre, le poids ou la mesure plutôt que par des mots superlatifs.",
                "Une théorie mathématique sur la probabilité de gagner aux jeux de hasard.",
                "Un dictionnaire de termes économiques."
            ],
            "explanation": "Petty a choisi de s'exprimer en termes de nombre, de poids ou de mesure plutôt qu'avec des mots comparatifs.",
            "slide_page": 36
        },
        {
            "question": "9. Quelle est la différence entre l'approche allemande et l'approche anglaise au XVIIe siècle ?",
            "correct_text": "L'allemande est descriptive (Statistik) tandis que l'anglaise est probabiliste (prédiction).",
            "options": [
                "L'allemande utilise Excel et l'anglaise utilise la calculatrice.",
                "L'allemande est descriptive (Statistik) tandis que l'anglaise est probabiliste (prédiction).",
                "L'allemande est centrée sur le commerce et l'anglaise sur la démographie.",
                "L'allemande est théorique alors que l'anglaise est purement administrative."
            ],
            "explanation": "L'école allemande est descriptive (description de l'État) tandis que l'anglaise est probabiliste et prédictive.",
            "slide_page": 43
        },
        {
            "question": "10. À quel moment la statistique peut-elle être 'biaisée' par le statisticien ?",
            "correct_text": "À toutes les étapes : collecte, description, analyse et interprétation.",
            "options": [
                "Uniquement lors de la collecte des données sur le terrain.",
                "Seulement lors de la création des graphiques finaux.",
                "À toutes les étapes : collecte, description, analyse et interprétation.",
                "Jamais, si le statisticien utilise des formules mathématiques officielles."
            ],
            "explanation": "Le biais peut survenir à la collecte, la description, l'analyse ou l'interprétation.",
            "slide_page": 58
        },
        {
            "question": "11. Quel exemple le cours utilise-t-il pour montrer qu'un chiffre peut créer deux réalités différentes ?",
            "correct_text": "Le choix entre présenter le nombre de chômeurs ou le taux de chômage.",
            "options": [
                "La comparaison entre les budgets de la France et de l'Angleterre.",
                "Le choix entre présenter le nombre de chômeurs ou le taux de chômage.",
                "L'utilisation de différentes couleurs sur une carte électorale.",
                "Le calcul de la moyenne plutôt que de la médiane pour les salaires."
            ],
            "explanation": "On peut présenter '2 millions de personnes sans emploi' ou 'un taux de chômage à son plus bas' pour décrire la même réalité.",
            "slide_page": 54
        },
        {
            "question": "12. Quel est le but ultime de ce cours de méthodes quantitatives ?",
            "correct_text": "Comprendre l'idée transmise par les chiffres et identifier les points forts/faibles de l'argumentation.",
            "options": [
                "Devenir un expert en programmation informatique.",
                "Apprendre à calculer des variances complexes sans calculatrice.",
                "Comprendre l'idée transmise par les chiffres et identifier les points forts/faibles de l'argumentation.",
                "Prouver que les sciences sociales sont plus précises que les sciences dures."
            ],
            "explanation": "L'enjeu est de comprendre l'idée transmise et d'identifier les forces et faiblesses de l'argumentation chiffrée.",
            "slide_page": 68
        }
    ]
    
    for q in raw_questions:
        random.shuffle(q['options'])
    
    st.session_state.shuffled_questions = raw_questions

# --- AFFICHAGE DU FORMULAIRE ---
with st.form(key='quiz_form_inline'):
    user_answers = {}
    score = 0
    
    for i, q in enumerate(st.session_state.shuffled_questions):
        st.markdown(f"**{q['question']}**")
        
        user_answers[i] = st.radio(
            "Votre réponse :",
            q['options'],
            key=f"q_{i}",
            index=None,
            label_visibility="collapsed"
        )
        
        if st.session_state.quiz_submitted:
            if user_answers[i] == q['correct_text']:
                st.success(f"✅ Correct ! {q['explanation']}")
                score += 1
            else:
                slide_url = f"{BASE_URL_SLIDES}#page={q['slide_page']}"
                st.error(f"❌ Incorrect.")
                st.markdown(
                    f"**La bonne réponse était :** {q['correct_text']}\n\n"
                    f"💡 {q['explanation']}  "
                    f"👉 <a href='{slide_url}' target='_blank' style='text-decoration:none; color:#FF4B4B;'>Voir le slide page {q['slide_page']}</a>",
                    unsafe_allow_html=True
                )
        st.write("---")

    submit_button = st.form_submit_button(label="Valider mes réponses")
    
    if submit_button:
        st.session_state.quiz_submitted = True
        st.rerun()

# --- RÉSULTATS ---
if st.session_state.quiz_submitted:
    st.metric("Votre Résultat Final", f"{score} / {len(st.session_state.shuffled_questions)}")
    
    if score == len(st.session_state.shuffled_questions):
        st.balloons()
    
    if st.button("🔄 Recommencer le Quiz"):
        st.session_state.quiz_submitted = False
        for q in st.session_state.shuffled_questions:
            random.shuffle(q['options'])
        st.rerun()