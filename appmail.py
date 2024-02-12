import streamlit as st
from datetime import datetime
import pytz
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Fonction pour envoyer un email
def send_email(to_email, subject, body, scheduled_time, sender_email, sender_password, smtp_server, smtp_port, survey_link):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Convertir le temps programmé en format de date et heure
    scheduled_datetime = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')

    # Récupérer le fuseau horaire local du destinataire
    recipient_timezone = pytz.timezone('Europe/Paris')  # Remplacez 'Europe/Paris' par le fuseau horaire du destinataire

    # Convertir le temps programmé au fuseau horaire local du destinataire
    scheduled_datetime_local = scheduled_datetime.astimezone(recipient_timezone)

    # Définir la date d'envoi programmée dans l'e-mail
    msg['Date'] = scheduled_datetime_local.strftime('%Y-%m-%d %H:%M:%S')

    # Corps de l'e-mail
    

    msg.attach(MIMEText(body_text, 'plain'))

    # Connexion au serveur SMTP
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Démarrer le chiffrement TLS (si nécessaire)
        server.starttls()

        # Authentification auprès du serveur SMTP
        server.login(sender_email, sender_password)

        # Envoi de l'e-mail
        server.sendmail(sender_email, to_email, msg.as_string())

# Interface utilisateur Streamlit avec valeurs par défaut
st.title("Application d'envoi d'e-mails programmé après une commande client contenant l'enquête de satisfaction")

# Formulaire pour saisir les détails de l'e-mail avec valeurs par défaut
to_email = st.text_input("Adresse e-mail du destinataire:", value="stanlesieurpro@gmail.com")
subject = st.text_input("Objet de l'e-mail:", value="L'Oréal : Invitation à participer à notre enquête de satisfaction.")
body = st.text_area("Corps de l'e-mail:")
scheduled_time = st.text_input("Heure programmée (YYYY-MM-DD HH:MM:SS):",value="2024-01-17 10:00:00")
sender_email = st.text_input("Adresse e-mail de l'expéditeur:", value="*****@gmail.com")
sender_password = st.text_input("Mot de passe de l'expéditeur:", type="password", value="****")
smtp_server = st.text_input("Serveur SMTP:", value="smtp.gmail.com")
smtp_port = st.number_input("Port SMTP:", min_value=1, max_value=65535, value=25)
survey_link = st.text_input("Lien vers l'enquête:", value="https://docs.google.com/forms/d/e/...")

# Bouton pour envoyer l'e-mail
if st.button("Envoyer l'e-mail"):
    send_email(to_email, subject, body, scheduled_time, sender_email, sender_password, smtp_server, smtp_port, survey_link)
    st.success("L'e-mail a été envoyé avec succès!")
