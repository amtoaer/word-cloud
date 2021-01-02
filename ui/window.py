import tkinter
import re
from tkinter import Entry, Frame, Label, ttk, Button, messagebox
from tkinter.constants import END, EXTENDED
from threading import Thread
from PIL.ImageTk import PhotoImage
from ui.loading import Loading
from backend.utils import handleURLs


class Window(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('舆情热词分析')
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.url_rules = re.compile(
            '^(http(s)?:\/\/)\w+[^\s]+(\.[^\s]+){1,}$')
        self.image = None
        self.loading = None
        self.word_cloud = None
        self.__draw()

    def __draw(self):
        top_frame = tkinter.LabelFrame(self, text='编辑区')
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)
        self.URL = tkinter.StringVar()
        Entry(top_frame, textvariable=self.URL).grid(
            row=0, column=0, sticky='WE')
        Button(top_frame, text='+', command=self.__add).grid(row=0,
                                                             column=1, sticky='WE')
        self.URLs = tkinter.Listbox(top_frame, selectmode=EXTENDED)
        self.URLs.grid(row=1, column=0, sticky='WE')
        Button(top_frame, text='-', command=self.__delete).grid(row=1,
                                                                column=1, sticky='WE')
        top_frame.grid(row=0, column=0, sticky='WE')

        Button(self, text='分析', command=self.__analyse).grid(
            row=1, column=0, sticky='WE')

        bottom_frame = ttk.Notebook(self)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        tmp_frame = Frame(bottom_frame)
        tmp_frame.grid_rowconfigure(0, weight=1)
        tmp_frame.grid_columnconfigure(0, weight=1)
        self.image_label = Label(tmp_frame)
        self.image_label.grid(row=0, column=0, sticky='NWSE')
        bottom_frame.add(tmp_frame, text='词云图')
        columns = ('关键词', '出现次数')
        self.top10 = ttk.Treeview(
            bottom_frame, columns=columns, show='headings')
        for column in columns:
            self.top10.heading(column, text=column)
        bottom_frame.add(self.top10, text='top 10词频分析')
        bottom_frame.grid(row=2, column=0, sticky='WE')

    def __add(self):
        URL = self.URL.get()
        if self.url_rules.fullmatch(URL) == None:
            messagebox.showerror(title='错误', message='请输入正确的URL！')
            return
        elif URL in self.URLs.get(0, self.URLs.size()):
            messagebox.showerror(title='错误', message='该URL已在表中！')
            return
        self.URLs.insert(END, URL)
        self.URL.set('')

    def __delete(self):
        for index in reversed(self.URLs.curselection()):
            self.URLs.delete(index)

    def __analyse(self):
        if self.URLs.size() == 0:
            messagebox.showerror(title='错误', message='当前URL列表为空！')
            return
        self.loading = Loading(self)
        Thread(target=self.__handleURLs).start()

    def __handleURLs(self):
        URLs = self.URLs.get(0, self.URLs.size())
        tmp_image, top_10 = handleURLs(URLs)
        self.image = PhotoImage(tmp_image)
        self.image_label.configure(image=self.image)
        for last_couple in self.top10.get_children():
            self.top10.delete(last_couple)
        for couple in top_10:
            self.top10.insert('', END, values=couple)
        self.loading.destroy()

    def run(self):
        self.mainloop()
