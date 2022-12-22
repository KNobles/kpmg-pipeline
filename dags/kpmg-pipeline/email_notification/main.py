import pandas as pd
from send_email import send_email, send_newsletter
from algoliasearch.search_client import SearchClient
import datetime
import time

# Connect and authenticate with your Algolia app
client = SearchClient.create("QVBA9ZZPRA", "f80677d8b7ca3145e40331dc47390bb2")

index = client.init_index('KPMG_newsletter')
index2 = client.init_index('KPMG_index')
index3 = client.init_index('FULL_KPMG_index')
number_of_users = 0

for record in index.browse_objects():
    number_of_users += 1

print(number_of_users)

def new_user(name, lastname, email, newsletter, subscription):
    id_number = number_of_users + 1
    user = {"objectID":id_number, "name":name, "lastname":lastname, "email":email, "newsletter":newsletter, "subscription":subscription}
    print(user)
    index.save_object(user).wait()

# new_user("Koumeil", "", "k.belkhidar@gmail.com", True, ['2000000'])
# new_user("Ahmet", "", "a.samilcicek@gmail.com", True, ['2000000'])
# new_user("Olivier", "", "olivier_d@usa.net", True, ['2000000'])
# new_user("dav", "", "dav3_vr@outlook.com", True, ['2000000'])
# new_user("pierre", "", "pierre@warnier.net", True, ['2000000'])
# new_user("julien", "", "julien-desmedt@hotmail.com", True, ['2000000'])

# update = "2000000"
# for user in index.browse_objects():
#     if update == "2000000":
#         if "2000000" in user['subscription']:
#             send_email('update', user['email'], user['name'], update)

themes = ['Wage increases', 'social peace', 'Social peace - clause', 'Minimum hourly/monthly wage' , 'Wages', 'Actual wages']

#update mail
# for person in index.search('2000000')['hits']:
#     print(person['email'])
#     send_email('update', person['email'], person['name'], '2021-12-13', themes, 'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/200/200-2021-013463.pdf'," travail) le 23 avril 2019, la convention collective de travail n\u00b0 19/9 a \u00e9t\u00e9 sign\u00e9e au conseil national du travail en ex\u00e9cution des accords conclus au conseil national du travail. cette convention collective de travail porte \u00e0 80 p.c. l'intervention de l'employeur dans le prix des transports en commun publics par chemin de fer et exprime cette intervention sous la forme de montants forfaitaires qui ne sont pas index\u00e9s. une \u00e9ventuelle adaptation de ces forfaits sera n\u00e9goci\u00e9e tous les deux ans par les partenaires sociaux. vous trouverez ci-dessous la grille contenant les montants en vigueur \u00e0 partir du 1er juillet 2019. Cette convention collective de travail d\u00e9finit les modalit\u00e9s d'intervention de l'employeur dans les frais de transport des employ\u00e9s, en ce qui concerne les transports en commun publics, les transports organis\u00e9s par l'employeur avec la participation financi\u00e8re des employ\u00e9s, ainsi que les indemnit\u00e9s v\u00e9lo et les moyens de transport personnels. Elle pr\u00e9voit un remboursement mensuel et des contr\u00f4les de la r\u00e9alit\u00e9 des d\u00e9clarations des employ\u00e9s. Elle entre en vigueur le 1er janvier 2022, \u00e0 l'exception de l'indemnit\u00e9 v\u00e9lo qui entre en vigueur le 1er juillet 2022.")

#weekly newletter
for person in index.search('', {'filters': 'newsletter=1'})['hits']:
    print(person['email'])
    send_newsletter('weekly report',person['email'])

