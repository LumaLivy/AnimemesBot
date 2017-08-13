import praw as Praw
import tweepy as Tweepy
from tweepy_config import *

import urllib.request

import random
import sys
import time
import os

def postAnimemes():
    #praw setup with private details from in praw.ini
    reddit = Praw.Reddit("animemesbot")

    #tweepy setup info is taken from another secret file
    auth = Tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    tweepy = Tweepy.API(auth)

    #subreddit prep section
    subreddit_file = open(subreddits_file_path, 'r')
    subreddit_names = subreddit_file.read().strip().split("\n")
    subreddit_file.close()

    #make sure the file is a direct image link so the bot isn't confused
    extension_okay = False

    while extension_okay == False:
        post = reddit.subreddit(random.choice(subreddit_names)).random() #pick a random post
        extension = post.url[-4:] #get the extension from the url

        for file_type in ['.jpg', '.png', '.gif']:
            if (extension == file_type):
                extension_okay = True
                break

    #the file name the image will be temporarily saved as
    image_file = "meme" + extension

    #download the image and save it as 'meme.jpg' for example
    urllib.request.urlretrieve(post.url, image_file)

    #setup the body message for the tweet
    status = '"' + post.title + '" from /r/' + post.subreddit.display_name

    #this is probably not an elegant solution, but it works.
    #alternate title if status above is too long
    if (len(status) > 140):
        status = '"' + post.title + '"'

        #if the status is still too long
        if (len(status) > 140):
            status = 'from /r/' + post.subreddit.display_name

        #if the status is too long at this point, I'm pretty sure something went horribly wrong.

    #tweet everything
    tweepy.update_with_media(image_file, status)

    #delete the image from the system
    os.remove(image_file)

#showtime
postAnimemes()
