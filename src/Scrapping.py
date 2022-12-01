import requests
from bs4 import BeautifulSoup
import pandas as pd

url_price = "https://ajuntament.barcelona.cat/estadistica/castella/Estadistiques_per_temes/Habitatge_i_mercat_immobiliari/Mercat_immobiliari/Preu_oferta_habitatge_segona_ma/evo/t2mad.htm"
html = requests.get(url_price)
soup = BeautifulSoup(html.content, "html.parser")
table = soup.find_all("table")[0]
rows = table.find_all('tr')
rows = [row.text.strip().replace("\xa0", "").split("\n") for row in rows]
colnames = rows[4]
data = rows[9:-18]
df_price = pd.DataFrame(data, columns=colnames)
df_price.to_csv("Data/prices data/prices.csv", index = False)


url_risk = "https://ajuntament.barcelona.cat/estadistica/castella/Estadistiques_per_temes/Poblacio_i_demografia/Poblacio/Enquesta_sociodemografica/esd17/persones/taxes/trp.htm"
html = requests.get(url_risk)
soup = BeautifulSoup(html.content, "html.parser")
table = soup.find_all("table")[0]
rows = table.find_all('tr')
rows = [row.text.strip().replace("\xa0", "").split("\n") for row in rows]
colnames = rows[12], rows[4]
data = rows[13:-18]
df_risk = pd.DataFrame(data, columns=colnames)
df_risk.to_csv("Data/Risk data/poverty.csv", index = False)


url_births = "https://ajuntament.barcelona.cat/estadistica/castella/Estadistiques_per_temes/Poblacio_i_demografia/Documents_relacionats/dem/a2020/t205.htm"
html = requests.get(url_births)
soup = BeautifulSoup(html.content, "html.parser")
table = soup.find_all("table")[0]
rows = table.find_all('tr')
rows = [row.text.strip().replace("\xa0", "").split("\n") for row in rows]
colnames = rows[5]
data = rows[10:-5]
df_births = pd.DataFrame(data, columns=colnames)
df_births.to_csv("Data/Natural growth data/births.csv", index = False)


url_deaths = "https://ajuntament.barcelona.cat/estadistica/castella/Estadistiques_per_temes/Poblacio_i_demografia/Documents_relacionats/dem/a2020/t208.htm"
html = requests.get(url_deaths)
soup = BeautifulSoup(html.content, "html.parser")
table = soup.find_all("table")[0]
rows = table.find_all('tr')
rows = [row.text.strip().replace("\xa0", "").split("\n") for row in rows]
colnames = rows[5]
data = rows[10:-5]
df_deaths = pd.DataFrame(data, columns=colnames)
df_deaths.to_csv("Data/Natural growth data/deaths.csv", index = False)