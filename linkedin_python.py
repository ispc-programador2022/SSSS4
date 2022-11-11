import requests 
from bs4 import BeautifulSoup
#Nuevo immport para nuevo código con paginado
import pandas
from pandas import DataFrame
import csv


#Primera forma utilizando una sola página:
# #definimos una variable con la dirección del website que vamos a anlizar
# webLinkedinJobs = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist'
# #Usamos la librería request para hacer una solicitud GET a la página. Guardamos el resultado en "result"
# result = requests.get(webLinkedinJobs)
# #Obtenemos el texto de un elemento beatifulsoup y lo asignamos a una variable "content"
# content = result.text

# #utilizamos la herramienta beatifulsoup y como parámetro pasamos el contenido y el parser. Obtenemos la sopa de contenidos
# #soup = BeautifulSoup(content, 'lxml')
# #Podemos usar un print y el método de beatifulsoup "prettify" para evaluar el contenido:
# #print(soup.prettify())

# #Para buscar un elemento dentro del HTML (Luego de inspeccionarlo en en navegador) usamos el método "find" de bs4
# #Primer argumento el nombre del tag, segundo argumento el nombre del atributo. Eso lo igualamos a una variable "contenedor"
# #contenedor = soup.find('div', class_= 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
# #Dentro del contenedor buscamos algun elemento que nos interese para obtener el texto:
# #soup.find('h3', class_='base-search-card__title').get_text() 
# #Mejorando el código:
# titulo = contenedor.find('h3', class_='base-search-card__title').get_text()
# #Imprimimos en consola el resultado:
# #print(titulo)

# titulos = soup.find_all('h3', class_='base-search-card__title')
# titulos_trabajos = []

# for titulo in titulos:
#     titulos_trabajos.append(titulo.text.strip())
#print(titulos_trabajos)

#################################################################################################################

#Otra forma utilizando paginación
#Primero importamos pandas y csv

#Luego creamos un comando para crear una estructura de archivo csv en el que completaremos nuestros datos scrapeados
with open('Resultado_linkedin.csv', mode='w') as csv_file:
    fieldnames = ['Title', 'Location', 'Salary', 'Date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

#Creamos listas de variables vacias para guardar los datos.
job_title = []
job_location = []
job_salary = []
job_date = []

#Definimos la función para el scrapeo 
def linkedin_scraper(webpage, page_number):
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content,'lxml')

    soup_title= soup.findAll('h3', class_='base-search-card__title')
    soup_location= soup.findAll("span",class_='job-search-card__location')
    soup_salary= soup.findAll("span",class_='job-search-card__salary-info')
    soup_date= soup.findAll("time",class_='job-search-card__listdate')

    for x in range(len(soup_title)):
        job_title.append(soup_title[x].a.text.strip())
        job_location.append(soup_location[x].text.strip())
        job_salary.append(soup_salary[x].text.strip())
        job_date.append(soup_date[x].text.strip())

    #Generando la página siguiente en el URL
    if page_number <20: 
        page_number = page_number + 1
        linkedin_scraper(webpage, page_number)

#Creamos una variable con la URL: 
webLinkedinJobs = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist/'
#Llamando a la función con los parámetros iniciales:
linkedin_scraper(webLinkedinJobs, 0)
 
#crear el dataframe y llenar con estos datos el archivo csv
 
data = { 'job_title':job_title, 'job_location': job_location, 'job_salary':job_salary, 'job_date':job_date}
 
df = DataFrame(data, columns = ['job_title','job_location','job_salary','job_date'])
 
df.to_csv(r'D:\Documentos\ISPC_PI_TP2\SSSS4\linkedin_ds-jobs.csv')