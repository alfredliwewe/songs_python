import requests


def download_one():
    res = requests.post("http://localhost/songs/api/reader.php", {"downloadPlayed": "true"}).json()
    return res


can = True
while can:
    res = download_one()
    if res['status'] is None:
        print(res['message'])
        can = False
    else:
        print("Downloaded " + res['title'])
