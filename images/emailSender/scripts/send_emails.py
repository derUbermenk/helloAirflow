import argparse
from genericpath import isfile
import os
import sys

class EmailSender():
    def __init__(self, ds, path_to_emails, path_to_logs):
        self.ds = ds 
        self.path_to_emails = path_to_emails
        self.path_to_logs = path_to_logs
        return

def checkPath(filePath: str):
    if os.path.isfile(filePath):
        return
    elif os.path.exists(filePath):
        return
    else:
        sys.exit(1)

def initializeSender(args) -> EmailSender:
    parser = argparse.ArgumentParser(
        prog="EmailSender",
        description="a program that sends emails"
    )

    parser.add_argument('ds', help="execution date")
    parser.add_argument('path_to_emails', help="path to emails.json")
    parser.add_argument('path_to_logs', help="save path of run logs")

    _args = parser.parse_args(args)

    sender = EmailSender(_args.ds, _args.path_to_emails, _args.path_to_logs)
    return sender