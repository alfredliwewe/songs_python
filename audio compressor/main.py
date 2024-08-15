from pydub import AudioSegment
import requests
import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="songs",
    password=""
)

cursor = db.cursor(buffered=True)
def getSong():
    res = requests.post("http://localhost/songs/api/reader.php", {"getSongResize": "true"}).json()
    return res


def reduce_mp3_size(input_file, output_file, bitrate='64k'):
    audio = AudioSegment.from_mp3(input_file)
    audio.export(output_file, format="mp3", bitrate=bitrate)


def uploadSong(filename, songId):
    with open(filename, 'rb') as file:
        files = {'file': (filename, file, 'multipart/form-data')}
        response = requests.post("http://localhost/songs/api/reader.php", data={"upload64bits": songId}, files=files)

        if response.status_code == 200:
            print("File uploaded successfully")
            print(response.text)
        else:
            print("Failed to upload the file")


def downloadFile(url, filename):
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download the file")


can = True
while can:
    res = getSong()
    if res['status']:
        downloadFile("http://localhost/songs/songs/" + res['filename'], "saves/" + res['filename'])
        # download song
        reduce_mp3_size("saves/" + res['filename'], "saves/" + res['filename'], bitrate='64k')
        uploadSong("saves/" + res['filename'], res['id'])
        print("Done with " + res['title'])
        pass
    else:
        can = False
        print("Almost done")
