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
El foco estara puesto en extraer la informacion de forma tal que pueda ser analisada, procesada para que luego a traves de una API la cual estara desplegada en internet, a traves de render, le brinde al usuario la devolucion de peticiones. 
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

## Estructura del Proyecto

* etl.ipynb: Contiene los notebooks con la extraccion, transformacion y carga de los datos que despues seran consumidos por la API.
* credits.parquet: Archivo con el dataset de credits creado luego del etl para ser consumido por la API.
* movies.parquet: Archivo con el dataset de Movies creado luego del etl para ser consumido por la API.
* main.py: Archivo con los endpoint creados para la API.
* README.md: Archivo de documentacion del proyecto.

## Fuentes de datos

La fuente de datos original para este proyecto fueron dos archivos en el formato CSV, los cuales fueron transformados a parquet para un mejor y eficiente manejo de los datos.

## Metodologia

Principalmente de utilizaron funciones y librerias de python para tener los datasets ordenados, limpios. Luego de eso, se produjo a recortar los datasets con el proposito de no forzar el procesamiento de los entornos a utilizar, tambien teniendo en cuenta que estamos por desarrollar un MPV.

## Contribucion y colaboracion

Los contribuidores son bienvenidos a reportar problemas, enviar solicitudes de funciones o enviar pull requests en el repositorio de GitHub. Antes de contribuir, por favor revisa las pautas de contribución en el archivo CONTRIBUTING.md.

## Autores:

Este proyecto fue realizado por: Luis Gonzalez.
* Linkedin: www.linkedin.com/in/luis-gonzalez28/
* Mail: luedugonzalez@gmail.com
* Movil: +54 9 2317-514044

