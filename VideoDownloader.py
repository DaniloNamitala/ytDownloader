from Video import Video
import PIL.Image
import PIL.ImageTk
from io import BytesIO
from urllib.request import urlopen
from tkinter import *

class GuiVideo(Video, Frame):
    def __init__(self, parent, url, audioOnly) -> None:
        Video.__init__(self,url, audioOnly)
        Frame.__init__(self, parent, highlightbackground="blue", highlightthickness=2)
        self._create_frame()
    
    def _create_frame(self):
        
        self._create_thumb()

    def _create_thumb(self):
        with urlopen(self.thumb_url) as url:
            _raw = url.read()
            url.close() 
        self._photo_image = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(_raw)).resize((160,90)))
        self._image = Label(self, image=self._photo_image)
        self._image.pack()

        

class Downloader:
    def __init__(self):
        self._root = Tk()
        self._root.title("Video Downloader")
        self._main_frame = Frame(self._root)
        self._main_frame.pack()
        self._teste = GuiVideo(self._main_frame,"https://www.youtube.com/watch?v=dlejA2rlF3I", False)
        self._teste.pack()

    def start(self):
        self._root.mainloop()

def main():
    myApp = Downloader()
    myApp.start()
    

if __name__ == "__main__":
    main()
