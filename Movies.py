from matplotlib import category
import pandas as pd
pd.option_context('display.max_columns', None, 'display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
import numpy as np
from ast import literal_eval
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
movies = pd.read_csv("movies_metadata.csv")

#size of the data set
dim = movies.shape

#Let's list all columns name of our data sets
columns =movies.columns.values

movies=movies.drop(['poster_path','production_companies','spoken_languages','belongs_to_collection','homepage','production_countries','status','original_title'], axis=1)

movies.dtypes

original_memory=movies.memory_usage(deep=True)
movies.memory_usage(deep=True)

def to_boolean(x):
    '''Take an object value and convert into boolean
       return NaN is the the value is incorrect
    '''
    try:
        x = bool(x)
    except:
        x= np.nan
    return x

#creating a function to convert to int
def to_int(num):
    try:
        num=int(num)
    except:
        num=np.nan
    return num

# converting a column to float
def to_float(num):
    '''Take an object type and convert to float
       return NaN for non numeric values
    '''
    try:
        num=float(num)
    except:
        num=np.nan
    return num

#converting a column as category
def to_category(num):
    '''Take an object type and convert to categorical
       return NaN if convertion fails
    '''
    try:
        num=category(num)
    except:
        num=np.nan
    return num

#converting a column as int
def to_int(num):
    '''Take an object type and convert to int
       return NaN if convertion fails
    '''
    try:
        num=int(num)
    except:
        num=np.nan
    return num

#converting the adult column in movie boolean
movies['adult']=movies['adult'].apply(to_boolean)

#converting the video column in movie boolean
movies['video']=movies['video'].apply(to_boolean)


#converting the budget column to float
movies['budget']=movies['budget'].apply(to_float)

#converting the popularity column to float
movies['popularity']=movies['popularity'].apply(to_float)

#converting the budget column to float
movies['revenue']=movies['revenue'].apply(to_float)

#converting the vote_count column to float
movies['vote_count']=movies['vote_count'].apply(to_float)

#converting the vote_average column to float
movies['vote_average']=movies['vote_average'].apply(to_float)

#converting the Id column to int
movies['id']=movies['id'].apply(to_int)

#converting the Id column to categorical
movies['original_language']=movies['original_language'].apply(to_category)

#convert release_date to datetime
movies['release_date']=pd.to_datetime(movies['release_date'], errors='coerce')

print(movies['runtime'].describe())
movies['runtime']=movies['runtime'].apply(to_int)

#getting the current memory size and compare with the original
current_memory=movies.memory_usage(deep=True)
(1-current_memory/original_memory)*100
#movies.dtypes

#let us fill all the genres with non value by an empty list.

movies['genres']=movies['genres'].fillna('[]')

#evaluating the column and return the right object
movies['genres']=movies['genres'].apply(literal_eval)

#then convert the colum to a list of genres
movies['genres']=movies['genres'].apply(lambda genre : [x['name'] for x in genre] if isinstance(genre,list) else [])
movies.iloc[0]['genres']

tempgenre=movies.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1,drop=True)
tempgenre.name='genre'
tempgenre_semrep = tempgenre.drop_duplicates()

movie_gen=movies.drop('genres', axis=1).join(tempgenre)
movie_gen = movie_gen.sort_values('popularity', ascending=False)

generos = { 
    1: 'Animation',
    2: 'Comedy',
    3: 'Family',
    4: 'Adventure',
    5: 'Fantasy',
    6: 'Romance',
    7: 'Drama',
    8: 'Action',
    9: 'Crime',
    10: 'Thriller',
    11: 'Horror',
    12: 'History',
    13: 'Science Fiction',
    14: 'Mystery',
    15: 'War',
    16: 'Foreign',
    17: 'Music',
    18: 'Documentary',
    19: 'Western',
    20: 'TV Movie',
    21: 'Carousel Productions',
    22: 'Vision View Entertainment',
    23: 'Telescene Film Group Productions',
    24: 'Aniplex',
    25: 'GoHands',
    26: 'BROSTA TV',
    27: 'Mardock Scramble Production Committee',
    28: 'Sentai Filmworks',
    29: 'Odyssey Media',
    30: 'Pulser Productions',
    31: 'Rogue State',
    32: 'The Cartel'
}

generos_invertidos = {valor: chave for chave, valor in generos.items()}


def encontrar_chave_por_valor(dicionario, valor_procurado):
    for chave, valor in dicionario.items():
        if valor == valor_procurado:
            return chave

def pesquisar_por_genero():
    escolha = genero_var.get()
    x = generos_invertidos[escolha]
    gen = generos[x]
    result = movie_gen.loc[movie_gen['genre'] == gen]
    result = result.head(200)
    result = result.sort_values('vote_average', ascending=False)
    result = result[['title', 'runtime', 'overview']]
    result.reset_index(drop=True, inplace=True)
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, result) 
    caminho_arquivo_excel = 'filmes.xlsx'
    result.to_excel(caminho_arquivo_excel, index=False)
    with open('arquivo.txt', 'w') as arquivo:
        for indice, valor in result['overview'].items():
            arquivo.write(f"---RESUMO DO FILME {result['title'][indice]}---\n \n {valor} \n \n")



janela = tk.Tk()
janela.title("Pesquisar Filmes por Gênero")


genero_var = tk.StringVar()
genero_var.set("Select")

genero_menu = tk.OptionMenu(janela, genero_var, *generos.values())
genero_menu.pack()

botao_pesquisar = tk.Button(janela, text="Pesquisar", command=pesquisar_por_genero)
botao_pesquisar.pack()

text_box = ScrolledText(janela, width=150, height=35)
text_box.pack()

janela.mainloop()
