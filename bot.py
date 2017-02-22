#!/usr/bin/env python

import os
import tweepy
from secrets import *
from time import strftime, gmtime

# ====== Individual bot configuration ==========================
bot_username = 'ResurrectionBot'
logfile_name = bot_username + ".log"
# ==============================================================

# Twitter authentication
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

# static reply bot has a constant tweet text
def create_tweet(sname):
    message = "He is risen indeed!"
    # Format as a reply to given twitter user
    text = "@%s " % (sname)
    text += message
    return text

def send_tweet(text, s):
    """Send out the text as a tweet."""
    # Send the tweet and log success or failure
    try:
        api.update_status(text, s.id)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        try:
            log("Tweeted: " + text + "\nIn reply to: " + s.text.encode('utf-8'))
        except UnicodeDecodeError:
            log("Tweet text could not be decoded, check online")

def is_okay(tweet):
    list = ['RT @',
            'dick',
            'indeed']
    for i in list:
        if i in tweet.text:
            return False
    return True

def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)

if __name__ == "__main__": # basically treated as the main method if bot.py is executed on its own
    # Read in last time_stamp
    with open("time_stamp.txt", 'r') as f:
        time_stamp = f.read()
    # list of specific strings we want to check for in Tweets
    match_list = ['He is risen',
        'he is risen',
        'He is Risen']

    for tweet in tweepy.Cursor(api.search,
                            q="He is risen",
                            lang = "en",
                            since_id = time_stamp).items(100):
        for j in match_list: # check each exact string
            if (j in tweet.text) and (not tweet.retweeted) and is_okay(tweet):
                sn = tweet.user.screen_name
                m = create_tweet(sn)
                send_tweet(m, tweet)

    # Update time_stamp so we only pass over a series of tweets once
    with open("time_stamp.txt", 'w') as f:
        f.write(strftime("%d %b %Y %H:%M:%S", gmtime()))

# TODO still have some possible repeats, since_id does not seem to work
# properly, problem may be reverting to max_id when overloaded or in general.
# Shippable solution: only run every week to ensure no overlap
# TODO automate to automatically run every so often, look at markov_bot
# TODO make sure does not say bad things
