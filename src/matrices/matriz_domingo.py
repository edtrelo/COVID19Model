import pandas as pd
import numpy as np

np.random.seed(123)

fp = "https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/cleandata/viajes/viajes_sabado_por_cve_umun_2017.csv"
matriz_sab = pd.read_csv(fp, index_col=0, encoding='utf-8', sep = ',', dtype = {'origen':str})
# creamos la matriz para los domingos
matriz_dom = matriz_sab.copy()
# leemos el ajuste que hicimos para datos de sábado-domingo

# obtenemos el ajuste que realizamos para los logaritmos de los cociente en la variabilidad sábado/domingo
ajuste = pd.read_csv("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/transformeddata/var_movilidad_sabdom_ajuste.csv")
df, loc, scale = ajuste.iloc[:, 1]

n = len(matriz_dom)
# multiplicamos las entradas de la matriz de sábado por el parámetro de proporcionalidad
beta = np.exp(scale*(np.random.standard_t(df, size = (n, n))) + loc)
for i in range(n):
    for j in range(n):
        matriz_dom.iloc[i, j] *= beta[i, j] 
# aplicamos la función piso
myfloor = lambda x: np.floor(x).astype(int) # hay unas entradas que son negativas, pero cerca del cero.
matriz_dom = matriz_dom.apply(myfloor)
matriz_dom.to_csv('data/cleandata/viajes/viajes_domingo_por_cve_umun_2017.csv', 
                                 sep = ',', encoding =  'utf-8')