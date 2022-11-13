import requests #request a la web
import bs4
from bs4 import BeautifulSoup #Librería BS4
from urllib.parse import urljoin #Parsear HTML
import pandas as pd #Librería Pandas
from IPython.core.display import HTML #Para visualizar HTML
from pathlib import Path  

#Agrego en una variable la web a scrapear
url_inicial = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist'
#Agrego una url_raiz que nos va a servir para sobreescribir
url_root = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist'

#Berifico el staduscode con request:
r=requests.get(url_inicial)
status_code=r.status_code
headers= r.headers
#print(f'Estatus code: {status_code} - Headers: {headers}') #Devuelve 200 + los headers, OK.

#Utilizamos bs4 para pasar el sitio a texto plano:
soup = BeautifulSoup(r.text,'lxml')
#Los muestro
#print(soup.prettify())

#Obtengo el elemento que contiene los links a la página y lo guardo en una lista de trabajos
jobs_list = soup.find_all("div", {"class":"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"})

#Ahora utilizo ese listado para obtener los link contenidos dentro de cada uno de los jobs:
jobs_links = [x.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href') for x in jobs_list]

#Definimos una función para obtener links que toma dos parámetros, una soup de la web y la url:
def get_url_items(soup, url_page):
    #Primero listamos cada uno de los jobs dentro de la página:
    jobs_list = soup.find_all("div", {"class":"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"})
    #Luego obtenemos los link de cada uno de los jobs:
    jobs_links = [x.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href') for x in jobs_list]
    #Y retornamos la lista de links:
    return jobs_links

# Definimos una lista donde guardar los link de cada jobs_links e iteramos con un ciclo while:
links_jobs = []
i=0

while i<20: #Definimos la cantidad de páginas que vamos a scrapear
    #Vamos a ir sobreescribiendo la url que pasamos al inicio:
    next_page = url_inicial +'/'+ str(i)
    # print(f'Estoy en la página: {next_page}')
    i+=1
    #Request de cada página
    r_pag = requests.get(next_page)
    #Obtengo la sopa de la página inicial
    s_pag = BeautifulSoup(r_pag.text,'lxml')
    #Obtengo los links con la función
    links = get_url_items(s_pag, next_page)
    #Agregamos los links a la lista de jobs (Listas dentro de lista)
    links_jobs.append(links)

    #Sale del bucle si no hay mas paginas:
    if not next_page:
        break

# #Muestro los links de la página 5
# print(links_jobs[5])

# Creamos una lista que contiene cada uno de las páginas que contienen trabajos y es la que utilizaremos para obtener datos:
list_scrapper = []
for i in links_jobs:#Iteramos sobre los links de trabajos
    for j in i: #Iteramos sobre las listas de trabajos
        list_scrapper.append(j)

# #Función para manejar valores nulos

# def output_value1(arg1):
#     if((s_job.find(arg1)) != None):
#         return s_job.find(arg1).get_text(strip=True)
#     else:
#         return 'Sin valor'

def output_value2(arg1, clase):
    if((s_job.find(arg1, clase)) != None):
        return s_job.find(arg1, clase).get_text(strip=True)
    else:
        return 'Sin valor'

# print(len(list_scrapper))
#Verificamos un job en particular y creamos una sopa del mismo:
uno=list_scrapper[10]
r_job = requests.get(uno)
s_job = BeautifulSoup(r_job.text,'lxml')
#Buscamos dentro de la página los elementos que nos sirven para analizar:
# print(s_job)


# #Obtenemos: Titulo del trabajo, organización, lugar, posteado hace cuanto, salario:
# job=s_job.find('h1').get_text(strip=True) #strip quita espacios al inicio y al final del str
# organization=s_job.find('a', class_='topcard__org-name-link topcard__flavor--black-link').get_text(strip=True)
# place=output_value('span', 'topcard__flavor topcard__flavor--bullet')
# posted_time_ago = output_value('span', 'posted-time-ago__text topcard__flavor--metadata')
# salary = output_value('a', 'app-aware-link')
# print(f'Trabajo: {job} / Organizacion: {organization} / Lugar: {place} / Posteado hace: {posted_time_ago}/ Salario: {salary}')

#Función para hacer scraper de cada trabajo y obtener los datos utiles:
def scrapper_job(url,num):

    content_job = {}
    r=requests.get(url)
    s_job = BeautifulSoup(r.text,'lxml')

    #Manejo de errores:
    try:
        #Obtenemos: Titulo del trabajo, organización, lugar, posteado hace cuanto, salario:
        job=s_job.find('h1').get_text(strip=True) #strip quita espacios al inicio y al final del str
        # job=output_value1('h1') #strip quita espacios al inicio y al final del str
        content_job['Trabajo'] = job

        organization=s_job.find('a', class_='topcard__org-name-link topcard__flavor--black-link').get_text(strip=True)
        content_job['Organizacion'] = organization
        
        
        place=s_job.find('span', class_='topcard__flavor topcard__flavor--bullet').get_text(strip=True)
        content_job['Lugar'] = place

        posted_time_ago = s_job.find('span', class_='posted-time-ago__text topcard__flavor--metadata').get_text(strip=True)
        content_job['Posteado hace'] = posted_time_ago

        salary = output_value2('a', 'app-aware-link')
        content_job['Salario'] = salary
    except Exception as ex:
        print(f'Error en la funcion scrapper - PAGINA Nº {num}: ' + str(ex))
    return content_job

#Utilizamos la función para scrapear(Limitamos a 500 páginas)
list_scrapper = list_scrapper[0:500]
data_jobs = []
for idx, i in enumerate(list_scrapper):
    print(f'estas escrapeando la pagina: {idx}')
    data_jobs.append(scrapper_job(i,idx))

#Creamos un dataframe
df_jobs=pd.DataFrame(data_jobs)
print(df_jobs)

# #Lo visualizamos en HTML
# df_jobs.to_html(escape=False)
# HTML(df_jobs.to_html(escape=False))

#Creamos un archivo csv:
df_jobs.to_csv('dataframe/linkedin_ds-jobs.csv')
#Creamos un archivo xlsx:
df_jobs.to_excel('dataframe/linkedin_ds-jobs.xlsx')


