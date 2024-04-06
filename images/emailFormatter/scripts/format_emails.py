import argparse
from ast import arg
import email
from genericpath import exists
from string import Formatter
import sys
from tabnanny import check
import pandas as pd
import json
import os

class EmailFormatter():
    def __init__(self, path_to_users: str, ds: str, save_path: str):
        self.path_to_users = path_to_users 
        self.ds = ds
        self.save_path = save_path
        return

    def load_user_info(self) -> pd.DataFrame:
        users = pd.read_csv(self.path_to_users)
        return  users

    def formatEmails(self, users: pd.DataFrame) -> dict:
        emails = {}

        # Define the template
        template = """
{ds}
{email}

Dear {user},

I hope this email finds you well and that your tuna consumption has been satisfactory!
We're reaching out to let you know that the warranty on your last can of tuna is about to expire. Yes, that's right, your extended tuna warranty is coming to an end. Don't panic just yet, though! You still have time to renew and ensure your peace of mind when it comes to enjoying delicious tuna meals."""

        # Iterate over rows in the DataFrame
        for index, row in users.iterrows():
            email_=row['email']
            user_=row['user']
            # Substitute values in the template
            email_content = template.format(
                ds='2024-02-01',
                email=email_,
                user=user_
            )

            emails[email_] = email_content

            
        return emails 

    def saveToJSON(self, emails: dict):
        file_path = self.save_path + f"/{self.ds}_emails.json"
        with open(file_path, 'w') as json_file:
            json.dump(emails, json_file)

    def run(self):
        users = self.load_user_info()
        emails = self.formatEmails(users)
        self.saveToJSON(emails)

def checkFilePath(filePath: str):
    if os.path.exists(filePath):
        return
    else:
        sys.exit(1)

def initializeFormatter(args) -> EmailFormatter:
    parser = argparse.ArgumentParser(
        prog="EmailFormatter",
        description="a program that formats email")
    
    parser.add_argument('path_to_users', help="path to csv file")
    parser.add_argument('ds', help="execution date")
    parser.add_argument('save_dir', help="save directory")

    _args = parser.parse_args(args)

    formatter = EmailFormatter(_args.path_to_users, _args.ds, _args.save_dir)

    checkFilePath(formatter.path_to_users)

    return formatter 

def main(args):
    formatter = initializeFormatter(args)
    formatter.run()
    
if __name__ == "__main__":
    main(sys.argv[1:])