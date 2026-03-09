import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Safe Submit", page_icon="🛡️")
st.title("🛡️ Race-Condition-Proof Submission")

# 1. Setup the connection securely using st.secrets
# We use the same secrets file, but we load it into the 'gspread' library directly.
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

s_info = st.secrets["connections"]["gsheets"]
credentials = Credentials.from_service_account_info(
    s_info,
    scopes=scopes,
)
client = gspread.authorize(credentials)

# 2. The Form
with st.form("safe_form"):
    name = st.text_input("Name")
    answer = st.number_input("Answer", step=1)
    submitted = st.form_submit_button("Submit Safely")

    if submitted:
        if not name:
            st.error("Please enter your name.")
        else:
            try:
                # Open the sheet by URL (from secrets)
                sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
                spreadsheet = client.open_by_url(sheet_url)
                
                # Select the first worksheet
                worksheet = spreadsheet.sheet1
                
                # Create the row data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row_data = [name, answer, timestamp]
                
                # --- THE MAGIC FIX ---
                # append_row adds data to the first empty row at the bottom.
                # It does NOT read or overwrite the rest of the sheet.
                worksheet.append_row(row_data)
                
                st.success("✅ Saved! No data was overwritten.")
                
            except Exception as e:
                st.error(f"Error: {e}")