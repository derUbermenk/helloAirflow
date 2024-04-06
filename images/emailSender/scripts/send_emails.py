import argparse
import email
from genericpath import isfile
import os
import sys
import logging
import pdb
import json

class EmailSender():
    def __init__(self, ds, path_to_emails, path_to_logs):
        self.ds = ds 
        self.path_to_emails = path_to_emails
        self.path_to_logs = path_to_logs
        return

    def run(self):
        logging.basicConfig(filename=self.path_to_logs, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', force=True)

        logging.info("Preparing Emails")

        emails = self.load_emails()
        self.send_emails(emails)

        logging.info("Done Sending emails")

    def load_emails(self) -> dict:
        with open(self.path_to_emails, 'r') as file:
            # Load JSON data into a dictionary
            emails = json.load(file)

        return emails

    def send_emails(self, emails: dict):
        for user in emails:
            # sending done here
            logging.info(f"Sent email to {user}")

def checkPath(filePath: str):
    if os.path.exists(filePath):
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