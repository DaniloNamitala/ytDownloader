from tkinter.ttk import Progressbar
from Video import Video
import PIL.Image
import PIL.ImageTk
from io import BytesIO
from urllib.request import urlopen
from tkinter import *
import threading
from Video import State

class GuiVideo(Video, Frame):
    def __init__(self, parent, url, audioOnly) -> None:
        Video.__init__(self, url, audioOnly)
        Frame.__init__(self, parent, highlightbackground="blue", highlightthickness=2, width=350, height=90)
        self._path = "./"
        self._state = State.WAITING
        self._create_frame()
    
    def _create_frame(self):
        self._create_thumb()
        self._create_title()
        self._create_bottom_bar()
        self._create_download_button()

    def _create_thumb(self):
        with urlopen(self.thumb_url) as url:
            _raw = url.read()
            url.close() 
        self._photo_image = PIL.ImageTk.PhotoImage(PIL.Image.open(BytesIO(_raw)).resize((160,90)))
        self._image = Label(self, image=self._photo_image)
        self._image.pack(side=LEFT, padx=5, anchor="w")
    
    def _create_title(self):
        self._title = Label(self, text=self.title, font=("Calibri",10), justify=LEFT, anchor="w")
        self._title.pack(side=TOP, padx=(0,5), fill="x")

    def _create_bottom_bar(self):
        self._bottom_bar = Frame(self, highlightbackground="red", highlightthickness=2)
        self._progress_bar = Progressbar(self._bottom_bar, orient=HORIZONTAL, mode='determinate', length=150)
        self._progress_bar.pack(side=LEFT, padx=5, anchor="w")
        self._bottom_bar.pack(side=BOTTOM, anchor="w", fill="x")    
    
    def _create_download_button(self):
        self._dowload_button = Button(self._bottom_bar, cursor="hand1")
        self._dowload_button.pack(side=RIGHT, anchor="e", padx=2)
        self._dowload_button.bind("<Button-1>", self._button_click)

    def _button_click(self, event):
        if(self._state == State.WAITING):
            threading.Thread(target=self.download, args=(self._path, self._step_progress_bar)).start()
        elif(self._state == State.DOWNLOADING):
            self._update_state(State.PAUSED)
        elif(self._state == State.PAUSED):
            self._update_state(State.DOWNLOADING)

    def _step_progress_bar(self, downloaded, size):
        self._progress_bar['value'] = int((downloaded/size)*100)

    def _notify_state(self):
        if(self._state == State.DOWNLOADING):
            self._icon = PIL.ImageTk.PhotoImage(PIL.Image.open("./icons/pause-solid.png").resize((25,25)))
            self._dowload_button.configure(image=self._icon, background="white")
        elif(self._state == State.PAUSED):
            self._icon = PIL.ImageTk.PhotoImage(PIL.Image.open("./icons/play-solid.png").resize((25,25)))
            self._dowload_button.configure(image=self._icon)
        elif(self._state == State.WAITING):
            self._icon = PIL.ImageTk.PhotoImage(PIL.Image.open("./icons/dowload-solid.png").resize((25,25)))
            self._dowload_button.configure(image=self._icon)
        elif(self._state == State.DONE):
            self._icon = PIL.ImageTk.PhotoImage(PIL.Image.open("./icons/check-solid.png").resize((25,25)))
            self._dowload_button.configure(image=self._icon)
        elif(self._state == State.CONVERTING):
            self._icon = PIL.ImageTk.PhotoImage(PIL.Image.open("./icons/floppy-disk-solid.png").resize((25,25)))
            self._dowload_button.configure(image=self._icon)
        return super()._notify_state()

class Downloader:
    def __init__(self):
        self._root = Tk()
        self._root.geometry("500x700")
        self._root.title("Video Downloader")
        self._main_frame = Frame(self._root,  highlightbackground="yellow", highlightthickness=2)
        self._main_frame.pack(fill="both")
        self._teste = GuiVideo(self._main_frame,"https://www.youtube.com/watch?v=dlejA2rlF3I", True)
        self._teste.pack(padx=5, fill="x", pady=2)
        self._teste2 = GuiVideo(self._main_frame,"https://www.youtube.com/watch?v=rwe12UfuArc", True)
        self._teste2.pack(padx=5, fill="x", pady=2)
        self._teste3 = GuiVideo(self._main_frame,"https://www.youtube.com/watch?v=JcnFsqvCocY", True)
        self._teste3.pack(padx=5, fill="x", pady=2)

    def start(self):
        self._root.mainloop()

def main():
    myApp = Downloader()
    myApp.start()
    

if __name__ == "__main__":
    main()
