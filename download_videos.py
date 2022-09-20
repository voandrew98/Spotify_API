from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas
import os

def DownloadVideoFromTitles(los):
    vID = []
    for index, item in enumerate(los):
        video_id = ScrapeVideoId(item)
        vID += [video_id]
        print("Downloading song")
        DownloadVideoFromId(vID)

def DownloadVideoFromId(lov):
    SAVE_PATH = str(os.path.join(Path.home(),"Downloads/songs"))
    try:
        os.mkdir(SAVE_PATH)
    except:
        print("download folder exists")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(lov)

def ScrapeVideoId(query):
    print("Getting video id for: ", query)
    BASIC = "http://www.youtube.com/results?search_query="
    URL=(BASIC+query)
    page = requests.get(URL)
    session = HTMLSession()
    response = session.get(URL)
    response.html.render(sleep=1)
    soup = BeautifulSoup(response.html.html, "html.parser")

    results = soup.find('a', id="Video Title")
    return results['href'].split('watch?v=')[1]

def __main__():
    data = pandas.read.csv('songs.csv')
    data = data['column'].tolist()
    print("Found ", len(data), " songs!")
    DownloadVideoFromTitles(data[0:1])
__main__()