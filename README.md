# Drilfiction.txt: what if dril wrote fanfiction?
Tested on macOS 10.14 (18A391). Might work on other OSes. Written in Python 3 and licensed under GPLv3. Based on Pynsufferable: https://github.com/adwareboi/pynsufferable-twitter-bot

The bot in action: [drilfiction](https://twitter.com/drilfiction)

### What does it do?
I had originally considered creating a bot to generate Markov chains based on twitter accounts dril and fanfiction_txt, but this proved insufficient, as the results made too little sense. Branched from another project, this is a single python script bot that can randomly tweet mashed up tweets between 2 accounts, randomly tweet Markov chains, or upload photos. It keeps a record of previous tweets in a sqlite database and compares new output to them to avoid repeating itself too much.

It also can stream mentions and reply to them by changing all the vowels by 'i' or using text files as resource. Several infamously bad fanfictions are set as the default, in fitting with the theme.

### Why does it do that?
I'm teaching myself to program and had a bad idea. Maybe it was a good idea. It depends on who's looking.

### Dependecies:
- Third party libraries: `tweepy`, `unidecode`, `sqlite3`, `stringdist`, and `termcolor`
- Also you may need to install `logging` and `configparser`
- Built-in libraries: `os`, `sys`, `re`, `time`, `random` and `threading`

All of these can be installed via `pip`

### How to use it:
I just run it from a terminal since I'm a scrub, but you can run it wherever you want as you do it with python 3. I'm considering creating a web and desktop app version.
Steps:
1. You will need to create a [Twitter App](https://developer.twitter.com/en/apps) linked to an account. Get the API keys needed in order to access.
2. Edit bot.cfg with your parameters. Otherwise it won't work. See the details below
3. Enjoy. Or don't. Whatever.

### Configuration:
The configuration is pretty straightforward, here's the default one for the current version [2.0]. Hopefully it's descriptive enough:

```
[Twitter]
# Set the access keys. Get yours at developer.twitter.com. Do not use quotes.
CONSUMER_KEY =
CONSUMER_SECRET =
ACCESS_KEY =
ACCESS_SECRET =


[Bot]
# Available main modes:
# default: random. Needs: IMAGE_PROB, IMAGE_FOLDER, TWEET_COUNT, ACCOUNTS, MAX_TRIES, UPPER_PROB
# image: posts only images from a folder, needs: IMAGE_FOLDER
# write: posts only mash up tweets, needs: TWEET_COUNT, SEARCH_COUNT, ACCOUNTS, MAX_TRIES, MIN_LENGTH, UPPER_PROB
# markov: generates markov chain tweets. Needs: M_COUNT, ACCOUNTS, MAX_TRIES, MIN_LENGTH, UPPER_PROB
MODE = default

# Accounts. Separate by commas. Do not use quotes. Duplicates will be erased. (Use only one line)
ACCOUNTS = dril, fanfiction_txt
# How many tweets to retrieve from the first account.
# If it's too large, the bot may take more time. Should not be very big to avoid rate limit.
# If it's too small, the bot can fail more frequently. Should not be smaller than 10.
# 50~100 gives the bot a large amount of tweets to choose from and doesn't take that long to retrieve.
# Twitter's API allows up to 3200. That's a lot, so don't use it unless you want things to be very slow.
TWEET_COUNT = 800
# How many tweets to retrieve from the second account.
# Twitter's search API sucks and limits this to 100 items.
SEARCH_COUNT = 100
# Length limits of Tweet1.
# Sometimes a too-short tweet leads to unsatisfying results.
# Being too restrictive in these values can lead to difficulty finding acceptable tweets to build on.
MIN_LENGTH = 45
# How many times tries to get valid tweets.
# Use positive integers at least greater than 2, although 10 is good.
# If it's smaller than 2, the bot can fail very often when getting tweets.
# If it's small, the bot can fail more frequently.
# If it's very large, the bot can waste time.
# A value between 5~15 should be fine.
MAX_TRIES = 7
# Probability of a new tweet of being uppercase.
UPPER_PROB = 0.07
# Levenshtein distance used for comparison. This number can be a float between 0.0 and 1.0.
# Higher values allow for more similarity.
# Setting this too low will probably prevent things from working.
DISTANCE = 0.75
# How many tweets to retrieve from each account when generating markov tweets.
# Larger numbers provide a better corpus but can take longer to obtain.
M_COUNT = 200
# How closely do you want this to hew to sensical? 2 is low and 4 is high.
ORDER = 2
# Image folder name. Relative to the folder where the script is. Do not use quotes.
IMAGE_FOLDER = photos
# Image probability when MODE is set to default. Keep in mind that this is not *real* probability,
# as every time tweets are not generated correctly (quite often) this parameter will be used again,
# increasing the probability of posting a photo.
IMAGE_PROB = 0.01
# Markov tweet probability when MODE is set to default. Same as above, but for Markov type tweets.
MARKOV_PROB = 0.1
ALLOW_RTS = False

# Available time modes:
# fixed: tweet every TIME_INTERVAL hours
# random: tweets randomly between an interval
# Time intervals should not be very small to avoid rate limit.
TIME_MODE = random
# Amount of time (in hours) the bot will wait to tweet again when TIME_MODE is fixed
FIXED_TIME_INTERVAL = 0.5
# Set the min and max time when TIME_MODE is random
TIME_INTERVAL_MIN = 0.3
TIME_INTERVAL_MAX = 1.5


[Replies]
# Set to False to deactivate replies
ALLOW_REPLIES = True
# Available reply modes:
# default: random mode, needs: FILE, FILE_SPLIT, FILE_PROB
# file: posts only images from a folder, needs: FILE, FILE_SPLIT, FILE_PROB
# vowel: replies changing all the vowels for 'i'
REPLIES_MODE = default
# Text file name(s). Relative to the folder where the script is. Separate with commas; do not use quotes.
# Includes some of the worst fanfictions ever. You can use whatever you want as long as the file can be
# sliced in pieces by a distinct string, such as ';;'
FILES = my_immortal, garf, hlflc, danube, zybourne
# A string to split the file in small pieces. Do not use quotes.
FILE_SPLIT = ;;
# Probability of post an item from the text file when REPLIES MODE is default
FILE_PROB = 0.90


[Misc]
# Set to False to deactivate the console output
CONSOLE_OUTPUT = True

```
___

## [Stable] Changelog:

### 2.0 New Mode

- Added Markov chain mode; bot will now tweet sentences generated via Markov chain
- typo fixes in docs
- added some more bad fanfic/text for replies

### 1.1: Improvements

- Improved code to get tweets from primary and secondary accounts since the twitter API sucks
- Updated reply function to randomly choose from several text files
- Removed MAX_LENGTH, this wasn't really helping and made wait times too long
- Various small settings tweaks

### 1.0: Forked from PYNSUFFERABLE
- Mostly just tweaks to fit with the theme of my stupid idea.
- Added code to save tweets to a database and compare new tweets with old ones to prevent repetition
