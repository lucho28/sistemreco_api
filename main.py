from fastapi import FastAPI
import pandas as pd

# Cargar los archivos parquet
data_movies = pd.read_parquet('Source/data_movies.parquet')
#data_credits = pd.read_parquet('datasets/credits.parquet')


app = FastAPI()

# Función auxiliar para la función "cantidad_filmaciones_mes"
meses_nombre = ["enero", "febrero", "marzo", "abril", "mayo",
                "junio", "julio", "agosto", "septiembre",
                "octubre", "noviembre", "diciembre"]
meses_numero = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
meses = dict(zip(meses_nombre, meses_numero))


# Endpoints
@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}

# Endpoint para cantidad de filmaciones por mes
# mejorar la salida
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(Mes):
    meses_nombre = ["enero","febrero","marzo","abril","mayo",
                    "junio","julio","agosto","septiembre",
                    "octubre","noviembre","diciembre"]
    meses_numero = [1,2,3,4,5,6,7,8,9,10,11,12]
    meses = dict(zip(meses_nombre,meses_numero))

    Mes = Mes.lower()
    return int((data_movies["release_date"].dt.month == meses[Mes]).sum())


# 3. Endpoint para crear columna de retorno
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(Dia):
    dias_nombre = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
    dias_numero = [1,2,3,4,5,6,7]
    dias = dict(zip(dias_nombre,dias_numero))

    Dia = Dia.lower()
    return int((data_movies["release_date"].dt.month == dias[Dia]).sum())

# Endpoint para obtener información de una película por título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo_de_la_filmacion):
    # Buscar la fila que contiene el título
    filmacion = data_movies[data_movies['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Si no se encuentra el título, devolver un mensaje indicando eso
    if filmacion.empty:
        return f"La película {titulo_de_la_filmacion} no fue encontrada en la base de datos."
    
    # Obtener los datos de título, año y popularidad
    titulo = filmacion['title'].values[0]
    año_estreno = filmacion['release_year'].values[0]
    score = filmacion['popularity'].values[0]

    # Formatear el mensaje de retorno
    return f"La película {titulo} fue estrenada en el año {int(año_estreno)} con un score/popularidad de {float(score):.2f}"


@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo_de_la_filmacion):
    # Filtrar el DataFrame para encontrar la película con el título proporcionado
    pelicula = data_movies[data_movies['title'] == titulo_de_la_filmacion]
    
    # Verificar si se encontró la película
    if pelicula.empty:
        return f"La película '{titulo_de_la_filmacion}' no se encontró en el dataset."
    
    # Obtener la cantidad de votos y el promedio de votos
    cantidad_votos = pelicula['vote_count'].values[0]
    promedio_votos = pelicula['vote_average'].values[0]
    
    # Verificar si la cantidad de votos es mayor o igual a 2000
    if cantidad_votos >= 2000:
        return f"La película '{titulo_de_la_filmacion}' tiene {cantidad_votos} votos con un promedio de {promedio_votos:.2f}."
    else:
        return f"La película '{titulo_de_la_filmacion}' no cumple con el mínimo de 2000 votos. Tiene {cantidad_votos} votos."