![zenodo 10086087](https://github.com/ssanchezromer/supers/assets/148953141/ced0a9ec-c9d4-4fe8-9248-0d86906a3416)![Header](/app/static/imagen_cabecera.png)

# Tipología y ciclo de vida de los datos - UOC
## Webscraping practice 1 - Supermarket price comparation
Este proyecto es una práctica de la asignatura "Tipología y ciclo de vida de los datos" del Máster en Ciencia de Datos de la UOC.

Hemos creado un raspador web que extrae los precios de los productos de los principales supermercados en España y los compara.
Finalmente, los resultados se guardan en un archivo CSV y hemos creado una aplicación Flask para visualizar los resultados.

### Contexto
En esta actividad se ha llevado a cabo la recopilación de datos con el propósito de comparar los precios de los productos en tres supermercados diferentes: Mercadona, Caprabo y Bonpreu. 

Sitios web (enlaces):
Mercadona : https://tienda.mercadona.es/ 
Caprabo: https://www.capraboacasa.com/es 
Bonpreu: https://www.bonpreuesclat.cat/es/home 

Esta iniciativa se ha desarrollado en respuesta a la notable subida de precios de diferentes productos, como puede ser el aceite de oliva, un hecho que ha impactado en la economía de los consumidores, y por consiguiente ha generado un creciente interés de identificar las opciones de compra más económicas. 

### Grupo de trabajo: 

Sergi Sánchez Romer
Lucia Blanc Velázquez


### Contenido del repositorio:

**Readme.md: Expone de forma breve el contenido de la práctica**
**src/*.*: Scripts con el código del programa**
**csv/products.csv: Incluye el conjunto de datos resultante y también en cada carpeta del supermercado se incluye el csv referente a cada uno de los sitios webs scrapeados.**
**app/*.*: Scripts con el código para inicializar la app de Flask.**
**pdf/ProductsSupers.pdf: Documento pdf con el contenido explicado de la práctica**
**video/*.*: Video de presentación de la práctica.**


### DOI del dataset generado
El Dataset generado contiene el título **Comparación de los productos de Mercadona, Caprabo y Bonpreu** y se encuentra publicado en Zenodo. 

![Uploadin<svg xmlns="http://www.w3.org/2000/svg"
     width="190.859375" height="20">
        <linearGradient id="b" x2="0" y2="100%">
            <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
            <stop offset="1" stop-opacity=".1"/>
        </linearGradient>
        <mask id="a" width="190.859375" height="20">
            <rect width="190.859375" height="20" rx="3"
            fill="#fff"/>
        </mask>
        <g mask="url(#a)">
            <path fill="#555" d="M0 0h31.375v20H0z" />
            <path fill="#007ec6"
            d="M31.375 0h159.484375v20H31.375z"
            />
            <path fill="url(#b)" d="M0 0h190.859375v20H0z" />
        </g>
        <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,
        Verdana,Geneva,sans-serif" font-size="11">
            <text x="16.1875" y="15" fill="#010101"
            fill-opacity=".3">
                DOI
            </text>
            <text x="16.1875" y="14">
                DOI
            </text>
            <text x="110.6171875"
            y="15" fill="#010101" fill-opacity=".3">
                10.5281/zenodo.10086087
            </text>
            <text x="110.6171875" y="14">
                10.5281/zenodo.10086087
            </text>
        </g>
    </svg>g zenodo.10086087.svg…]()


### Pasos a seguir para la creación del entorno y inicialización del scraping: 
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
