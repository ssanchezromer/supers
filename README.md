![imagen_cabecera](https://github.com/ssanchezromer/supers/assets/148953141/41c8b979-8845-4bb0-9770-c1bb3a268a37)

# Tipología y ciclo de vida de los datos - UOC
## Webscraping practice 1 - Supermarket price comparison

Este proyecto es una práctica de la asignatura "Tipología y ciclo de vida de los datos" del Máster en Ciencia de Datos de la UOC.

Hemos creado un raspador web que extrae los precios de los productos de los principales supermercados en España y los compara. Finalmente, los resultados se guardan en un archivo CSV y hemos creado una aplicación Flask para visualizar los resultados.

## Contexto
En esta actividad se ha llevado a cabo la recopilación de datos con el propósito de comparar los precios de los productos en tres supermercados diferentes: Mercadona, Caprabo y Bonpreu.

Sitios web (enlaces):
Mercadona: https://tienda.mercadona.es/
Caprabo: https://www.capraboacasa.com/es
Bonpreu: https://www.bonpreuesclat.cat/es/home

Esta iniciativa se ha desarrollado en respuesta a la notable subida de precios de diferentes productos, como puede ser el aceite de oliva, un hecho que ha impactado en la economía de los consumidores, y por consiguiente ha generado un creciente interés de identificar las opciones de compra más económicas.

## Grupo de trabajo:

Sergi Sánchez Romer
Lucia Blanc Velázquez

## Contenido del repositorio:

**Readme.md: Expone de forma breve el contenido de la práctica**

**src/*.*: Scripts con el código del programa**

**csv/products.csv: Incluye el conjunto de datos resultante y también en cada carpeta del supermercado se incluye el csv referente a cada uno de los sitios webs scrapeados.**

**app/*.*: Scripts con el código para inicializar la app de Flask.**

**pdf/ProductsSupers.pdf: Documento pdf con el contenido explicado de la práctica**

**video/*.*: Video de presentación de la práctica.**

## DOI del dataset generado
El Dataset generado contiene el título **Comparación de los productos de Mercadona, Caprabo y Bonpreu** y se encuentra publicado en Zenodo.

![zenodo 10086087 png](https://github.com/ssanchezromer/supers/assets/148953141/56f8f9f2-c2c9-4e00-b5ab-aa44bda9af12)

## Pasos a seguir para la creación del entorno y la inicialización del scraping:

**1. Crear entorno:**

> python -m venv env_name

**2. Activar entorno:**

  Windows:

> env_name\Scripts\activate

  MacOS & Linux:

> env_name/bin/activate

**3. Instalación de librerías:**

> pip install -r requirements.txt

**4. Ejecución del programa**

> python main.py
