import geopandas as gpd
import pandas as pd
import pickle

fp  = "D:/Edgar Trejo/Universidad/Proyecto/COVID19Model/data/rawdata/Censo 2010 (Municipal)/inegi_refcenmuni_2010.shp"
mapaMX = gpd.read_file(fp, encoding = 'latin')

mizmvm = pd.read_csv("D:/Edgar Trejo/Universidad/Proyecto/COVID19Model/data/transformeddata/cves_miZMVM.csv",
                   dtype = {'cve_umun':str})

cves = mizmvm['cve_umun'].to_list()
# flageamos a los municipios de la ZMVM
mapaMX['inZMVM'] = mapaMX['cve_umun'].apply(lambda x: 1 if x in cves else 0)
# filtramos
miZMVM = mapaMX[mapaMX.inZMVM == 1]

miZMVM.to_file("data/cleandata/miZMVMmap/miZMVM.shp")

