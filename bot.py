# -*- coding: utf-8 -*-
# butts lol

import platform
import os
if platform.system() == "Windows":
    os.system('color')
import re
import sys
import time
import html
import tweepy
import random
import markov
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import threading
import unidecode
import stringdist
import configparser
from termcolor import cprint

# CONFIG & SETUP #

CONFIG = configparser.ConfigParser()
CONFIG.read('bot.cfg')
logging.basicConfig(handlers=[RotatingFileHandler('./bot.log', maxBytes=500, backupCount=1)], level=logging.INFO,
                    format='%(asctime)s - %(levelname)s\t\t%(message)s')
AUTH = tweepy.OAuthHandler(str(CONFIG.get('Twitter', 'CONSUMER_KEY')),
                           str(CONFIG.get('Twitter', 'CONSUMER_SECRET')))
AUTH.set_access_token(str(CONFIG.get('Twitter', 'ACCESS_KEY')),
                      str(CONFIG.get('Twitter', 'ACCESS_SECRET')))
API = tweepy.API(AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, timeout=60)

USERNAME = API.verify_credentials().screen_name
MARKOV_CHOOSER = float(CONFIG.get('Bot', 'MARKOV_PROB'))

sys.stdout = sys.__stdout__
if CONFIG.getboolean('Misc', 'CONSOLE_OUTPUT') is False:
    sys.stdout = open(os.devnull, 'w')

MAIN_MODE = str(CONFIG.get('Bot', 'MODE'))
if MAIN_MODE == 'default':
    COUNT = int(CONFIG.get('Bot', 'TWEET_COUNT'))
    M_COUNT = int(CONFIG.get('Bot', 'M_COUNT'))
    ORDER = int(CONFIG.get('Bot', 'ORDER'))
    SEARCH_COUNT = int(CONFIG.get('Bot', 'SEARCH_COUNT'))
    if SEARCH_COUNT > 100:
        cprint('You cannot use a number greater than 100, the twitter API will not return more results. Check the configuration file.', 'red')
        logging.error('You cannot use a number greater than 100.')
        exit()
    TRIES = int(CONFIG.get('Bot', 'MAX_TRIES'))
    IMAGE_FOLDER = str(CONFIG.get('Bot', 'IMAGE_FOLDER'))
    if os.path.isdir(IMAGE_FOLDER) == False:
        os.mkdir(IMAGE_FOLDER)
    MAIN_CHOOSER = float(CONFIG.get('Bot', 'IMAGE_PROB'))
    UPPER_PROB = float(CONFIG.get('Bot', 'UPPER_PROB'))
    ALLOW_RTS = CONFIG.getboolean('Bot', 'ALLOW_RTS')
    DISTANCE = float(CONFIG.get('Bot', 'DISTANCE'))
    MIN_LENGTH = int(CONFIG.get('Bot', 'MIN_LENGTH'))
    ACCOUNTS = tuple(set(i for i in (str(CONFIG.get('Bot', 'ACCOUNTS'))
                                     .replace(' ', '')).split(',') if i))
    if len(ACCOUNTS) == 1:
        cprint('You MUST specify more than 1 account. Check bot.cfg.', 'red')
        logging.error('You MUST specify more than 1 account. Check bot.cfg.')
        exit()
elif MAIN_MODE == 'write':
    COUNT = int(CONFIG.get('Bot', 'TWEET_COUNT'))
    SEARCH_COUNT = int(CONFIG.get('Bot', 'SEARCH_COUNT'))
    if SEARCH_COUNT > 100:
        cprint('You cannot use a number greater than 100, the twitter API will not return more results. Check the configuration file.', 'red')
        logging.error('You cannot use a number greater than 100.')
        exit()
    TRIES = int(CONFIG.get('Bot', 'MAX_TRIES'))
    UPPER_PROB = float(CONFIG.get('Bot', 'UPPER_PROB'))
    MAIN_CHOOSER = 0
    ALLOW_RTS = CONFIG.getboolean('Bot', 'ALLOW_RTS')
    DISTANCE = float(CONFIG.get('Bot', 'DISTANCE'))
    MIN_LENGTH = int(CONFIG.get('Bot', 'MIN_LENGTH'))
    ACCOUNTS = tuple(set(i for i in (str(CONFIG.get('Bot', 'ACCOUNTS'))
                                     .replace(' ', '')).split(',') if i))
    if len(ACCOUNTS) == 1:
        cprint('You MUST specify more than 1 account. Check the configuration file.', 'red')
        logging.error('You MUST specify more than 1 account. Check the configuration file.')
        exit()
elif MAIN_MODE == 'markov':
    M_COUNT = int(CONFIG.get('Bot', 'M_COUNT'))
    ORDER = int(CONFIG.get('Bot', 'ORDER'))
    TRIES = int(CONFIG.get('Bot', 'MAX_TRIES'))
    UPPER_PROB = float(CONFIG.get('Bot', 'UPPER_PROB'))
    MAIN_CHOOSER = 2
    ALLOW_RTS = CONFIG.getboolean('Bot', 'ALLOW_RTS')
    MIN_LENGTH = int(CONFIG.get('Bot', 'MIN_LENGTH'))
    ACCOUNTS = tuple(set(i for i in (str(CONFIG.get('Bot', 'ACCOUNTS'))
                                     .replace(' ', '')).split(',') if i))
    if len(ACCOUNTS) == 1:
        cprint('You MUST specify more than 1 account. Check the configuration file.', 'red')
        logging.error('You MUST specify more than 1 account. Check the configuration file.')
        exit()
elif MAIN_MODE == 'image':
    IMAGE_FOLDER = str(CONFIG.get('Bot', 'IMAGE_FOLDER'))
    if os.path.isdir(IMAGE_FOLDER) == False:
        os.mkdir(IMAGE_FOLDER)
    MAIN_CHOOSER = 1
else:
    cprint('ERROR: Main mode is not declared properly. Check bot.cfg.', 'red')
    logging.error('ERROR: Main mode is not declared properly. Check bot.cfg.')
    exit()

TIME_MODE = str(CONFIG.get('Bot', 'TIME_MODE'))
if TIME_MODE == 'fixed':
    TIME_MIN = TIME_MAX = float(CONFIG.get('Bot', 'FIXED_TIME_INTERVAL'))
elif TIME_MODE == 'random':
    TIME_MIN = float(CONFIG.get('Bot', 'TIME_INTERVAL_MIN'))
    TIME_MAX = float(CONFIG.get('Bot', 'TIME_INTERVAL_MAX'))
else:
    cprint('ERROR: Time mode is not declared properly. Check bot.cfg.', 'red')
    logging.error('ERROR: Time mode is not declared properly. Check bot.cfg.')
    exit()

ALLOW_REPLIES = CONFIG.getboolean('Replies', 'ALLOW_REPLIES')
if ALLOW_REPLIES is True:
    REPLIES_MODE = str(CONFIG.get('Replies', 'REPLIES_MODE'))
    if REPLIES_MODE == 'default':
        FILES = tuple(set(i for i in (str(CONFIG.get('Replies', 'FILES'))
                                         .replace(' ', '')).split(',') if i))
        FILE_SPLIT = str(CONFIG.get('Replies', 'FILE_SPLIT'))
        REPLY_CHOOSER = float(CONFIG.get('Replies', 'FILE_PROB'))
    elif REPLIES_MODE == 'file':
        FILES = tuple(set(i for i in (str(CONFIG.get('Replies', 'FILES'))
                                         .replace(' ', '')).split(',') if i))
        FILE_SPLIT = str(CONFIG.get('Replies', 'FILE_SPLIT'))
        REPLY_CHOOSER = 1
    elif REPLIES_MODE == 'vowel':
        REPLY_CHOOSER = 0
    else:
        cprint('ERROR: Reply mode is not declared properly. Check bot.cfg.', 'red')
        logging.error('ERROR: Reply mode is not declared properly. Check bot.cfg.')
        exit()

cprint('DRILFICTION.TXT 2.0', 'grey', 'on_blue', end='')
cprint(' - a really stupid twitter bot based on PYNSUFFERABLE and heroku_ebooks.', 'blue')

class GetTweetsError(Exception):
    """Works like an interrupt for an error that may happen when getting tweets."""

class Stream(tweepy.StreamListener):
    """Replies streaming. Overrides method on tweepy.StreamListener."""
    def on_status(self, status):
        """Triggers always we get a new status"""
        cprint('\nNew mention from: ', 'green', end='')
        cprint(status.author.screen_name, 'magenta')
        logging.info(str('New mention: ' + status.author.screen_name + ' - ' + status.text))
        reply = clean(status.text)
        if (random.random() == 1.0):
            # reply with "no."
            reply = 'no.'
        elif (REPLY_CHOOSER > random.random() < 1.0) or (not reply):
            # REPLY FILE SELECTION
            FILE = random.choice(FILES)
            file = open(FILE, 'r')
            reply = random.choice(''.join(file.readlines()).split(FILE_SPLIT))
            file.close()
        else:
            reply = reply \
                .replace('a', 'i').replace('á', 'í').replace('A', 'I').replace('Á', 'Í') \
                .replace('e', 'i').replace('é', 'í').replace('E', 'I').replace('É', 'Í') \
                .replace('o', 'i').replace('ó', 'í').replace('O', 'I').replace('Ó', 'Í') \
                .replace('u', 'i').replace('ú', 'í').replace('U', 'I').replace('Ú', 'Í')
        if len(reply) > 259:
            reply = reply[0:258]
        API.update_status(''.join(('@', status.author.screen_name, ' ', reply)), status.id)
        cprint('\nReplied: ', 'green')
        cprint(reply, 'magenta')

# Doing this to compare new tweets with old to avoid too much repetition. -kh
# Saves successful tweets to a database

def save_tweet(tweet, tweet_type):
    conn = sqlite3.connect("drilfiction.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY, tweet TEXT, tweet_type TEXT)")
    cur.execute("INSERT INTO tweets VALUES (NULL, ?, ?)", (tweet, tweet_type))
    conn.commit()

# Accesses the DB for comparison

def search_tweets():
    conn = sqlite3.connect("drilfiction.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tweets")
    rows = cur.fetchall()
    COLUMN = 1
    column=[elt[COLUMN] for elt in rows]
    return column

# Compares the tentative tweet with older ones to avoid becoming too repetitive

def compare_tweets(tweet):
    for item in search_tweets():
        row = item
        if stringdist.levenshtein_norm(row, tweet) > DISTANCE:
            cprint('GetTweetsError: New Tweet is too similar to old tweets. Trying again.')
            logging.error(str('GetTweetsError: New Tweet is too similar to old tweets. Trying again.'))
            raise GetTweetsError
            return False
        else:
            return True

def clean(raw_tweet, word_start=('@', 'http://', 'https://', 'RT'), word_end='…',
          from_word=('meirl', 'me_irl', '#', '…', '"')):
    """ Cleans up every tweet word by word, using some variables specified this function:
    'word_start' defines what words to erase if they start with some string (like http:// on links).
    'word_end' is the same as WORD_START, but at the end of the word. (like '…' on truncated words).
    'from_word' defines what str should be deleted from a word, without deleting the word itself.
    Also, if ALLOW_RTS is set to False, it will ignore tweets starting with 'RT @'.
    """
    cleaned = list()
    if (ALLOW_RTS is False) and raw_tweet.startswith('RT @'):
        return ''
    else:
        for word in raw_tweet.split():
            if (not word.startswith(word_start)) and (not word.endswith(word_end)):
                for i in from_word:
                    word = word.replace(i, '')
                if word:
                    cleaned.append(word)
        return ' '.join(cleaned)

def start_replies():
    """When enabled, it will wait for new mentions and reply to them. See Stream class above"""
    while True:
        try:
            rp_stream = tweepy.Stream(auth=API.auth, listener=Stream())
            rp_stream.filter(track=[str('@' + USERNAME)])

        except Exception as rp_except:
            cprint('Replies: Stream was stopped! Reconnecting in 60 secs. Exception:', 'red')
            print(rp_except.args)
            logging.error('Replies: Stream was stopped! Reconnecting. Exception:')
            logging.error(rp_except.args)
            time.sleep(60)
            continue

def new_tweet():
    """Publishes new tweets"""

    # ACCOUNT SELECTION
    acc1 = random.choice(ACCOUNTS)
    acc2 = random.choice(ACCOUNTS)
    while acc1 == acc2:
        acc2 = random.choice(ACCOUNTS)

    # RETRIEVING TWEETS:
    # tweets1 is gotten directly from the acc1 timeline. Then, tweet1 is chosen randomly.
    # tweets2 is a bit more tricky: If we want to join 2 tweets we need a reference, a common word:
    # union. This is chosen randomly from tweet1 and used as a search argument to get tweets2 from
    # acc2. The way twitter search works, this is not always true, we can get tweets that do not
    # contain union. So we discard those. Good job twitter.
    # Sometimes also the search returns nothing, sometimes returns invalid tweets, such as
    # image links or some other trash. TRIES specifies how many times should the bot should try to get tweets.
    # In case the TRIES limit is reached, an exception will be raised: GetTweetsError,
    # but it works more like an interrupt to avoid an infinite loop.

    cprint('Mode: Mashup', 'yellow')
    cprint('Getting tweets...', 'yellow')
    if COUNT > 1000:
        cprint('Hang in there, this could take some time!', 'yellow')
    tweets1 = list(filter(None,
                          [clean(t.full_text)
                           for t in tweepy.Cursor(API.user_timeline, id=acc1, tweet_mode="extended").items(COUNT)]))
    # If tweets1 is empty (this is REALLY unusual)
    if not tweets1:
        cprint('GetTweetsError: wtf, tweet1 is empty, this is very unusual. Check: ' + acc1)
        logging.error(str('GetTweetsError: Tweet1 is empty, this is very unusual. Check: ' + acc1))
        raise GetTweetsError
    tweet1 = random.choice(tweets1)
    if len(tweet1) < MIN_LENGTH:
        cprint('GetTweetsError: Ugh, tweet1 is too short. Trying again.')
        logging.error(str('GetTweetsError: Tweet1 is too short. Trying again.'))
        raise GetTweetsError

    union = unidecode.unidecode(random.choice(tweet1.split())).lower()
    tweets2 = list()
    for t in list(filter(None, [clean(t.full_text)
                                for t in
                                API.search(q=''.join(('from:', acc2, ' ', union)),
                                           count=SEARCH_COUNT, tweet_mode='extended')])):
        try:
            (t.split()).index(union)
            tweets2.append(t)
        except ValueError:
            pass
    # If tweets2 is empty, we can assume that 'union' is the problem (could be a weird
    # word, a number, a word in another language, etc.) so we choose it again.
    i = 0
    while not tweets2:
        i = i + 1
        union = unidecode.unidecode(random.choice(tweet1.split())).lower()
        tweets2 = list()
        for t in list(filter(None, [clean(t.full_text)
                                    for t in
                                    API.search(q=''.join(('from:', acc2, ' ', union)),
                                               count=SEARCH_COUNT, tweet_mode='extended')])):
            try:
                (t.split()).index(union)
                tweets2.append(t)
            except ValueError:
                pass
        # If we run out of tries, we stop trying.
        if TRIES < i:
            cprint('GetTweetsError: ' + '\t|\t'.join((acc1, acc2, tweet1)), 'red')
            logging.error(str('GetTweetsError: ' + '\t|\t'.join((acc1, acc2, tweet1))))
            raise GetTweetsError
    tweet2 = random.choice(tweets2)

    # JOINING TWEETS TOGETHER
    # Searches for 'union' in the selected tweets above. To avoid case sensibility and some things
    # like accentuation, we standardize the tweets. But tweets are joined together without being
    # standard, so we don't lose the original.

    cprint('Joining tweets together...', 'yellow')
    try:
        loc1 = (unidecode.unidecode(tweet1).lower().split()).index(union)
        loc2 = (unidecode.unidecode(tweet2).lower().split()).index(union)
    except ValueError:
        cprint('ValueError: ' + '\t|\t'.join((acc1, acc2, tweet1, tweet2, union)), 'red')
        logging.error(str('ValueError: ' + '\t|\t'.join((acc1, acc2, tweet1, tweet2, union))))
        raise GetTweetsError

    if random.random() < 0.5:
        newtweet = ' '.join(tweet1.split()[0:loc1 + 1]) + ' ' \
                   + ' '.join(tweet2.split()[loc2 + 1:len(tweet2)])
    else:
        newtweet = ' '.join(tweet2.split()[0:loc2 + 1]) + ' ' \
                   + ' '.join(tweet1.split()[loc1 + 1:len(tweet1)])
    if random.random() < UPPER_PROB:
        newtweet = newtweet.upper()
    if len(newtweet) > 280:
        newtweet = newtweet[0:279]

    # COMPARING, SAVING, UPLOADING & CONSOLE OUTPUT
    cprint('Comparing with old tweets', 'yellow')
    if compare_tweets(newtweet) == True:
        tweet_type = "mashup"
        cprint('Saving to database...', 'yellow')
        save_tweet(newtweet, tweet_type)
        newtweet = html.unescape(newtweet)
        cprint('Updating status...', 'yellow')
        API.update_status(status=newtweet)
        cprint(acc1 + '  -  ', 'magenta', end='')
        cprint(tweet1, 'white')
        cprint(acc2 + '  -  ', 'magenta', end='')
        cprint(tweet2, 'white')
        cprint(union + ' |  ', 'magenta', end='')
        cprint(newtweet, 'cyan')
        logging.info('\t|\t'.join((acc1, acc2, tweet1, tweet2, union, newtweet)))
    else:
        new_tweet()

def markov_tweet():
    """Publishes tweets generated from Markov chains"""
    acc1 = random.choice(ACCOUNTS)
    acc2 = random.choice(ACCOUNTS)
    while acc1 == acc2:
        acc2 = random.choice(ACCOUNTS)
    corpus = []
    cprint('Mode: Markov', 'yellow')
    cprint('Getting tweets...', 'yellow')
    if M_COUNT >= 500:
        cprint('Buckle in, this could take a while! ', 'yellow')
    # Generates a corpus based on two twitter accounts
    corpus_tweets1 = list(filter(None,
                          [clean(t.full_text)
                           for t in tweepy.Cursor(API.user_timeline, id=acc1, tweet_mode="extended").items(M_COUNT)]))
    cprint('Adding %s to corpus' % (acc1,), 'yellow')
    if not corpus_tweets1:
        cprint('GetTweetsError: wtf, corpus_tweets1 is empty, this is very unusual. Check: ' + acc1)
        logging.error(str('GetTweetsError: corpus_tweets1 is empty, this is very unusual. Check: ' + acc1))
        raise GetTweetsError
    else:
        corpus += corpus_tweets1
    corpus_tweets2 = list(filter(None,
                          [clean(t.full_text)
                           for t in tweepy.Cursor(API.user_timeline, id=acc2, tweet_mode="extended").items(M_COUNT)]))
    cprint('Adding %s to corpus' % (acc2,), 'yellow')
    if not corpus_tweets2:
        cprint('GetTweetsError: wtf, corpus_tweets2 is empty, this is very unusual. Check: ' + acc2)
        logging.error(str('GetTweetsError: corpus_tweets2 is empty, this is very unusual. Check: ' + acc2))
        raise GetTweetsError
    else:
        corpus += corpus_tweets2
    cprint('Corpus complete!', 'yellow')
    if len(corpus) == 0:
        cprint('GetTweetsError: Aw hell naw, no statuses found in corpus!', 'red')
        logging.error(str('GetTweetsError: No statuses found in corpus!'))
        raise GetTweetsError
        markov_tweet()
    mine = markov.MarkovChainer(ORDER)
    for status in corpus:
        if not re.search('([\.\!\?\"\']$)', status):
            status += "."
        mine.add_text(status)
    for x in range(0, 10):
        newtweet = mine.generate_sentence()

    # randomly drop the last word, like the horse_ebooks of yore.
    if random.randint(0, 4) == 0 and re.search(r'(in|to|from|for|with|by|our|of|your|around|under|beyond)\s\w+$', newtweet) is not None:
        cprint('Losing last word randomly', 'yellow')
        newtweet = re.sub(r'\s\w+.$', '', newtweet)

    # if a tweet is very short, this will add a second sentence to it.
    if newtweet is not None and len(newtweet) < 40:
        cprint('Short tweet. Adding another sentence.', 'yellow')
        newer_status = mine.generate_sentence()
        if newer_status is not None:
            newtweet += " " + mine.generate_sentence()
        else:
            newtweet = newtweet
    elif random.random() < UPPER_PROB:
        newtweet = newtweet.upper()

    # SAVING, UPLOADING & CONSOLE OUTPUT
    cprint('Saving to database...', 'yellow')
    tweet_type = "markov"
    save_tweet(newtweet, tweet_type)
    cprint('Updating status...', 'yellow')
    newtweet = html.unescape(newtweet)
    API.update_status(status=newtweet)
    cprint('Markov  -  ', 'magenta', end='')
    cprint(newtweet, 'cyan')
    logging.info('\t|\t'.join((newtweet)))

def new_image():
    """Publishes images chosen randomly from a folder."""
    # Checks if there are any images in the specified folder.
    # If not and mode is 'image', exits for now.
    if len(os.listdir(IMAGE_FOLDER)) == 0:
        cprint('No images found! Consider adding images to /{}.'.format(IMAGE_FOLDER), 'red')
        logging.error('No images in image folder.')
        if MAIN_MODE == 'image':
            cprint('Exiting, sorry!', 'yellow')
            exit()
    else:
        cprint('Mode: Image', 'yellow')
        image_filename = random.choice(os.listdir(IMAGE_FOLDER))
        API.update_with_media('/'.join((IMAGE_FOLDER, image_filename)), status='')
        logging.info(''.join(('Image:', image_filename)))
        tweet_type = "image"
        save_tweet(image_filename, tweet_type)
        cprint('Uploading...', 'yellow')
        cprint('NEW TWEET WITH MEDIA: ', 'blue', end='')
        cprint(image_filename, 'magenta')
        cprint('Deleting %s so I won\'t repost it later' % (image_filename,), 'yellow')
        os.remove(os.path.join(IMAGE_FOLDER, image_filename))

def main():
    """ Main code. Basically does almost everything."""
    while True:
        try:
            cprint(time.strftime('%d/%m/%Y  /  %H:%M:%S'), 'blue')
            start = float(time.time())

            if MAIN_MODE == 'markov':
                markov_tweet()
            elif random.random() < MARKOV_CHOOSER:
                markov_tweet()
            elif random.random() < MAIN_CHOOSER:
                new_image()
            else:
                new_tweet()

            # TIME
            cprint('Done in (s): ', 'green', end='')
            cprint(float(time.time()) - start, 'magenta')

            # WAIT
            wait_time = int(60 * random.uniform(TIME_MIN, TIME_MAX))
            cprint('New tweet in: ', 'green', end='')
            cprint(int(wait_time), 'magenta', end='')
            cprint(' minutes', 'green')
            time.sleep(wait_time * 60)
        except GetTweetsError:
            cprint('GetTweetsError: Error getting tweets, trying again.', 'red')
            logging.error('GetTweetsError: Error getting tweets.')
            continue
        except Exception as mn_except:
            cprint('Main: Something was wrong! Retrying. Exception args:', 'red')
            print(mn_except.args)
            logging.error('Main: Something was wrong! Retrying. Exception args:')
            logging.error(mn_except.args)
            continue

try:
    if ALLOW_REPLIES is True:
        REPLIES = threading.Thread(target=start_replies)
        REPLIES.setDaemon(True)
        REPLIES.start()
    main()
except KeyboardInterrupt:
    exit()
