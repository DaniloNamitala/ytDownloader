from tkinter import *
from Constants import *
from GuiVideo import GuiVideo
import PIL.ImageTk
import PIL.Image

class Downloader:
    def __init__(self):
        self._root = Tk()
        self._root.geometry("500x700")
        self._root.title("Video Downloader")
        self._root.configure(background=COLOR_BG)
        self._create_top_frame()
        self._divider = Frame(self._root, bg=COLOR_BLACK, height=3)
        self._divider.pack(side=TOP, fill="x")
        self._create_video_frame()
        self._video_list = list()

    def _create_video_frame(self):
        self._video_frame = Frame(self._root, background=COLOR_BG)
        self._video_frame.pack(fill=BOTH, anchor='n', expand=True, side=TOP)
    
    def _create_top_frame(self):
        self._top_frame = Frame(self._root, background=COLOR_BG)
        self._top_frame.pack(side=TOP, anchor="w", fill="x")
        
        self._icon = PIL.ImageTk.PhotoImage(PIL.Image.open("./icons/download-solid.png").resize((20,20)))
        self._button_add = Button(self._top_frame, relief=FLAT, image=self._icon, background=COLOR_BG, highlightthickness=0)
        self._button_add.pack(side=RIGHT, anchor="e", fill="y")
        self._button_add.bind("<Button-1>", self._add_click)

        self._url_text = Entry(self._top_frame, relief=FLAT, highlightcolor=COLOR_BLACK, highlightbackground="grey")
        self._url_text.pack(side=RIGHT, anchor="e", fill="x", pady=3, padx=3, expand=True)
    
    def _add_click(self, event):
        _video = GuiVideo(self._video_frame, self._url_text.get(), True)
        _video.pack(padx=5, fill="x", pady=2)
        
        self._video_list.append(_video)

    def _temporary(self):
        self._teste = GuiVideo(self._video_frame,"https://www.youtube.com/watch?v=rwe12UfuArc", True)
        self._teste.pack(padx=5, fill="x", pady=2)
        self._teste2 = GuiVideo(self._video_frame,"https://www.youtube.com/watch?v=rwe12UfuArc", True)
        self._teste2.pack(padx=5, fill="x", pady=2)
        self._teste3 = GuiVideo(self._video_frame,"https://www.youtube.com/watch?v=JcnFsqvCocY", True)
        self._teste3.pack(padx=5, fill="x", pady=2)

    def start(self):
        self._root.mainloop()

def main():
    myApp = Downloader()
    myApp.start()
    

if __name__ == "__main__":
    main()
