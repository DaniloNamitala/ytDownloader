#!/usr/bin/python3

from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import os
import sys
import math
import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--playlist', help='Especify if the url is a playlist', action="store_true")
    parser.add_argument('url', help='Video or playlsit url')
    parser.add_argument('path',type=Path, help='The destination path', default="./")
    parser.add_argument('-a','--audio', help='Download only the audio', action="store_true")
    return parser.parse_args()

def get_stream(video, audioOnly):
    if(audioOnly):
        audio_streams = video.streams.filter(only_audio=True).order_by('abr').desc()
        return audio_streams[1]
    else:
        video_streams = video.streams.filter(progressive=True).order_by('resolution').desc()
        return video_streams[1]

def rename_file(path, old_name, new_name, extension):
    number = 0
    old_name = old_name[len(path):]
    name = new_name+extension
    while(os.path.isfile(path+name)):
        number += 1
        name = new_name + '(' + str(number) + ')'+extension
    os.rename(path+old_name, path+name)

def  progress(stream, chunk=None,bytes_remaining=None):
    decimal_percent = (stream.filesize-bytes_remaining)/stream.filesize
    blocks = math.floor(decimal_percent*20)
    bar = '[' + blocks * chr(9608)+ (20-blocks)*' '+']'
    print(f'{bar} {decimal_percent* 100:.2f}%', end='\r')

def complete(stream,file_path = None):
    print('')

def download_video(data):
    try:
        video = YouTube(data['url'], on_progress_callback=progress, on_complete_callback=complete)
    except:
        print("Something gone wrong with the video url, check if it still exist")
        exit()
    stream = get_stream(video, data['audioOnly'])
    output_file = stream.download(output_path = data['path'], filename="temp")
    sufix = '.mp4'
    if(data['audioOnly']):
        sufix = '.mp3'
    rename_file(data['path'],output_file, video.title,sufix)

def download_single(data):
    print(f"Downloading 1 of 1")
    bar = '[' + 20 * ' ' +']'
    print(f'{bar} 0.00%', end='\r')
    download_video(data)
    print("Successfully Completed")
    

def dowload_playlist(data):
    try:
        playlist = Playlist(data['url'])
    except:
        print("Something gone wrong with the playlist url, check if it still exist and is not private")
        exit()
    count = 0
    for video in playlist.video_urls:
        count+=1
        print(f"Downloading {count} of {len(playlist.video_urls)}")
        bar = '[' + 20 * ' ' +']'
        print(f'{bar} 0.00%', end='\r')

        video_data = data
        video_data['url'] = video
        download_video(video_data)
    print("Successfully Completed")
        

def main():
    args = create_parser()
    data = {'path':os.path.abspath(args.path)+'/', 'url':args.url,'isPlaylist':args.playlist,'audioOnly':args.audio}
 
    if(args.playlist):
        dowload_playlist(data)
    else:   
        download_single(data)

if __name__ == "__main__":
    main()
