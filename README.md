# Proyecto Recomendaciones de Peliculas
## Introducción
Este proyecto tiene como objetivo crear un sistema de recomendación de películas basado en datos suministrados por 2 bases de datos iniciales que son movies_dataset.csv y credits.csv (se pueden encontrar en la carpeta db_movies). Para lograr esto, se realizaron varias etapas, incluyendo la Extracción, Transformación y Carga de datos (ETL), el Análisis Exploratorio de Datos (EDA), creación de funciones para averiguar algunos datos de las peliculas y por ultimo el sistema de recomendación.
## Contenido
- ETL y EDA
- Funciones
- Sistema de Recomendación
## ETL y EDA
En este proyecto, utilizamos las siguientes bibliotecas para realizar la extracción, transformación y carga de datos (ETL):

- pandas: para trabajar con datos tabulares.
- numpy: para realizar operaciones numéricas y arreglos.
- ast: para trabajar con evaluación de expresiones literales de Python.
- re: para trabajar con expresiones regulares.
- os: para operaciones relacionadas con el sistema.

Para el desarrollo del ETL y EDA se comenzo leyendo el archivo movies_dataset.csv y el archivo credits.parquet (Ambos se encuentran comprimidos en la carpeta db_movies, es posible que se tenga que modificar la ruta al momento de usar el codigo), se hace una inspección rapida de cada uno de los dataframe creados y se empiezan a desanidar los datos que se necesitan, para la columna **belongs_to_collection** se recorrieron los valores de la columna belongs_to_collection y verificamos si cada valor es nulo o no. Si el valor no es nulo, utilizamos ast.literal_eval para convertir la cadena en un diccionario. Luego, creamos un DataFrame a partir de ese diccionario y lo agregamos a la lista dataframes_desanidados. Si el valor es nulo, creamos un DataFrame con el valor nulo y también lo agregamos a la lista.

Este proceso de desanidamiento nos permite trabajar con los datos anidados de forma más fácil, luego concatenamos los datos en la lista para que se puedan trabajar como un dataframe con las nuevas columnas que se desanidaron y por ultimo cambiamos el nombre de las columnas para que no se repitan.

Para **genders**:
Se define un patrón de búsqueda utilizando expresiones regulares para extraer el ID del género de la columna "genres". Luego, se rellenan los valores nulos en esa columna con una cadena vacía y se aplica una función lambda para buscar el ID del género en cada valor. Los resultados se almacenan en un nuevo DataFrame llamado genres_id.

Después, se aplica otra función lambda a cada elemento del DataFrame genres_id para combinar los IDs de género en una cadena separada por comas. Finalmente, se renombra la columna "genres" a "genres_id" para reflejar el contenido transformado.

Este proceso nos permite obtener los IDs de género de manera estructurada y prepararlos para su posterior análisis, se aplico el mismo procedimiento para sacar "name", al igual que para desanidar las otras columnas que son , **production_countries**, **production_companies**, **spoken_languages**.

Luego se combinan los dataframes resultados de este proceso de desanidación, (Esto es posible ya que todos tienen el mismo numero de filas y mantinene su orden por que los valores nulos se mantienen), se unen con el dataframe inicial, donde ya es posible borrar las columnas que desanidamos.

Para la columna **revenue** se verifica la cantidad de valores nulos en la columna. A continuación, se rellenan los valores nulos en la misma columna con 0 utilizando el método fillna(0).

Siguiendo con la columna **release_date**, esta se convierte al tipo de datos datetime en el DataFrame df_limpio utilizando el método pd.to_datetime(). Se utiliza el argumento errors="coerce" para manejar cualquier error en la conversión luego, se obtiene el número de valores no nulos en la columna utilizando el método count(). Además, se obtiene la suma de valores nulos en la misma columna.
Por último, se eliminan las filas que contienen valores nulos en la columna utilizando el método dropna() con el argumento subset=["release_date"] e inplace=True.
Este proceso nos permite tener la columna **release_date** en un formato adecuado y sin valores nulos, lo cual es importante para realizar análisis y visualizaciones posteriores.

Para crear una columna nueva llamada **return** necesitaremos las columnas **revenue y budget**, el cual haciendo un analisis rapido se puede obervar que **budget** es de tipo **str**, se pasara a float y se crea una nueva columna en el DataFrame, que contiene la relación **revenue/budget**, en el caso que de inf el resultado se remplaza por 0.

Se eliminan las columnas **video, imdb_id, adult, original_title, poster_path, homepage** ya que no van a servirnos de nada para nuestras funciones.

Se utiliza el atributo dt.year de la columna "**release_date** para obtener el año de lanzamiento de cada película y se asigna a la nueva columna **release_year**, esta nueva columna es útil para realizar análisis o filtrar los datos por año de lanzamiento de las películas.

Para empezar con credits, nos damos cuenta que toca desanidar los datos de las columnas **cast y crew**.

Se crea la función **desanidar_cast**, es utilizada para desanidar los datos de la columna **cast** en el DataFrame. Esta columna contiene información sobre el elenco de actores de cada película, pero los datos están anidados.
La función utiliza expresiones regulares para extraer los atributos deseados de los datos de la columna. Estos atributos incluyen **cast_id, character, credit_id, gender, id', name, order y profile_path**, esta funciona de la siguiente manera:
1. La función recibe como argumento la columna **cast** y realiza las siguientes operaciones.
2. Utiliza expresiones regulares para extraer los valores de cada atributo de la cadena de texto de la columna.
3. Crea un DataFrame para cada atributo extraído.
4. Se renombran las columnas en el DataFrame.
5. Concatena los DataFrames de cada atributo en un único DataFrame resultante.
6. Devuelve el DataFrame resultante que contiene los atributos desanidados del elenco.

Para la columna **crew** se crea la funcion **desanidar_crew** que funciona de la misma forma que **desanidar_cast**.

Se unen estos dos DataFrames nuevos.

Se utiliza **Merge** para combinar los dos DataFrames "originales" ya limpios usando la columna **id**.

Para finalizar se crean 5 archivos nuevos (los puedes encontrar en la carpeta **db_movies**), estos se usaran para las funciones.

## Funciones







