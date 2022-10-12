from pickletools import optimize
import tweepy
import requests 
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import os
import boto3

txtFileName = 'keys.txt'
delimiter = ':'

file = open(txtFileName, 'r')

def findValues(string):
    string = string.rstrip('\n')
    value = string[string.index(delimiter)+1:]
    value = value.replace(' ','')
    return value

for line in file:
    if line.startswith('api_key'):
        apiKey = findValues(line)
    if line.startswith('api_secret'):
        apiSecretKey = findValues(line)
    if line.startswith('access_token'):
        accessToken = findValues(line)
    if line.startswith('access_secret'):
        accessSecret = findValues(line)

authentificatorApi = tweepy.OAuthHandler(apiKey, apiSecretKey)
authentificatorApi.set_access_token(accessToken, accessSecret)
api = tweepy.API(authentificatorApi, wait_on_rate_limit = True)

def downloadImageS3(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
    session = boto3.Session()
    s3 = session.resource('s3')
    bucket_name = 'YourBucketName' # YourBucketName is the name of your bucket in S3
    key = 'image.jpg' # key is the name of file on your bucket
    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(r.raw, key)
 
def getdata(url): 
    r = requests.get(url) 
    return r.text 

def downloadImageNasa(url):
    fullname = "image_to_upload.jpeg"
    urllib.request.urlretrieve(url,fullname) 

def downloadImageAstrobin(url):
    path = "astrobin.jpg"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    file = open(path, "wb")
    file.write(response.content)

def resizeImage():
    foo = Image.open('astrobin.jpg')
    imageSize = foo.size
    rgb_foo = foo.convert('RGB')
    rgb_foo = rgb_foo.resize((imageSize), Image.ANTIALIAS)
    rgb_foo.save('astrobin.jpg', optimize=True, quality=85)

#ASTROBIN

def postImages(event=None,context=None):
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

    downloadImageAstrobin(astrobinImageLink)

    imageSize = os.path.getsize('astrobin.jpg')

    if imageSize > 5000000:
        resizeImage()

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
    downloadImageNasa(nasaImageLink)

    infos = infos.text.strip().replace('Copyright:', '').replace('&', '').replace('Image Credit', 'Image Credits:') + '\n'

    apodLink = 'https://apod.nasa.gov/apod/astropix.html \n'

    postText2 = 'Astronomy Picture of the Day (APOD) by apod.nasa:\n'  + infos + apodLink + '#astrophotography #astronomy #APOD #nasa #astrobin'

    api.update_status_with_media(PostText2, 'image_to_upload.jpeg')

keysTxtFile.close()
