# Proyecto Recomendaciones de Peliculas
## Introducción
Este proyecto tiene como objetivo crear un sistema de recomendación de películas basado en datos suministrados por 2 bases de datos iniciales que son movies_dataset.csv y credits.csv (se pueden encontrar en la carpeta db_movies). Para lograr esto, se realizaron varias etapas, incluyendo la Extracción, Transformación y Carga de datos (ETL), el Análisis Exploratorio de Datos (EDA), creación de funciones para averiguar algunos datos de las peliculas y por ultimo el sistema de recomendación.
## Contenido
- ETL
- EDA
- Funciones
- Sistema de Recomendación
## ETL
En este proyecto, utilizamos las siguientes bibliotecas para realizar la extracción, transformación y carga de datos (ETL):

- pandas: para trabajar con datos tabulares.
- numpy: para realizar operaciones numéricas y arreglos.
- ast: para trabajar con evaluación de expresiones literales de Python.
- re: para trabajar con expresiones regulares.
- os: para operaciones relacionadas con el sistema.

Para el desarrollo del ETL se comenzo leyendo el archivo movies_dataset.csv y el archivo credits.parquet (Ambos se encuentran comprimidos en la carpeta db_movies), se hace una inspección rapida de cada uno de los dataframe creados y se empiezan a desanidar los datos que se necesitan, para la columna **belongs_to_collection** se recorrieron los valores de la columna belongs_to_collection y verificamos si cada valor es nulo o no. Si el valor no es nulo, utilizamos ast.literal_eval para convertir la cadena en un diccionario. Luego, creamos un DataFrame a partir de ese diccionario y lo agregamos a la lista dataframes_desanidados. Si el valor es nulo, creamos un DataFrame con el valor nulo y también lo agregamos a la lista.

Este proceso de desanidamiento nos permite trabajar con los datos anidados de forma más fácil, luego concatenamos los datos en la lista para que se puedan trabajar como un dataframe con las nuevas columnas que se desanidaron y por ultimo cambiamos el nombre de las columnas para que no se repitan

