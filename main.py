import mysql.connector
import sqlite3
import json
import time

from cache import Cache
from series import Series
from strings import Strings

print("Hello there")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="songs",
    password=""
)

db3 = sqlite3.connect('example.db')

# Create a cursor object to execute SQL queries
cursor3 = db3.cursor()

cursor = db.cursor(buffered=True)


def find_top_listener():
    cursor.execute("SELECT DISTINCT user FROM song_plays")
    all_users = cursor.fetchall()
    progress = {}
    for row in all_users:
        cursor.execute("SELECT COUNT(id) FROM song_plays WHERE user = %s ", (row[0],))
        count = cursor.fetchone()
        progress[row[0]] = count[0]

    sorted_dict = dict(sorted(progress.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict;


def find_top_countries_listened():
    cursor.execute("SELECT id,country FROM web_artists WHERE id IN (SELECT DISTINCT artist FROM song_plays)")
    # get artists and their countries
    artist_country = {}
    artist_listenership = {}
    for row in cursor.fetchall():
        artist_country[row[0]] = row[1]
        cursor.execute("SELECT COUNT(id) FROM song_plays WHERE artist = %s ", (row[0],))
        count = cursor.fetchone()
        artist_listenership[row[0]] = count[0]

    # countries and listener ship
    country_listen = {}
    for artist in artist_listenership:
        country = artist_country.get(artist)
        if country_listen.get(country) is None:
            country_listen[country] = artist_listenership[artist]
        else:
            country_listen[country] += artist_listenership[artist]
            pass
        pass

    country_sorted = dict(sorted(country_listen.items(), key=lambda item: item[1], reverse=True))
    return country_sorted


def user_top_countries_listened(user):
    cursor.execute(
        "SELECT id,country FROM web_artists WHERE id IN (SELECT DISTINCT artist FROM song_plays WHERE user = %s)",
        (user,))
    # get artists and their countries
    artist_country = {}
    artist_listenership = {}
    for row in cursor.fetchall():
        artist_country[row[0]] = row[1]
        cursor.execute("SELECT COUNT(id) FROM song_plays WHERE artist = %s AND user = %s", (row[0], user,))
        count = cursor.fetchone()
        artist_listenership[row[0]] = count[0]

    # countries and listener ship
    country_listen = {}
    for artist in artist_listenership:
        country = artist_country.get(artist)
        if country_listen.get(country) is None:
            country_listen[country] = artist_listenership[artist]
        else:
            country_listen[country] += artist_listenership[artist]
            pass
        pass

    country_sorted = dict(sorted(country_listen.items(), key=lambda item: item[1], reverse=True))
    return country_sorted


def main():
    top_countries = find_top_countries_listened()
    print(top_countries)

    print("\n Just countries \n\n")

    print(list(top_countries.keys()))
    print("Making a series of users")

    cursor.execute("SELECT DISTINCT user FROM song_plays")
    users_list = []
    for row in cursor.fetchall():
        users_list.append(row[0])
        pass
    series = Series(cursor3)
    series.set("people", users_list)
    db3.commit()


def user_top_artists(user):
    cursor.execute("SELECT DISTINCT artist FROM song_plays WHERE user = %s ", (user,))
    artists_plays = {}
    rows = cursor.fetchall()
    for row in rows:
        cursor.execute("SELECT COUNT(id) AS count_all FROM song_plays WHERE artist = %s AND user = %s", (row[0], user,))
        count = int(cursor.fetchone()[0])
        artists_plays[row[0]] = count
    # sort the data
    data_sorted = dict(sorted(artists_plays.items(), key=lambda item: item[1], reverse=True))
    return data_sorted


def save_user_preference(user):
    top_artists = user_top_artists(user)
    top_countries = user_top_countries_listened(user)

    artists_data = json.dumps(top_artists)
    countries_data = json.dumps(top_countries)
    cursor.execute("INSERT INTO `user_cache`(`id`, `user`, `name`, `content`, `date`) VALUES (NULL, %s, %s, %s, %s)",
                   (user, "top_artists", artists_data, time.time()))
    cursor.execute("INSERT INTO `user_cache`(`id`, `user`, `name`, `content`, `date`) VALUES (NULL, %s, %s, %s, %s)",
                   (user, "top_countries", countries_data, time.time()))
    db.commit()


def country_trending_artists(country):
    cache = Cache(cursor)
    data = cache.get("country_artists", country)
    if data is None:
        ids = []
        cursor.execute("SELECT id FROM web_artists WHERE country = %s ", (country,))
        for row in cursor.fetchall():
            ids.append((row[0]))
        data = Strings.implode(",", ids)

        cache.set("country_artists", country, data)
        db.commit()
        pass

    available_artists = {}
    cursor.execute("SELECT DISTINCT artist FROM song_plays WHERE artist IN (" + data + ")")
    rows = cursor.fetchall()
    for row in rows:
        cursor.execute("SELECT COUNT(id) AS count_all FROM song_plays WHERE artist = %s ", (row[0],))
        count = int(cursor.fetchone()[0])
        available_artists[row[0]] = count
        pass
    data_sorted = dict(sorted(available_artists.items(), key=lambda item: item[1], reverse=True))
    return data_sorted


print(country_trending_artists(91))
