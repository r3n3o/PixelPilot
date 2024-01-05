def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def ajust_windows(ajuwin):
    ajuwin.attributes("-toolwindow", 1)
    ajuwin.attributes("-topmost", 1)
    ajuwin.resizable(False, False)
    ajuwin.grab_set()
