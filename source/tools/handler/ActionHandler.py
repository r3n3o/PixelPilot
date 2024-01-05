import tkinter as tk
import webbrowser
import qrcode
from PIL import ImageTk, Image
from tkinter import messagebox

class ActionHandler:
    def __init__(self, parent, center_window, ajust_windows):
        self.root = parent
        self.center_window = center_window
        self.ajust_windows = ajust_windows

    def on_exit_button(self):
        if messagebox.askokcancel("Confirmar", "¿Estás seguro de que quieres Salir?"):
            self.root.destroy()

    def on_donate_button(self, center_window, ajust_windows):
        def open_link(link):
            webbrowser.open(link)

        donate_window = tk.Toplevel(self.root)
        donate_window.title("Métodos de donación")

        label = tk.Label(donate_window, text="Puedes hacer una donación a través de los siguientes métodos:")
        label.pack()

        methods = ["PayPal", "Bitcoin(BTC)", "USDT(TRC20)", "BNB(BEP20)"]
        addresses = ["https://paypal.me/r3n30", "1Fxu7L83m1qDUM84fvsrQN3iwEjaxeRLEy", "TSAi16seGKMoygZGof4zETf4r4X6fAdrnR", "0x686c626E48bfC5DC98a30a9992897766fed4Abd3"]
        for method, address in zip(methods, addresses):
            if method == "PayPal":
                method_label = tk.Label(donate_window, text=f"{method}: {address}", fg="blue", cursor="hand2")
                method_label.bind("<Button-1>", lambda e, address=address: open_link(address))
            else:
                method_label = tk.Label(donate_window, text=f"{method}: {address}")
            method_label.pack()

        ajust_windows(donate_window)
        center_window(donate_window)

    def on_about_button(self, center_window, ajust_windows):
      info_window = tk.Toplevel(self.root)
      info_window.title("Acerca de...")

      updaterinfo = tk.Label(info_window, text="Nombre del software: MiatollUpdater for Pixel Experience")
      updaterinfo.pack()
      updaterver = tk.Label(info_window, text="Versión del software: 0.1_Alpha")
      updaterver.pack()
      updaterdev = tk.Label(info_window, text="Desarrollador: R3N3")
      updaterdev.pack()

      ajust_windows(info_window)
      center_window(info_window)

    def on_help_button(self, center_window, ajust_windows):
      help_window = tk.Toplevel(self.root)
      help_window.title("Ayuda")

      label = tk.Label(help_window, text="Para obtener ayuda sobre cómo usar el programa, puedes hacer lo siguiente:")
      label.pack()

      link = tk.Label(help_window, text="Ver videos en YouTube", fg="blue", cursor="hand2")
      link.pack()
      link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.youtube.com/results?search_query=tutorial+programa"))
      
      ajust_windows(help_window)
      center_window(help_window)