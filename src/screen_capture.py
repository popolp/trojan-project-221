from PIL import ImageGrab
from config import Config

class ScreenCapture():

    def __init__(self, config: Config):
        self.screenshotCounter = 0
        self.config = config
    
    def captureScreen(self): 
        picture = ImageGrab.grab()
        self.screenshotCounter += 1
        picture.save(self.config.screenshotPath + f'\\{self.screenshotCounter}.jpg')
        return self.config.screenshotPath + f'\\{self.screenshotCounter}.jpg'