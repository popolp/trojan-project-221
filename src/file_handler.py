import shutil, gzip
from config import Config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import blocks


class FileHandler:
    def __init__(self, config: Config):
        self.screenshotCounter = 0
        self.config = config

    def zip_file(self, file_path):
        with open(f"{file_path}", "rb") as f_in:
            with open(f"{file_path}.gz", "wb") as f_out:
                with gzip.GzipFile(f"{file_path}", "wb", fileobj=f_out) as f_out:
                    shutil.copyfileobj(f_in, f_out)

    def upload_file(self, msg_client: WebClient, file_path):
        if file_path[-3:] != "jpg":
            self.zip_file(file_path)
            file_path = file_path + ".gz"
        try:
            msg_client.files_upload(
                token=self.config.botToken,
                file=file_path,
                channels=self.config.channelId,
            )
        except (FileNotFoundError, SlackApiError) as e:
            self.send_message(blocks.plain_text(f"Error: {e}"))

