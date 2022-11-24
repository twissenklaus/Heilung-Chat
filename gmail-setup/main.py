from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
'''
emailMsg = '87585987668686868'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'franciscolucasdasilva54@gmail.com'
mimeMessage['subject'] = 'abacate zero'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
'''
#message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

result = service.users().messages().list(userId='me').execute()

# We can also pass maxResults to get any number of emails. Like this:
# result = service.users().messages().list(maxResults=200, userId='me').execute()
messages = result.get('messages')
'''
conteudo = ""
email_de = ""
email_para = ""
assunto = ""

obj = {}
trds = []
i = 0
for x in messages:
    txt = service.users().messages().get(userId='me', id=x['id']).execute()
    print(txt)
    if not txt["threadId"] in trds:
        trds.append(txt["threadId"])
        obj[txt["threadId"]] = []
    if "INBOX" in txt["labelIds"]:
        conteudo = txt["snippet"]
        for hd in txt["payload"]["headers"]:
            if hd['name'] == "From":
                email_de = hd["value"]
            if hd['name'] == "To":
                email_para = hd["value"]
            if hd['name'] == "Subject":
                assunto = hd["value"]
            
        obj[txt["threadId"]] += [
        {"de":email_de,
        "para":email_para,
        "assunto":assunto,
        "conteudo":conteudo,
        "timestamp": txt["internalDate"]}]
jaFoi = []
for t in trds:
    for ss in obj[t]:
        print("****************")
        print(ss["assunto"])
        print(ss["conteudo"])
        oo = ss["conteudo"].split("} ")[0] + "}" 
        oo = oo.replace("&#39;", '"')
        print(oo)
        aaa = json.loads(oo)
        print("sssssssssss")
        print(aaa["de"])
        print("****************")
        jaFoi.append(t)
'''      



conteudo = ""
email_de = ""
email_para = ""
assunto = ""

obj = []
i = 0

for x in messages:
    txt = service.users().messages().get(userId='me', id=x['id']).execute()
    if "INBOX" in txt["labelIds"]:
        obj.append(txt)
        conteudo = txt["snippet"]
        for hd in txt["payload"]["headers"]:
            if hd['name'] == "From":
                email_de = hd["value"]
            if hd['name'] == "To":
                email_para = hd["value"]
            if hd['name'] == "Subject":
                assunto = hd["value"]
        print("De:", email_de)
        print("Para:", email_para)
        print("Assunto:", assunto)
        print("Conteudo:", conteudo)
        print()


