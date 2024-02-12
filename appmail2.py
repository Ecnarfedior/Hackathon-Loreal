import streamlit as st
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.utils import formatdate
import pytz

def send_email(to_email, subject, body, scheduled_time, sender_email, sender_password, smtp_server, smtp_port, survey_link, rp1, rp2, rp3):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    scheduled_datetime = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')

    recipient_timezone = pytz.timezone('Europe/Paris')
    scheduled_datetime_local = scheduled_datetime.astimezone(recipient_timezone)

    msg['Date'] = formatdate(float(scheduled_datetime_local.strftime('%s')))

    body_text = f"""
    Cher(e) ami(e),
    ...
    """

    msg.attach(MIMEText(body_text, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())

# Interface utilisateur Streamlit
st.title("Application d'envoi d'e-mail programmé de retour sur leur participation à l'enquête")

to_email = st.text_input("Adresse e-mail du destinataire:")
subject = st.text_input("Sujet de l'e-mail:")
body = st.text_area("Corps de l'e-mail:")
scheduled_time = st.text_input("Date et heure programmées (format: YYYY-MM-DD HH:mm:ss):")
sender_email = st.text_input("Votre adresse e-mail:")
sender_password = st.text_input("Votre mot de passe e-mail:", type="password")
smtp_server = st.text_input("Serveur SMTP:")
smtp_port = st.number_input("Port SMTP:", min_value=1, max_value=65535, value=25)
survey_link = st.text_input("Lien vers l'enquête:")
rp1 = st.text_input("Référence produit 1:")
rp2 = st.text_input("Référence produit 2:")
rp3 = st.text_input("Référence produit 3:")

if st.button("Envoyer l'e-mail"):
    send_email(to_email, subject, body, scheduled_time, sender_email, sender_password, smtp_server, smtp_port, survey_link, rp1, rp2, rp3)
    st.success("L'e-mail a été programmé et sera envoyé à la date spécifiée.")
