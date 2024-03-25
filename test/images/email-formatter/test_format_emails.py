from datetime import datetime
from images.emailFormatter.scripts.format_emails import EmailFormatter, initializeFormatter
from pytest_mock import mocker

def test_initializeFormatter():
    date_string = "2024-02-01"
    path_to_users= "/path/to/users.csv"
    args = [path_to_users, date_string]
    formatter = initializeFormatter(args)

    assert isinstance(formatter, EmailFormatter)

    assert formatter.path_to_users, path_to_users
    assert formatter.ds, date_string

def test_run_1(mocker):

    ''' #class EmailFormatter()
    class EmailFormatter():
        def load_user_info(self):
            return
        
        def formatEmails(self):
            return
            
        def saveToJSON(self):
            return
            
        def run(self):
            self.load_user_info()
            self.formatEmails()
            # self.saveToJSON()
            return
    '''

    path_to_users= "/path/to/users.csv"
    date_string = "2024-02-01"
    formatter = EmailFormatter(path_to_users, date_string) 

    mock_load_user_info = mocker.patch.object(formatter, 'load_user_info')
    mock_formatEmails = mocker.patch.object(formatter, 'formatEmails')
    mock_saveToJSON = mocker.patch.object(formatter, 'saveToJSON')

    formatter.run()
    # should call load_user_info() once
    mock_load_user_info.assert_called_once()

    # should call formatEmails() once
    mock_formatEmails.assert_called_once()

    # should call saveToJSON() once
    mock_saveToJSON.assert_called_once()

