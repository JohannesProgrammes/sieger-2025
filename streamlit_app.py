import streamlit as st
import pandas as pd
import requests
import base64
import json
from io import StringIO  # <- Hier wird StringIO importiert

# 🔧 GITHUB EINSTELLUNGEN (ANPASSEN)
GITHUB_USER = "JohannesProgrammes"
REPO_NAME = "sieger-2025"
CSV_PATH = "data/umfrage_ergebnisse.csv"
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # ⚠ Sicher speichern! Nutze secrets, falls öffentlich.

# 📥 Funktion: CSV aus GitHub laden
def load_data():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{CSV_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        return pd.read_csv(pd.compat.StringIO(decoded_content)), response.json()["sha"]
    else:
        return pd.DataFrame(columns=["Name", "Alter", "Geschlecht", "Feedback"]), None

# 📤 Funktion: CSV in GitHub speichern
def save_data(df, sha):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{CSV_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    # CSV-Datei in Base64 encodieren
    csv_content = df.to_csv(index=False).encode("utf-8")
    encoded_content = base64.b64encode(csv_content).decode("utf-8")
    
    # JSON-Body für GitHub API
    data = {
        "message": "Update Umfrage-Ergebnisse",
        "content": encoded_content,
        "sha": sha  # Damit die API weiß, dass sie die Datei aktualisieren soll
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200 or response.status_code == 201:
        st.success("Antwort gespeichert! ✅")
    else:
        st.error(f"Fehler beim Speichern: {response.json()}")

# 🌟 Streamlit UI
st.set_page_config(page_title="📊 Umfrage 2025", page_icon="📊")
st.title("📊 Umfrage 2025")
st.write("Bitte beantworte die folgenden Fragen:")

# Daten aus GitHub laden
df, sha = load_data()

# 🚀 Umfrage-Eingaben
name = st.text_input("Wie heißt du?")
alter = st.slider("Wie alt bist du?", 10, 100, 25)
geschlecht = st.radio("Geschlecht", ["Männlich", "Weiblich", "Divers"])
feedback = st.text_area("Feedback")

# ✅ Antwort speichern
if st.button("Antwort absenden"):
    new_data = pd.DataFrame([[name, alter, geschlecht, feedback]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    save_data(df, sha)

# 📊 Ergebnisse anzeigen
if st.checkbox("Ergebnisse anzeigen"):
    st.dataframe(df)
