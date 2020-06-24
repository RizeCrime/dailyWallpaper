##  ksetwallpaper.py is taken from https://github.com/pashazz/ksetwallpaper

import praw 
import configparser 
import requests
import shutil
import os
import datetime

import ksetwallpaper

## set up reddit api
config = configparser.ConfigParser()
config.read('auth.ini')
client_id = config['Login']['client_id']
client_secret = config['Login']['client_secret']
## not actually needed
# user_name = config['Login']['user_name']
# user_password = config['Login']['user_password']
## not actually sure but whatever
user_agent = 'Wallpaper finder'

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)#, username=user_name, password=user_password)
## should print your user if you use login name and password, None if only api
# print(reddit.user.me())

## get top posts of the day
subreddit = reddit.subreddit('wallpaper')
for submission in subreddit.top(time_filter='day', limit=3):
    ## check if file ends in .png or .jpg and save the file ending (just to sort out some weird other formats)
    print(submission.title)
    if '.jpg' in submission.url or '.png' in submission.url:
        top_post = submission
        break
    else:
        continue
## debugging/testing
# for submission in subreddit.top(time_filter='day', limit=1):
#     print(submission.title)
#     print(submission.url)

## check for / create directory to store wallpapers in
path = './wallpapers'
try:
    os.mkdir(path)
## if the folder already exists I don't care, error handling 12/10 right here
except FileExistsError:
    pass

## reduce name length to max 12 chars
if len(top_post.title) > 12:
    post_title = f'{top_post.title[:12]}xxx'
else:
    post_title = top_post.title
## set wallpaper name to date of download (example: '2020-06-24') and append the original id and title
wp_name = f'{str( datetime.date.today().isoformat() )}_{top_post.id}_{post_title}{top_post.url[-4:]}'
## download image from top post of the day
r = requests.get(top_post.url, stream = True)
r.raw.decode_content = True
## save to disk
with open(f'./wallpapers/{wp_name}', 'wb') as image:
    shutil.copyfileobj(r.raw, image)

## set as wallpaper
ksetwallpaper.setwallpaper(os.path.abspath(f'./wallpapers/{wp_name}'))
print(os.path.abspath(f'./wallpapers/{wp_name}'))