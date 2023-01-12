from typing import Union
from fastapi import FastAPI



# Creacion de una aplicación FastAPI.

app = FastAPI()

#definiendo metodos:

@app.get ("/")
async def read_root():
    return {"Hello":
            "World!"}

@app.get("/validad/{numero}")
def validar_capicua(numero:str):
    respuesta = 'no es capicúa'

    if numero == numero[::-1]:
        respuesta= 'es capicúa'
    return {'El número' : numero, 'que' : respuesta}