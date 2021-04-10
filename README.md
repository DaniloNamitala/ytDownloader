# 	YouTube Downloader 

## About
YouTube Downloader is a python script to download videos and audio from youtube videos

## Content Table

* [About](#about)
* [Content Table](#content-table)
* [Installation](#installation)
* [Usage](#usage)
* [Exemples](#exemples)

## Installation
### Linux
Install [Python](https://www.python.org/)  at lastest version. Actually is 3.9.x, so run the following command: 
	
	$ sudo apt install python 3.9

Now you'll need to install the library [pytube](https://hithub.com/pytube/pytube):

	$ pip3 install pytube
if pip or pip3 is not available install run:

	$ sudo apt install pip3
and try the second command again.
## Usage
With python installed run the help command to get the instructions:

	$ python3 ./downloader.py -h

the result will be: 

	usage: downloader.py [-h] [-p] [-a] url path

	positional arguments:
	  url             Video or playlsit url
	  path            The destination path

	optional arguments:
	  -h, --help      show this help message and exit
	  -p, --playlist  Especify if the url is a playlist
	  -a, --audio     Download only the audio

## Exemples
- Downloading a single video in mp4 format:
	
		$ python3  ./dowloader.py https://www.youtube.com/watch?v=YOq2afxPJkM ./myfolder/ 

- Downloading a music playlist in mp3 format:
	
		$ python3  ./dowloader.py -pa https://www.youtube.com/playlist?list=PL5XvdXjPkManLzT0fUXTXWVfdLxGrLYCr ./myfolder/ 
