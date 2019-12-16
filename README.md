# Send invoices to our members

## Getting started

- Get hold of an .env-file or configure your own from .env.example
- Send a test email (use test.csv), double check that year, reference number, name and email is correct by running `python3 mailer.py`
- test.csv has two entries where emails are sent to @mailinator.com. Go to http://mailinator.com to see the emails with formatting and all.
- Create a csv file from the membership list with the format `Viite,Nimi,Sukunimi,Etunimi,Sähköposti,DUP1,DUP2` (dup1 and dup2 are not used)
- When you are really really sure that the emails are ready to be sent, use `python3 --year [year] --csvfile [filename]