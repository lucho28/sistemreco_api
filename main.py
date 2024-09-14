from fastapi import FastAPI
import pandas as pd
from scipy.sparse import hstack
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Cargar los archivos parquet
data_movies = pd.read_parquet('Source/data_movies.parquet')
data_credits_actores = pd.read_parquet('Source/data_credits_actores.parquet')
data_credits_directores = pd.read_parquet('Source/data_credits_directores.parquet')
# Recorte para utilizar en el modelo
# Me quedo solo con el genero 'Animation'
data_movies_recortado = data_movies[data_movies['genre_name'].str.contains('Animation', case=False, na=False)]

#################################################################################   
#                                                                               #
#   SIMILITUD DEL COSENO                                                        #
#                                                                               #    
# Procesar el texto de 'overview' usando TF-IDF
tfidf = TfidfVectorizer(stop_words='english')

# Llenar nulos en 'overview' con cadenas vacías para evitar
# errores de procesamiento y no tendra efecto en la matriz
# de caracteristicas
data_movies_recortado['overview'] = data_movies_recortado['overview'].fillna('')

# Aplicar TF-IDF a la columna 'overview' que es la que contiene la sinopsis de 
# las peliculas.
tfidf_matrix = tfidf.fit_transform(data_movies_recortado['overview'])

# Uso ona hot encoding para 'genre_name'. Tambien lleno los valores nulos
# con cadenas vacias. Al igual que se hizo con 'overview'
data_movies_recortado['genre_name'] = data_movies_recortado['genre_name'].fillna('')
genre_dummies = pd.get_dummies(data_movies_recortado['genre_name'])

# Normalizo 'release_year' para garantizar que las variables numericas 
# tengan una misma escala.
# Tambien rellenamos con nulos.
scaler = MinMaxScaler()
data_movies_recortado['release_year'] = data_movies_recortado['release_year'].fillna(0)
release_year_scaled = scaler.fit_transform(data_movies_recortado[['release_year']])

# Combino las las columnas que elegi para las caracteristicas
# (TF-IDF, genre_name, y release_year)
# Combino todas las caracteristicas en una sola matriz
features = hstack([tfidf_matrix, genre_dummies, release_year_scaled])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(features)


app = FastAPI()

# Endpoints
@app.get("/")
def read_root():
    return {"message": "API funcionando correctamente"}

# Endpoint para cantidad de filmaciones por mes
# mejorar la salida
@app.get("/cantidad_filmaciones_mes/{nombre_mes}")
def cantidad_filmaciones_mes(nombre_mes):
    """
    Devuelve la cantidad de películas estrenadas en un mes especifico.

    Parámetros:
    -----------
    Mes : str
        El nombre del mes en español (sin acentos). Por ejemplo: "enero", "febrero", etc.

    Retorna:
    --------
    int
        El numero total de peliculas que se estrenaron en el mes ingresado.
    """

    # Lo siguiente es para comparar con el campo month de la fecha
    # release_date
    meses_nombre = ["enero","febrero","marzo","abril","mayo",
                    "junio","julio","agosto","septiembre",
                    "octubre","noviembre","diciembre"]
    meses_numero = [1,2,3,4,5,6,7,8,9,10,11,12]
    meses = dict(zip(meses_nombre,meses_numero))

    nombre_mes = nombre_mes.lower()

    # Verificar si el mes ingresado es valido
    if nombre_mes not in meses:
        return {'Error': f"El mes '{nombre_mes}' no es valido. Por favor ingresa un mes valido."}

    cantidad_pelis=  int((data_movies["release_date"].dt.month == meses[nombre_mes]).sum())
    return {
        'Total de peliculas estrenadas': cantidad_pelis,
    }

# Endpoint para cantidad de filmaciones por dia
@app.get("/cantidad_filmaciones_dia/{nombre_dia}")
def cantidad_filmaciones_dia(nombre_dia):
    """
    Devuelve la cantidad de peliculas estrenadas en un dia especifico de la semana.

    Parametros:
    -----------
    Dia : str
        El nombre del dia en español (sin acentos). Por ejemplo: "lunes", "martes", etc.

    Retorna:
    --------
    int
        El numero total de peliculas que se estrenaron en el dia de la semana proporcionado.
    """

    # Lo siguiente es para comparar con los dias del release_date
    dias_nombre = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]
    dias_numero = [1,2,3,4,5,6,7]
    dias = dict(zip(dias_nombre,dias_numero))

    nombre_dia = nombre_dia.lower()

    if nombre_dia not in dias:
        return {'Error': f"El dia '{nombre_dia}' no es valido. Por favor ingresa un dia valido."}

    cantidad_pelis=  int((data_movies["release_date"].dt.dayofweek == dias[nombre_dia]).sum())
    
    return {
        'Total de peliculas estrenadas': cantidad_pelis,
    }

# Endpoint para obtener score/popularidad de un titulo
@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion):
    """
    Devuelve el titulo, año de estreno y la popularidad de una pelicula especifica.

    Parametros:
    -----------
    titulo_de_la_filmacion : str
        El titulo de la pelicula a buscar. No es sensible a mayusculas/minusculas.

    Retorna:
    --------
    str
        Un mensaje que contiene el titulo de la pelicula, el ano de estreno y su score de popularidad.
        Si no se encuentra la pelicula, se devuelve un mensaje indicando que no fue encontrada.
    """  
    # Busco la fila que contiene el titulo
    pelicula = data_movies[data_movies['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Si no se encuentra el titulo retorno un mensaje
    if pelicula.empty:
        return f"La pelicula {titulo_de_la_filmacion} no fue encontrada. "
    
    # Obtener los datos de titulo, año y popularidad
    titulo = pelicula['title'].values[0]
    año_estreno = int(pelicula['release_year'].values[0])
    score = round(float(pelicula['popularity'].values[0]),2)

    return {
        'Pelicula': titulo,
        'Año estreno': año_estreno,
        'Score/popularidad': score,
    }



# Endpoint para obtener los votos de un titulo
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo_de_la_filmacion):
    """
    Devuelve la cantidad de votos y el promedio de votos de una pelicula especifica si tiene al menos 2000 votos.

    Parametros:
    -----------
    titulo_de_la_filmacion : str
        El titulo de la pelicula a buscar. 

    Retorna:
    --------
    dict o str
        Si la pelicula tiene al menos 2000 votos, devuelve un diccionario con el titulo, la cantidad de votos y el promedio de votos.
        Si la pelicula tiene menos de 2000 votos, devuelve un mensaje indicando que no cumple con el minimo de votos.
        Si la pelicula no se encuentra en el dataset, devuelve un mensaje indicando eso.
    """

    # obtengo la delicula del DataFrame
    pelicula = data_movies[data_movies['title'].str.lower() == titulo_de_la_filmacion.lower()]
    # Si no encuentro la pelicula doy un mensaje
    if pelicula.empty:
        return f"La pelicula '{titulo_de_la_filmacion}' no se encontro. "
    
    # Obtener la cantidad de votos y el promedio de votos
    cantidad_votos = pelicula['vote_count'].values[0]
    promedio_votos = pelicula['vote_average'].values[0]
    
    # Verificar si la cantidad de votos es mayor o igual a 2000
    if cantidad_votos >= 2000:
        return {
            'Pelicula':titulo_de_la_filmacion,
            'Cantidad de votos': cantidad_votos,
            'Promedio de votos': round(promedio_votos,2),
        }
    else:
        return f"La pelicula '{titulo_de_la_filmacion}' no cumple con el mínimo de 2000 votos. Tiene {cantidad_votos} votos."


# Endpoint para obtener informacion sobre un actor
# cantidad de pelicula, retorno.
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor):
    """
    Devuelve informacion sobre el exito de un actor basado en el retorno de las peliculas en las que ha participado.

    Parametros:
    -----------
    nombre_actor : str
        El nombre del actor a buscar en el dataset.

    Retorna:
    --------
    dict o str
        Si el actor es encontrado, devuelve un diccionario con el nombre del actor, el retorno total, la cantidad de peliculas y el promedio de retorno.
        Si el actor no es encontrado, devuelve un mensaje indicando que no fue encontrado en los registros.
    """

    # Obtengo el actor del dataset de actores para obtener las películas en las que ha participado.
    actor_peliculas = data_credits_actores[data_credits_actores['actor'].str.lower() == nombre_actor.lower()]


    # Uno con el dataset de peliculas para obtener el retorno de cada pelicula.
    actor_peliculas_retorno = pd.merge(actor_peliculas, data_movies[['id', 'return']], on='id', how='left')

    # Verificar si el actor ha participado en alguna pelicula
    if actor_peliculas_retorno.empty:
        return f"El actor {nombre_actor} no ha sido encontrado en los registros."

    # Calcular el éxito total y el promedio de retorno del actor
    total_retorno = round(actor_peliculas_retorno['return'].sum(),3)
    cantidad_peliculas = actor_peliculas_retorno.shape[0]
    promedio_retorno = round(actor_peliculas_retorno['return'].mean(),2)

    # Devolver el éxito del actor, la cantidad de películas y el promedio de retorno
    return {
        'Actor': nombre_actor,
        'Retorno total': total_retorno,
        'Cantidad de peliculas': cantidad_peliculas,
        'Promedio retorno': promedio_retorno
    }


# Endpoint para obtener informacion de un director.
# Lista de peliculas, retorno.
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director):
    """
    Devuelve informacion sobre el exito de un director basado en las peliculas que ha dirigido.

    Parametros:
    -----------
    nombre_director : str
        El nombre del director a buscar en el dataset.

    Retorna:
    --------
    dict o str
        Si el director es encontrado, devuelve un diccionario con el nombre del director, el retorno total de todas sus peliculas
        y una lista con los detalles de cada pelicula (titulo, fecha de lanzamiento, retorno, presupuesto y ganancia).
        Si el director no es encontrado, devuelve un mensaje indicando que no fue encontrado en los registros.
    """
    
    # Obtengo del dataset de directores las películas dirigidas por el director
    director_peliculas = data_credits_directores[data_credits_directores['director'].str.lower() == nombre_director.lower()]


    # Uno con el dataset de peliculas para obtener los detalles de cada una
    director_peliculas_detalles = pd.merge(director_peliculas, data_movies[['id', 'title', 'release_date', 'return', 'budget', 'revenue']], on='id', how='left')

    # Verificar si el director ha dirigido alguna película
    if director_peliculas_detalles.empty:
        return f"El director {nombre_director} no ha sido encontrado en los registros."

    # Calcular el éxito total del director (sumando el retorno de todas sus películas)
    total_retorno = round(director_peliculas_detalles['return'].sum(),2)

    # Preparar la lista de películas con sus detalles
    peliculas_detalles = director_peliculas_detalles[['title', 'release_date', 'return', 'budget', 'revenue']]

    # Aqui el exito del director, el total de retorno y los detalles de cada pelicula
    return {
        'Director': nombre_director,
        'Retorno total': total_retorno,
        'Detalles de peliculas': peliculas_detalles
    }


# Endpoint para obtener 5 recomendaciones de un titulo dado
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo):
    """
    Devuelve una lista de peliculas recomendadas en base a la similitud de coseno del titulo proporcionado.

    Parametros:
    -----------
    title : str
        El titulo de la pelicula para la cual se desea obtener recomendaciones. No es sensible a mayusculas/minusculas.

    Retorna:
    --------
    list o str
        Si el titulo es encontrado, devuelve una lista con los titulos de las 5 peliculas mas similares.
        Si el titulo no es encontrado, devuelve un mensaje indicando que no fue encontrado en el dataset.
    """
    # Verificar si el titulo existe en el DataFrame
    if titulo.lower() not in data_movies_recortado['title'].str.lower().values:
        return f"No se encontro el titulo '{titulo}' en el dataset."

    # Obtener el índice de la película que coincide con el título
    id = data_movies_recortado[data_movies_recortado['title'].str.lower() == titulo.lower()].index[0]

    # Obtener las puntuaciones de similitud de coseno para esa pelicula
    sim_scores = list(enumerate(cosine_sim[id]))

    # Ordenar las peliculas en función de las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los indices de las 5 peliculas mas similares
    sim_scores = sim_scores[1:6]

    # Obtener los indices de las películas
    indices_peliculas = [i[0] for i in sim_scores]

    # Retorno la lista de las 5 peliculas mas similares
    return data_movies_recortado['title'].iloc[indices_peliculas].tolist()

