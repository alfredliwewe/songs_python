import time
import yt_dlp as ydl
import json
import requests

delay_seconds = 2

def get_one():
    try :
        res = requests.post("https://amuzeemw.com/web-handler.php", data={'getPendingYoutube':'true'}).json()
        if res['status'] == True:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            ydl1 = ydl.YoutubeDL(ydl_opts)

            url = 'https://www.youtube.com/watch?v='+res['vid']
            info_dict = ydl1.extract_info(url, download=False)
            # print(info_dict)

            # Specify the file path
            file_path = "data.json"

            # Write the dictionary to a JSON file
            with open(file_path, "w") as json_file:
                json.dump(info_dict, json_file)
                pass

            # upload to local server
            json_str = json.dumps(info_dict, indent=0)
            response = requests.post("https://amuzeemw.com/web-handler.php", data={'extractedYoutube':json_str,'vid':res['vid']})
            print(response.text)
        else:
            print("list is empty for now")
            pass
        pass
    except :
        print("failed")


while True:
    get_one()
    time.sleep(delay_seconds)