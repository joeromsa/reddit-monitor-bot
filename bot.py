import praw
import smtplib
import config
from emailbot import emailbot

#log into reddit api. Bot credintials in praw.ini
reddit = praw.Reddit('bot1')

#subreddit for the bot
subreddit = reddit.subreddit('buildapcsales')

#variables with what we are looking for, the size, and thee email object
word = "[monitor]"
size = "34"
desc = "ultrawide"
email = emailbot('subject', 'msg')

#looking at the new submissions
for submission in subreddit.stream.submissions():
    if word in submission.title.lower() and size in submission.title or desc in submission.title.lower():
        email.subject = submission.title
        email.msg = submission.url
        email.send_email()
        print("Title: ", submission.title)




