import requests


# res = requests.post("http://localhost/crawling/boomplay.php", {"link":"https://www.boomplay.com/trending-songs"})
# print(res.text)

def file_put_contents(filename, data):
    file = open(filename, 'w')
    file.write(data)


def start_parsing():
    links = [
        {"name": "boom_trending", "link": "https://www.boomplay.com/trending-songs"},
        {"name": "top_nigeria", "link": "https://www.boomplay.com/playlists/850210?from=charts"},
        {"name": "top_africa", "link": "https://www.boomplay.com/playlists/880218?from=charts"},
        {"name": "top_world", "link": "https://www.boomplay.com/playlists/57457753?from=charts"},
    ]

    for row in links:
        row = dict(row)
        req = requests.post("http://localhost/crawling/boomplay.php", {"link": row.get("link")})
        file_put_contents("boom/" + row.get("name") + ".json", req.text)
        print("Downloaded:: " + row.get("name"))


start_parsing()
