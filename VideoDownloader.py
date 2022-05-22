#!/usr/bin/python3


from pathlib import Path
import os
import math
import argparse
from Video import Video
from pytube import Playlist
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

def print_progress_bar(blocks_number, conclued, total):
    decimal_percent = conclued/total
    blocks = math.floor(decimal_percent*blocks_number)
    bar = '[' + blocks * chr(9608)+ (blocks_number-blocks)*' '+']'
    print(f'{bar} {decimal_percent* 100:.2f}%', end='\r')

#Call video_download for one video
def download_single(data):
    Video(data['url'], data['audioOnly']).download(data['path'] , print_progress_bar)
    print("\nSuccessfully Completed")

#Create a playlist object and call download_video for each video
def dowload_playlist(data,threads_number):
    try:
        playlist = list(map(lambda url: url, Playlist(data['url']).video_urls))
    except:
        print("Something gone wrong with the playlist url, check if it still exist and is not private")
        exit()
    print(f"Downloading {len(playlist)} videos")
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_number) as executor:
        for url in playlist:
            futures.append(executor.submit(Video(url, data['audioOnly']).download, path=data['path'], progress=None))

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
