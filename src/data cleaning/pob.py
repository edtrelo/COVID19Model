import requests
import pandas as pd

url = 'https://es.wikipedia.org/wiki/Zona_metropolitana_del_valle_de_M%C3%A9xico'
html = requests.get(url).content
df_list = pd.read_html(html)
# primer tabla de la página
wiki_df = df_list[1]

# obtenemos la columna con la población de 2020
pob = wiki_df.iloc[1:, 6]
cves = wiki_df.iloc[1:, 0]

dictdf = {'cve_umun':list(cves), 'pop':list(pob)}
df = pd.DataFrame(dictdf)

df['pop'] = df['pop'].apply(lambda x: x.replace(df.iloc[0, 1][3], ''))
df['pop'] = df['pop'].astype(int)

miZMVM = pd.read_csv('data/transformeddata/cves_miZMVM.csv', dtype = {'cve_umun':str})
cvesmiZMVM = miZMVM['cve_umun'].tolist()

df = df[df['cve_umun'].isin(cvesmiZMVM)]

df.to_csv('data/cleandata/pob_miZMVM.csv', index=False)