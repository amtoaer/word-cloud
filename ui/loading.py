from tkinter import Label, Toplevel, ttk
from tkinter.constants import HORIZONTAL


class Loading(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        # disable delete event
        self.protocol('WM_DELETE_WINDOW', self.__null)
        self.title('通知')
        self.resizable(False, False)
        self.__draw()
        self.grab_set()
        self.progress.start()

    def __draw(self):
        Label(self, text='正在处理中，请稍候...').pack()
        self.progress = ttk.Progressbar(
            self, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.progress.pack()

    def __null():
        return
