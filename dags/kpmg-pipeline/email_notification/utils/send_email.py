import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from algoliasearch.search_client import SearchClient
import datetime
import time
from dotenv import load_dotenv

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

#load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

#read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")



def send_email(subject, receiver_email, name, pubbl_date, themes, link, summery):
    #create the base text message
    theme_text = (', '.join(themes))
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["from"] = formataddr(("KPMG", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email
    msg.set_content(f'''
<table style="margin: 0;padding: 0;border-spacing: 0;overflow: hidden;background-color: #ebf5ff;" cellspacing="0" cellpadding="0" border="0" width="100%" >
    <tbody style="margin: 0;padding: 0;">
        <tr style="font-family: Helvetica, sans-serif;font-size: 100%;margin: 0;padding: 0;">
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-size: 0;margin: 0;padding: 0;height: 50px;background-color: rgba(255, 255, 255, 0)" width="60%"></td>
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
        </tr>
        <tr style="margin: 0;padding: 0">
            
            <td style="font-family: Helvetica, sans-serif;font-size: 16px;margin: 0;font-weight: normal;line-height: 24px;background-color: #ffffff;width:100%;" border="0">
                <h3>A new document has been pubblished </h3>
                <p>The document has been pubblished on the royal gazette the following day: {pubbl_date}</p>
                <br>
                <p>{summery}</p>
                <br>
                <p>The main themes are: {theme_text}</p>
                <a href={link}>Download the document</a>
            </td>
            
        <tr style="margin: 0;padding: 0">
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-size: 0;margin: 0;padding: 0;height: 24px;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
''', subtype='html')


    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())





def send_newsletter(subject, receiver_email):
    #Connect and authenticate with your Algolia app
    client = SearchClient.create("QVBA9ZZPRA", "f80677d8b7ca3145e40331dc47390bb2")
    index = client.init_index('KPMG_index')
    #geting the date of the previous week
    date = datetime.datetime.now() - datetime.timedelta(weeks=1)
    date_timestamp = int(time.mktime(date.timetuple()))
    #
    objectmail = ""
    for new_article in index.search('', {'filters': 'retrieveDate > ' + str(date_timestamp)})['hits']:
        new_article_text = f"""<br><h3>{new_article['title']}</h3><br><p>{new_article['summary']}<br><p>{new_article['cla_theme']}</p><br><a href={new_article['pdfLink']}>Download the document</a></p><br>"""
        objectmail += new_article_text
    #create the base text message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["from"] = formataddr(("KPMG", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email
    msg.set_content(f'''
<table style="margin: 0;padding: 0;border-spacing: 0;overflow: hidden;background-color: #ebf5ff;" cellspacing="0" cellpadding="0" border="0" width="100%" >
    <tbody style="margin: 0;padding: 0;">
        <tr style="font-family: Helvetica, sans-serif;font-size: 100%;margin: 0;padding: 0;">
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-size: 0;margin: 0;padding: 0;height: 50px;background-color: rgba(255, 255, 255, 0)" width="60%"></td>
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
        </tr>
        <tr style="margin: 0;padding: 0">
            <td style="font-size: 0;margin: 0 ;padding: 15;width: 14px;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-family: Helvetica, sans-serif;font-size: 16px;margin: 0;font-weight: normal;line-height: 24px;background-color: #ffffff;" border="0">
                <tr>{objectmail}</tr>
            </td>
            <td style="font-size: 0;margin: 0;padding: 0;width: 14px;background-color: rgba(255, 255, 255, 0)"></td>
        </tr>
        <tr style="margin: 0;padding: 0">
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-size: 0;margin: 0;padding: 0;height: 24px;background-color: rgba(255, 255, 255, 0)"></td>
            <td style="font-size: 0;margin: 0;padding: 0;background-color: rgba(255, 255, 255, 0)"></td>
''', subtype='html')
    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())



themes = ['Wage increases', 'social peace', 'Social peace - clause', 'Minimum hourly/monthly wage' , 'Wages', 'Actual wages']
if __name__ == "__main__":
    send_email('update', 'lounol.co@gmail.com', 'Louis', '2021-12-13', themes, 'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/200/200-2021-013463.pdf'," travail) le 23 avril 2019, la convention collective de travail n\u00b0 19/9 a \u00e9t\u00e9 sign\u00e9e au conseil national du travail en ex\u00e9cution des accords conclus au conseil national du travail. cette convention collective de travail porte \u00e0 80 p.c. l'intervention de l'employeur dans le prix des transports en commun publics par chemin de fer et exprime cette intervention sous la forme de montants forfaitaires qui ne sont pas index\u00e9s. une \u00e9ventuelle adaptation de ces forfaits sera n\u00e9goci\u00e9e tous les deux ans par les partenaires sociaux. vous trouverez ci-dessous la grille contenant les montants en vigueur \u00e0 partir du 1er juillet 2019. Cette convention collective de travail d\u00e9finit les modalit\u00e9s d'intervention de l'employeur dans les frais de transport des employ\u00e9s, en ce qui concerne les transports en commun publics, les transports organis\u00e9s par l'employeur avec la participation financi\u00e8re des employ\u00e9s, ainsi que les indemnit\u00e9s v\u00e9lo et les moyens de transport personnels. Elle pr\u00e9voit un remboursement mensuel et des contr\u00f4les de la r\u00e9alit\u00e9 des d\u00e9clarations des employ\u00e9s. Elle entre en vigueur le 1er janvier 2022, \u00e0 l'exception de l'indemnit\u00e9 v\u00e9lo qui entre en vigueur le 1er juillet 2022.")