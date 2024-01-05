import os
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox

class BackupandRestore:
    def __init__(self, parent, log, backup_button, restore_button, progress_backup_label, progress_backup, center_window, ajust_windows):
        self.root = parent
        self.log = log
        self.backup_button = backup_button
        self.restore_button = restore_button
        self.progress_backup_label = progress_backup_label
        self.progress_backup = progress_backup
        self.center_window = center_window
        self.ajust_windows = ajust_windows

    def backup_android(self):
        # Muestra una ventana para que el usuario seleccione qué datos desea respaldar
        backup_options_window = tk.Toplevel(self.root)
        backup_options_window.title("Opciones de copia de seguridad")
        self.ajust_windows(backup_options_window)
        self.center_window(backup_options_window)

        # Crea variables para almacenar las opciones seleccionadas por el usuario
        system_var = tk.BooleanVar()
        important_folders_var = tk.BooleanVar()
        user_data_var = tk.BooleanVar()
        imei_folder_var = tk.BooleanVar()

        # Crea casillas de verificación para cada opción
        system_checkbutton = tk.Checkbutton(backup_options_window, text="Sistema", variable=system_var)
        system_checkbutton.pack()
        important_folders_checkbutton = tk.Checkbutton(backup_options_window, text="Carpetas importantes", variable=important_folders_var)
        important_folders_checkbutton.pack()
        user_data_checkbutton = tk.Checkbutton(backup_options_window, text="Datos del usuario", variable=user_data_var)
        user_data_checkbutton.pack()
        imei_folder_checkbutton = tk.Checkbutton(backup_options_window, text="Carpeta IMEI (miatoll)", variable=imei_folder_var)
        imei_folder_checkbutton.pack()

        # Crea un botón para iniciar la copia de seguridad con las opciones seleccionadas
        start_backup_button = tk.Button(backup_options_window, text="Iniciar copia de seguridad", command=lambda: self.start_backup(system_var.get(), important_folders_var.get(), user_data_var.get(), imei_folder_var.get()))
        start_backup_button.pack()

    def start_backup(self, system, important_folders, user_data, imei_folder):
         # Deshabilita los botones
         self.backup_button.config(state="disabled")
         self.restore_button.config(state="disabled")

         # Actualiza el texto de la etiqueta de progreso
         self.progress_backup_label.config(text="Haciendo copia de seguridad...")

         # Agrega una entrada al registro
         self.log.insert(tk.END, "Iniciando copia de seguridad...\n")

         # Inicia un subproceso para hacer la copia de seguridad y actualizar la barra de progreso
         threading.Thread(target=self.backup_thread, args=(system, important_folders, user_data, imei_folder)).start()

    def backup_thread(self, system, important_folders, user_data, imei_folder):
         # Ruta del archivo de copia de seguridad
         backup_path = r"C:\\Users\\R3N3\Documents\\Python\\files\\backup\\backup.ab"

         # Comprueba si el archivo de copia de seguridad ya existe
         if os.path.exists(backup_path):
             # Pregunta al usuario si desea reemplazar el archivo existente
             if not messagebox.askyesno("Reemplazar copia de seguridad", "Ya existe una copia de seguridad. ¿Desea reemplazarla?"):
                 # Si el usuario no quiere reemplazar el archivo existente, no hace nada
                 self.log.insert(tk.END, "Copia de seguridad cancelada por el usuario\n")
                 self.backup_button.config(state="normal")
                 self.progress_backup_label.config(text="Esperando")
                 return

         # Construye el comando ADB en función de las opciones seleccionadas por el usuario
         command = "adb backup"

         if system:
             command += " -system"

         if important_folders:
             command += " -noapk com.example.folder1 com.example.folder2"

         if user_data:
             command += " -noapk -noshared -nosystem"

         if imei_folder:
             command += " -noapk com.android.providers.telephony"

         command += f" -f {backup_path}"

         # Ejecuta el comando y captura su salida
         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

         self.log.insert(tk.END,"Ejecutando comando ADB...\n")

         while process.poll() is None:
             line = process.stdout.readline().decode()
             if line:
                 self.log.insert(tk.END,line)
                 self.progress_backup.step(5)
                 time.sleep(0.1)
                 self.root.update_idletasks()

         for line in process.stdout.readlines():
             self.log.insert(tk.END,line.decode())

         for line in process.stderr.readlines():
             self.log.insert(tk.END,line.decode())

         self.progress_backup.stop()

         self.restore_button.config(state="normal")

         self.progress_backup_label.config(text="Copia de seguridad completada")

         self.log.insert(tk.END,"Copia de seguridad completada\n")

    def restore_backup(self):
       # Muestra una ventana para que el usuario seleccione qué datos desea restaurar
       restore_options_window = tk.Toplevel(self.root)
       restore_options_window.title("Opciones de restauración")
       self.center_window(restore_options_window)

       # Crea variables para almacenar las opciones seleccionadas por el usuario
       system_var = tk.BooleanVar()
       important_folders_var = tk.BooleanVar()
       user_data_var = tk.BooleanVar()
       imei_folder_var = tk.BooleanVar()

       # Crea casillas de verificación para cada opción
       system_checkbutton = tk.Checkbutton(restore_options_window, text="Sistema", variable=system_var)
       system_checkbutton.pack()
       important_folders_checkbutton = tk.Checkbutton(restore_options_window, text="Carpetas importantes", variable=important_folders_var)
       important_folders_checkbutton.pack()
       user_data_checkbutton = tk.Checkbutton(restore_options_window, text="Datos del usuario", variable=user_data_var)
       user_data_checkbutton.pack()
       imei_folder_checkbutton = tk.Checkbutton(restore_options_window, text="Carpeta IMEI (miatoll)", variable=imei_folder_var)
       imei_folder_checkbutton.pack()

       # Crea un botón para iniciar la restauración con las opciones seleccionadas
       start_restore_button = tk.Button(restore_options_window, text="Iniciar restauración", command=lambda: self.start_restore(system_var.get(), important_folders_var.get(), user_data_var.get(), imei_folder_var.get()))
       start_restore_button.pack()

    def start_restore(self, system, important_folders, user_data, imei_folder):
       # Deshabilita los botones
       self.backup_button.config(state="disabled")
       self.restore_button.config(state="disabled")

       # Actualiza el texto de la etiqueta de progreso
       self.progress_backup_label.config(text="Restaurando copia de seguridad...")

       # Agrega una entrada al registro
       self.log.insert(tk.END, "Iniciando restauración...\n")

       # Inicia un subproceso para restaurar la copia de seguridad y actualizar la barra de progreso
       threading.Thread(target=self.restore_thread,args=(system,
                                                         important_folders,
                                                         user_data,
                                                         imei_folder)).start()

    def restore_thread(self,
                       system,
                       important_folders,
                       user_data,
                       imei_folder):
      # Ruta del archivo de copia de seguridad
      backup_path = r"C:\\Users\\R3N3\\Documents\\Python\\files\\backup\\backup.ab"

      if not os.path.exists(backup_path):
          self.log.insert(tk.END,"No se encontró ninguna copia de seguridad para restaurar\n")
          self.backup_button.config(state="normal")
          self.progress_backup.config(text="Esperando")
          return

      command = f"adb restore {backup_path}"

      process = subprocess.Popen(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=True)

      self.log.insert(tk.END,"Ejecutando comando ADB...\n")

      while process.poll() is None:
          line = process.stdout.readline().decode()
          if line:
              self.log.insert(tk.END,line)
              self.progress_backup.step(5)
              time.sleep(0.1)
              self.root.update_idletasks()

      for line in process.stdout.readlines():
          self.log.insert(tk.END,line.decode())

      for line in process.stderr.readlines():
          self.log.insert(tk.END,line.decode())

      self.progress_backup.stop()

      self.backup_button.config(state="normal")

      self.progress_backup_label.config(text="Restauración completada")

      self.log.insert(tk.END,"Restauración completada\n")