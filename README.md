# Reddit Monitoring Bot
This bot is used to monitor a subreddit and pull certain posts out that you are looking for. 
It will notify you by text message everytime there is a new post and then store those posts in 
a local database in order to keep you from getting notifications of duplicates. 

## Uses
This program's main use is for monitoring any subreddit of your choosing to be notified by text message whenever
there is a post with the keywords you have specified in the program.

An example use of this program is having it monitor the subreddit r/buildapcdeals for posts containing the words "monitor", 
"34in" and "ultrawide" to be instantly notified of a good deal on an ultrawide monitor. 

## Prerequisites
This program runs on python 3.7.4 and requires the praw and twilio packages to be installed.

```
pip install praw
pip install twilio
```

## Set Up
All areas that require personal information in the program will be denoted with *****

Follow these steps to set up the program:

* Enter the reddit account's client_id, client_secret, password, and username
  in the praw.ini file under [bot1] section. 
  To get more information, see [registering a reddit developer application](https://old.reddit.com/prefs/apps/)
  
* Enter your twilio client account id and auth token. Visit [Twilio](https://www.twilio.com) to make a free account.

* Enter the subreddit you wish to monitor.

* Add the key word variables you wish to use to filter out posts with.

* Add the phone number you wish to recieve notifications to and your twilio account number to send messages from.


## Deployment
This program was built with the idea of being put on a Raspberry Pi and to be ran every few minutes through a cron job. 
However it can run on any system and scheduled by a cron job or its equivalent such as a scheduled task.

## Author
joeromsa
