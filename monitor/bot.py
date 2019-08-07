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


#Get the data from the database
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

#check if already in datbase
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

#add data to the database
def add_data():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        num = 0

        for items in posts:
                        c.execute("INSERT INTO posts VALUES (:title, :url, :id)", {'title': posts[num], 'url': url[num], 'id': post_id[num]})
                        conn.commit()
                        num += 1

        conn.close()

#returns the title of all posts
def check_items():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("SELECT title FROM posts")
        data = c.fetchall()
        print(data)

        conn.close()

#deletes everything in the database
def delete_all():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("DELETE FROM posts")
        conn.commit()
       
        conn.close()

#deletes 2/3 of the database
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

#gets all the rowid from the database
def get_all_data():
        conn = sqlite3.connect('databaseForMonitor.db.db')

        c = conn.cursor()

        c.execute("SELECT rowid FROM posts")
        data = c.fetchall()
        print(data)
        conn.commit()
       
        conn.close()

    
#log into reddit api. Bot credintials in praw.ini
reddit = praw.Reddit('bot1')

#client call
client = Client("AC10a274c321bf8dc2858c68027b3c1089", "78707f12326e57eec6da92a1269beb9e")

#subreddit for the bot
subreddit = reddit.subreddit('buildapcsales')

#variables with what we are looking for, the size, and the email object
word = "[monitor]"
size = "34\""
desc = "ultrawide"

#lists to hold title of posts, url, and id
posts = []
url = []
post_id = []

#looking at the new submissions
for submission in subreddit.new():
    if word in submission.title.lower() and size in submission.title or desc in submission.title.lower():
        post_id.append(submission.id)
        posts.append(submission.title)
        url.append(submission.url)



#Check if database and tables have been created yet.
database_check()

#check if posts are new     
check(post_id)

#notify of the new posts
num = 0
for data in posts:
        msg = posts[num] + "\n\n" + url[num]
        print(msg)
        client.messages.create(to="+14028850351", from_="+15313018826", body=msg)
        num += 1

#add new data to the database
add_data()
delete_most()











