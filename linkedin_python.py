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
print(soup.prettify())
