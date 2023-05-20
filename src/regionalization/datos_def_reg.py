import pandas as pd
import pickle as pkl

regiones = pd.read_csv("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/transformeddata/regiones.csv",
                       index_col=0, dtype = {'cve_umun':str})

# definimos una función para asignar su región a un municipio dado
def asignar_region(x):
    return regiones.loc[x, 'region']
        
fp = 'data/cleandata/datosepi/defunciones_miZMVM.csv'
casos = pd.read_csv(fp, sep = ',', encoding = 'utf-8', dtype = {'cve_ent':str})
casos['region'] = casos.cve_ent.apply(asignar_region)
casos = casos.groupby("region").sum(numeric_only=True)

casos.to_csv('data/cleandata/datosepi/defunciones_reg.csv')