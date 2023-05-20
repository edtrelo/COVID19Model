import pandas as pd

pobmiZMVM = pd.read_csv('data/cleandata/pob_miZMVM.csv',
                        dtype = {'cve_umun':str})

regiones = pd.read_csv("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/transformeddata/regiones.csv",
                       dtype = {'cve_umun':str}, index_col=0)

# definimos una función para asignar su región a un municipio dado
def asignar_region(x):
    return regiones.loc[x, 'region']


pobmiZMVM['region'] = pobmiZMVM['cve_umun'].apply(asignar_region)
pob = pobmiZMVM.groupby("region").sum(numeric_only=True)
pob.to_csv('data/cleandata/pob_reg.csv')