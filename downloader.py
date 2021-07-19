import grequests, requests, time
import concurrent.futures
import sys

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

def download_wav(link):
    pass

def get_urls(song, formato):
    urls = []
    for x in range(1, 500, 20):
        url = f"https://loader.to/ajax/download.php?start={x}&end={x+19}&format={formato}&url={song}"
        urls.append(url)

    return urls

def load_playlist(song, formato):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': '*/*',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://loader.to/en8/',
        'Alt-Used': 'loader.to',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    reqs = [grequests.get(link) for link in get_urls(song, formato)]
    resp = grequests.map(reqs)
    return resp

def get_download_urls(ids):
    urls = [f"https://loader.to/ajax/progress.php?id={id}" for id in ids]
    return urls

def download_part_playlist(url):
    response = requests.request("GET", url[1], headers=headers)

    while response.json()["download_url"] == None and response.json()["text"] != "No Files":
        if response.json()["progress"] != None:
            progress = int(response.json()["progress"])/10
            sys.stdout.write('\r')
            sys.stdout.write(f"Download in corso... {progress}%")
        response = requests.request("GET", url[1], headers=headers)
        time.sleep(1)

    if response.json()["text"] != "No Files":
        req = requests.get(response.json()["download_url"])
        open(f"playlist{url[0]+1}" + ".zip", "wb").write(req.content)


def download_playlist(response):
    ids = [r.json()["id"] for r in response]
    urls = get_download_urls(ids)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_part_playlist, enumerate(urls))


if __name__ == '__main__':
    print("SOFTWARE DI STEFANO ZARRO, FATTO CON IL ❤ PER FEDERICO MIGNONE\n\n")
    while True:
        song = str(input("Inserisci link di YouTube (Video singolo o Playlist): "))
        if song == "" or not song.startswith("https://youtube.com"):
            continue

        choose = input("[1] per scaricare in MP3\n[2] per scaricare in WAV\n")
        formato = {"1":"mp3",
                   "2":"wav",
                   }

        start = time.time()
        if "playlist" in song:
            r = load_playlist(song, formato[choose])
            download_playlist(r)

        sys.stdout.write('\r')
        sys.stdout.write(f"Scaricata in {round(time.time() - start)} secondi...\n")