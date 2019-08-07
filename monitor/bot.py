import praw
import sqlite3
from twilio.rest import Client

#Gets the individual id of each post stored in the database and returns it as a list.
def get_data_id():
        conn = sqlite3.connect('database.db')

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

#Checks if a post is already in the datbase by using the list returned from get_data_id. If it is it is removed from the local lists
#of id, titles, and urls.
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

#Inserts data to the database
def add_data():
        conn = sqlite3.connect('database.db')

        c = conn.cursor()

        num = 0

        for items in posts:
                        c.execute("INSERT INTO posts VALUES (:title, :url, :id)", {'title': posts[num], 'url': url[num], 'id': post_id[num]})
                        conn.commit()
                        num += 1

        conn.close()

#Returns the title of all posts and prints them to the screen. Used for testing purposes. 
def check_items():
        conn = sqlite3.connect('database.db')

        c = conn.cursor()

        c.execute("SELECT title FROM posts")
        data = c.fetchall()
        print(data)

        conn.close()

#Deletes everything in the database. Used for testing purposes.
def delete_all():
        conn = sqlite3.connect('database.db')

        c = conn.cursor()

        c.execute("DELETE FROM posts")
        conn.commit()
       
        conn.close()

#Deletes 2/3 of the database by fetchin gthe first entry in the data base and the last, then subtracting to find the toatl number of
#of entries. If the total is larger than 200 it is then multiplied by 2/3 and all entries with a rowid less than that is deleted.
def delete_most():
        conn = sqlite3.connect('database.db')

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

#Gets all the rowids from the database and prints them to the screen. Used for testing purposes.
def get_all_data():
        conn = sqlite3.connect('database.db')

        c = conn.cursor()

        c.execute("SELECT rowid FROM posts")
        data = c.fetchall()
        print(data)
        conn.commit()
       
        conn.close()

        
#Logs into reddit api. Bot credintials located in praw.ini
reddit = praw.Reddit('bot1')

#Client call for twilio api, used to send text messages.
client = Client("AC10a274c321bf8dc2858c68027b3c1089", "78707f12326e57eec6da92a1269beb9e")

#Subreddit that the bot will be pulling from.
subreddit = reddit.subreddit('buildapcsales')

#Variables with what we are looking for.
word = "[monitor]"
size = "34\""
desc = "ultrawide"

#Lists to hold title of posts, url, and id.
posts = []
url = []
post_id = []

#Loop to pull the new submissions, break into parts, and add to respective lists.
for submission in subreddit.new():
    if word in submission.title.lower() and size in submission.title or desc in submission.title.lower():
        post_id.append(submission.id)
        posts.append(submission.title)
        url.append(submission.url)


#Checks if posts are new.     
check(post_id)

#Constructs message and sends as text.
num = 0
for data in posts:
        msg = posts[num] + "\n\n" + url[num]
        print(msg)
        client.messages.create(to="+14028850351", from_="+15313018826", body=msg)
        num += 1

#Adds new data to the database and deletes data if full enough.
add_data()
delete_most()









