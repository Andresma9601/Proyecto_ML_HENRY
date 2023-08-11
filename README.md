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

Ahora para el EDA se visualizo toda la información de las 42 columnas que quedaron y se escogieron las siguientes:
1.	**Budget**: Presupuesto de la película (valor numérico).
2.	**original_language**: Idioma original de la película (valor categórico).
3.	**popularity**: Popularidad de la película (valor numérico).
4.	**release_date**: Fecha de lanzamiento de la película (valor categórico).
5.	**revenue**: Ganancias de la película (valor numérico).
6.	**runtime**: Duración de la película en minutos (valor numérico).
7.	**title**: Título de la película (texto).
8.	**vote_average**: Promedio de votos de la película (valor numérico).
9.	**vote_count**: Cantidad de votos de la película (valor numérico).
10.	**genres_name**: Géneros de la película (valor categórico).
11.	**name_production_company**: Nombre de la compañía de producción (valor categórico).
12.	**name_country**: Nombre del país de origen de la película (valor categórico).
13.	**language**: Idioma de la película (valor categórico).
14.	**return**: Valor de retorno de la película (valor numérico).
15.	**release_year**: Año de lanzamiento de la película (valor numérico).
16.	**cast_name**: Nombre del elenco de la película (valor categórico).
17.	**job**: Trabajo realizado por el equipo de producción (valor categórico).

A partir de estas columnas se creo un nuevo DataFrame con el cual se dividieron en variables numericas y categoricas, luego de un corto analisis exploratorio de datos se logro evidenciar que las mejores columnas para trabajar en el modelo de recomendacion fueron:
1.	**title**: El título de una película o contenido puede ser una característica importante para los usuarios, ya que es uno de los elementos más visibles y reconocibles. Los usuarios suelen tener preferencias específicas en términos de género, actores o temas específicos que pueden estar relacionados con el título.
2.	**genres_name**: Los géneros cinematográficos son una forma común de categorizar y agrupar películas o contenido similar. Los usuarios a menudo tienen preferencias claras en términos de géneros que les gustan o no les gustan. Incluir esta variable puede ayudar al modelo a comprender las preferencias de los usuarios y ofrecer recomendaciones más relevantes basadas en los géneros preferidos.
3.	**vote_average**: La calificación promedio de una película o contenido puede ser un indicador de su calidad percibida. Los usuarios a menudo confían en las calificaciones y críticas para seleccionar contenido. Incluir esta variable puede ayudar al modelo a tener en cuenta la calidad percibida y ofrecer recomendaciones que se alineen con las preferencias de calidad de los usuarios.
4.	**vote_count**: El número de votos recibidos por una película o contenido puede ser un indicador de su popularidad o relevancia. Las películas populares o con un alto número de votos suelen ser más conocidas y pueden tener un mayor atractivo para los usuarios. Incluir esta variable puede ayudar al modelo a tener en cuenta la popularidad y ofrecer recomendaciones que reflejen las preferencias de contenido popular.

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

La función **peliculas_idioma** tiene como objetivo determinar cuántas películas están disponibles en un idioma específico en base a un archivo CSV que contiene información sobre diversas películas.

Primero, se define una ruta relativa al archivo CSV mediante la variable df_idioma.

Luego, se combina la ruta relativa con una URL base (que se presume definida en otra parte del código) para obtener la ruta completa al archivo CSV, que se almacena en la variable csv_path.

Se utiliza la biblioteca Pandas para leer el contenido del archivo CSV desde la ruta completa definida en csv_path, creando un DataFrame llamado df_idioma.

Del DataFrame df_idioma, se selecciona solamente la columna "language" para crear un nuevo DataFrame llamado df, que contiene únicamente información sobre los idiomas de las películas.

Se realiza una búsqueda en la columna "language" del DataFrame df para determinar si el idioma proporcionado está presente en alguna de las entradas. La búsqueda se realiza sin considerar las diferencias entre mayúsculas y minúsculas (case=False).

Los resultados de la búsqueda se almacenan en un nuevo DataFrame llamado peliculas. Cada fila de este DataFrame contiene un valor booleano que indica si la película está en el idioma especificado.

Se renombra la columna "language" en el DataFrame peliculas a "bool" para reflejar que los valores son booleanos que representan si la película está en el idioma deseado.

Se concatena el DataFrame peliculas con el DataFrame original df, creando un nuevo DataFrame llamado df2. Este DataFrame incluye tanto la columna booleana "bool" como la columna original "language".

Luego, se itera a través de los valores de la columna "bool" en el DataFrame df2.

Si en algún punto durante la iteración se encuentra un valor True, significa que al menos una película está en el idioma especificado. En este caso, se filtran las filas del DataFrame df2 donde el valor de "bool" es True, lo que significa que solo se retienen las películas en el idioma deseado. A continuación, se calcula el número total de películas en ese idioma y se retorna un mensaje que indica cuántas películas están disponibles en dicho idioma.

Si durante la iteración no se encuentra ningún valor True, significa que no hay películas en el idioma especificado. En este caso, la función devuelve un mensaje que informa que no existen películas en ese idioma.

La función **peliculas_duracion** tiene como objetivo obtener información sobre la duración y el año de estreno de una película específica en base a un archivo CSV que contiene datos sobre diversas películas y sus puntuaciones.

Primero, la función carga un archivo CSV desde una ruta relativa definida en la variable df_duracion.

Luego, la ruta completa al archivo CSV se construye concatenando una URL base (que se asume definida en otro lugar del código) con la ruta relativa. El resultado se almacena en la variable csv_path.

Se utiliza la biblioteca Pandas para leer el contenido del archivo CSV desde la ruta completa definida en csv_path, creando un DataFrame llamado df_duracion.

Del DataFrame df_duracion, se seleccionan las columnas "title", "release_year" y "runtime" para crear un nuevo DataFrame llamado df, que contiene información sobre el título de la película, el año de estreno y la duración.

Se inicializan las variables dato1 y dato2 con el valor None. Estas variables se utilizarán para almacenar los datos de interés después de realizar ciertas operaciones.

El título de la película ingresado se convierte a minúsculas mediante la variable pelicula_lower.

Luego, se verifica si el título de la película en minúsculas está presente en la columna "title" del DataFrame df_duracion, también en minúsculas. Si el título se encuentra en el DataFrame, se procede a realizar algunas operaciones.

Se filtra el DataFrame df_duracion para retener únicamente las filas donde el título de la película coincide con el título ingresado en minúsculas.

Se obtienen los valores de la fila filtrada: el año de estreno se almacena en la variable dato1 (en la primera columna de esa fila) y la duración se almacena en la variable dato2 (en la segunda columna de esa fila).

Se construye un mensaje de salida utilizando los valores obtenidos. Si tanto dato1 como dato2 no son None, significa que se encontró información sobre la película y se devuelve un mensaje que muestra el título de la película en formato de título (inicial en mayúscula) junto con su duración y año de estreno.

Si los valores dato1 o dato2 siguen siendo None, significa que no se encontró información para la película ingresada. En este caso, se devuelve un mensaje que informa que no se encontró información sobre la película.

La función **franquicia** tiene como objetivo obtener información sobre la ganancia total y el promedio de ganancia de una franquicia específica, basándose en un archivo CSV que contiene datos sobre diversas franquicias y sus ingresos.

Inicialmente, la función carga un archivo CSV desde una ruta relativa definida en la variable df_franquicia.

Luego, la ruta completa al archivo CSV se construye concatenando una URL base (que se asume definida en otro lugar del código) con la ruta relativa. El resultado se almacena en la variable csv_path.

Se utiliza la biblioteca Pandas para leer el contenido del archivo CSV desde la ruta completa definida en csv_path, creando un DataFrame llamado df_franquicia.

Del DataFrame df_franquicia, se seleccionan las columnas "name_production_company" (nombre de la compañía productora) y "revenue" (ingresos) para crear un nuevo DataFrame llamado df, que contiene información relevante para cada franquicia.

El nombre de la franquicia ingresado se convierte a minúsculas mediante la variable franquicia_lower.

Se verifica si el nombre de la franquicia en minúsculas está presente en la columna "name_production_company" del DataFrame df_franquicia, también en minúsculas. Si la franquicia se encuentra en el DataFrame, se procede a realizar algunas operaciones.

Se realiza una búsqueda en la columna "name_production_company" para determinar si el nombre de la franquicia ingresado está presente. Los resultados de la búsqueda (indicando si la franquicia está presente o no) se almacenan en un DataFrame llamado franquicias.

La columna "name_production_company" en el DataFrame franquicias se renombra a "bool" para indicar que los valores son booleanos que representan la presencia o ausencia de la franquicia.

Se concatena el DataFrame franquicias con el DataFrame original df, creando un nuevo DataFrame llamado df2. Este DataFrame incluye tanto la columna booleana "bool" como la columna original "revenue".

Se itera a través de los valores de la columna booleana "bool" en el DataFrame df2.

Si se encuentra al menos una ocurrencia True en la columna "bool", se filtran las filas del DataFrame df2 para retener solo las filas donde el valor de "bool" es True. Luego se calcula la ganancia total de la franquicia y el promedio de ganancia. Estos valores se utilizan para construir un mensaje de salida que muestra la ganancia total y el promedio de ganancia para la franquicia ingresada.

Si durante la iteración no se encuentra ninguna ocurrencia True en la columna "bool", significa que la franquicia ingresada no está presente en el DataFrame. En este caso, la función devuelve un mensaje que indica la ausencia de datos para esa franquicia.

La función **peliculas_pais** tiene como objetivo determinar cuántas películas fueron filmadas en un país específico, utilizando un archivo CSV que contiene información sobre películas y sus países de producción.

Al principio, la función carga un archivo CSV desde una ruta relativa definida en la variable df_pais.

Luego, se construye la ruta completa al archivo CSV concatenando una URL base (que se asume definida en otro lugar del código) con la ruta relativa. El resultado se almacena en la variable csv_path.

La biblioteca Pandas se utiliza para leer el contenido del archivo CSV desde la ruta completa definida en csv_path, creando un DataFrame llamado df_pais.

Del DataFrame df_pais, se selecciona únicamente la columna "name_country" (nombre del país) para crear un nuevo DataFrame llamado df, que contiene información sobre los países de producción de las películas.

El nombre del país ingresado se utiliza para realizar una búsqueda en la columna "name_country" del DataFrame df, considerando si el nombre del país está presente (insensible a mayúsculas y minúsculas) en la columna.

Los resultados de la búsqueda se almacenan en un DataFrame llamado paises.

La columna "name_country" en el DataFrame paises se renombra a "bool" para indicar que los valores son booleanos que representan la presencia o ausencia del país.

Se concatena el DataFrame paises con el DataFrame original df, creando un nuevo DataFrame llamado df2. Este DataFrame incluye tanto la columna booleana "bool" como la columna original "name_country".

Se itera a través de los valores de la columna booleana "bool" en el DataFrame df2.

Si se encuentra al menos una ocurrencia True en la columna "bool", se filtran las filas del DataFrame df2 para retener solo las filas donde el valor de "bool" es True. Luego se calcula el total de películas que fueron filmadas en el país ingresado. Este valor se utiliza para construir un mensaje de salida que indica la cantidad total de películas filmadas en ese país.

Si durante la iteración no se encuentra ninguna ocurrencia True en la columna "bool", significa que el país ingresado no está presente en el DataFrame. En este caso, la función devuelve un mensaje que indica la ausencia de datos para ese país.

La función **productoras_exitosas** tiene como objetivo proporcionar información sobre el éxito financiero de una productora específica, utilizando un archivo CSV que contiene datos sobre distintas productoras y sus ingresos.

La función comienza cargando un archivo CSV desde una ruta relativa definida en la variable df_productoras.

Luego, se construye la ruta completa al archivo CSV concatenando una URL base (que se asume definida en otro lugar del código) con la ruta relativa. El resultado se almacena en la variable csv_path.

Se utiliza la biblioteca Pandas para leer el contenido del archivo CSV desde la ruta completa definida en csv_path, creando un DataFrame llamado df_productoras.

Del DataFrame df_productoras, se seleccionan las columnas "name_production_company" (nombre de la compañía productora) y "revenue" (ingresos) para crear un nuevo DataFrame llamado df, que contiene información relevante para cada productora.

El nombre de la productora ingresado se utiliza para realizar una búsqueda en la columna "name_production_company" del DataFrame df, considerando si el nombre de la productora está presente (insensible a mayúsculas y minúsculas) en la columna.

Los resultados de la búsqueda se almacenan en un DataFrame llamado productoras.

La columna "name_production_company" en el DataFrame productoras se renombra a "bool" para indicar que los valores son booleanos que representan la presencia o ausencia de la productora.

Se concatena el DataFrame productoras con el DataFrame original df, creando un nuevo DataFrame llamado df2. Este DataFrame incluye tanto la columna booleana "bool" como la columna original "revenue".

Se itera a través de los valores de la columna booleana "bool" en el DataFrame df2.

Si se encuentra al menos una ocurrencia True en la columna "bool", se filtran las filas del DataFrame df2 para retener solo las filas donde el valor de "bool" es True. Luego se calcula la ganancia total de la productora y el total de películas producidas por la misma. Estos valores se utilizan para construir un mensaje de salida que muestra la ganancia total y el total de películas producidas por la productora ingresada.

Si durante la iteración no se encuentra ninguna ocurrencia True en la columna "bool", significa que la productora ingresada no está presente en el DataFrame. En este caso, la función devuelve un mensaje que indica la ausencia de datos para esa productora.

La función **get_director** tiene como objetivo obtener información sobre las películas dirigidas por un director específico utilizando un archivo CSV que contiene información sobre diversas películas y sus equipos de producción.

Se define una ruta relativa al archivo CSV en la variable df_director.

La ruta completa al archivo CSV se construye concatenando una URL base (que se asume definida en otro lugar del código) con la ruta relativa. El resultado se almacena en la variable csv_path.

Se utiliza la biblioteca Pandas para leer el contenido del archivo CSV desde la ruta completa definida en csv_path, creando un DataFrame llamado df_director.

Del DataFrame df_director, se seleccionan las columnas relevantes para la información deseada, como el trabajo del equipo, el nombre del equipo (director), la fecha de lanzamiento, el retorno, los ingresos, el presupuesto y el título de la película. Esto crea un nuevo DataFrame llamado df.

Se realiza una búsqueda en la columna "crew_name" (nombre del equipo) del DataFrame df para determinar si el nombre del director está presente. La búsqueda es insensible a mayúsculas y minúsculas (case=False).

Los resultados de la búsqueda se almacenan en un DataFrame llamado peliculas_director.

La columna "crew_name" en el DataFrame peliculas_director se renombra a "bool" para indicar que los valores son booleanos que representan si el director está asociado con la película.

Se concatena el DataFrame peliculas_director con el DataFrame original df, creando un nuevo DataFrame llamado df2. Este DataFrame incluye tanto la columna booleana "bool" como las columnas originales del DataFrame df.

Se itera a través de los valores de la columna booleana "bool" en el DataFrame df2.

Si se encuentra al menos una ocurrencia True en la columna "bool", se filtran las filas del DataFrame df2 para retener solo las filas donde el valor de "bool" es True. Luego, se seleccionan las columnas relevantes ("title", "return", "revenue" y "budget") del DataFrame filtrado df2 para obtener información sobre las películas dirigidas por el director.

Se crea una lista vacía llamada list_peliculas que se utilizará para almacenar información sobre las películas dirigidas por el director.

Se itera a través de las filas del DataFrame peliculas_director. Para cada película, se extraen los valores relevantes (título, retorno, ingresos y presupuesto) y se construye un mensaje que contiene esta información. El mensaje se agrega a la lista list_peliculas.

Una vez que se han procesado todas las películas, la función devuelve la lista list_peliculas, que contiene mensajes individuales para cada película dirigida por el director.

Si durante la iteración no se encuentra ninguna ocurrencia True en la columna "bool", significa que el director ingresado no está presente en el DataFrame. En este caso, la función devuelve un mensaje que indica que el director no ha dirigido ninguna película de la lista.
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
Aca puedes entrar a hacer tus consultas https://proyecto-peliculas-8iw2.onrender.com/docs
