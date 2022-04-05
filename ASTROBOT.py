from pickletools import optimize
import tweepy
import requests 
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import os

keysTxtFile = open('keys.txt', 'r')

apiKey = keysTxtFile.readline().strip()
apiSecretKey = keysTxtFile.readline().strip()
accessToken = keysTxtFile.readline().strip()
accessSecretToken = keysTxtFile.readline().strip()

authentificatorApi = tweepy.OAuthHandler(apiKey, apiSecretKey)
authentificatorApi.set_access_token(accessToken, accessSecretToken)
api = tweepy.API(authentificatorApi, wait_on_rate_limit = True)

def getdata(url): 
    r = requests.get(url) 
    return r.text 

def download_image(url):
    fullname = "image_to_upload.jpeg"
    urllib.request.urlretrieve(url,fullname) 

#ASTROBIN

htmldata = getdata("https://www.astrobin.com/iotd/archive/") 
soup = BeautifulSoup(htmldata, 'html.parser')

tittle = soup.find('div', class_= 'iotd-archive-image').find('h3')
credits = soup.find('div', class_= 'data hidden-phone').find('p').find('a')
imageAddress = soup.find('figure').find('a').get('href')

linkImageUrl = 'https://www.astrobin.com/full' + imageAddress
linkImageSpecs = 'https://www.astrobin.com' + imageAddress

htmldata = getdata(linkImageSpecs)
soup = BeautifulSoup(htmldata, 'html.parser')

infos = soup.find( "div", class_= 'body').text.strip('\n')
specs = specs.replace('Imaging Telescopes Or Lenses', 'Telescope:').replace('Imaging Cameras', 'Camera:').replace('Software','Software:').replace('Accessories','Accessories:')
specs = specs.replace('Guiding Telescopes Or Lenses','GuideScope:').replace('Guiding Cameras','Guider:').replace('Mounts', 'Mount:').replace('Filters', 'Filters:')
specs = specs.replace('\n\n·\n\n', ', ')
specs = specs.encode('utf-8').decode('ascii', 'ignore')
specs = specs[:280]

htmldata = getdata(linkImageUrl)
soup = BeautifulSoup(htmldata, 'html.parser')

astrobinImageLink = soup.find('figure').find('img')['src']

path = "astrobin.jpg"
response = requests.get(astrobinImageLink, headers={'User-Agent': 'Mozilla/5.0'})
file = open(path, "wb")
file.write(response.content)

imageSize = os.path.getsize('astrobin.jpg')

if imageSize > 5000000:
    foo = Image.open('astrobin.jpg')
    imageSize = foo.size
    rgb_foo = foo.convert('RGB')
    rgb_foo = rgb_foo.resize((imageSize), Image.ANTIALIAS)
    rgb_foo.save('astrobin.jpg', optimize=True, quality=85)

creditsText = 'Image Credit & Copyright: ' + credits.text.strip()

postText = 'Image Of The Day (IOTD) by Astrobin: \n' + tittle.text + '\n' + creditsText + '\n' + linkImageUrl + '\n' + '#astrophotography #astronomy #APOD #nasa #astrobin' + '\n'
postText[:280]

media_id = api.media_upload('astrobin.jpg').media_id
original_tweet = api.update_status(postText, media_ids=[media_id])
reply1_tweet = api.update_status(status=specs, in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata = True)

#NASA

htmldata = getdata("https://apod.nasa.gov/apod/astropix.html") 
soup = BeautifulSoup(htmldata, 'html.parser')

infos = soup.findAll("center")[1]

linkToNasaImage = soup.find('img')['src']   
nasaImageLink = 'https://apod.nasa.gov/apod/' + linkToNasaImage        
download_image(nasaImageLink)

infos = infos.text.strip().replace('Copyright:', '').replace('&', '').replace('Image Credit', 'Image Credits:') + '\n'

apodLink = 'https://apod.nasa.gov/apod/astropix.html \n'

postText2 = 'Astronomy Picture of the Day (APOD) by apod.nasa:\n'  + infos + apodLink + '#astrophotography #astronomy #APOD #nasa #astrobin'

api.update_status_with_media(PostText2, 'image_to_upload.jpeg')

keysTxtFile.close()
