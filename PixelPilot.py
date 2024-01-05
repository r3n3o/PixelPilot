import tkinter as tk
import logging
from tkinter import ttk
from source.config.Paths import Paths
from source.tools.progress_dialog.Progress_Dialog import ProgressDialog
from source.tools.handler.ActionHandler import ActionHandler
from source.tools.backup.BackupandRestore import BackupandRestore
from source.tools.loadzip.LoadZip import LoadZip
from source.tools.magisk_root.Magisk_Rooted import Magisk_Rooted
from source.tools.reboot.Reboot import Reboot
from source.config.Window_Config import center_window, ajust_windows
from source.config.Logging_Config import LoggingConfig

root = tk.Tk()
root.title("PixelPilot")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.6)}")
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.6)
window_x = int((screen_width - window_width) / 2)
window_y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
root.resizable(False, False)

# Crear marco para la barra de acciones
action_frame = tk.Frame(root)
action_frame.pack(side="top", fill="x")

# Crear botones para la barra de acciones
exit_button = tk.Button(
    action_frame, text="Salir", command=lambda: action_handler.on_exit_button()
)
donate_button = tk.Button(
    action_frame,
    text="Donaciones",
    command=lambda: action_handler.on_donate_button(center_window, ajust_windows),
)
about_button = tk.Button(
    action_frame,
    text="Acerca de",
    command=lambda: action_handler.on_about_button(center_window, ajust_windows),
)
help_button = tk.Button(
    action_frame,
    text="Ayuda",
    command=lambda: action_handler.on_help_button(center_window, ajust_windows),
)
refresh_button = tk.Button(action_frame,
    text="Refrescar")


# Empaquetar los botones en la barra de acciones
exit_button.pack(side="right")
donate_button.pack(side="right")
about_button.pack(side="right")
help_button.pack(side="right")
refresh_button.pack(side="right")

# Crear etiqueta para mostrar el estado de conexión
connection_label = tk.Label(action_frame, text="Conectado")
connection_label.pack(side="left")

# Crear marco para las secciones verticales
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="both", expand=True)

# Crear marco para la sección inferior
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="both", expand=True)

# Crear marcos para las secciones izquierda y derecha
left_frame = tk.Frame(bottom_frame, bg="lavender", bd=2, relief="groove")
right_frame = tk.Frame(bottom_frame, bg="lavender", bd=2, relief="groove")

# Empaquetar los marcos en el marco inferior
left_frame.pack(side="left", fill="both", expand=False)
right_frame.pack(side="right", fill="both", expand=True)

# Crear un nuevo marco dentro del marco left_frame
flash_frame = tk.Frame(left_frame)
flash_frame.grid(row=0,column=1,columnspan=3)

# Crear botones en la sección izquierda
flash_button = tk.Button(left_frame, text="Flash", width=10, height=5)
reboot_button = tk.Button(left_frame, command=lambda: reboot.reboot_thread(), text="Reboot")
reboot_recovery_button = tk.Button(left_frame, command=lambda: reboot.reboot_recovery_thread(), text="Reboot Recovery")
reboot_fastboot_button = tk.Button(left_frame, command=lambda: reboot.reboot_fastboot_thread(), text="Reboot Fastboot")

# Organizar el botón "Flash" en la sección izquierda usando el método grid
flash_button.grid(row=0, column=1)

# Crear una etiqueta para separar el botón "Flash" de los otros botones
separator_label = tk.Label(left_frame, text="Reboot")
separator_label.grid(row=11, column=1)

# Organizar los otros botones en la sección izquierda usando el método grid
reboot_button.grid(row=12, column=0)
reboot_recovery_button.grid(row=12, column=1)
reboot_fastboot_button.grid(row=12, column=2)


# Crear variables de control para los checkboxes
rom_var = tk.IntVar()
recovery_var = tk.IntVar()
boot_var1 = tk.IntVar()
boot_var2 = tk.IntVar()

# Función para asegurar que solo un checkbox esté activo a la vez
def check_checkboxes():
    if rom_var.get() == 1:
        recovery_var.set(0)
        boot_var1.set(0)
        boot_var2.set(0)
    elif recovery_var.get() == 1:
        rom_var.set(0)
        boot_var1.set(0)
        boot_var2.set(0)
        recovery_var.set(1)
    elif boot_var1.get() == 1:
        rom_var.set(0)
        recovery_var.set(0)
        boot_var2.set(0)
    elif boot_var2.get() == 1:
        rom_var.set(0)
        recovery_var.set(0)
        boot_var1.set(0)

# Crear etiquetas y checkboxes cerca del botón "Flash"
rom_label = tk.Label(left_frame, text="ROM", font=("Helvetica", 6))
rom_checkbox = tk.Checkbutton(left_frame, variable=rom_var, command=check_checkboxes, state="disabled")
recovery_label = tk.Label(left_frame, text="Recovery", font=("Helvetica", 6))
recovery_checkbox = tk.Checkbutton(left_frame, variable=recovery_var, command=check_checkboxes, state="disabled")
boot_label = tk.Label(left_frame, text="Boot or Patched_Boot", font=("Helvetica", 6))
boot_checkbox1 = tk.Checkbutton(left_frame, variable=boot_var1, command=check_checkboxes, state="disabled")
boot_checkbox2 = tk.Checkbutton(left_frame, variable=boot_var2, command=check_checkboxes, state="disabled")

# Organizar las etiquetas y checkboxes en varias filas cerca del botón "Flash" usando el método grid
rom_label.grid(row=8,column=0,padx=(3),pady=(3))
rom_checkbox.grid(row=9,column=0,padx=(1),pady=(1))
recovery_label.grid(row=8,column=1,padx=(3),pady=(3))
recovery_checkbox.grid(row=9,column=1,padx=(1),pady=(1))
boot_label.grid(row=8,column=2,padx=(3),pady=(1))
boot_checkbox1.grid(row=9,column=2,padx=(1),pady=(1))
boot_checkbox2.grid(row=10,column=2,padx=(1),pady=(1))





# Crear un widget de registro en la sección derecha
log = tk.Text(right_frame)
log.config(width=25, height=5)
# Empaquetar el widget de registro en la sección derecha
log.pack(side="right", fill="both", expand=True)

# Crear marcos para las secciones verticales
backup_frame = tk.Frame(top_frame, bg="skyblue", bd=2, relief="groove")
rom_frame = tk.Frame(top_frame, bg="palegreen", bd=2, relief="groove")
root_frame = tk.Frame(top_frame, bg="lightpink", bd=2, relief="groove")

# Empaquetar los marcos en el marco superior
backup_frame.pack(side="left", fill="both", expand=True)
rom_frame.pack(side="left", fill="both", expand=True)
root_frame.pack(side="left", fill="both", expand=True)

# Crear títulos para cada sección
backup_title = tk.Label(backup_frame, text="Backup", font=("Arial", 18))
rom_title = tk.Label(rom_frame, text="ROM", font=("Arial", 18))
root_title = tk.Label(root_frame, text="Root", font=("Arial", 18))


# Empaquetar los títulos en sus respectivos marcos
backup_title.pack(pady=10)
rom_title.pack(pady=10)
root_title.pack(pady=10)

# Crear botones y etiquetas para la sección "Backup"
backup_button = tk.Button(
    backup_frame,
    text="Hacer copia de seguridad",
    command=lambda: backup_and_restore.backup_android(),
    state="normal",
)
restore_button = tk.Button(
    backup_frame,
    text="Restaurar backup",
    command=lambda: backup_and_restore.restore_backup(),
    state="disabled",
)
progress_backup_label = tk.Label(backup_frame, text="Esperando", width=20)
progress_backup = ttk.Progressbar(
    backup_frame, orient="horizontal", length=50, mode="determinate"
)

# Crear botones y etiquetas para la sección "Flash"
zip_button = tk.Button(rom_frame , text="Selecionar la ROM", command=lambda: loadzip.on_load_rom_thread())
extrac_buttom = tk.Button(
    rom_frame,
    text="Extraer boot.img",
    command=lambda: loadzip.extrac_boot_thread(),
    state="disabled",
)
recovery_button = tk.Button(rom_frame , text="Seleccionar Recovery", command=lambda: loadzip.load_recovery_thread(), state="normal")

# Crear botones y etiquetas para la sección "Root"
bootload_button = tk.Button(root_frame, text="Enviar Boot.img", command=lambda: magisk_root.push_boot_image_thread(),  state="normal")
patch_magisk_button = tk.Button(root_frame, text="Parchear con Magisk",command=lambda: magisk_root(), state="disabled")
magisk_download = tk.Button(root_frame, text="Recuperar Patched Boot.img", command=lambda: magisk_root.pull_patched_boot_image_thread(), state="normal")


# Empaquetar los botones y etiquetas en el marco "Backup"
progress_backup_label.pack(pady=10)
progress_backup.pack(pady=10)
backup_button.pack(pady=10)
restore_button.pack(pady=10)

# Empaquetar los botones y etiquetas en el marco "Flash"
zip_button.pack(pady=10)
extrac_buttom.pack(pady=10)
recovery_button.pack(pady=10)

# Empaquetar los botones y etiquetas en el marco "Root"
bootload_button.pack(pady=10)
patch_magisk_button.pack(pady=10)
magisk_download.pack(pady=10)

# Crea una instancia de ActionROM y le pasa las variables necesarias como argumentos
logger = logging.getLogger("LoggingConfig")
LoggingConfig()
paths = Paths()
progress_dialog = ProgressDialog(root, "Trabajando...", center_window, ajust_windows)
loadzip = LoadZip(root, log, paths, progress_dialog, extrac_buttom, recovery_button, rom_var, rom_checkbox, recovery_var, recovery_checkbox)
magisk_root = Magisk_Rooted(root, log, paths, bootload_button, patch_magisk_button, progress_dialog)
reboot = Reboot(log, paths, progress_dialog, logger)
action_handler = ActionHandler(root, center_window, ajust_windows)
backup_and_restore = BackupandRestore(
    root,
    log,
    backup_button,
    restore_button,
    progress_backup_label,
    progress_backup,
    center_window,
    ajust_windows,
)
root.mainloop()
