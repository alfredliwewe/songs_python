import requests


def file_put_contents(filename, data):
    file = open(filename, 'w')
    file.write(data)


def file_get_contents(filename):
    f = open(filename, "r")
    return f.read()


def download():
    res = requests.get("https://www.billboard.com/charts/hot-100/")
    file_put_contents("bill.html", res.next)


def start_parsing():
    links = [
        {"name": "hot100", "link": "https://www.billboard.com/charts/hot-100/"},
        {"name": "hot200", "link": "https://www.billboard.com/charts/billboard-200/"},
        {"name": "hot_tiktok", "link": "https://www.billboard.com/charts/tiktok-billboard-top-50/"},
        {"name": "global_200", "link": "https://www.billboard.com/charts/billboard-global-200/"},
    ]

    for row in links:
        row = dict(row)
        req = requests.post("http://localhost/crawling/billboard.php", {"link": row.get("link")})
        file_put_contents("saves/" + row.get("name") + ".json", req.text)
        print("Downloaded:: " + row.get("name"))


start_parsing()
print("done")
