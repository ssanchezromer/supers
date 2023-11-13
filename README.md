![imagen_cabecera](https://github.com/ssanchezromer/supers/assets/148953141/41c8b979-8845-4bb0-9770-c1bb3a268a37)

# Tipología y ciclo de vida de los datos - UOC
## Webscraping práctica 1 - Comparación precios supermercados

Este proyecto es una práctica de la asignatura "Tipología y ciclo de vida de los datos" del Máster en Ciencia de Datos de la UOC.

Hemos creado un raspador web que extrae los precios de los productos de los principales supermercados en España y los compara. Finalmente, los resultados se guardan en un archivo CSV y hemos creado una aplicación Flask para visualizar los resultados.

## Contexto
En esta actividad se ha llevado a cabo la recopilación de datos con el propósito de comparar los precios de los productos en tres supermercados diferentes: Mercadona, Caprabo y Bonpreu.

Sitios web (enlaces):
<ul>
<li><strong>Mercadona:</strong>&nbsp;&nbsp;<a href="https://tienda.mercadona.es/" target="_blank">https://tienda.mercadona.es/</a></li>
<li><strong>Caprabo:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.capraboacasa.com/es" target="_blank">https://www.capraboacasa.com/es</a></li>
<li><strong>Bonpreu:</strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://www.compraonline.bonpreuesclat.cat/products" target="_blank">https://www.compraonline.bonpreuesclat.cat/products</a></li>
</ul>

Esta iniciativa se ha desarrollado en respuesta a la notable subida de precios de diferentes productos, como puede ser el aceite de oliva, un hecho que ha impactado en la economía de los consumidores, y por consiguiente ha generado un creciente interés de identificar las opciones de compra más económicas.

## Grupo de trabajo:

Sergi Sánchez Romero

Lucia Blanc Velázquez


## Contenido del repositorio:

- **Readme.md:** Expone de forma breve el contenido de la práctica.
- **source/.:** Carpeta con el código del programa principal (**main.py**) y el de la aplicación Flask (**run.py**). Además incluye:
  - **app/.:** Carpeta con el código para inicializar la app de Flask.
  - **csv/.:** Carpeta que incluye el conjunto de datos resultante (products.csv) y también en cada carpeta del supermercado se incluye el csv referente a cada uno de los sitios webs scrapeados.
  - **modules/.:**: Carpeta con las librerías necesarias
  - **requirements.txt:** Archivo con las librerías necesarias para el entorno de la práctica.
- **pdf/comparacionPrecioSupers.pdf:** Documento pdf con el contenido explicado de la práctica.
- **video/.:** Video de presentación de la práctica.
  



## DOI del dataset generado
El Dataset generado contiene el título **Comparación de los productos de Mercadona, Caprabo y Bonpreu** y se encuentra publicado en Zenodo.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10086087.svg)](https://doi.org/10.5281/zenodo.10086087)

## Pasos a seguir para la creación del entorno y la inicialización del scraping:

Una vez descargado el código de la carpeta **source** realizaremos los siguientes pasos para poder ejecutar la aplicación:

**1. Crear entorno:**

> python -m venv *env_name*

**2. Activar entorno:**

  Windows:

> *env_name*\Scripts\activate

  MacOS & Linux:

> *env_name*/bin/activate

**3. Instalación de librerías:**

> pip install -r requirements.txt

**4. Ejecución del programa**

> python main.py
