from pytube import YouTube
from moviepy.editor import *
from pytube import request
from pytube import Stream
from Constants import *

class Video:
    def __init__(self, url, audioOnly = False) -> None:
        self._url = url
        self._state = State.WAITING
        self._ytObj = YouTube(url)
        self._audioOnly = audioOnly
        self._title = self._ytObj.title.replace("/","-")
        self._filename = f"{self._title}.{'mp3' if self._audioOnly else 'mp4'}"
        self._tempfilename = f"{self._title}.{'mp3.temp' if self._audioOnly else 'mp4'}"
    
    @property
    def title(self):
        return self._title
    
    @property
    def thumb_url(self):
        return self._ytObj.thumbnail_url
    
    def _update_state(self, state):
        self._state = state
        self._notify_state()

    def _notify_state(self):
        pass

    def _get_stream(self) -> Stream:
        if(self._audioOnly):
            audio_streams = self._ytObj.streams.filter(only_audio=True).order_by('abr').desc()
            self._stream = audio_streams[1]
        else:
            video_streams = self._ytObj.streams.filter(progressive=True).order_by('resolution').desc()
            self._stream = video_streams[0]
        return self._stream

    def download(self, path, progress = lambda d, fz: None):
        self._update_state(State.DOWNLOADING)
        stream = self._get_stream()
        with open(f"{path}{self._tempfilename}", "wb") as file:
            downloaded = 0
            filesize = stream.filesize
            progress(downloaded, filesize)
            stream = request.stream(stream.url)
            chunk = next(stream,None)
            while chunk:
                file.write(chunk)
                downloaded += len(chunk)
                progress(downloaded, filesize)
                print(self._state)
                if self._state == State.STOP: break
                while self._state == State.PAUSED: pass
                chunk = next(stream,None)
        if(self._state == State.STOP):
            os.remove(f"{path}{self._tempfilename}")
            self._update_state(State.WAITING)
            return
        print(end="\n")
        if self._audioOnly:
            self._convert(path)

    def _convert(self, path):
        self._update_state(State.CONVERTING)
        audio = AudioFileClip(f"{path}{self._filename}.temp")
        audio.write_audiofile(f"{path}{self._filename}", verbose=False, logger=None)
        os.remove(f"{path}{self._filename}.temp")
        self._update_state(State.DONE)