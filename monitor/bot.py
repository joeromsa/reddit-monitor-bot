import praw
import sqlite3
from twilio.rest import Client
import os.path
from os import path

#Checks if this is the first time using the program. If it is creates the database and tables.
def database_check():
        if not path.exists("databaseForMonitor.db"):
                conn = sqlite3.connect('databaseForMonitor.db')

                c = conn.cursor()

                c.execute("""CREATE TABLE posts (
                                title text,
                                url text,
                                id integer
                                )""")

                conn.commit()

                conn.close()


#Gets the id of the idividual reddit posts from the database and returns them as a list.
def get_data_id():
        conn = sqlite3.connect('databaseForMonitor.db')

        c = conn.cursor()

        c.execute("SELECT id FROM posts")
        data = c.fetchall()

        result = [list(i) for i in data]

        conn.commit()

        conn.close()

        ar = []

        for row in result:
                for item in row:
                      ar.append(item)  

        return ar

#Checks if the posts in the database match the ideas in the list of newly pulled ids. If match there is a match, the 
#id, title, and url is removed from their respective lists.
def check(id):
        for items in get_data_id():
                num = 0
                if items == id[num]:
                        post_id.pop(num)
                        posts.pop(num)
                        url.pop(num)
                elif items != id[num]:
                        continue
                num += 1

#A loop that takes the number of items in the posts list and adds the title, url, and id to the database
def add_data():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        num = 0

        for items in posts:
                        c.execute("INSERT INTO posts VALUES (:title, :url, :id)", {'title': posts[num], 'url': url[num], 'id': post_id[num]})
                        conn.commit()
                        num += 1

        conn.close()

#Returns the title of all posts in the database and prints them to the screen. Used for testing purposes. 
def check_items():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("SELECT title FROM posts")
        data = c.fetchall()
        print(data)

        conn.close()

#Deletes everything in the database. Used for testing purposes.
def delete_all():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("DELETE FROM posts")
        conn.commit()
       
        conn.close()

#Gets the rowid of the oldest entry in the database and the newest, then subtracts to find how many posts are in the database.
#If the total is over 200, it is multiplied by 2/3 and that amount, starting with the oldest is removed from the database.
def delete_most():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("SELECT rowid FROM posts ORDER BY rowid DESC")
        bottom = c.fetchone()[0]
        conn.commit()

        c.execute("SELECT rowid FROM posts ORDER BY rowid ASC")
        top = c.fetchone()[0]
        conn.commit()

        total = bottom - top

        if total >= 200:
                
                amount = round(total * (2/3))

                c.execute("DELETE FROM posts where rowid<= :value", {'value': amount})
                conn.commit()
        
                conn.close()
        
        else:
                conn.close()

#Gets all the rowids from the database. Used for testing purposes.
def get_all_data():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("SELECT rowid FROM posts")
        data = c.fetchall()
        print(data)
        conn.commit()
       
        conn.close()

    
#Log into reddit api. Bot credintials found in the praw.ini file.
reddit = praw.Reddit('bot1')

#Client call to the twilio api to send text messages.
client = Client("####", "#####")

#Subreddit for the program to get posts from.
subreddit = reddit.subreddit('buildapcsales')

#Variables used to sort data.
word = "[monitor]"
size = "34\""
desc = "ultrawide"

#Lists to hold title of posts, url, and id.
posts = []
url = []
post_id = []

#Loop to pull the new submissions from the subreddit and add the parts to their respective lists.
for submission in subreddit.new():
    if word in submission.title.lower() and size in submission.title or desc in submission.title.lower():
        post_id.append(submission.id)
        posts.append(submission.title)
        url.append(submission.url)



#Check if database and tables have been created yet.
database_check()

#Check if posts are new.   
check(post_id)

#Creating the messages and notifying the user of any new posts that match the criteria.
num = 0
for data in posts:
        msg = posts[num] + "\n\n" + url[num]
        print(msg)
        client.messages.create(to="####", from_="####", body=msg)
        num += 1

#Add new data to the database and delete posts if needed.
add_data()
delete_most()











