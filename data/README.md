# Manifest

This directory contains the following data.

# burtin.json

- Data: Antibiotics Efficacy
- Source: https://mbostock.github.io/protovis/ex/antibiotics-burtin.html
- Import: pd.read_json('burtin.json', orient='records')

# mpg.csv

- Data: Car fuel efficiency
- Source: https://raw.githubusercontent.com/tidyverse/ggplot2/master/data-raw/mpg.csv
- Description: https://ggplot2.tidyverse.org/reference/mpg.html

# phillips-ue-cpi.csv

- Data: CPI and Unemployment rate for OECD countries
- Source: https://data.oecd.org/price/inflation-cpi.htm and https://data.oecd.org/unemp/unemployment-rate.htm
- Provenance: See Renku KG to see how this file is constructed from the oecd dataset

# mortality-fr.csv

- Data: Count of daily deaths in France from 1 Jan 2000 to 18 May 2020
- Source
    - http://coulmont.com/blog/2020/04/24/2020-une-mortalite-specifique/
    - https://www.insee.fr/fr/statistiques/4487988?sommaire=4487854 (downloaded 23-05-2021)
    - https://en.wikipedia.org/wiki/Demographics_of_France#Vital_statistics_from_1900[25] (use en since they have an estimate of 2021 population)
- Provenance: See Renku KG to see how this file is constructed from the fr-covid dataset
