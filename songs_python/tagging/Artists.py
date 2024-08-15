class Artists:
    def __init__(self, cursor):
        self.cursor = cursor

    def getIds(self, names):
        ids = []

        for name in names:
            self.cursor.execute("SELECT * FROM web_artists WHERE name LIKE %s", (name,))
            if self.cursor.rowcount > 0:
                row = self.cursor.fetchone()
                ids.append(row[0])
            else:
                # save new artist
                self.cursor.execute("INSERT INTO `web_artists`(`id`, `webid`, `name`, `photo`, `resampled`, "
                                    "`biography`, `status`, `link`, `website`, `country`, `actions`, `gender`, "
                                    "`genre`) VALUES (NULL, '0', %s, '', '', '', 'active','','','0','0','','')", (name,))
                self.cursor.execute("SELECT * FROM web_artists WHERE name LIKE %s ", (name,))
                row = self.cursor.fetchone()
                ids.append(row[0])
            pass
        return ids


class Song:
    def __init__(self, cursor, id):
        self.cursor = cursor
        self.id = id

    def setSupporting(self, ids):
        for id in ids:
            self.cursor.execute("SELECT * FROM contributing WHERE song = %s AND artist = %s ", (id, self.id,))
            if self.cursor.rowcount == 0:
                self.cursor.execute("INSERT INTO `contributing`(`id`, `song`, `artist`) VALUES (NULL, %s, %s)", (id, self.id))

    def setProducers(self, ids):
        for id in ids:
            self.cursor.execute("SELECT * FROM producers WHERE song = %s AND artist = %s ", (id, self.id,))
            if self.cursor.rowcount == 0:
                self.cursor.execute("INSERT INTO `producers`(`id`, `song`, `artist`) VALUES (NULL, %s, %s)", (id, self.id))

    def setTags(self, tags):
        values = ""
        for tag in tags:
            tag = makeTag(tag)
            id = 0

            self.cursor.execute("SELECT * FROM tags WHERE name = %s ", (tag,))
            if self.cursor.rowcount == 0:
                self.cursor.execute("INSERT INTO `tags`(`id`, `name`, `actions`) VALUES (NULL, %s, %s)",
                                    (tag, 0))
                self.cursor.execute("SELECT * FROM tags WHERE name = %s ", (tag,))
                row = self.cursor.fetchone()
                id = row[0]
            else:
                row = self.cursor.fetchone()
                id = row[0]
            if values == "":
                values = "(NULL, '"+str(id)+"', '"+str(self.id)+"')"
            else:
                values = values +", "+"(NULL, '"+str(id)+"', '"+str(self.id)+"')"
            pass

        self.cursor.execute("INSERT INTO tag_song (id,tag,song) VALUES "+values)



def makeTag(text):
    text = str(text)
    text = text.replace(" ", "").lower().strip()
    return text