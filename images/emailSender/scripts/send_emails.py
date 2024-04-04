import argparse
from genericpath import isfile
import os
import sys
import logging

class EmailSender():
    def __init__(self, ds, path_to_emails, path_to_logs):
        self.ds = ds 
        self.path_to_emails = path_to_emails
        self.path_to_logs = path_to_logs
        return

    def run(self):
        log_file_name = "{path_to_logs}/{ds}_logs.log"

        logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Preparing Emails")

        emails = self.load_emails()
        self.send_emails(emails)

        logging.info("Done Sending emails")

    def load_emails(self) -> dict:
        return

    def send_emails(self, emails: dict):
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