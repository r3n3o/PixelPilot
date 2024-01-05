import os
import subprocess
import threading
import tkinter as tk

class Magisk_Rooted:
    def __init__(self, parent, log, paths, bootload_button, patch_magisk_button, progress_dialog):
        self.root = parent
        self.log = log
        self.paths = paths.get_paths()
        self.bootload_button = bootload_button
        self.patch_magisk_button = patch_magisk_button
        self.progress_dialog = progress_dialog

    
    def push_boot_image_thread(self):
        # Crea un hilo para ejecutar el método on_load_rom
        thread = threading.Thread(target=self.push_boot_image, args=())
        thread.start()

    def push_boot_image(self):
        self.progress_dialog.show()
    # Copia la imagen de arranque al dispositivo utilizando ADB
        destination_path = self.paths["destination_path"]
        boot_img_path = os.path.join(destination_path, 'boot.img')
        if os.path.exists(boot_img_path):
            self.log.insert(tk.END, 'Enviando boot.img a /sdcard/Download\n')
            subprocess.run([self.paths["adb_path"], 'push', boot_img_path, '/sdcard/Download'])
            self.log.insert(tk.END, 'boot.img enviado exitosamente\n')
        else:
            self.log.insert(tk.END, 'Error: boot.img no se encuentra en la dirección especificada\n')
            self.log.insert(tk.END, 'Por favor extraiga el archivo boot.img en la dirección especificada\n')
            
        self.progress_dialog.destroy()




    def pull_patched_boot_image_thread(self):
        # Crea un hilo para ejecutar el método on_load_rom
        thread = threading.Thread(target=self.pull_patched_boot_image, args=())
        thread.start()
    
    def pull_patched_boot_image(self):
        self.progress_dialog.show()

    # Lista los archivos en la carpeta de descargas del dispositivo
        result = subprocess.run([self.paths["adb_path"], 'shell', 'find', '/sdcard/Download', '-name', '*.img'], stdout=subprocess.PIPE)
        file_list = result.stdout.decode('utf-8').split('\n')
        file_list = [file_name.rstrip('\r') for file_name in file_list]
        print(f"file_list: {file_list}")
    # Busca el archivo de la imagen parcheada
        patched_boot_image = None
        for file_name in file_list:
            if file_name.startswith('/sdcard/Download/magisk_patched-'):
                patched_boot_image = os.path.basename(file_name)
                break

    # Copia la imagen parcheada al PC utilizando ADB
        if patched_boot_image:
            source_path = f'/sdcard/Download/{patched_boot_image}'
            destination_path = os.path.join(self.paths["destination_path"], patched_boot_image)
            self.log.insert(tk.END, 'Recuperando {} de /sdcard/Download\n'.format(patched_boot_image))
            result = subprocess.run([self.paths["adb_path"], 'pull', source_path, destination_path])
            if result.returncode == 0:
                self.log.insert(tk.END, '{} recuperado exitosamente\n'.format(patched_boot_image))
            else:
                self.log.insert(tk.END, 'Error: No se pudo recuperar el archivo {}\n'.format(patched_boot_image))
        else:
            self.log.insert(tk.END, 'Error: No se encontró ninguna imagen parcheada en /sdcard/Download\n')

        self.progress_dialog.destroy()

