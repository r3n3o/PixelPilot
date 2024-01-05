import os

class Paths:
    def __init__(self):
    # Obtiene la ruta del archivo principal del programa
        self.main_dir = os.path.dirname(os.path.abspath(__file__))


    def get_paths(self):
        paths = {
            "backup_path": os.path.join(self.main_dir, "..", "..",  "files", "backup", "backup.ab"),
            "destination_path": os.path.join(self.main_dir, "..", "..", "files", "output"),
            "input_path": os.path.join(self.main_dir, "..", "..",  "files", "input"),
            "magisk_zip_path": os.path.join(self.main_dir, "..", "..",  "files", "output", "bootpatch"),
            "adb_path": os.path.join(self.main_dir, "..", "..", "lib", "adb.exe"),
            "magisk_repo_path": os.path.join(self.main_dir, 'Magisk'),
            "log_path": os.path.join(self.main_dir, "..", "..",  "files", "log")
        }
        return paths