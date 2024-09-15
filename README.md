# Proyecto Data Science - Sistema de recomendacion

## Tabla de contenidos

- [Descripcion](#Description)
- [Instalacion y requisitos](#instalacion-y-requisitos)
- [Pasos para la instalacion](#pasos-para-la-instalacion)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Fuentes de datos](#fuentes-de-datos)
- [Metodologia](#metodologia)
- [Contribucion y colaboracion](#contribucion-y-colaboracion)
- [Autores](#autores)

## Descripcion

Este proyecto va a estar centrado en la revision y procesamiento de 2 DataSets que contendran informacion sobre la industria cinematografica, contando con datos sobre Actores, Directores, Generos, Titulos como sus mas relevantes.
El foco estara puesto en extraer la informacion de forma tal que pueda ser analisada, procesada para que luego a traves de una API la cual estara desplegada en internet, en render, le brinde al usuario la devolucion de peticiones. 
Ademas la principal funcionalidad sera, darle una lista de 5 peliculas recomendadas similares a un titulo ingresado por el mismo.


##  Instalacion y requisitos

* Python 3.11 o superior
* Pandas
* matplotlib
* Scikit-learn
* ast
* seaborn
* pyarrow
* numpy

### Pasos para la instalacion

1. Clonar repositorio: git clone https://github.com/lucho28/sistemreco_api.git
2. Crear entorno virtual: python3 -m venv venv
3. Activar entorno virtual
    * Windows: venv\Scripts\activate   
    * macOS/Linux: source venv/bin/activate
4. Instalar las dependencias: pip install -r requirements.txt
5. Comenzar ejecutando de la carpeta Notebook el archivo ETL.ipynb y luego EDA.ipynb.
6. En condiones normales podras desplegar la API en render ya que se recortaron los datos para hacerlo desde la cuenta free que te ofrece.
7. Tambien desde local uvicorn main:app -reload y desde el navegador localhost:8000/docs

## Estructura del Proyecto

* Notebook/ETL.ipynb: En este notebook encontraran la extraccion, transformacion y carga de los datos que luego van a ser consumidos por la API. Esta el proceso de limpieza y transformacion de los datasets leidos de los archivos csv. Que tendran como resultado fina 3 datasets. data_movies, data_credits_actores y data_cradits_directores.
* Notebook/EDA.ipynb: Em este notebook entontraremos un breve analisis de los datasets, donde sacamos algunas conclusiones de los datos.
* Source: Es la carpeta donde luego del ETL guardo los archivos en parquet.
* main.py: Archivo con los endpoint creados para la API.
* README.md: Archivo de documentacion del proyecto.

## Fuentes de datos

La fuente de datos original para este proyecto fueron dos archivos en el formato CSV, los cuales fueron transformados a parquet para un mejor y eficiente manejo de los datos.

## Metodologia

La metodologia abordada fue comenzar primero con el datasets de peliculas llamado data_movies, transformando los datos, revisando valores nulos, columnas candidatas a ser eliminadas, etc.

Considerando que lo que se pide en un MVP se eliminaron algunas columnas mas de las recomendadas. Siguiendo el mismo lineamiento para el dataset data_credits solo de desanidaron los actores y directores con los id de las peliculas.

Esto me sirvio para poder realizar las funciones get_actor y get_director y traer la informacion de ellos con sus respectivos retornos y puntuaciones.

Otro recorte que tuve que hacer es tomar un genero de peliculas dato que al desplegar la api me excedia del limite de memoria brindado por la version free de redner.

Entonces lo que hice fue recordar el dataset data_movies en solo las peliculas que son de animacion y tiene aproximadamente 2000 registros.

Quizas estoy intervenga en el features que le damos a la matriz de la similitud del coseno, asi que agregamos el overview y el año de estreno (release_year).

A partir de aqui se realizaron las funciones que se pedian teniendo en cuenta el chequeo de los datos de entrada y que las salidas sigan un mismo lineamiento (Diccionarios).

## Funciones de la API

1. cantidad_filmaciones_mes(nombre_mes): Devuelve la cantidad de filmaciones estrenadas en un mes especifico ingresado como parametro.
2. cantidad_filmaciones_dia(nombre_dia): Devuelve la cantidad de filmaciones estrenadas en un dia especifico ingresado como parametro.
3. score_titulo(titulo_de_la_filmacion): Devuelve el score/popularidad de un titulo especifico ingresado como parametro.
4. votos_titulo(titulo): Devuelvo los votos si son mayores a 2000 de un titulo especifico ingresado como parametro. Si no llega a los 2000 votos devuelve un mensaje indicandolo.
5. get_actor(nombre_actor): Devuelve la cantidad de peliculas junto con su retorno de un actor especifico ingresado como parametro.
6. get_director(nombre_director): Devuelve la una lista de peliculas junto con sus retornos de un director especifico ingresado como parametro.
7. recomendacion(titulo): Devuelve una lista de 5 peliculas recomendadas similares al titulo ingresado como parametro.

## Contribucion y colaboracion

Los contribuidores son bienvenidos a reportar problemas, enviar solicitudes de funciones o enviar pull requests en el repositorio de GitHub. Antes de contribuir, por favor revisa las pautas de contribución en el archivo CONTRIBUTING.md.

## Autores:

Este proyecto fue realizado por:

* Nombre: Luis Gonzalez.
* Linkedin: www.linkedin.com/in/luis-gonzalez28/
* Mail: luedugonzalez@gmail.com
* Movil: +54 9 2317-514044

