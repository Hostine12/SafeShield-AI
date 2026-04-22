import streamlit as st
import joblib
import string
import time
from nltk.corpus import stopwords
from PIL import Image

# --- CONFIGURATION ET STYLE ---
 
st.set_page_config(
    page_title="SafeShield AI | Détecteur de Spam",
    page_icon="logo.png",  
    layout="centered"
)

# Injection de CSS personnalisé pour le design
st.markdown("""
    <style>
    .main {
        background-color: transparent;
    }
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #4338CA;
        border: none;
        transform: scale(1.02);
    }
    .result-card {
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        text-align: center;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE IA ---
def nettoyer_texte(message):
    message_sans_punc = [char for char in message if char not in string.punctuation]
    message_sans_punc = ''.join(message_sans_punc)
    # On garde la version multilingue qu'on a construite ensemble
    stop_words = set(stopwords.words('english') + stopwords.words('french'))
    return [word for word in message_sans_punc.split() if word.lower() not in stop_words]

@st.cache_resource
def load_model():
    model = joblib.load('modele_spam.pkl')
    vectorizer = joblib.load('vectoriseur.pkl')
    return model, vectorizer

model, vectorizer = load_model()

# --- INTERFACE UTILISATEUR ---


# 1. Charger l'image
icon_image = Image.open("encrypted.png")

# 2. Créer deux colonnes avec des largeurs inégales
# On donne très peu d'espace à la colonne 1 (l'icône) et le reste au titre
col1, col2 = st.columns([0.15, 0.85])

with col1:
    st.image(icon_image, width=60)

with col2:
    # Correction de l'alignement vertical du texte
    st.markdown("<h1 style='margin-top: -5px; padding-bottom: 0;'>SafeShield AI</h1>", unsafe_allow_html=True)
    st.caption("Protection intelligente contre le spam et le phishing")

st.divider()

# Sidebar pour les réglages et infos
with st.sidebar:
    # Utilisation de ton image locale pour la cohérence
    st.image(icon_image, width=80)
    st.title("Tableau de Bord")
    
    st.divider()
    st.header("Performances de l'IA")
    st.metric(label="Précision (FR/EN)", value="97.2%", delta="Confiance haute")
    st.info("Ce modèle analyse la fréquence des mots suspects pour identifier les fraudes.")
 

st.subheader("Analyseur de messages intelligent")
st.write("Collez un SMS ou un email suspect ci-dessous pour vérifier s'il s'agit d'une tentative de fraude.")

# Zone de saisie
user_input = st.text_area("", placeholder="Entrez le message ici...", height=150)

# Bouton d'analyse
if st.button("Lancer l'analyse sécurisée"):
    if user_input:
        with st.spinner('Analyse des patterns linguistiques en cours...'):
            time.sleep(0.8)  # Petite pause pour l'effet "IA qui réfléchit"
            
            # Prediction
            data = vectorizer.transform([user_input])
            prediction = model.predict(data)
            probabilities = model.predict_proba(data) # Optionnel: pour voir le score
            
            # Affichage stylisé
            if prediction[0] == 'spam':
                st.markdown(f"""
                    <div style="background-color: #fee2e2; border-left: 5px solid #ef4444; padding: 20px; border-radius: 10px;">
                        <h3 style="color: #991b1b; margin: 0;">🚨 Alerte : Spam détecté</h3>
                        <p style="color: #b91c1c;">Ce message présente des caractéristiques typiques d'une fraude ou d'une publicité indésirable.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background-color: #dcfce7; border-left: 5px solid #22c55e; padding: 20px; border-radius: 10px;">
                        <h3 style="color: #166534; margin: 0;">✅ Message sécurisé</h3>
                        <p style="color: #15803d;">L'analyse n'a détecté aucune menace suspecte dans ce contenu.</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Veuillez entrer un texte avant de lancer l'analyse.")