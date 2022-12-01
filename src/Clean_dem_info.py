import pandas as pd
import numpy as np
import cleaning_functions as clfun
import mapping_functions as mapp


'''First we concatenate the different data that we have and we open it. We are focusing now in the internal migration data'''

#####clfun.concatenate_csv("../Data/Moving Data", "movements.csv")

internal_migration = pd.read_csv("Data/Moving data/movements.csv")

internal_migration  = clfun.drop_value(internal_migration,"Nom_Districte_baixa", "No consta")
internal_migration  = clfun.drop_value(internal_migration,"Nom_Barri_baixa", "No consta")
internal_migration  = clfun.drop_value(internal_migration,"Nom_Districte_alta", "No consta")
internal_migration  = clfun.drop_value(internal_migration,"Nom_Barri_alta", "No consta")
internal_migration  = clfun.drop_value(internal_migration,"Nombre", "0")

clfun.drop_column(internal_migration , ["Codi_Districte_baixa", "Codi_Barri_baixa", "Codi_Districte_alta", "Codi_Barri_alta"])

internal_migration = internal_migration[internal_migration['Nom_Barri_baixa'] != internal_migration['Nom_Barri_alta']]

internal_migration.to_csv("Data/Moving data/internal_migration.csv", index=False)


'''Next, we clean the disposable income dataset'''

# clfun.concatenate_csv("Data/disposable_income data", "income.csv")


disposable_income = pd.read_csv("Data/disposable_income data/income.csv")
clfun.merge_columns(disposable_income,"Euros_Any", "Import_€_Any")
clfun.drop_column(disposable_income , ["Codi_Districte", "Codi_Barri"])

disposable_income.to_csv("Data/disposable_income data/disposable_income.csv", index=False)


'''Then, we clean the density dataset'''

# clfun.concatenate_csv("../Data/Density data", "density")

density_districts = pd.read_csv("Data/Density data/density")

clfun.drop_column(density_districts , ["Codi_Districte", "Codi_Barri", "Superfície Residencial (ha)"])

density_districts.to_csv("Data/Density data/density_districts.csv", index=False)

district_prices = pd.read_csv("Data/prices data/prices.csv")

district_prices.rename(columns={'Años': "Años", '4º trimestre': "Price", "Años": "Districtes"}, inplace=True, errors='raise')
clfun.drop_column(district_prices, [ "1r trimestre", '2º trimestre', '3º trimestre'])
district_prices  = clfun.drop_value(district_prices,"Districtes", "BARCELONA")
district_prices = clfun.drop_rows(district_prices, "Districtes", ["2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"])

district_prices = district_prices.drop([180, 181])
district_prices = district_prices[:-10]
district_prices.reset_index(drop=True, inplace=True)

clfun.set_years(district_prices,"Any", 2001)
district_prices["Districtes"] = district_prices["Districtes"].apply(lambda x: x.split(". ")[1])
district_prices.to_csv("Data/prices data/district_prices.csv")


'''We load the Poverty Risk index'''

poverty_districts = pd.read_csv("Data/Risk data/poverty.csv", decimal=',')
poverty_districts.rename(columns={"('Por distritos',)": "Districtes", "('Tasa de riesgo a la pobreza',)": 'Tasa de riesgo'}, inplace=True, errors='raise')
poverty_districts["Districtes"] = poverty_districts["Districtes"].apply(lambda x: x.split(". ")[1])
poverty_districts.to_csv("Data/Risk data/poverty_risk.csv", index = False)


'''We load the births/deaths dataframes'''

births_districts = pd.read_csv("Data/Natural growth data/births.csv", decimal=',')
births_districts['Distrito'] = births_districts['Distrito'].apply(lambda x: x.split(". ")[1])
births_districts = births_districts.set_index("Distrito").transpose()
births_districts.rename(index={0: 2016, 1: 2017, 2: 2018, 3: 2019, 4: 2020}, inplace=True)
births_districts.to_csv("Data/Natural growth data/births_districts.csv", index = False)


deaths_districts = pd.read_csv("Data/Natural growth data/deaths.csv", decimal=',')
deaths_districts["Distrito"] = deaths_districts["Distrito"].apply(lambda x: x.split(". ")[1])
deaths_districts = deaths_districts.set_index("Distrito").transpose()
deaths_districts.rename(index={0: 2016, 1: 2017, 2: 2018, 3: 2019, 4: 2020}, inplace=True)
deaths_districts.to_csv("Data/Natural growth data/deaths_districts.csv", index = False) 