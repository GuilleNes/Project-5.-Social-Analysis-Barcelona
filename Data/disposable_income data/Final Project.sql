USE final_project;

SELECT * FROM df_income
WHERE Nom_Districte = "Eixample"
AND Any = 2019
order by Euros_Any DESC;
