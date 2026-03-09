import streamlit as st

st.set_page_config(
    page_title="Méthodes Quantitatives - Sciences Po",
    page_icon="🏫"
)

st.title("🏫 Evaluation - Méthodes Quantitatives")
st.subheader("Plateforme d'évaluation du cours")

st.markdown("""
Bienvenue sur la plateforme d'évaluation du cours de **Méthodes Quantitatives**. 
Cette application vous permet de passer vos examens et quiz interactifs.

### 🚀 Consignes générales
1. **Accédez aux quiz** depuis le menu latéral à gauche.
2. **Remplissez le formulaire de l'examen.** Assurez-vous que toutes vos réponses sont complètes avant de soumettre.
3. **Résultats et Soumission :** 
    * Une fois soumis, vos réponses seront enregistrées de manière sécurisée.
    * Vous pourrez télécharger ou enregistrer une copie de vos réponses avec la correction.
    * **Attention :** Une fois le formulaire soumis, vous ne pourrez plus modifier vos réponses.
""")

st.divider()

st.markdown("""
### 👨‍💻 Contact & Code Source 
            
Cet outil a été développé par **Ahmed BAHIAOUI** pour les étudiants de la première année du collège universitaire de Sciences Po.

* 💻 **Code Source :** Retrouvez le projet sur : [![GitHub](https://img.shields.io/badge/GitHub-Repo-181717?logo=github)](https://github.com/abahiaoui/sciencespo-mq-training)
            


Si vous rencontrez un problème technique ou avez une question sur les exercices, n'hésitez pas à me contacter :
* 📧 **Sciences Po :** [ahmed.bahiaoui@sciencespo.fr](mailto:ahmed.bahiaoui@sciencespo.fr)

*(Si l'adresse Sciences Po est désactivée, adresse fallback : [ahmed.bahiaoui.mail@gmail.com](mailto:ahmed.bahiaoui.mail@gmail.com))*
""")