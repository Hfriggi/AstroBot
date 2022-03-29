from time import time
import tweepy
import requests 
from bs4 import BeautifulSoup
import urllib.request
import time
import numpy as np

keysTXT = open('keys.txt', 'r')

api_key = keysTXT.readline().strip()
api_secret_key = keysTXT.readline().strip()
access_token = keysTXT.readline().strip()
access_token_secret = keysTXT.readline().strip()

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)


#ASTROBIN

def getdata(url): 
    r = requests.get(url) 
    return r.text 

htmldata = getdata("https://www.astrobin.com/iotd/archive/") 
soup = BeautifulSoup(htmldata, 'html.parser')

titulo = soup.findAll("h3")
credito = soup.find('div', class_= 'data hidden-phone').find('p').find('a')
endereco = soup.find('figure').find('a')

data = soup.find_all('div', class_="astrobin-image-container")
a_class = data[0].find_all('a')
url_ = a_class[0].get('href')

linke = 'https://www.astrobin.com/full' + url_
link_ = 'https://www.astrobin.com' + url_

g = requests.get(link_)
soup = BeautifulSoup(g.text, 'html.parser')

infos = soup.find( "div", class_= 'body').text.strip('\n')
specs = infos.replace('Imaging Telescopes Or Lenses', 'Telescope:').replace('Imaging Cameras', 'Camera:').replace('Software','Software:').replace('Accessories','Accessories:').replace('Guiding Telescopes Or Lenses','GuideScope:').replace('Guiding Cameras','Guider:').replace('Mounts', 'Mount:').replace('Filters', 'Filters:')
specs = specs.replace('\n\n·\n\n', ', ')

if len(specs) > 279:
    specs = specs[:279]

h = requests.get(linke)
soup = BeautifulSoup(h.text, 'html.parser')

images = soup.find('figure')

for image in images:
    name = image['alt']
    link = image['src']   
    

path = "astrobin.jpeg"
response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
file = open(path, "wb")
file.write(response.content)

texto_credito2 = 'Image Credit & Copyright: ' + credito.text.strip()


textoposta = 'Image Of The Day (IOTD) by Astrobin: \n' + titulo[0].text.strip() + '\n' + texto_credito2 + '\n' + linke + '\n' + '#astrophotography #astronomy #APOD #nasa #astrobin' + '\n'

if len(textoposta) > 279:
    textoposta = textoposta[:279]

media_id = api.media_upload('astrobin.jpeg').media_id
original_tweet = api.update_status(textoposta, media_ids=[media_id])
reply1_tweet = api.update_status(status=specs, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata = True)

#NASA

def getdata2(url): 
    r = requests.get(url) 
    return r.text 

htmldata = getdata2("https://apod.nasa.gov/apod/astropix.html") 
soup = BeautifulSoup(htmldata, 'html.parser')

Container = soup.findAll("center")[1].find("a")
Container2 = soup.findAll("b")
    
images = soup.find_all('img')
for image in images:
    name = image['alt']
    link = image['src']
        
    RealImage = 'https://apod.nasa.gov/apod/' + link

def download_image(url):
    fullname = "image_to_upload.jpeg"
    urllib.request.urlretrieve(url,fullname)     
download_image(RealImage)
            
mensagem = 'Astronomy Picture of the Day (APOD) by apod.nasa:'

texto = Container2[0].text.strip()

texto_credito = 'Image Credit & Copyright: ' + Container.text

apod = 'https://apod.nasa.gov/apod/astropix.html'

titulo = 'Astronomy Picture of the Day (APOD) by apod.nasa: \n' +texto + '\n' +texto_credito + '\n' + apod + '\n' + '#astrophotography #astronomy #APOD #nasa #astrobin'

api.update_status_with_media(titulo, 'image_to_upload.jpeg')

keysTXT.close()