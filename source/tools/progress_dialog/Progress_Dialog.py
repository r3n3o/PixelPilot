import tkinter as tk
from tkinter import ttk

class ProgressDialog:
    def __init__(self, parent, message, center_window, ajust_windows):
        self.root = parent
        self.message = message
        self.center_window = center_window
        self.ajust_windows = ajust_windows
        self.window = None

    def should_close(self):
        return True

    def set_message(self, message):
        self.message = message
        if self.window:
            self.label.config(text=message)

    def show(self):
        if not self.window or not self.window.winfo_exists():
            self.window = tk.Toplevel(self.root)
            self.window.protocol("WM_DELETE_WINDOW", self.disable_event)
            self.label = ttk.Label(self.window, text=self.message)
            self.label.pack()
            self.progressbar = ttk.Progressbar(self.window, mode='indeterminate')
            self.progressbar.pack()
            self.center_window(self.window)
            self.ajust_windows(self.window)
            self.progressbar.start()
            self.window.grid_columnconfigure(0, weight=1)
        else:
            if self.should_close():
                self.destroy()
            else:
                self.window.deiconify()



    def disable_event(self):
        pass


    def destroy(self):
        if self.window:
            self.progressbar.stop()
            self.window.destroy()
