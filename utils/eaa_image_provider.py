import os
import random
from utils.path_helper import PathHelper

class EaaImageProvider:
    def __init__(self):
        self.folder_path = PathHelper.resource_path(os.path.join("iaps"))
        self.images = [f for f in os.listdir(self.folder_path) if f.endswith('.jpg')]
    
    def getNextImage(self):
        if not self.images:
            return None
        return random.choice(self.images)
