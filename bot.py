import praw

#log into reddit api. Bot credintials in praw.ini
reddit = praw.Reddit('bot1')

#subreddit for the bot
subreddit = reddit.subreddit('buildapcsales')

#variables with what we are looking for and the size
word = "[monitor]"
size = "34"

#looking at the new submissions
for submission in subreddit.stream.submissions():
    if word in submission.title.lower():
        print("Title: ", submission.title)
 
