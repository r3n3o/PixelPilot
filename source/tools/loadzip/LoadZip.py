import os
import logging
import zipfile
import hashlib
import threading
import tkinter as tk
from tqdm import tqdm
from tkinter import filedialog, messagebox

class TqdmLogger(tqdm):
    def __init__(self, log_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_widget = log_widget

    def write(self, s):
        self.log_widget.insert("end", s.strip() + "\n")
        logging.info(s.strip())   

class LoadZip:
    def __init__(
        self, parent, log, paths, progress_dialog, extrac_buttom, recovery_button, rom_var, rom_checkbox, recovery_var, recovery_checkbox
    ):
        self.root = parent
        self.log = log
        self.paths = paths
        self.progress_dialog = progress_dialog
        self.extrac_buttom = extrac_buttom
        self.recovery_button = recovery_button
        self.rom_var = rom_var
        self.rom_checkbox = rom_checkbox
        self.recovery_var = recovery_var
        self.recovery_checkbox = recovery_checkbox

     

    def on_load_rom_thread(self):
        # Crea un hilo para ejecutar el método on_load_rom
        thread = threading.Thread(target=self.on_load_rom, args=())
        thread.start()

    def on_load_rom(self):
        
        # Permite al usuario cargar manualmente un archivo zip
        filename = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        self.progress_dialog.show()
        if filename:
            with open(filename, "rb") as file:
                data = file.read()
                md5 = hashlib.md5(data).hexdigest()

                # Actualiza el registro con el nombre del archivo y el hash md5
                self.log.insert(
                    tk.END, f"Archivo cargado: {os.path.basename(filename)}\n"
                )
                self.log.insert(tk.END, f"Hash MD5: {md5}\n")
                self.extrac_buttom.config(state="normal")
                self.rom_checkbox.config(state="normal")
                self.rom_var.set(0)
                # Almacena el nombre del archivo en una variable de instancia
                self.filename = filename
        else:
            # Muestra un mensaje en el registro si el usuario no selecciona nada
            self.log.insert(tk.END, "No se seleccionó ningún archivo\n")
        self.progress_dialog.destroy()
            

    def extrac_boot_thread(self):
        thread = threading.Thread(target=self.extrac_boot, args=())
        thread.start()

    def extrac_boot(self):
        self.progress_dialog.show()
        self.log.insert(tk.END, "Extrayendo boot...\n")
        destination_path = self.paths.get_paths()["destination_path"]
        logging.info(f"destination_path: {destination_path}\n")
        logging.info(f"Abrir archivo zip: {self.filename}\n")
        try:
        # Open zip file
            with zipfile.ZipFile(self.filename, "r") as zip_ref:
            # Search for boot.img file in zip file
                boot_img = next(
                    (
                        file
                        for file in zip_ref.infolist()
                        if file.filename.endswith("boot.img")
                    ),
                    None,
                )
                if not boot_img:
                    self.log.insert(tk.END, 
                        "No se encontró el archivo boot.img en el archivo zip"
                    )
                    return

                if not os.path.exists(
                    os.path.join(destination_path, boot_img.filename)
                ) or messagebox.askyesno(
                    "Sobrescribir archivo",
                    f"El archivo {boot_img.filename} ya existe. ¿Desea sobrescribirlo?",
                ):
                 # Extract boot.img file
                    with TqdmLogger(self.log) as pbar:
                        zip_ref.extract(boot_img, path=destination_path)
                        pbar.update()
                        self.log.insert(tk.END, f"El archivo {boot_img.filename} se extrajo correctamente\n")


        except zipfile.BadZipFile:
            self.log.insert(tk.END, "No se pudo abrir el archivo zip")
            logging.error("No se pudo abrir el archivo zip")
        except Exception as e:
        # Log error in event log
            self.log.insert(tk.END, f"Error al extraer el archivo: {e}\n")
            logging.error(f"Error al extraer el archivo: {e}")
        self.progress_dialog.destroy()

    def load_recovery_thread(self):
        thread = threading.Thread(target=self.load_recovery, args=())
        thread.start()
        
    def load_recovery(self):
        recovery_path = filedialog.askopenfilename(filetypes=[("Image files", "*.img")])
        self.progress_dialog.show()
        if recovery_path:
            with open(recovery_path, "rb") as file:
                data = file.read()
                md5 = hashlib.md5(data).hexdigest()

        # Actualiza el registro con el nombre del archivo y el hash md5
            self.log.insert(
                tk.END, f"Archivo cargado: {os.path.basename(recovery_path)}\n"
            )
            self.log.insert(tk.END, f"Hash MD5: {md5}\n")
            self.recovery_checkbox.config(state="normal")
            self.recovery_var.set(1)

        # Almacena el nombre del archivo en una variable de instancia
            self.recovery_filename = recovery_path
        else:
        # Muestra un mensaje en el registro si el usuario no selecciona nada
            self.log.insert(tk.END, "No se seleccionó ningún archivo\n")
        self.progress_dialog.destroy()
