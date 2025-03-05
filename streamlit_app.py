import streamlit as st
import pandas as pd
import os

# Titel der Umfrage
st.set_page_config(page_title="📊 Umfrage 2025", page_icon="📊")
st.title("📊 Umfrage 2025")
st.write("Bitte beantworte die folgenden Fragen:")

# Dateiname für die Speicherung der Umfragedaten
DATA_FILE = "data/umfrage_ergebnisse.csv"

# Sicherstellen, dass der Ordner existiert
os.makedirs("data", exist_ok=True)

# Fragen der Umfrage
name = st.text_input("Wie heißt du?")
alter = st.slider("Wie alt bist du?", 10, 100, 25)
geschlecht = st.radio("Was ist dein Geschlecht?", ["Männlich", "Weiblich", "Divers"])
zufriedenheit = st.selectbox("Wie zufrieden bist du mit dieser Umfrage?", ["Sehr zufrieden", "Zufrieden", "Neutral", "Unzufrieden", "Sehr unzufrieden"])
feedback = st.text_area("Hast du noch weiteres Feedback?")

# Antwort speichern
if st.button("Antwort absenden"):
    new_entry = pd.DataFrame(
        [[name, alter, geschlecht, zufriedenheit, feedback]],
        columns=["Name", "Alter", "Geschlecht", "Zufriedenheit", "Feedback"]
    )
    
    # Prüfen, ob Datei existiert, um Header zu setzen
    if os.path.exists(DATA_FILE):
        new_entry.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        new_entry.to_csv(DATA_FILE, mode="w", header=True, index=False)
    
    st.success("Vielen Dank für deine Teilnahme! 🎉")

# Ergebnisse anzeigen
if st.checkbox("Ergebnisse anzeigen"):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df)
    else:
        st.warning("Noch keine Antworten vorhanden.")
