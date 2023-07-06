import tweepy
import requests 
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import io
import json
import sys

def getdata(url): 
    r = requests.get(url) 
    return r.text 

client = tweepy.Client(
    consumer_key='',
    consumer_secret= '',
    access_token= '',
    access_token_secret= ''
)

auth = tweepy.OAuth1UserHandler(
   "", "",
   "", ""
)
api = tweepy.API(auth)

def postImages(event=None,context=None):

    sessionKeys = {'api_key': '', 
                   'api_secret': ''}

    imageOfDaylink = requests.get(url='http://astrobin.com/api/v1/imageoftheday/', params= sessionKeys)

    if imageOfDaylink.status_code == 200:
        print('API Astrobin APOD get success:', imageOfDaylink.status_code)

        response = json.loads(imageOfDaylink.text)
        image_value = response['objects'][0]['image']
        print('\n' +'doing a get in:' + 'http://astrobin.com' + image_value)

        imageSpecs = requests.get(url='http://astrobin.com' + image_value, params= sessionKeys)
        if imageSpecs.status_code == 200:
            print('\n' +'API ' + 'http://astrobin.com' + image_value + ' get success:', imageOfDaylink.status_code)
        
        response = json.loads(imageSpecs.text)

        imageMedium = response['url_hd']
        imageTiny = response['url_regular']
        skyPlot = response['url_advanced_skyplot']
        telescopes = response['imaging_telescopes']
        cameras = response['imaging_cameras']
        user = response['user']
        tittle = response['title']
        telescopes = ', '.join(map(str, telescopes))
        cameras = ', '.join(map(str, cameras))

        creditsText = 'Image Credit & Copyright: ' + user
        linkImageUrl = 'https://astrobin.com' + image_value
        
        imageGet = requests.get(url=imageMedium, params= sessionKeys).content

        skyPlotGet = requests.get(url=skyPlot).content

        skyPlotImage = io.BytesIO(skyPlotGet)

        print('skyPlot: ', skyPlotImage)

        imageSize = sys.getsizeof(imageGet)

        if imageSize > 5000000:
            imageGet = requests.get(url=imageTiny, params= sessionKeys).content
            imageSize = sys.getsizeof(imageGet)
            if imageSize > 5000000:
                image = io.BytesIO(imageGet)
                print(image)
            else:
                print('shit')
        else:
            image = io.BytesIO(imageGet)
            print('\n' +'image size = ', imageSize)
            print(image)

        print('-------------------------------------------------' + '\n' + 'POST TEXT:')
        postText = 'Image Of The Day (IOTD) by Astrobin: \n' + tittle + '\n' + creditsText + '\n' + linkImageUrl.replace('/api/v1/image', '') + '\n' + '#astrophotography #astronomy #APOD #nasa #astrobin' + '\n'
        postText[:279]

        print(postText)

        print('-------------------------------------------------' + '\n' + 'IMAGE SPECS:')
        specs = '\n' + 'telescopes: ' + telescopes.replace('"', '') + '\n' + 'cameras: '+ cameras.replace('"', '') + '\n' + 'Location on the sky (Red Square bellow):'
        print(specs)

        print('-------------------------------------------------' + '\n' + 'POSTING TWEET:' + '\n')


        media_id = api.media_upload('image.jpeg', file=image).media_id
        skyPlotImage_id = api.media_upload('image.jpeg', file=skyPlotImage).media_id
        
        media_id = str(media_id)
        skyPlotImage_id = str(skyPlotImage_id)
        print('media sucessfully uploaded, media id: ', media_id, '\n', 'skyPlotMedia Id = ', skyPlotImage_id)

        original_tweet = client.create_tweet(text=postText, media_ids=[media_id])
        print(original_tweet)
        original_tweet = original_tweet.data['id']
        print('tweet sucessfully uploaded, tweet id: ', original_tweet)

        reply1_tweet = client.create_tweet(text=specs, in_reply_to_tweet_id=original_tweet, media_ids=[skyPlotImage_id])
        print('reply sucessfully uploaded, tweet id: ', original_tweet)

    else:
        print('API Astrobin APOD get error: ', imageOfDaylink.status_code)

postImages()
