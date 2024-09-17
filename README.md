# Proyecto Data Science - Sistema de recomendación

## Tabla de contenidos

- [Descripción](#Description)
- [Instalación y requisitos](#instalación-y-requisitos)
- [Pasos para la instalación](#pasos-para-la-instalación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Fuentes de datos](#fuentes-de-datos)
- [Metodología](#metodología)
- [Contribución y colaboración](#contribución-y-colaboracion)
- [Autores](#autores)

## Descripción

Este proyecto va a estar centrado en la revisión y procesamiento de 2 DataSets que contendrán información sobre la industria cinematográfica, contando con datos sobre Actores, Directores, Géneros, Títulos como sus mas relevantes.
El foco estará puesto en extraer la información de forma tal que pueda ser analizada, procesada para que luego a través de una API la cual estará desplegada en internet, en render, le brinde al usuario la devolución de peticiones. 
Además la principal funcionalidad sera, darle una lista de 5 películas recomendadas similares a un titulo ingresado por el mismo.

## Instalación y requisitos

* Python 3.11 o superior
* Pandas
* matplotlib
* Scikit-learn
* ast
* seaborn
* pyarrow
* numpy

### Pasos para la instalación

1. Clonar repositorio: git clone https://github.com/lucho28/sistemreco_api.git
2. Crear entorno virtual: python3 -m venv venv
3. Activar entorno virtual
* Windows: venv\Scripts\activate 
* macOS/Linux: source venv/bin/activate
4. Instalar las dependencias: pip install -r requirements.txt
5. Comenzar ejecutando de la carpeta Notebook el archivo ETL.ipynb y luego EDA.ipynb.
6. En condiciones normales podrás desplegar la API en render ya que se recortaron los datos para hacerlo desde la cuenta free que te ofrece.
7. También desde local uvicorn main:app -reload y desde el navegador localhost:8000/docs

## Estructura del Proyecto

* Notebook/ETL.ipynb: En este notebook encontraran la extracción, transformación y carga de los datos que luego van a ser consumidos por la API. Esta el proceso de limpieza y transformación de los datasets leídos de los archivos csv. Que tendrán como resultado fina 3 datasets. data_movies, data_credits_actores y data_cradits_directores.
* Notebook/EDA.ipynb: En este notebook encontraremos un breve análisis de los datasets, donde sacamos algunas conclusiones de los datos.
* Source: Es la carpeta donde luego del ETL guardo los archivos en parquet.
* main.py: Archivo con los endpoint creados para la API.
* README.md: Archivo de documentación del proyecto.

## Fuentes de datos

La fuente de datos original para este proyecto fueron dos archivos en el formato CSV, los cuales fueron transformados a parquet para un mejor y eficiente manejo de los datos.

## Metodología

La metodología abordada fue comenzar primero con el datasets de películas llamado data_movies, transformando los datos, revisando valores nulos, columnas candidatas a ser eliminadas, etc.

Considerando que lo que se pide en un MVP se eliminaron algunas columnas mas de las recomendadas. Siguiendo el mismo lineamiento para el dataset data_credits solo se desanidaron los actores y directores con los id de las películas.

Esto me sirvió para poder realizar las funciones get_actor y get_director, y traer la información de ellos con sus respectivos retornos y puntuaciones.

Otro recorte que tuve que hacer es tomar un genero de películas dado que al desplegar la api me excedía del limite de memoria brindado por la versión free de Render.

Entonces lo que hice fue recortar el dataset data_movies en solo las películas que son de animación y tiene aproximadamente 2000 registros.

Quizás esto intervenga en el features que le damos a la matriz de la similitud del coseno, así que agregamos el overview y el año de estreno (release_year).

Es decir, se hizo una combinacion de genero, sinopsis y años de estreno en una sola matriz y luego se calculo la similitud del coseno en funcion de esas caracteristicas.

A partir de aquí se realizaron las funciones que se pedían teniendo en cuenta el chequeo de los datos de entrada y que las salidas sigan un mismo lineamiento (Diccionarios).

## Funciones de la API

1. cantidad_filmaciones_mes(nombre_mes): Devuelve la cantidad de filmaciones estrenadas en un mes especifico ingresado como parámetro.
2. cantidad_filmaciones_dia(nombre_dia): Devuelve la cantidad de filmaciones estrenadas en un día especifico ingresado como parámetro.
3. score_titulo(titulo_de_la_filmacion): Devuelve el score/popularidad de un titulo especifico ingresado como parámetro.
4. votos_titulo(titulo): Devuelvo los votos si son mayores a 2000 de un titulo especifico ingresado como parámetro. Si no llega a los 2000 votos devuelve un mensaje indicándolo.
5. get_actor(nombre_actor): Devuelve la cantidad de películas junto con su retorno de un actor especifico ingresado como parámetro.
6. get_director(nombre_director): Devuelve la una lista de películas junto con sus retornos de un director especifico ingresado como parámetro.
7. recomendacion(titulo): Devuelve una lista de 5 películas recomendadas similares al titulo ingresado como parámetro.

## Contribución y colaboración

Los contribuidores son bienvenidos a reportar problemas, enviar solicitudes de funciones o enviar pull requests en el repositorio de GitHub. Antes de contribuir, por favor revisa las pautas de contribución en el archivo CONTRIBUTING.md.

## Autores:

Este proyecto fue realizado por:

* Nombre: Luis Gonzalez.
* Linkedin: www.linkedin.com/in/luis-gonzalez28/
* Mail: luedugonzalez@gmail.com
* Móvil: +54 9 2317-514044
