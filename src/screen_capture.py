from PIL import ImageGrab
from config import Config

"""
This class is used to manage the screen capturing function.
Uses a counter to determine the name of the images captured, 
and saves them in the specified path in the config file.
"""
class ScreenCapture():

    def __init__(self, config: Config):
        self.screenshotCounter = 0
        self.config = config
    
    def captureScreen(self): 
        picture = ImageGrab.grab()
        self.screenshotCounter += 1
        picture.save(self.config.screenshotPath + f'\\{self.screenshotCounter}.jpg')
        return self.config.screenshotPath + f'\\{self.screenshotCounter}.jpg'