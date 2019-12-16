import argparse
import csv
import dotenv
import markdown2
import os
import requests

from dotenv import load_dotenv
load_dotenv()

from markdown2 import Markdown
markdowner = Markdown()

parser = argparse.ArgumentParser(description="Membership invoice sender")
parser.add_argument("--year", required=True, help="The year for the invoice")
parser.add_argument("--csvfile", default="test.csv", help="The CSV file")
args = parser.parse_args()

year = args.year
csvfile = args.csvfile

subject = "JÄSENMAKSULASKU vuodelle {} / Membership fee invoice for {}".format(year, year)

with open('message.md', 'r') as mf:
    message = mf.read()

def send_message(name, email, message):
    return requests.post(
        "https://api.mailgun.net/v3/ %s /messages" % (os.getenv("mg_domain")),
        auth=("api", os.getenv("mg_api_key")),
        data={"from": "Amigos del Tango <info@tango.fi>",
              "to": email,
              "subject": subject,
              "html": markdowner.convert(message),
              "text": message,
              })

with open(csvfile, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        if line_count <= 200000:
            print(f'\t{row["Nimi"]} {row["Sähköposti"]} {row["Viite"]}.')
            mailMessage = message.replace('###NAME###', row["Nimi"]).replace('###VIITENUMERO###', row["Viite"]).replace('###YEAR###', year)
            print(mailMessage)
            ret = send_message(row["Nimi"], row["Sähköposti"], mailMessage)
            print(ret.text)
            
        line_count += 1
    print(f'Processed {line_count} lines.')
    
    