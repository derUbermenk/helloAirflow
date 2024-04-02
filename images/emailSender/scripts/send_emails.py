import os
import sys

class EmailSender():
    def __init__(self):
        return

def checkPath(filePath: str):
    if os.path.exists(filePath):
        return
    else:
        sys.exit(1)