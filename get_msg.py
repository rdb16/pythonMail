import os
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
import poplib


def get_msg_id(str_line):
    str_id = str_line.replace("Message-ID: <", "")
    str_id = str_id.replace(">", "")
    return str_id



load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_GET_USER')
EMAIL_PASSWORD = os.getenv('GET_PASS')

Mailbox = poplib.POP3_SSL('pop.free.fr', 995)
Mailbox.user(EMAIL_ADDRESS)
Mailbox.pass_(EMAIL_PASSWORD)

nbofMessages = len(Mailbox.list()[1])
for i in range(nbofMessages):
    print('num : ', i)
    mailtext = ""
    msg_id = ""
    for bline in Mailbox.retr(i+1)[1]:
        line = str(bline, encoding='utf-8')
        mailtext += line + '\n'
        if 'Message-ID:' in line:
            msg_id = get_msg_id(line)

    msg_name = "received_files/" + msg_id + ".txt"
    # ouverture exclusive si-non rejet
    with open(msg_name, 'x') as fp:
        fp.write(mailtext)
    # on delete l'email traité
    Mailbox.dele(i + 1)

Mailbox.quit()

print('NB de messages à ramasser : ', nbofMessages)