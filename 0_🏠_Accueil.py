import streamlit as st

st.set_page_config(
    page_title="Méthodes Quantitatives - Sciences Po",
    page_icon="🏫"
)

st.title("🏫 Méthodes Quantitatives")
st.subheader("Plateforme d'entraînement interactive")

st.markdown("""
Bienvenue sur l'outil d'accompagnement du cours de **Méthodes Quantitatives**. 
Cette application vous permet de réviser les notions théoriques et de perfectionner votre maîtrise d'Excel.

### 🚀 Comment réviser ?
1. **Choisissez une séance et exercice** dans le menu latéral à gauche.
2. **Sélectionnez un mode :**
    * **Mode Papier & Calculatrice :** Pour vous préparer au format de l'examen (petits jeux de données).
    * **Mode Excel :** Pour pratiquer sur des bases de données réelles (fichiers .xlsx).
3. **Recevez un feedback immédiat :** L'outil corrige vos calculs et vos formules.
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