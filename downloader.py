import requests, base64, time

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
  'Accept': '*/*',
  'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'Origin': 'https://yt1s.com',
  'Connection': 'keep-alive',
  'Referer': 'https://yt1s.com/youtube-to-mp3/it',
  'Cookie': '__cfduid=dfb17ccc5f5d183fa81e5b0c8c96687831619183127',
  'TE': 'Trailers'
}

def get_code(link, mode="mp3"):
    print("Downloading...")
    url = "https://yt1s.com/api/ajaxSearch/index"
    payload = {
        "q":link,
        "vt":mode,
    }
    payload = f'q={link}&vt={mode}'

    r = requests.post(url, data=payload, headers=headers)
    return r.json()["kc"], r.json()["vid"]

def download_mp3(link):
    code, vid = get_code(link, "mp3")

    url ="https://yt1s.com/api/ajaxConvert/convert"
    payload = {
        "vid":vid,
        "k":code,
    }

    r = requests.post(url, data=payload, headers=headers)
    title = r.json()["title"]
    download = r.json()["dlink"]

    req = requests.get(download)
    open(title + ".mp3", "wb").write(req.content)

def download_mp4(link):
    code, vid = get_code(link, "mp4")

    url = "https://yt1s.com/api/ajaxConvert/convert"
    payload = {
        "vid": vid,
        "k": code,
    }

    r = requests.post(url, data=payload, headers=headers)
    title = r.json()["title"]
    download = r.json()["dlink"]

    req = requests.get(download)
    open(title + ".mp4", "wb").write(req.content)

if __name__ == '__main__':
    while True:
        song = str(input("Enter youtube video link (or nothing to exit): "))
        if song == "":
            exit(0)

        choose = input("1 for MP3\n2 for MP4\n")
        start = time.time()
        if choose == "1":
            download_mp3(song)
        elif choose == "2":
            download_mp4(song)
        print(f"Downloaded in {round(time.time() - start)} seconds")

