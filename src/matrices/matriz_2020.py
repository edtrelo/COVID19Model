import pandas as pd
import numpy as np

np.random.seed(123)

# obtenemos el ajuste que realizamos para los logaritmos de los cociente en la variabilidad anual
ajuste = pd.read_csv("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/transformeddata/var_movilidad_anual_ajuste.csv")
coef, inter = 0.67563376, 9228.25867856

# usamos los ajustes de la recta afluencia2017 vs afluencia2020
es2017 = pd.read_csv("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2017.csv",
                     encoding='utf-8', index_col=0, dtype = {'origen':str})
# para sábado y domingo 2020 y 2017 suponemos que son iguales.
# hacemos el ajuste
es2020 = es2017.copy()
n = len(es2020)

for i in range(n):
    for j in range(n):
        es2020.iloc[i, j] = coef*es2017.iloc[i, j] + inter
# función piso
myfloor = lambda x: np.floor(x).astype(int)
es2020 = es2020.apply(myfloor)
# guardamos los archivos
# guardamos los archivos
es2020.to_csv("data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2020.csv",
              encoding='utf-8',)