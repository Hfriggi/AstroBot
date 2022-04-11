# AstroBot - Twitter bot
This script in python gets the AstroPhotography Of the Day (APOD) from NASA.APOD and Astrobin APOD and post in a twitter account using Twitter API.

For use this script locally, you will need to get yours keys from Twitter API and put then in a archive called keys.txt one by line in this order:

api_key <br /> 
api_secret_key <br />
access_token <br />
access_token_secret <br />

Make sure the api_key is in the first line, api_secret_key in second line, acess_token in third line and acess_token_secret in the last line. And, of course, this keys.txt
need to be in the same folder than ASTROBOT.py

This script generate 2 jpeg files, one named file_to_upload.jpeg and another called astrobin.jpeg and use this 2 images to make the post in twitter.

To use this bot in AWS, you will need to zip all libs and the script file to a zip file and up it to AWS lambda function

The posts will be like the images bellow:

![image](https://user-images.githubusercontent.com/91426980/162233963-2faf2f9a-d7a8-4ea4-b6f6-dfbcd6fe1054.png)
![image](https://user-images.githubusercontent.com/91426980/162234141-d3347aad-8b65-4f46-9594-abad576c1e69.png)

Enjoy!
