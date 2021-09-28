#!/usr/bin/python3

from pytube import YouTube
from pytube import Playlist
from pytube import request 
from pathlib import Path
import os
import sys
import math
import argparse
import concurrent.futures
#Parse arguments
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--playlist', help='Especify if the url is a playlist', action="store_true")
    parser.add_argument('url', help='Video or playlsit url')
    parser.add_argument('path',type=Path, help='The destination path', default="./")
    parser.add_argument('-a','--audio', help='Download only the audio', action="store_true")
    parser.add_argument('-mt','--multithreading', type=int, help="Number of threads for downloading", default=1)
    return parser.parse_args()

#Return the apropriate video stream to download
#by default it return the highest quality for videos and the second for audios
def get_stream(video, audioOnly):
    if(audioOnly):
        audio_streams = video.streams.filter(only_audio=True).order_by('abr').desc()
        return audio_streams[1]
    else:
        video_streams = video.streams.filter(progressive=True).order_by('resolution').desc()
        return video_streams[0]

def print_progress_bar(blocks_number, conclued, total):
    decimal_percent = conclued/total
    blocks = math.floor(decimal_percent*blocks_number)
    bar = '[' + blocks * chr(9608)+ (blocks_number-blocks)*' '+']'
    print(f'{bar} {decimal_percent* 100:.2f}%', end='\r')

#Create the video object and download it
def download_video(url, path, audioOnly, progress):
        video = YouTube(url)
        stream = get_stream(video, audioOnly)
        sufix = "mp4"
        if audioOnly:
            sufix = "mp3"
        with open(f"{path}{video.title}.{sufix}", "wb") as file:
            downloaded = 0
            filesize = stream.filesize
            stream = request.stream(stream.url)
            chunk = next(stream,None)
            while chunk:
                file.write(chunk)
                downloaded += len(chunk)
                chunk = next(stream,None)
                if progress:
                    progress(30, downloaded, filesize)

#Call video_download for one video
def download_single(data):
    print(f"Downloading 1 video")
    print_progress_bar(30,0,30)
    download_video(data['url'], data['path'], data['audioOnly'], print_progress_bar)
    print("\nSuccessfully Completed")

#Create a playlist object and call download_video for each video
def dowload_playlist(data,threads_number):
    try:
        playlist = Playlist(data['url'])
    except:
        print("Something gone wrong with the playlist url, check if it still exist and is not private")
        exit()
    count = 0
    print(f"Downloading {len(playlist)} videos")
    print_progress_bar(50,0,10)
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_number) as executor:
        for video in playlist.video_urls:
            futures.append(executor.submit(download_video, url=video, path=data['path'], audioOnly=data['audioOnly'], progress=None))
        
        for future in concurrent.futures.as_completed(futures):
            count+=1
            print_progress_bar(50,count,len(playlist))

    print("\nSuccessfully Completed")

#main funcion
def main():
    args = create_parser()
    data = {'path':os.path.abspath(args.path)+os.path.sep, 'url':args.url,'isPlaylist':args.playlist,'audioOnly':args.audio}
    
    if not os.path.exists(data["path"]): #create path
        os.makedirs(data["path"])

    if(args.playlist):
        dowload_playlist(data,args.multithreading)
    else:   
        download_single(data)

if __name__ == "__main__":
    main()
