import mysql.connector


def implode(glue, values):
    str1 = ""
    for v in values:
        if str1 == "":
            str1 = str(v)
        else:
            str1 = str1 + glue + str(v)

    return str1


def create_value(song_id,value):
    return "(NULL, '13', '"+str(song_id)+"', '"+str(value)+"')"


db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="songs",
    password=""
)

cursor = db.cursor()

# get artist ids
song_store = {}

cursor.execute("SELECT song FROM song_plays")
res = cursor.fetchall()
for row in res:
    if song_store.__contains__(row[0]):
        song_store[row[0]] = song_store[row[0]] + 1
    else:
        song_store[row[0]] = 1
    pass

# generate sql
pos = 0
values = []
sql = ""

for k in song_store:
    v = song_store[k]
    values.append(create_value(k,v))
    pos = pos + 1

    if pos == 90:
        sql = sql + "INSERT INTO `user_song`(`id`, `user`, `song`, `value`) VALUES " + implode(",", values) + ";\n\n"
        values = []
        pos = 0
sql = sql + "INSERT INTO `user_song`(`id`, `user`, `song`, `value`) VALUES " + implode(",", values) + ";\n\n"

f = open("song_relation.sql", "w")
f.write(sql)
f.close()
print("Probably finished")