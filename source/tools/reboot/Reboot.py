import subprocess
import threading
import tkinter as tk
from tkinter import messagebox

class Reboot:
    def __init__(self, log, paths, progress_dialog, logger):
        self.log = log
        self.paths = paths.get_paths()
        self.progress_dialog  = progress_dialog
        self.logger = logger

    def reboot_thread(self):
        # Crea un hilo para ejecutar el método reboot
        thread = threading.Thread(target=self.reboot, args=())
        thread.start()

    def reboot(self):
    # Muestra un cuadro de diálogo de confirmación antes de reiniciar el dispositivo
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea reiniciar el dispositivo?"):
            self.logger.info("El usuario confirmó que desea reiniciar el dispositivo")
            try:
                self.progress_dialog.show()
                # Ejecuta el comando ADB para mostrar la lista de dispositivos conectados
                result = subprocess.run([self.paths["adb_path"], "devices"], capture_output=True, text=True)
                self.log.insert(tk.END, result.stdout + result.stderr)

                # Ejecuta el comando ADB para reiniciar el dispositivo
                result = subprocess.run([self.paths["adb_path"], "reboot"], capture_output=True, text=True)
                self.log.insert(tk.END, result.stdout + result.stderr)
                self.progress_dialog.destroy()
            except Exception as e:
                self.log.insert(tk.END, f"Error al ejecutar comandos ADB: {e}\n")
            self.progress_dialog.destroy()
        else:
            self.log.insert(tk.END, "El usuario no aceptó reiniciar el dispositivo\n")


    def reboot_recovery_thread(self):
        # Crea un hilo para ejecutar el método reboot
        thread = threading.Thread(target=self.reboot_recovery, args=())
        thread.start()

    def reboot_recovery(self):
        # Muestra un cuadro de diálogo de confirmación antes de reiniciar el dispositivo en modo de recuperación
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea reiniciar el dispositivo en modo de recuperación?"):
            self.logger.info("El usuario confirmó que desea reiniciar el dispositivo")
            self.progress_dialog.show()
            try:
                # Ejecuta el comando ADB para mostrar la lista de dispositivos conectados
                result = subprocess.run([self.paths["adb_path"], "devices"], capture_output=True, text=True)
                self.log.insert(tk.END, result.stdout + result.stderr)
                # Ejecuta el comando ADB para reiniciar el dispositivo en modo de recuperación
                result = subprocess.run([self.paths["adb_path"], "reboot", "recovery"], capture_output=True, text=True)
                self.log.insert(tk.END, result.stdout + result.stderr)
            except Exception as e:
                self.log.insert(tk.END, f"Error al ejecutar comandos ADB: {e}\n")
            self.progress_dialog.destroy()
        else:
            self.log.insert(tk.END, "El usuario no aceptó reiniciar el dispositivo en recovery\n")


    def reboot_fastboot_thread(self):
        # Crea un hilo para ejecutar el método reboot
        thread = threading.Thread(target=self.reboot_fastboot, args=())
        thread.start()

    def reboot_fastboot(self):
        # Muestra un cuadro de diálogo de confirmación antes de reiniciar el dispositivo en modo fastboot
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea reiniciar el dispositivo en modo fastboot?"):
            self.logger.info("El usuario confirmó que desea reiniciar el dispositivo")
            self.progress_dialog.show()
            try:
                # Ejecuta el comando ADB para mostrar la lista de dispositivos conectados
                result = subprocess.run([self.paths["adb_path"], "devices"], capture_output=True, text=True)
                self.log.insert(tk.END, result.stdout + result.stderr)
                # Ejecuta el comando ADB para reiniciar el dispositivo en modo fastboot
                result = subprocess.run([self.paths["adb_path"], "reboot", "bootloader"], capture_output=True, text=True)
                self.log.insert(tk.END, result.stdout + result.stderr)
            except Exception as e:
                self.log.insert(tk.END, f"Error al ejecutar comandos ADB: {e}\n")
            self.progress_dialog.destroy()
        else:
            self.log.insert(tk.END, "El usuario no aceptó reiniciar el dispositivo en fastboot\n")
