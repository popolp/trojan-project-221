from config import Config
import os, string, psutil


class ComputerInfo:
    def __init__(self, config: Config):
        self.__config = config

    def get_process_list(self):
        output_filepath = str(self.__config.logPath + f"\\{self.__config.processList}")
        
        with open(file=output_filepath, mode="w", encoding="utf-8") as f:
            for p in psutil.process_iter():
                f.write(f"{p.name()} {p.pid}\n")
        
        return output_filepath

    def get_dirlist(self):
        available_drives = [
            "%s:" % d for d in string.ascii_uppercase if os.path.exists("%s:" % d)
        ]
        output_filepath = str(self.__config.logPath + f"\\{self.__config.dirlist}")

        with open(file=output_filepath, mode="w", encoding="utf-8") as f:
            for drive in available_drives:
                for subdir, dirs, files in os.walk(drive + "\\"):
                    for file in files:
                        f.write(os.path.join(subdir, str(file.encode("utf-8"))) + "\n")

        return output_filepath