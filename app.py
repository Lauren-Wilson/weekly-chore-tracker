import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

#%%
# Google Sheets Setup
SHEET_URL = "https://docs.google.com/spreadsheets/d/1oVdiLIFMQpJKKTqvu3k955inWT-91KXhaR5p6tqkY4E/edit?usp=sharing"  # Replace with your actual Google Sheet URL
CREDENTIALS_FILE = "weekly-chore-tracker-51adb7b626aa.json"  # Replace with your JSON file path

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1  # Open the first sheet

# Function to get the current balance
def get_balance():
    records = sheet.get_all_values()
    df = pd.DataFrame(records[1:], columns=records[0])  # Convert to DataFrame, skip headers
    df["AMOUNT"] = pd.to_numeric(df["AMOUNT"])  # Ensure numeric values
    return df["AMOUNT"].sum() if not df.empty else 10  # Default balance is 10

# Function to update balance
def update_balance(amount):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, amount])

# Streamlit UI
st.title("💰 Weekly Chore Tracker")

# Display Current Balance
balance = get_balance()
st.subheader(f"Current Balance: **${balance:.2f}**")

# Add or Subtract Chore Amount
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Add $7"):
        update_balance(7)
        st.rerun()

with col2:
    if st.button("❌ Subtract $3"):
        update_balance(-3)
        st.rerun()
