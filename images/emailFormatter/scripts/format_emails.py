import argparse
from string import Formatter
import pandas as pd

class EmailFormatter():
    def __init__(self, path_to_users: str, ds: str):
        self.path_to_users = path_to_users 
        self.ds = ds
        return

    def load_user_info(self) -> pd.DataFrame:
        return pd.DataFrame() 

    def formatEmails(self, users: pd.DataFrame) -> dict:
        return {} 

    def saveToJSON(self, emails: dict):
        return

    def run(self):
        users = self.load_user_info()
        emails = self.formatEmails(users)
        self.saveToJSON(emails)



def initializeFormatter(args) -> EmailFormatter:
    parser = argparse.ArgumentParser(
        prog="EmailFormatter",
        description="a program that formats email")
    
    parser.add_argument('path_to_users', help="path to csv file")
    parser.add_argument('ds', help="execution date")

    _args = parser.parse_args(args)

    formatter = EmailFormatter(_args.path_to_users, _args.ds)

    return formatter 
