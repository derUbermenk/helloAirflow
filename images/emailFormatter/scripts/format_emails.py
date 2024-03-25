import argparse
from string import Formatter
import pandas

class EmailFormatter():
    def __init__(self, path_to_users: str, ds: str):
        self.path_to_users = path_to_users 
        self.ds = ds
        return

    def load_user_info(self):
        return

    def formatEmail(self):
        return

    def saveToJSON(self):
        return

    def run(self):
        return


def initializeFormatter(args) -> EmailFormatter:
    parser = argparse.ArgumentParser(
        prog="EmailFormatter",
        description="a program that formats email")
    
    parser.add_argument('path_to_users', help="path to csv file")
    parser.add_argument('ds', help="execution date")

    _args = parser.parse_args(args)

    formatter = EmailFormatter(_args.path_to_users, _args.ds)

    return formatter 
