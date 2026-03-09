# 🏫 Méthodes Quantitatives - Sciences Po Training App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sciencespo-mq-training.streamlit.app/)

This is an interactive educational platform built with **Python** and **Streamlit** to help Sciences Po students master quantitative methods. The application bridges the gap between theoretical understanding (manual calculations) and professional application (Excel Pivot Tables).

## 🎯 Objectives

The tool allows students to:
1.  **Review Concepts:** Quizzes and theoretical reminders based on the course slides.
2.  **Understand the Logic:** "Manual Mode" offers small datasets ($N \approx 20$) to perform calculations by hand or calculator.
3.  **Master Excel:** "Excel Mode" generates large, realistic datasets ($N \approx 200$) to practice Pivot Tables (TCD), Grouping, and Formulas.
4.  **Self-Correct:** The app provides instant feedback by scanning uploaded Excel files or checking manual inputs.

## 🚀 Features

### 🔄 Infinite Practice
Every exercise is generated randomly upon request. Contexts vary between **Sociology**, **Political Science**, **Economics**, and **Demography**, ensuring students practice the *method* rather than memorizing answers.

### 📚 Curriculum Covered (Work in Progress)

* **S1 | Introduction:** Interactive Quiz on the history and definition of statistics.
* **S2 | Simple Distribution:**
    * *Manual:* Counting frequencies on a small sorted list.
    * *Excel:* Creating a Pivot Table (TCD) for categorical variables.
* **S2 | Grouping (Binning):**
    * *Manual:* Grouping continuous variables (e.g., Grades, Salaries) into intervals $[a, b[$.
    * *Excel:* Using the "Group" feature in Pivot Tables.
* **S2 | Cumulative Distribution:**
    * *Manual:* Calculating running totals ($N_i$).
    * *Excel:* Using anchored formulas (`=SUM($B$2:B2)`).
* **S3 | Central Tendency:**
    * *Manual:* Calculating Median, Simple Mean, and Weighted Mean.
    * *Excel:* Using functions `MEDIAN`, `AVERAGE`, and `SUMPRODUCT`.
* **S3 | Dispersion (Variance & Std Dev):**
    * *Manual:* Step-by-step decomposition (Difference $\to$ Square $\to$ Sum $\to$ Root).
    * *Excel:* Understanding Population functions (`VAR.P`, `STDEV.P`) vs Sample functions.

## 💻 Usage

### 🌐 Online (Recommended)
You can use the application directly in your browser without installing anything. This is the best method for students.

👉 **[Click here to open the App](https://sciencespo-mq-training.streamlit.app/)**

### 🛠️ Local Installation (For Developers)
To run this app locally on your machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abahiaoui/sciencespo-mq-training.git
    cd sciencespo-mq-training
    ```

2.  **Install requirements:**
    Make sure you have Python installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run 0_🏠_Accueil.py
    ```

## 👨‍💻 Author & Contact

**Ahmed BAHIAOUI**

This tool was developed to support the Quantitative Methods course at Sciences Po.

If you encounter any technical issues or have questions about the exercises, please feel free to contact me:

* 📧 **Sciences Po:** [ahmed.bahiaoui@sciencespo.fr](mailto:ahmed.bahiaoui@sciencespo.fr)
* 📧 **Fallback:** [ahmed.bahiaoui.mail@gmail.com](mailto:ahmed.bahiaoui.mail@gmail.com)
