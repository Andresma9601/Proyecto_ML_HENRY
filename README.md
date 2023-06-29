# Proyecto Recomendaciones de Peliculas
## Introducción
Este proyecto tiene como objetivo crear un sistema de recomendación de películas basado en datos suministrados por 2 bases de datos iniciales que son movies_dataset.csv (se pueden encontrar en la carpeta db_movies dividido en 2 partes, movies_dataset1.csv y movies_dataset2.csv ) y credits.parquet (se pueden encontrar en la carpeta db_movies dividido en 3 partes, como credits1.parquet, credits2.parquet y credits3.parquet), para cada uno de los DataBase se concatenan sus partes con axis=0 osea uno debajo del otro, se reinicia el index y los tenemos listos para trabajas. 

Para lograr el proyecto, se realizaron varias etapas, incluyendo la Extracción, Transformación y Carga de datos (ETL), el Análisis Exploratorio de Datos (EDA), creación de funciones para averiguar algunos datos de las peliculas y por ultimo el sistema de recomendación.
## Contenido
- ETL y EDA
- Funciones
- Sistema de Recomendación
- Dirección a la API
## ETL y EDA
En este proyecto, utilizamos las siguientes bibliotecas para realizar la extracción, transformación y carga de datos (ETL):

- pandas: para trabajar con datos tabulares.
- numpy: para realizar operaciones numéricas y arreglos.
- ast: para trabajar con evaluación de expresiones literales de Python.
- re: para trabajar con expresiones regulares.
- os: para operaciones relacionadas con el sistema.

Para el desarrollo del ETL y EDA se comenzo leyendo el archivo movies_dataset.csv y el archivo credits.parquet (Ambos se encuentran en la carpeta db_movies, como se hablo en la introduccion se encuentran divididos), se hace una inspección rapida de cada uno de los dataframe creados y se empiezan a desanidar los datos que se necesitan, para la columna **belongs_to_collection** se recorrieron los valores de la columna **belongs_to_collection** y verificamos si cada valor es nulo o no. Si el valor no es nulo, utilizamos ast.literal_eval para convertir la cadena en un diccionario. Luego, creamos un DataFrame a partir de ese diccionario y lo agregamos a la lista dataframes_desanidados. Si el valor es nulo, creamos un DataFrame con el valor nulo y también lo agregamos a la lista.

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
Se importan las bibliotecas necesarias, como:
- FastAPI
- pandas
- TfidfVectorizer
- KMeans
- cosine_similarity.

A continuación, se crea una instancia de la aplicación FastAPI utilizando app = FastAPI(). Esto permite crear una API web que escucha y responde a las solicitudes entrantes.

Se define una ruta raíz mediante el decorador @app.get("/"). Esta ruta se accede a través de la URL base "http://127.0.0.1:8000/". Cuando se accede a esta ruta, se devuelve un diccionario con un mensaje de bienvenida.

Se crea la variable **DOWNLOAD_ROOT** contiene una URL base que se utilizará más adelante en el código.

Se define una nueva ruta en la API llamada "/peliculas_mes/{mes}". Esta ruta espera recibir un parámetro "mes" que representa el nombre de un mes en español.

Se define un diccionario para traducir los meses de ingles a españl, luego se crea la función **cantidad_filmaciones_mes** para calcular la cantidad de filmaciones que se estrenaron en un mes específico.
Dentro de la función, se especifica la ruta relativa del archivo CSV que contiene los datos de las películas por día. Luego, se combina la URL base (**DOWNLOAD_ROOT**) con la ruta relativa para obtener la URL completa del archivo CSV.
A continuación, se procede a leer el archivo CSV desde la URL completa y almacenar los datos en un DataFrame.
Se convierte la columna **release_date** del DataFrame a tipo datetime utilizando pandas, luego, el mes ingresado se convierte a minúsculas para que coincida con los datos del DataFrame. Se verifica si el mes ingresado está presente en el diccionario que mapea los meses en español a los meses en inglés.
Si el mes está presente en el diccionario, se obtiene la traducción al inglés. Se filtran las filas del DataFrame que corresponden al mes consultado, finalmente, se cuenta la cantidad de filmaciones en el mes consultado utilizando len(filmaciones_mes) y se devuelve un mensaje que indica la cantidad de películas estrenadas en ese mes.
Si el mes ingresado no está en el diccionario, se devuelve un mensaje indicando que no es un mes en español.

Se crea la función **cantidad_filmaciones_dia** que recibe como parámetro dia, que representa el día de la semana en español del cual se desea conocer la cantidad de filmaciones.
El primer paso es definir un diccionario llamado dias_dict que mapea los nombres de los días de la semana en español a sus equivalentes en inglés. Esto se realiza para poder realizar una comparación adecuada con los datos del DataFrame.
Luego, se lee un archivo CSV que contiene datos de filmaciones, utilizando la ruta relativa del archivo y la URL base para obtener la URL completa del archivo CSV. El archivo se lee y se almacena en el DataFrame.
Después, se convierte la columna **release_date** del DataFrame de tipo string a tipo datetime.
A continuación, se convierte el parámetro dia a minúsculas para asegurarnos de que coincida con los datos del DataFrame.
Se verifica si el día ingresado está presente en el diccionario **dias_dict**. Si está presente, se obtiene su equivalente en inglés. Si el día ingresado no está en el diccionario, se retorna un mensaje indicando que no es un día en español válido.
Si el día ingresado está en el diccionario, se filtran las películas que fueron estrenadas en el día consultado. Esto se realiza utilizando una comparación entre el nombre del día de la columna **release_date** y el día en inglés obtenido del diccionario. El resultado se almacena en una variable.
Finalmente, se obtiene la cantidad de filmaciones en el día consultado utilizando la función y se retorna un mensaje indicando la cantidad de películas estrenadas en ese día.

Se crea la función **score_titulo**  que busca la puntuación y la información relacionada de una película específica.
En primer lugar, se establece la ruta relativa del archivo CSV que contiene los datos de puntuación de las películas en una variable. Luego, se combina la URL base con la ruta relativa para obtener la URL completa del archivo CSV. A continuación, se lee el archivo CSV desde la URL completa y se almacena en un DataFrame.
El título de la película ingresado se convierte a minúsculas para asegurar una comparación adecuada con los datos del DataFrame.
A continuación, se itera sobre los títulos de las películas en la columna **title** del DataFrame. Para cada título de película, se convierte a minúsculas y se verifica si coincide con el título ingresado. Si hay una coincidencia, se procede a filtrar el DataFrame para obtener los datos de la película encontrada.
Se obtienen datos específicos de la película encontrada, como el título, el año de estreno y el score/popularidad, utilizando la función **iloc** para acceder a las filas y columnas correspondientes en el DataFrame filtrado.
Por último, se retorna un mensaje que contiene los datos de la película encontrada, incluyendo el título, el año de estreno y el score/popularidad.
Si no se encuentra ninguna película con el título ingresado en la lista, se retorna un mensaje indicando que no se encontró la película.

Se crea la función **votos_titulo** busca la información de votos de una película específica.
En primer lugar, se establece la ruta relativa del archivo CSV que contiene los datos de votos de las películasen una variable. Luego, se combina la URL base con la ruta relativa para obtener la URL completa del archivo CSV. A continuación, se lee el archivo CSV desde la URL completa y se almacena en el DataFrame.
El título de la película ingresado se convierte a minúsculas para asegurar una comparación adecuada con los datos del DataFrame.
A continuación, se itera sobre los títulos de las películas en la columna "title" del DataFrame. Para cada título de película, se convierte a minúsculas y se verifica si coincide con el título ingresado. Si hay una coincidencia, se procede a filtrar el DataFrame para obtener los datos de la película encontrada.
Se crea un DataFrame diferente con las columnas **title, vote_count, vote_average y release_year**. Luego, se filtra el DataFrame para obtener las filas con el título de la película actual.
A continuación, se itera sobre los valores de **vote_count** en el DataFrame filtrado. Si el valor  es mayor o igual a 2000, se obtienen los valores de la primera fila del DataFrame filtrado, que corresponden al título de la película, el total de votos, el promedio de votos y el año de estreno. Luego, se devuelve un mensaje que contiene esta información.
Si el valor de la columna es menor a 2000, se devuelve un mensaje indicando que la película no cumple con la condición de tener al menos 2000 votos.
Si el título de la película no se encuentra en la lista, se devuelve un mensaje indicando que no es una película de la lista.

Se crea la función **get_actor** que busca información sobre la participación de un actor en películas.
En primer lugar, se establece la ruta relativa del archivo CSV que contiene los datos de actores, Luego, se combina la URL base con la ruta relativa para obtener la URL completa del archivo CSV. A continuación, se utiliza la función para leer el archivo CSV desde la URL completa y se almacena en un DataFrame
Se seleccionan las columnas **cast_name y return** del DataFrame, que corresponden al nombre del actor y al retorno de cada película en la que participó.
Luego, se realiza una búsqueda en la columna **cast_name** para verificar si el nombre del actor ingresado está presente. El resultado de la búsqueda se convierte en un DataFrame llamado peliculas_participante. Se renombra la columna **cast_name** del DataFrame a **bool** para indicar si el actor participó o no en cada película.
A continuación, se concatena el DataFrame obtenido anteriormente con el DataFrame original para tener toda la información en un solo DataFrame.
Se itera sobre los valores de la columna **bool** en el DataFrame. Si se encuentra al menos un valor True, se filtran las filas del DataFrame donde el valor de la columna es True, es decir, donde el actor participó en la película. Se calcula el total de películas en las que el actor ha participado, el retorno total obtenido por el actor y el promedio de retorno por película.

La función **get_director** busca información sobre las películas dirigidas por un director específico.
En primer lugar, se establece la ruta relativa del archivo CSV que contiene los datos de directores y películas, luego, se combina la URL base con la ruta relativa para obtener la URL completa del archivo CSV. A continuación, se utiliza la función para leer el archivo CSV desde la URL completa y se almacena en el DataFrame.
Se seleccionan las columnas relevantes del DataFrame, que incluyen el trabajo del director, su nombre, la fecha de estreno de la película, el retorno, los ingresos y el presupuesto de la película, y el título de la película.
Luego, se realiza una búsqueda en la columna **crew_name** para verificar si el nombre del director ingresado está presente. El resultado de la búsqueda se convierte en un DataFrame. Se renombra la columna **crew_name** del DataFrame a **bool** para indicar si el director dirigió o no cada película.
A continuación, se concatena el DataFrame obtenido anteriormente con el DataFrame original. para tener toda la información en un solo DataFrame.
Se itera sobre los valores de la columna **bool**. Si se encuentra al menos un valor True, se filtran las filas del DataFrame donde el valor es True, es decir, donde el director ha dirigido la película. Se seleccionan las columnas relevantes en el DataFrame resultante y se crea una lista para almacenar los resultados.
Luego, se itera sobre las filas del DataFrame. En cada iteración, se obtiene el título de la película, el retorno, los ingresos y el presupuesto. Se agrega un mensaje a la lista con esta información.
Finalmente, se devuelve la lista, que contiene los mensajes con la información de las películas dirigidas por el director especificado.
Si no se encuentra ninguna coincidencia, se devuelve un mensaje indicando que el director no ha dirigido ninguna película de la lista.

## Sistema de recomendación
Para este pedazo del proyecto intentare explicar de manera mas detallas y mas clara cada paso que se hizo para realizar este modelo:

1. Se define la ruta relativa del archivo CSV que contiene los datos de las películas en la variable data_movies. Esta ruta es la ubicación del archivo dentro del sistema de archivos.

2. Se utiliza la función read_csv de la biblioteca Pandas para cargar el archivo CSV en el DataFrame data.

3. En esta parte, se realiza una preparación de los datos en el DataFrame data. Se seleccionan las columnas relevantes para el análisis, que incluyen el título de la película, su popularidad, fecha de lanzamiento, duración y calificación promedio de votos. Además, se eliminan las filas que contienen valores faltantes (NaN) utilizando el método dropna(). Esto asegura que solo se utilicen películas con datos completos.

4. Se crea una instancia del vectorizador TF-IDF (TfidfVectorizer). TF-IDF es una técnica de procesamiento de lenguaje natural que asigna un valor a cada palabra en función de su frecuencia en un documento y en el corpus general. En este caso, se utiliza para convertir el texto del título de las películas en una representación numérica.

5. El vectorizador se aplica a los textos de las películas en el DataFrame data. Se concatenan las columnas relevantes que contienen información sobre el título, fecha de lanzamiento, duración y calificación promedio de votos. Esto se hace para capturar diferentes aspectos de las películas en la representación numérica. La función fit_transform del vectorizador transforma los datos de texto en una matriz numérica densa llamada X, que contiene las características numéricas de cada película.

6. Se define el número de clústeres k como 10. Un clúster es un grupo de elementos similares. Aquí se utiliza el algoritmo de agrupación k-means para agrupar las películas en función de sus características. Se crea una instancia del modelo KMeans con el número de clústeres especificado y un valor de random_state para reproducibilidad.

7. El modelo k-means se ajusta a los datos utilizando el método fit(). Esto significa que el algoritmo encuentra los clústeres que mejor representan las películas en función de sus características. Los clústeres se determinan de manera iterativa, minimizando la distancia entre las películas dentro de cada clúster y maximizando la distancia entre los clústeres.

8. El título de la película de consulta se vectoriza utilizando el mismo vectorizador TF-IDF. Esto se hace para obtener su representación numérica correspondiente. El título se convierte a minúsculas antes de la vectorización.

9. Se calcula la similitud coseno entre el título de la película de consulta vectorizado y todos los títulos de películas en el conjunto de datos. La similitud coseno es una medida que indica qué tan similares son dos vectores. Aquí se utiliza para medir la similitud entre el título de la película de consulta y los títulos de todas las películas en el conjunto de datos. Esto se hace utilizando la función cosine_similarity().

10. Se obtiene el índice de la película de consulta en el DataFrame data utilizando la función index. Esto nos dará la ubicación de la película en el DataFrame.

11. Las similitudes calculadas se ordenan en orden descendente utilizando el método argsort(). Esto nos dará los índices de las películas en el orden de su similitud con la película de consulta.

12. Se itera sobre los índices de las películas similares y se agregan los títulos al resultado final en la lista peliculas_similares. Si el índice corresponde a la película de consulta, se omite. Se limita la lista a las primeras 5 películas similares encontradas.

13. Finalmente, se devuelve la lista de títulos de películas similares como resultado.

## Dirección de la API
Aca puedes entrar a hacer tus consultas https://peliculas-2c5w.onrender.com/docs
