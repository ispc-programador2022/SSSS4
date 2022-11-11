import requests 
from bs4 import BeautifulSoup

#definimos una variable con la dirección del website que vamos a anlizar
webLinkedinJobs = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Scientist'
#Usamos la librería request para hacer una solicitud GET a la página. Guardamos el resultado en "result"
result = requests.get(webLinkedinJobs)
#Obtenemos el texto de un elemento beatifulsoup y lo asignamos a una variable "content"
content = result.text

#utilizamos la herramienta beatifulsoup y como parámetro pasamos el contenido y el parser. Obtenemos la sopa de contenidos
soup = BeautifulSoup(content, 'lxml')
#Podemos usar un print y el método de beatifulsoup "prettify" para evaluar el contenido:
#print(soup.prettify())

#Para buscar un elemento dentro del HTML (Luego de inspeccionarlo en en navegador) usamos el método "find" de bs4
#Primer argumento el nombre del tag, segundo argumento el nombre del atributo. Eso lo igualamos a una variable "contenedor"
contenedor = soup.find('div', class_= 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
#Dentro del contenedor buscamos algun elemento que nos interese para obtener el texto:
#soup.find('h3', class_='base-search-card__title').get_text() 
#Mejorando el código:
titulo = contenedor.find('h3', class_='base-search-card__title').get_text()
#Imprimimos en consola el resultado:
#print(titulo)

titulos = soup.find_all('h3', class_='base-search-card__title')
titulos_trabajos = []

for titulo in titulos:
    titulos_trabajos.append(titulo.text.strip())
 
#print(titulos_trabajos)

#Otra forma utilizando paginación
def linkedin_scraper(webpage, page_number):
    next_page = webpage + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content,'lxml')

    soup_title= soup.findAll("h2",{"class":"title"})
    soup_para= soup.findAll("div",{"class":"post-content image-caption-format-1"})
    soup_date= soup.findAll("span",{"class":"thetime"})

    for x in range(len(soup_title)):
        article_author.append(soup_para[x].a.text.strip())
        article_date.append(soup_date[x].text.strip())
        article_link.append(soup_title[x].a['href'])
        article_title.append(soup_title[x].a['title'])
        article_para.append(soup_para[x].p.text.strip())

#Generating the next page url
    
    if page_number <16: 
        page_number = page_number + 1
        opencodezscraping(webpage, page_number)
 
#calling the function with relevant parameters
 
opencodezscraping('https://www.opencodez.com/page/', 0)
 
#creating the data frame and populating its data into the csv file
 
data = { 'Article_Link': article_link, 'Article_Title':article_title, 'Article_Para':article_para, 'Article_Author':article_author, 'Article_Date':article_date}
 
df = DataFrame(data, columns = ['Article_Link','Article_Title','Article_Para','Article_Author','Article_Date'])
 
df.to_csv(r'C:\Users\scien\Desktop\Machine Learning\OpenCodez_Articles.csv')