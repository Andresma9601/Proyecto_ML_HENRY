from fastapi import FastAPI
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

app=FastAPI()

#http://127.0.0.1:8000

@app.get("/")
def index():
    return {"message":"Bienvenido, aca puedes hacer tus consultas"}

# Definición de la variable DOWNLOAD_ROOT que contiene la URL base
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/Andresma9601/Proyecto_ML_HENRY/main/"
       
@app.get("/peliculas_idioma/{idioma}")
# Función para calcular la cantidad de filmaciones en un idioma determinado
def peliculas_idioma(idioma: str):
    # Ruta relativa del archivo CSV
    df_idioma="db_movies/idioma.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path=DOWNLOAD_ROOT + df_idioma
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_idioma=pd.read_csv(csv_path)
    # Seleccionar la columna "language" del DataFrame df_idioma
    df = df_idioma[["language"]]
    # Buscar si el idioma está presente en la columna "language"
    peliculas = df["language"].str.contains(idioma, case=False)
    # Convertir el resultado de la búsqueda en un DataFrame
    peliculas = pd.DataFrame(peliculas)
    # Renombrar la columna "language" del DataFrame peliculas a "bool"
    peliculas = peliculas.rename(columns={'language': 'bool'})
    # Concatenar el DataFrame peliculas con el DataFrame original df
    df2 = pd.concat([peliculas, df], axis=1)
    # Iterar sobre los valores de la columna "bool" en el DataFrame df2
    for i in df2["bool"]:
        # Verificar si el valor es True
        if i == True:
            # Filtrar las filas del DataFrame df2 donde el valor de "bool" es True
            peliculas = df2.loc[df2["bool"] == True]
            # Calcular el total de películas en las que el idioma está presente
            total_peliculas = sum(peliculas["bool"])
            return f"{total_peliculas} peliculas estan en idioma {idioma}"
    else:
        # Devolver un mensaje indicando que no hay películas en ese idioma
        return f"No hay peliculas en este idioma"

# Diccionario de dias en español e inglés
@app.get("/peliculas_duracion/{pelicula}")
# Función para calcular la duracion de las peliculas.
def peliculas_duracion(pelicula: str):
    # Cargar el archivo CSV en un DataFrame
    df_duracion="db_movies/runtime.csv"
    csv_path = DOWNLOAD_ROOT + df_duracion
    df_duracion = pd.read_csv(csv_path)
    # Seleccionar las columnas "title", "release_year" y "runtime" del DataFrame df_duracion
    df = df_duracion[["title", "release_year", "runtime"]]
    # Inicialización de dato1 y dato2
    dato1 = None
    dato2 = None
    # Convertir el título ingresado a minúsculas
    pelicula_lower = pelicula.lower()
    # Verificar si el título ingresado en minúsculas está en la columna "title" en minúsculas
    if pelicula_lower in df_duracion["title"].str.lower().values:
        # Filtrar el DataFrame para la película específica
        df_duracion = df_duracion.loc[df_duracion["title"].str.lower() == pelicula_lower]
        # Obtener los valores de la fila filtrada
        dato1 = df_duracion.iloc[0, 1]
        dato2 = df_duracion.iloc[0, 2]
    # Construir el mensaje de salida
    if dato1 is not None and dato2 is not None:
        return f"La película {pelicula.title()} dura {dato2} y fue estrenada en el año {dato1}."
    else:
        return f"No se encontró información para la película {pelicula.title()}."
    
@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
    # Cargar el archivo CSV en un DataFrame
    df_franquicia = "db_movies/franquicia.csv"
    csv_path = DOWNLOAD_ROOT + df_franquicia
    df_franquicia= pd.read_csv(csv_path)
    # Seleccionar las columnas "name" y "revenue" del DataFrame df1
    df = df_franquicia[["name", "revenue"]]
    # Convertir el nombre de la franquicia ingresado a minúsculas
    franquicia_lower = franquicia.lower()
    # Verificar si el nombre de la franquicia en minúsculas está presente en la columna "name" en minúsculas
    franquicias = df["name"].str.lower().str.contains(franquicia_lower, case=False)
    franquicias = pd.DataFrame(franquicias)
    # Renombrar la columna "name" del DataFrame franquicias a "bool"
    franquicias = franquicias.rename(columns={'name': 'bool'})
    # Concatenar el DataFrame franquicias con el DataFrame original df
    df2 = pd.concat([franquicias, df], axis=1)
    for i in df2["bool"]:
        # Verificar si el valor es True
        if i == True:
            # Filtrar las filas del DataFrame df2 donde el valor de "bool" es True
            franquicias = df2.loc[df2["bool"] == True]
            # Calcular la ganancia total de la franquicia
            revenue = sum(franquicias["revenue"])
            # Calcular el promedio de ganancia
            promedio = revenue / franquicias["revenue"].count()
            # Devolver el mensaje con la información obtenida
            return f"La franquicia {franquicia.title()} tiene una ganancia total de {revenue} y una ganancia promedio de {promedio:.2f}"
    # Si no se encuentra la franquicia, devolver un mensaje indicando la ausencia de datos
    return f"No hay datos para esta franquicia"

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
    # Cargar el archivo CSV en un DataFrame
    df_pais = "db_movies/pelispais.csv"
    csv_path = DOWNLOAD_ROOT + df_pais
    df_pais= pd.read_csv(csv_path)
    # Seleccionar las columnas "name_country" del DataFrame df1
    df = df_pais[["name_country"]]
    # Verificar si el nombre del país ingresado está presente en la columna "name_country"
    paises = df["name_country"].str.contains(pais, case=False)
    # Crear un DataFrame con los resultados de la verificación
    paises = pd.DataFrame(paises)
    # Renombrar la columna "name_country" del DataFrame paises a "bool"
    paises = paises.rename(columns={'name_country': 'bool'})
    # Concatenar el DataFrame paises con el DataFrame original df
    df2 = pd.concat([paises, df], axis=1)
    for i in df2["bool"]:
        # Verificar si el valor es True
        if i == True:
            # Filtrar las filas del DataFrame df2 donde el valor de "bool" es True
            paises = df2.loc[df2["bool"] == True]
            # Contar el total de películas firmadas en el país
            total = paises["bool"].count()
            # Devolver el mensaje con la información obtenida
            return f"En el {pais.title()} se firmaron un total de {total} películas"
    # Si no se encuentra el país, devolver un mensaje indicando la ausencia de datos
    return f"No hay datos para este país"


@app.get("/productoras_exitosas/{productora}")
def productoras_exitosas(productora: str):
    # Cargar el archivo CSV en un DataFrame
    df_productoras = "db_movies/productora.csv"
    csv_path = DOWNLOAD_ROOT + df_productoras
    df_productoras= pd.read_csv(csv_path)
    # Seleccionar las columnas "name_production_company" y "revenue" del DataFrame df1
    df = df_productoras[["name_production_company", "revenue"]]
    # Verificar si el nombre de la productora ingresado está presente en la columna "name_production_company"
    productoras = df["name_production_company"].str.contains(productora, case=False)
    # Crear un DataFrame con los resultados de la verificación
    productoras = pd.DataFrame(productoras)
    # Renombrar la columna "name_production_company" del DataFrame productoras a "bool"
    productoras = productoras.rename(columns={'name_production_company': 'bool'})
    # Concatenar el DataFrame productoras con el DataFrame original df
    df2 = pd.concat([productoras, df], axis=1)
    for i in df2["bool"]:
        # Verificar si el valor es True
        if i == True:
            # Filtrar las filas del DataFrame df2 donde el valor de "bool" es True
            productoras = df2.loc[df2["bool"] == True]
            # Calcular la ganancia total de la productora
            revenue = sum(productoras["revenue"])
            # Calcular el total de películas producidas por la productora
            total = productoras["revenue"].count()
            # Devolver el mensaje con la información obtenida
            return f"La productora {productora.title()} tiene una ganancia total de {revenue} y un total de películas de {total}"
    # Si no se encuentra la productora, devolver un mensaje indicando la ausencia de datos
    return f"No hay datos para esta productora"

@app.get("/peliculas_director/{nombre_director}")
def get_director(nombre_director):
    # Ruta relativa del archivo CSV
    df_director="db_movies/Director.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path=DOWNLOAD_ROOT + df_director
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_director=pd.read_csv(csv_path)
    # Seleccionar las columnas relevantes del DataFrame movies_unique
    df = df_director[["job", "crew_name", "release_date", "return", "revenue", "budget", "title"]]
    # Realizar una búsqueda para determinar si el nombre del director está presente en la columna "crew_name"
    peliculas_director = df["crew_name"].str.contains(nombre_director, case=False)
    # Convertir el resultado de la búsqueda en un DataFrame
    peliculas_director = pd.DataFrame(peliculas_director)
    # Renombrar la columna "crew_name" del DataFrame peliculas_director a "bool"
    peliculas_director = peliculas_director.rename(columns={'crew_name': 'bool'})
    # Concatenar el DataFrame peliculas_director con el DataFrame original df
    df2 = pd.concat([peliculas_director, df], axis=1)
    # Iterar sobre los valores de la columna "bool" en el DataFrame df2
    for i in df2["bool"]:
        # Verificar si el valor es True
        if i == True:
            # Filtrar las filas del DataFrame df2 donde el valor de "bool" es True
            peliculas_director = df2.loc[df2["bool"] == True]
            # Seleccionar las columnas "title", "return", "revenue" y "budget" en el DataFrame resultante peliculas_director
            peliculas_director = peliculas_director[["title", "return", "revenue", "budget"]]
            list_peliculas=[]
            cont_peliculas=0
            while cont_peliculas < len(peliculas_director):
                movie = peliculas_director.iloc[cont_peliculas, 0]
                retorno = peliculas_director.iloc[cont_peliculas, 1]
                revenue=peliculas_director.iloc[cont_peliculas, 2]
                budget=peliculas_director.iloc[cont_peliculas, 3]
                list_peliculas.append(f"El director {nombre_director.title()} dirigio la siguiente pelicula {movie}, con un retorno de {retorno}, una ganancia de {revenue} y un presupuesto de {budget}")
                cont_peliculas+=1
            return list_peliculas
    else:
        # Si no se encuentra ninguna coincidencia, devolver un mensaje indicando que el director no ha dirigido ninguna película de la lista
        return f"Este director no ha dirigido ninguna de las películas de la lista"


@app.get("/recomendacion/{titulo}")
# Función para obtener películas similares
def obtener_peliculas_similares(titulo):
    data_movies="db_movies/datos_peliculas.csv"
    data = pd.read_csv(DOWNLOAD_ROOT+data_movies)
    # Preparación de los datos
    data = data[['title', 'popularity', 'release_date', 'runtime', 'vote_average']].dropna()
    # Ingeniería de características
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    X = vectorizer.fit_transform(data['title'] + ' ' + data['release_date'].astype(str) + ' ' + data['runtime'].astype(str) + ' ' + data['vote_average'].astype(str))
    # Construcción del modelo
    k = 10  # Número de clústeres
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X)
    # Transformar el título en un vector Tfidf
    titulo_vectorizado = vectorizer.transform([titulo.lower()])
    # Calcular la similitud coseno entre el título y todas las películas del conjunto de datos
    similitudes = cosine_similarity(titulo_vectorizado, X)
    # Obtener el índice de la película de consulta
    indice_pelicula_consulta = data[data['title'].str.lower() == titulo.lower()].index[0]
    # Ordenar las similitudes de forma descendente
    indices_peliculas_similares = similitudes.argsort()[0][::-1]
    # Encontrar las 5 películas más similares que no sean la película de consulta
    peliculas_similares = []
    for indice in indices_peliculas_similares:
        if indice != indice_pelicula_consulta:
            peliculas_similares.append(data.iloc[indice]['title'])
            if len(peliculas_similares) == 5:
                break
    return peliculas_similares
