import mysql.connector
from parse import TitleParser
from Artists import Artists, Song

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="songs",
    password=""
)

cursor = db.cursor(buffered=True)

artists_obj = Artists(cursor)


def makeTag(text):
    text = str(text)
    text = text.replace(" ", "")
    return text


def multipleContains(text, chars):
    text = str(text)
    result = False
    for char in chars:
        if text.__contains__(char):
            result = True

    return result

repeat = True
while repeat:
    cursor.execute("SELECT * FROM web_songs WHERE status = 'active' LIMIT 0,1 ")
    res = cursor.fetchone()

    if res is not None:
        # get artist data
        title = str(res[2])
        tags = []

        song = Song(cursor, res[0])

        parser = TitleParser(title)
        parts = parser.getParts()

        words = parts[0].split(" ")
        if len(words) <= 3:
            tags.append(makeTag(title))
        tags = tags + parser.getFeaturedArtists() + parser.getProducers()

        contributing = artists_obj.getIds(parser.getFeaturedArtists())
        song.setSupporting(contributing)

        p_ids = artists_obj.getIds(parser.getProducers())
        song.setProducers(p_ids)

        cursor.execute("SELECT * FROM web_artists WHERE id = '" + res[3] + "' ")
        artist = cursor.fetchone()
        tags.append(makeTag(artist[2]))
        print(tags)
        song.setTags(tags)
        cursor.execute("UPDATE web_songs SET status = 'tagged' WHERE id = %s ", (res[0],))
        print("Done with: "+title)
        db.commit()

        pass
    else:
        print("We are done")
        repeat = False
        pass
    pass
