# Drilfiction.txt: a very stupid twitter bot.

Tested on macOS 10.14 (18A391). Might work on other OSes. Written in Python 3 and licensed under GPLv3. Based on Pynsufferable: https://github.com/adwareboi/pynsufferable-twitter-bot

A living proof of the bot (: [drilfiction](https://twitter.com/drilfiction)

### What does it do?

I had originally considered creating a bot to generate Markov chains based on twitter accounts dril and fanfiction_txt, but this proved insufficient, as the results made too little sense. Branched from another project, this is a single python script bot that can randomly tweet mashed up tweets between 2 accounts or upload photos (although I don't use this particular feature). It keeps a record of previous tweets in a sqlite database and compares new output to them to avoid repeating itself too much.

It also can stream mentions and reply to them by changing all the vowels by 'i' or using a text file as resource. The infamous epic fanfiction "My Immortal" is set as the default, in fitting with the theme.

### Dependecies:
- Third party libraries: `tweepy`, `unidecode`, `sqlite3`, `stringdist`, and `termcolor`
- Also you may need to install `logging` and `configparser`
- Built-in libraries: `os`, `sys`, `time`, `random` and `threading`

All of these can be installed via `pip`

### How to use it:
I just run it from a terminal since I'm a scrub, but you can run it wherever you want as you do it with python 3. I'm considering creating a web and desktop app version.
Steps:
1. You will need to create a [Twitter App](https://developer.twitter.com/en/apps) linked to an account. Get the API keys needed in order to access.
2. Edit bot.cfg with your parameters. Otherwise it won't work. See the details below
3. Enjoy. Or don't. Whatever.

### Configuration:
The configuration is pretty straightforward, here's the default one for the current version [1.0]. Hopefully it's descriptive enough:

```
[Twitter]
# Set the access keys. Get yours on developer.twitter.com. Do not use quotes.
CONSUMER_KEY =
CONSUMER_SECRET =
ACCESS_KEY =
ACCESS_SECRET =


[Bot]
# Available main modes:
# default: random. Needs: IMAGE_PROB, IMAGE_FOLDER, TWEET_COUNT, ACCOUNTS, MAX_TRIES, UPPER_PROB
# image: posts only images from a folder, needs: IMAGE_FOLDER
# write: posts only mash up tweets, needs: TWEET_COUNT, ACCOUNTS, MAX_TRIES, UPPER_PROB
MODE = write

# Accounts. Separate by commas. Do not use quotes. Duplicates will be erased. (Use only one line)
ACCOUNTS = dril, fanfiction_txt
# How many tweets to retrieve from the accounts.
# If it's too large, the bot may take more time. Should not be very big to avoid rate limit.
# If it's too small, the bot can fail more frequently. Should not be smaller than 10.
# 50~100 gives the bot a large amount of tweets to choose from and doesn't take that long to retrieve.
TWEET_COUNT = 400
# Length limits of Tweet1.
# Sometimes a too-long or too-short tweet leads to unsatisfying results.
# Being too restrictive in these values can lead to difficulty finding acceptable tweets to build on.
MAX_LENGTH = 200
MIN_LENGTH = 120
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
# Higher values allow for more similarity (I think).
DISTANCE = 0.75
# Image folder name. Relative to the folder where the script is. Do not use quotes.
IMAGE_FOLDER = photos
# Image probability when MODE is set to default. Keep in mind that this is not *real* probability,
# as everytime tweets are not generated correctly (quite often) this parameter will be used again,
# increasing the probability of posting a photo.
IMAGE_PROB = 0.1
ALLOW_RTS = False

# Available time modes:
# fixed: tweet every TIME_INTERVAL hours
# random: tweets randomly between an interval
# Time intervals should not be very small to avoid rate limit.
TIME_MODE = random
# Amount of time (in hours) the bot will wait to tweet again when TIME_MODE is fixed
FIXED_TIME_INTERVAL = 0.5
# Set the min and max time when TIME_MODE is random
TIME_INTERVAL_MIN = 0.1
TIME_INTERVAL_MAX = 0.8


[Replies]
# Set to False to deactivate replies
ALLOW_REPLIES = True
# Available reply modes:
# default: random mode, needs: FILE, FILE_SPLIT, FILE_PROB
# file: posts only images from a folder, needs: FILE, FILE_SPLIT, FILE_PROB
# vowel: replies changing all the vowels for 'i'
REPLIES_MODE = default
# Text file name. Relative to the folder where the script is. Do not use quotes.
# The infamous epic fanfiction "My Immortal" is set as the default. You can use whatever you want as long as the file can be
# sliced in pieces by a distinct string, such as ';;'
FILE = my_immortal
# A string to split the file in small pieces. Do not use quotes.
FILE_SPLIT = ;;
# Probability of post an item from the text file when REPLIES MODE is default
FILE_PROB = 0.5


[Misc]
# Set to False to deactivate the console output
CONSOLE_OUTPUT = True

```
___

## [Stable] Changelog:

### 2.0: Say hello to my little bot
- Improved reply streaming system.
- Improved configuration management.
- Simpler exception management.
- Lots of both small and big code changes.
- Should be very stable, like, always running.
- Should be slightly faster.
- Now it's not necessary to specify your username for replies.
- Vastly improved readability the code.
- Specified what parameters depend of other on the config file.
- A ton of new comments and process description.
- Now you can avoid RTs when composing tweets. This may take some more time to find compatible tweets.
- Removed time countdown, as it was not that useful and in many console emulators wouln't display it right.
- `Tweets2` is now more reliable (see: known issues).
  - It searches on tweets if union is indexed, and if it's not, that tweet is discarded.
  - But if `union` is a weird word, a number, etc, it can return an empty tweet list.
  - The bot will try again a certain amount of times before giving up.
- More complex but also more informative logging
- Now it will show the time it takes to do its thing

**Known issues**
- [Partially Solved] [1.0]: May take a while to get tweets, specially `tweet2` etc etc etc. (read below)


### 1.2: Big one
- Lots of new configuration options is now available in the `bot.conf` file.
- New `TIME_MODE`, `REPLY_MODE`
- Better config management and checking
- New Reply system. Based on [tweepy streaming](http://docs.tweepy.org/en/latest/streaming_how_to.html)
  - Faster, live replies.
  - Does not need an auxiliar file
  - Much more reliable
  - Now can reply with the contents of a textfile
- Improved logging
- A ton of changes in the code
- When rate limit is reached, tweepy will notify.

**Known issues**
- [1.0]: May take a while to get tweets, specially `tweet2`. Sometimes it just doesn't get any _valid_ tweet. I guess this is because the way twitter search works, but I don't know how to fix this, if I can. Nevertheless, the bot manages to recover and try again.
- [1.0]: In some console emulators, it may not display messages right.


### 1.1: Polishing
- Rename project from autonota to pynsufferable.
- Now you can disable console output.
- Fixed a bug that would cause replies to crash when `lastmention` file does not exist
- More comments
- Changed file extension of `bot.conf` to `bot.cfg`
- Changed file name of `autonota-bot.py` to `bot.py`

**Known issues:**
- Same as 1.0


### 1.0: The config update
- Now you can easily tweak the script with the `bot.conf` file.
- Brand new modes! You can choose whether the bot should and should not do.
- Replies are working fine again
- Added some more terminal output
- Hope that the `bot.log` is now more legible
- Code optimization, minor changes.
- The most stable version yet, with more control over errors & exceptions. (I'd call it _fairly_ stable)
- The rest is basically the same.

**Known issues:**
- [Solved] [0.4.2]: Replies are bugged.
- May take a while to get tweets, specially `tweet2`. Sometimes it just doesn't get any _valid_ tweet. I guess this is because the way twitter search works, but I don't know how to fix this, if I can. Nevertheless, the bot manages to recover and try again.
- In some console emulators, it may not display messages right.
- You must create an empty file, name it `lastmention` and

___

## [Old] Changelog:
### 0.4.2: Optimization, minor changes

- Optimization: Removed some lines, redone many more.
- Now supports accentuation, special characters and caps.
- Better exceptions management.
- Now does not need an aux `mentions.log` file for replies.
- `bot.log` is now cooler.
- The chance of writing an all-caps tweet has been changed.
- Now with more comments.
- Should be more stable.

**Known issues:**
- Replies are bugged: Replies on `0.4.2` work diferently, without a mentions.log file to store the last mention. Instead if that, It uses TweepError exception to avoid duplicates of tweets. But seems that when some time has passed, it replies again to the last mention even if it's a duplicate.
- **Solution1:** I recommend you not using replies since this behaviour can be annoying. You can deactivate replies by commenting out threading lines at the end of the file.
- **Solution2:** Oooor you could use the `1.0` above versions instead come on they're just much better.


### 0.4.1: Initial GitHub Public Release

- Tweet composing support
- Photo posting support
- No config file
- No standarized log file
- [experimental]: Replies support
