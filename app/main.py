from typing import Union
from fastapi import FastAPI
import pandas as pd



# Creacion de una aplicación FastAPI.

app = FastAPI(title='Consultas sobre películas en las plataformas: Amazon, Disney, Hulu y Netflix')

#definiendo metodos:

@app.get ("/")
async def read_root():
    return {"Hello":
            "World!"}


def listaPalabrasfrec(listapalabras):
    frecuenciapalab = [listapalabras.count(p) for p in listapalabras]
    return dict(list(zip(listapalabras, frecuenciapalab)))
    
def ordenaDicFrec (dicFrec):
    aux= [(dicFrec[key], key) for key in dicFrec]
    aux.sort()
    aux.reverse()
    return aux 

'''
Ejemplo:

@app.get("/validad/{numero}")
def validar_capicua(numero:str):
    respuesta = 'no es capicúa'

    if numero == numero[::-1]:
        respuesta= 'es capicúa'
    return {'El número' : {numero}, 'validacion:' : {respuesta}}

'''

# vamos a escribir las funciones para las consultas deseadas.

# 1) Máxima duración según tipo de film (película/serie), por plataforma y por año: 
# El request debe ser: get_max_duration(año, plataforma, [min o season])

@app.get("/max_duration")
async def get_max_duration(Año: int, Plataforma: str , Min_or_Season: str):
    movies_df=pd.read_csv('https://raw.githubusercontent.com/CamiiloP14/Data-Engineering/master/movies.csv')
    movies_df['duracion_int'] =pd.to_numeric(movies_df['duracion_int'], errors='coerce')
    movies_df['Año_lanzamiento']=pd.to_numeric(movies_df['Año_lanzamiento'], errors='coerce')

    resultado=movies_df[(movies_df['Año_lanzamiento'] == Año) & (movies_df['Plataforma'] == Plataforma) & (movies_df['duracion_tipo']== Min_or_Season)].Duracion.max()
    resultado
    return {"Para el año": {Año},
    'por la platafoma': {Plataforma},
    'la máxima duración de la película/serie es de ': {resultado}}


# 2) Cantidad de películas y series (separado) por plataforma El request debe ser: get_count_plataform(plataforma)

@app.get("/count_plataform")
async def get_count_plataform( Plataforma: str):
    movies_df=pd.read_csv('https://raw.githubusercontent.com/CamiiloP14/Data-Engineering/master/movies.csv')
    resutado_2=movies_df[(movies_df['Plataforma'] == Plataforma)].Tipo.value_counts()
    return f"La cantidad de peliculas y series para la plataforma {Plataforma} es de: {resutado_2[0]} películas y {resutado_2[1]} series."
# resultado_2= movies_df['Plataforma']== Plataforma
#count_resultado_2= movies_df['resultado_2]['duracion_tipo'].value_counts()


# 3) Cantidad de veces que se repite un género y plataforma con mayor frecuencia del mismo. El request debe ser: get_listedin('genero')
# Como ejemplo de género pueden usar 'comedy', el cuál deberia devolverles un cunt de 2099 para la plataforma de amazon.


@app.get("/get_listedin")
async def get_listedin(genero: str):
    movies_df = pd.read_csv('https://raw.githubusercontent.com/CamiiloP14/Data-Engineering/master/movies.csv')
    plataforma_1=""
    plats= movies_df.Plataforma.unique()
    max=0
    for plat in plats:
        if movies_df[movies_df.Plataforma == plat].Listada_en.str.count(genero).sum() > max:
            max= movies_df[movies_df.Plataforma == plat].Listada_en.str.count(genero).sum ()
            plataforma_1=plat 
    return f"La plataforma con más titulos listados en el genero {genero} es: {plataforma_1} con un total de {max} titulos."

# 4) funcion
# Actor que más se repite según plataforma y año. El request debe ser: get_actor(plataforma, año)

@app.get("/get_actor")
async def get_actor(plataforma: str, año: int):
    movies_df = pd.read_csv('https://raw.githubusercontent.com/CamiiloP14/Data-Engineering/master/movies.csv')
    act= movies_df[(movies_df['Plataforma']== 'amazon') & (movies_df['Año_lanzamiento']== 2018)].Elenco.str.split(',')
    act= act.dropna()

    actores_año =[]
    for actores in act:
        for actor in actores:
            actor=actor.rstrip()
            actor=actor.lstrip()
            actores_año.append(actor)

    actor =listaPalabrasfrec(actores_año)
    actor=ordenaDicFrec(actor)

    return f"El actor que más se repite en: {plataforma}, en el año: {año} es {actor[0][1]} con un total de {actor[0][0]} apariciones."

