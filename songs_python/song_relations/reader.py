import mysql.connector
import numpy
from collections import OrderedDict
import json

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="songs",
    password=""
)

cursor = db.cursor(buffered=True)

# finding similar songs
song_id = 339517

# finding users who have listened to this song
dis_users = {}

ids = []
cursor.execute("SELECT DISTINCT user FROM song_plays WHERE song = %s ", (song_id,))  # AND duration > 70
all_rows = cursor.fetchall()
for row in all_rows:
    dis_users[row[0]] = 0
    ids.append(row[0])
    pass
# find how many times users listened the song


cursor.execute("SELECT * FROM song_plays WHERE song = %s ", (song_id,))  # AND duration > 70
all_rows = cursor.fetchall()
for row in all_rows:
    dis_users[row[1]] = dis_users[row[1]] + 1
    pass

# sort the dictionary
dis_users = dict(sorted(dis_users.items(), key=lambda item: item[1]))
reversed_dict = dict(reversed(list(dis_users.items())))
q1 = numpy.percentile(list(reversed_dict.values()), 25)
print("Original:")
print(reversed_dict)

# exclude people who have listened few times
upper = {}
for k, v in reversed_dict.items():
    if v >= q1:
        upper[k] = v

print("Reduced:")
print(upper)

# find other songs these people listen to
ids = ""
for k in list(upper.keys()):
    if ids == "":
        ids = str(k)
    else:
        ids = ids + "," + str(k)

cursor.execute("SELECT user,song FROM song_plays WHERE user IN (" + ids + ")")
major = {}
for row in cursor.fetchall():
    if major.__contains__(row[0]):
        line = dict(major.get(row[0]))
        if line.__contains__(row[1]):
            line[row[1]] = line[row[1]] +1
        else:
            line[row[1]] = 1
        major[row[0]] = line
    else:
        major[row[0]] = {row[1]:1}

# make a json
with open('saves.json', 'w') as json_file:
    json.dump(major, json_file)

print("Almost done")