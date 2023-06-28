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
       
# Diccionario de meses en español e inglés
meses_dict = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December"
}
@app.get("/peliculas_mes/{mes}")
# Función para calcular la cantidad de filmaciones en un mes determinado
def cantidad_filmaciones_mes(mes:str):
    # Ruta relativa del archivo CSV
    df_dia="db_movies/Dias.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path=DOWNLOAD_ROOT + df_dia
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_dia=pd.read_csv(csv_path)
    # Convertir de str a datetime
    df_dia["release_date"]=df_dia['release_date'] = pd.to_datetime(df_dia["release_date"])
    # Convierte el mes a minúsculas para que coincida con los datos del DataFrame
    mes = mes.lower()
    # Verifica si el mes ingresado está en el diccionario
    if mes in meses_dict:
        mes_ingles = meses_dict[mes]
        # Filtra las películas que fueron estrenadas en el mes consultado
        filmaciones_mes = df_dia["release_date"][df_dia["release_date"].dt.month_name().str.lower() == mes_ingles.lower()]
        # Obtiene la cantidad de filmaciones en el mes
        cantidad = len(filmaciones_mes)
        return f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"
    else:
        return f"no es un mes en español"

# Diccionario de dias en español e inglés
dias_dict = {
    "lunes": "Monday",
    "martes": "Tuesday",
    "miercoles": "Wednesday",
    "jueves": "Thursday",
    "viernes": "Friday",
    "sabado": "Saturday",
    "domingo": "Sunday"
}
@app.get("/peliculas_dia/{dia}")
# Función para calcular la cantidad de filmaciones en un dia determinado
def cantidad_filmaciones_dia(dia:str):
    # Ruta relativa del archivo CSV
    df_dia="db_movies/Dias.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path=DOWNLOAD_ROOT + df_dia
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_dia=pd.read_csv(csv_path)
    # Convertir de str a datetime
    df_dia["release_date"]=df_dia['release_date'] = pd.to_datetime(df_dia["release_date"])
    # Convierte el dia a minúsculas para que coincida con los datos del DataFrame
    dia = dia.lower()
    # Verifica si el dia ingresado está en el diccionario
    if dia in dias_dict:
        dia_ingles = dias_dict[dia]
        # Filtra las películas que fueron estrenadas en el dia consultado
        filmaciones_dia = df_dia["release_date"][df_dia["release_date"].dt.day_name().str.lower() == dia_ingles.lower()]
        # Obtiene la cantidad de filmaciones en el dia
        cantidad = len(filmaciones_dia)
        return f"{cantidad} de películas fueron estrenadas en los días {dia.capitalize()}"
    else:
        return f"no es un dia en español"
    
@app.get("/peliculas_score/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):  
    # Ruta relativa del archivo CSV
    df_score = "db_movies/Score.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path = DOWNLOAD_ROOT + df_score
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_score = pd.read_csv(csv_path)
    # Convierte el título de la película a minúsculas
    titulo_minuscula = titulo_de_la_filmacion.lower()
    # Itera sobre los títulos de las películas en el DataFrame movies_unique
    for movie in df_score["title"]:
        # Convierte el título de la película actual a minúsculas
        movie_minuscula = movie.lower()
        # Verifica si hay una coincidencia entre los títulos
        if movie_minuscula == titulo_minuscula:
            # Filtra el DataFrame movies_unique para obtener los datos de la película encontrada
            df = df_score
            df = df.loc[df["title"] == movie]
            # Obtiene los datos específicos de la película encontrada
            dato1 = df.iloc[0, 1]
            dato2 = df.iloc[0, 2]
            dato3 = df.iloc[0, 3]
            # Retorna un mensaje con los datos de la película encontrada
            return f"La película {dato1} fue estrenada en el año {dato2} con un score/popularidad de {dato3}"
    # Retorna un mensaje indicando que no se encontró la película en la lista
    return "No es una película de esta lista"

@app.get("/peliculas_votos/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    # Ruta relativa del archivo CSV
    df_votos="db_movies/Votos.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path=DOWNLOAD_ROOT + df_votos
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_votos=pd.read_csv(csv_path)
    # Convierte el título de la filmación a minúsculas
    titulo_minuscula = titulo_de_la_filmacion.lower()
    # Itera sobre los títulos de películas únicos en la variable "movies_unique"
    for movie in df_votos["title"]:
        # Convierte el título de la película actual a minúsculas
        movie_minuscula = movie.lower()
        # Verifica si el título de la película actual coincide con el título proporcionado
        if movie_minuscula == titulo_minuscula:
            # Crea un DataFrame con las columnas "title", "vote_count", "vote_average" y "release_year"
            df = df_votos
            # Filtra el DataFrame para obtener las filas con el título de la película actual
            df = df.loc[df["title"] == movie]
            # Itera sobre los valores de "vote_count" en el DataFrame filtrado
            for i in df["vote_count"]:
                # Verifica si el valor de "vote_count" es mayor o igual a 2000
                if i >= 2000:
                    # Obtiene los valores de la primera fila del DataFrame filtrado
                    dato1 = df.iloc[0, 1]
                    dato2 = df.iloc[0, 2]
                    dato3 = df.iloc[0, 3]
                    dato4 = df.iloc[0, 4]
                    # Devuelve una cadena de texto con información sobre la película y sus valoraciones
                    return f"La película {dato1} fue estrenada en el año {dato4}. La misma cuenta con un total de {dato2} valoraciones, con un promedio de {dato3}"
                else:
                    # Devuelve una cadena de texto indicando que la película no cuenta con más de 2000 votos
                    return f"Esta película no cumple con las condicion de tener al menos 2000 votos, por lo cual no se devuelve ningun valor"
    # Si el título de la película no se encuentra en la lista
    else:
        # Devuelve una cadena de texto indicando que no es una película de la lista
        return f"No es una película de esta lista"

@app.get("/peliculas_actor/{nombre_actor}")
def get_actor(nombre_actor:str):
    # Ruta relativa del archivo CSV
    df_actor="db_movies/Actor.csv"
    # Combinar la URL base y la ruta relativa para obtener la URL completa del archivo CSV
    csv_path=DOWNLOAD_ROOT + df_actor
    # Leer el archivo CSV desde la URL completa utilizando la función read_csv de Pandas
    df_actor=pd.read_csv(csv_path)
    # Seleccionar las columnas "cast_name" y "return" del DataFrame movies_unique
    df = df_actor[["cast_name", "return"]]
    # Buscar si el nombre del actor está presente en la columna "cast_name"
    peliculas_participante = df["cast_name"].str.contains(nombre_actor, case=False)
    # Convertir el resultado de la búsqueda en un DataFrame
    peliculas_participante = pd.DataFrame(peliculas_participante)
    # Renombrar la columna "cast_name" del DataFrame peliculas_participante a "bool"
    peliculas_participante = peliculas_participante.rename(columns={'cast_name': 'bool'})
    # Concatenar el DataFrame peliculas_participante con el DataFrame original df
    df2 = pd.concat([peliculas_participante, df], axis=1)
    # Iterar sobre los valores de la columna "bool" en el DataFrame df2
    for i in df2["bool"]:
        # Verificar si el valor es True
        if i == True:
            # Filtrar las filas del DataFrame df2 donde el valor de "bool" es True
            peliculas_participante = df2.loc[df2["bool"] == True]
            # Calcular el total de películas en las que el actor ha participado
            total_peliculas = sum(peliculas_participante["bool"])
            # Calcular el retorno total del actor
            retorno = sum(peliculas_participante["return"])
            # Calcular el promedio de retorno por película
            promedio = retorno / total_peliculas
            # Devolver un mensaje con la información obtenida
            return f"El actor {nombre_actor.title()} ha participado de {total_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno} con un promedio de {promedio} por filmación"
    # Si no se encuentra el nombre del actor en ninguna película
    else:
        # Devolver un mensaje indicando que el actor no participa en ninguna película
        return f"El actor no participa en ninguna pelicula"

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
def obtener_peliculas_similares(titulo, n=5):
    # Cargar los datos
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
    # Encontrar las n películas más similares que no sean la película de consulta
    peliculas_similares = []
    for indice in indices_peliculas_similares:
        if indice != indice_pelicula_consulta:
            peliculas_similares.append(data.iloc[indice]['title'])
            if len(peliculas_similares) == n:
                break
    return peliculas_similares
