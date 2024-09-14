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
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(Mes):
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

    Mes = Mes.lower()
    return int((data_movies["release_date"].dt.month == meses[Mes]).sum())


# Endpoint para cantidad de filmaciones por dia
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(Dia):
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

    Dia = Dia.lower()
    return int((data_movies["release_date"].dt.dayofweek == dias[Dia]).sum())


# Endpoint para obtener score/popularidad de un titulo
@app.get("/score_titulo/{titulo}")
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
    filmacion = data_movies[data_movies['title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Si no se encuentra el titulo retorno un mensaje
    if filmacion.empty:
        return f"La pelicula {titulo_de_la_filmacion} no fue encontrada. "
    
    # Obtener los datos de titulo, año y popularidad
    titulo = filmacion['title'].values[0]
    año_estreno = int(filmacion['release_year'].values[0])
    score = float(filmacion['popularity'].values[0])

    # Formatear el mensaje de retorno
    #return f"La pelicula {titulo} fue estrenada en el año {int(año_estreno)} con un score/popularidad de {float(score):.2f}"
    return {
        'Pelicula': titulo,
        'Anio esrteno': año_estreno,
        'Score/popularidad': score,
    }

# Endpoint para obtener los votos de un titulo
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


# Endpoint para obtener informacion sobre un actor
# cantidad de pelicula, retorno.
@app.get("/get_actor/{nombre}")
def get_actor(nombre_actor):
    # Filtrar el dataset de actores para obtener las películas en las que ha participado el actor
    actor_movies = data_credits_actores[data_credits_actores['actor'] == nombre_actor]

    # Unir con el dataset de películas para obtener el retorno de cada película en la que el actor ha participado
    actor_movies_with_returns = pd.merge(actor_movies, data_movies[['id', 'return']], on='id', how='left')

    # Verificar si el actor ha participado en alguna película
    if actor_movies_with_returns.empty:
        return f"El actor {nombre_actor} no ha sido encontrado en los registros."

    # Calcular el éxito total y el promedio de retorno del actor
    total_return = actor_movies_with_returns['return'].sum()
    movie_count = actor_movies_with_returns.shape[0]
    average_return = actor_movies_with_returns['return'].mean()

    # Devolver el éxito del actor, la cantidad de películas y el promedio de retorno
    return {
        'actor': nombre_actor,
        'total_return': total_return,
        'movie_count': movie_count,
        'average_return': average_return
    }


# Endpoint para obtener informacion de un director.
# Lista de peliculas, retorno.
@app.get("/get_director/{nombre}")
def get_director(nombre_director):
    # Filtrar el dataset de directores para obtener las películas dirigidas por el director
    director_movies = data_credits_directores[data_credits_directores['director'] == nombre_director]

    # Unir con el dataset de películas para obtener los detalles de cada película
    director_movies_with_details = pd.merge(director_movies, data_movies[['id', 'title', 'release_date', 'return', 'budget', 'revenue']], on='id', how='left')

    # Verificar si el director ha dirigido alguna película
    if director_movies_with_details.empty:
        return f"El director {nombre_director} no ha sido encontrado en los registros."

    # Calcular el éxito total del director (sumando el retorno de todas sus películas)
    total_return = director_movies_with_details['return'].sum()

    # Preparar la lista de películas con sus detalles
    peliculas_detalles = director_movies_with_details[['title', 'release_date', 'return', 'budget', 'revenue']]

    # Devolver el éxito del director, el total de retorno y los detalles de cada película
    return {
        'director': nombre_director,
        'total_return': total_return,
        'peliculas_detalles': peliculas_detalles
    }


# Endpoint para obtener 5 recomendaciones de un titulo dado
@app.get("/recomendacion/{titulo}")
def recomendacion(title):
    # Verificar si el título existe en el DataFrame
    if title not in data_movies_recortado['title'].values:
        return f"No se encontró el título '{title}' en el dataset."

    # Obtener el índice de la película que coincide con el título
    idx = data_movies_recortado[data_movies_recortado['title'] == title].index[0]

    # Obtener las puntuaciones de similitud de coseno para esa película
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas en función de las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de las 5 películas más similares
    sim_scores = sim_scores[1:6]  # Cambiado para obtener solo las 5 películas más similares

    # Obtener los índices de las películas
    movie_indices = [i[0] for i in sim_scores]

    # Retornar los títulos de las 5 películas más similares
    return data_movies_recortado['title'].iloc[movie_indices].tolist()
