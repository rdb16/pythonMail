import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
import smtplib

from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_SEND_USER')
EMAIL_PASSWORD = os.getenv('SEND_PASS')

msg = EmailMessage()
msg['Subject'] = 'avec image'
msg['From'] = EMAIL_ADDRESS
msg['To'] = '0607514708@free.fr'
msg.set_content("envoi tls avec pj , des pdf image")

attached_files_list = [f for f in listdir('attached') if isfile(join('attached', f))]
# on trie les PDF
attached_pdf_list = []
for f in attached_files_list:
    # on envoie que les pdf du dossiers
    if f.split(".")[-1] == "pdf":
        attached_pdf_list.append(f)

for pdf in attached_pdf_list:
    file = join('attached', pdf)
    with open(file, 'rb') as f:
        f_data = f.read()
        f_name = f.name

    msg.add_attachment(f_data, maintype='application', subtype='octet-stream', filename=f_name)

# le with fermera la connexion au serveur
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)


