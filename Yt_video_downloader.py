from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from pytube import YouTube
import re
import os
import pyautogui


class App:
    def __init__(self, root_):
        self.root = root_
        # to run through code use below
        self.root.iconbitmap(r"images\\youtube_121180.ico")

        # for exe use below
        # self.root.iconbitmap("youtube_121180.ico")
        self.root.title("YT Music/Video Downloader")
        self.root.geometry('1100x600')
        self.video_title_label = Label(root)

        # creating frame
        self.input_frame = Frame(root)
        self.input_frame.pack(padx=0, pady=70)

        # adding url entering field to frame
        self.name_var = StringVar()
        self.url_lbl = Label(self.input_frame, text="Paste Url here->")
        self.url_lbl.grid(row=1, column=0)
        self.url = Entry(self.input_frame, textvariable=self.name_var, width=70, bd=5)
        # url.configure(highlightbackground="red", highlightcolor= "red")
        self.url.grid(row=1, column=1, pady=10, padx=10)

        # making video title display bar
        self.video_title = Label(self.input_frame, text="Video Title:")
        self.video_title.grid(row=2, column=0)

        self.videos = Frame(self.root)
        self.videos.place(rely=0.2, relx=0.5, anchor=N)

        # making selection box for video or audio selection
        self.v_type = StringVar()
        self.format = ttk.Combobox(self.input_frame, width=14, textvariable=self.v_type)
        # format.bind("<<ComboboxSelected>>",self.callback)
        self.format['values'] = ["Video Download", "Audio Download"]
        self.format.grid(column=1, row=3)

        # search button to search the required file format
        self.btn_search_url = Button(self.input_frame, text="Search", borderwidth=7, relief="raised", padx=1, pady=2,
                                     command=self.main_function)
        self.btn_search_url.grid(row=10, column=1)

        # setting variable to help in progress bar
        self.size = 0
        self.step = 0

        # creating youtube object
        self.yt = ""
        # creating dict to store video or audio qualities
        self.dict = {}

        # store data
        self.title_display = StringVar()

    def threading(self):
        t1 = Thread(target=self.downloading)
        if self.size == 100:
            t1.join()
        t1.start()

    @staticmethod
    def percent(self, tem, total):
        perc = (float(tem) / float(total)) * float(100)
        return perc

    def progress_func(self, chunk, file_handle, bytes_remaining):

        remaining = (100 * bytes_remaining) / self.size
        self.step = 100 - int(remaining)
        # Creating progress bar
        progress = Progressbar(self.input_frame, orient=HORIZONTAL,
                               length=100, mode='determinate')
        progress.grid(row=15, column=1)
        progress['value'] = self.step
        # creating percentage download display
        progress_bar = f"{self.step}% Downloaded"
        progress_status = Label(self.input_frame, text=progress_bar)
        progress_status.grid(row=16, column=1)

    def downloading(self):
        try:
            stream = self.yt.streams.get_by_itag(self.dict[self.title_display.get()])
            self.size = stream.filesize

            # filedialog.asksaveasfilename(filetypes = files, initialfile=str(yt.title)
            # Below method is used to save to default location of downloads in user profile
            stream.download(output_path=f"{os.environ['UserProfile']}/Downloads")
        except KeyError:
            pyautogui.alert("Please choose valid resolution from list")

    def searching(self):
        self.threading()
        self.downloding()

    #def complete_func():
    #    print("Downloaded succesfully..")

    def main_function(self):
        # assigning title
        try:
            # var = StringVar()
            #global video_title_label
            self.video_title_label.destroy()
            self.yt = YouTube(self.name_var.get(), on_progress_callback=self.progress_func)
            # print(var)
            var = self.yt.title

            # print(var)
            self.video_title_label = Label(self.input_frame, text=var)
            self.video_title_label.grid(row=2, column=1)
            #self.dict = {}
            if self.v_type.get() == "Audio Download":
                var = self.yt.streams.filter(only_audio=True)
                #print(var)
                for i in var:
                    k = str(i)
                    l = re.findall(r'\d+', k)

                    self.dict[k[19:52]] = l[0]
                    print(dict)

            elif self.v_type.get() == "Video Download":

                var = self.yt.streams.filter(mime_type='video/mp4')
                for i in var:
                    # l.append(str(i))
                    # l.append(str(i))
                    # print(type(i))
                    k = str(i)
                    l = re.findall(r'\d+', k)
                    #print(l,type(l))
                    self.dict[k[19:52]] = l[0]

            else:
                pyautogui.alert("Please select correct download type from list")


            #
            # print(dict)
            selection_chosen = ttk.Combobox(self.input_frame, width=57, textvariable=self.title_display)
            selection_chosen['values'] = list(self.dict.keys())
            selection_chosen.grid(column=1, row=12)

            btn_download = Button(self.input_frame, text="Download", width=13, borderwidth=3, relief="raised",
                                  command=self.threading)
            btn_download.grid(column=1, row=13)

        except:
            pyautogui.alert(text='Not a valid YouTube Url', title='Invalid Url', button='OK')


if __name__ == "__main__":
    root = Tk()
    obj = App(root)
    mainloop()
