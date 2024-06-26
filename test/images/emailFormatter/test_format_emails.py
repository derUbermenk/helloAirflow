from datetime import datetime
import tempfile
import os
import json

from pandas import DataFrame
import pytest
from images.emailFormatter.scripts.format_emails import EmailFormatter, initializeFormatter, checkFilePath
from unittest.mock import MagicMock

def test_initializeFormatter(mocker):
    path_to_users = "/path/to/users.csv"
    date_string = "2024-02-01"
    save_dir = "/path/to/save_dir/emails.json"

    checkPathImportPath = "images.emailFormatter.scripts.format_emails.checkFilePath"
    mocker.patch(checkPathImportPath)

    args = [path_to_users, date_string, save_dir]
    formatter = initializeFormatter(args)

    assert isinstance(formatter, EmailFormatter)

    assert formatter.path_to_users == path_to_users
    assert formatter.ds == date_string
    assert formatter.save_path == save_dir 

def test_checkFilePath():
    temp_path = tempfile.TemporaryDirectory()
    nonExistentFilePath = "/non/existent/path/"
    existentFilePath = temp_path.name

    # it exits with code 1 if path does not exist
    try:
        checkFilePath(nonExistentFilePath)
    except SystemExit as e:
        assert True 
        assert e.code == 1
    else:
        assert False 

    # it does not exit if path exist
    try:
        checkFilePath(existentFilePath)
    except SystemExit as e:
        assert False
    else:
        assert True

def test_run_1(mocker):
    path_to_users = "/path/to/users.csv"
    date_string = "2024-02-01"
    save_dir = "/path/to/save_dir/emails.json"

    formatter = EmailFormatter(path_to_users, date_string, save_dir) 

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

def test_load_user_info(mocker):
    path_to_users = "/path/to/users.csv"
    date_string = "2024-02-01"
    save_dir = "/path/to/save_dir/emails.json"

    formatter = EmailFormatter(path_to_users, date_string, save_dir) 

    mocked_read_csv = MagicMock(return_value=DataFrame())
    mocker.patch('pandas.read_csv', new=mocked_read_csv)

    users = formatter.load_user_info()

    # calls pd read_csv with the path given to EmailFormatter
    mocked_read_csv.assert_called_once() 
    mocked_read_csv.assert_called_with(path_to_users)
    assert isinstance(users, DataFrame)

def test_formatEmails():
    data = {
    'user': ['Alice', 'Bob'],
    'email': ['alice@example.com', 'bob@example.com']
    }

    users = DataFrame(data)

    path_to_users= "/path/to/users.csv"
    date_string = "2024-02-01"
    save_dir = "/path/to/save_dir/emails.json"
    formatter = EmailFormatter(path_to_users, date_string, save_dir) 

    expected_emails = {
        "alice@example.com": "\n2024-02-01\nalice@example.com\n\nDear Alice,\n\nI hope this email finds you well and that your tuna consumption has been satisfactory!\nWe're reaching out to let you know that the warranty on your last can of tuna is about to expire. Yes, that's right, your extended tuna warranty is coming to an end. Don't panic just yet, though! You still have time to renew and ensure your peace of mind when it comes to enjoying delicious tuna meals.",
        "bob@example.com": "\n2024-02-01\nbob@example.com\n\nDear Bob,\n\nI hope this email finds you well and that your tuna consumption has been satisfactory!\nWe're reaching out to let you know that the warranty on your last can of tuna is about to expire. Yes, that's right, your extended tuna warranty is coming to an end. Don't panic just yet, though! You still have time to renew and ensure your peace of mind when it comes to enjoying delicious tuna meals."
    }

    observed_emails = formatter.formatEmails(users)

    assert observed_emails["alice@example.com"] == expected_emails["alice@example.com"] 
    assert observed_emails["bob@example.com"] == expected_emails["bob@example.com"] 
    assert len(observed_emails.keys()) == len(expected_emails.keys())

def test_saveToJSON():

    emails = {
        "alice@example.com": "\n2024-02-01\nalice@example.com\n\nDear Alice,\n\nI hope this email finds you well and that your tuna consumption has been satisfactory!\nWe're reaching out to let you know that the warranty on your last can of tuna is about to expire. Yes, that's right, your extended tuna warranty is coming to an end. Don't panic just yet, though! You still have time to renew and ensure your peace of mind when it comes to enjoying delicious tuna meals.",
        "bob@example.com": "\n2024-02-01\nbob@example.com\n\nDear Bob,\n\nI hope this email finds you well and that your tuna consumption has been satisfactory!\nWe're reaching out to let you know that the warranty on your last can of tuna is about to expire. Yes, that's right, your extended tuna warranty is coming to an end. Don't panic just yet, though! You still have time to renew and ensure your peace of mind when it comes to enjoying delicious tuna meals."
    }   

    tmp_dir = tempfile.TemporaryDirectory()
    path_to_users= "/path/to/users.csv"
    date_string = "2024-02-01"
    save_path = os.path.join(tmp_dir.name, f"{date_string}_emails.json") 
    formatter = EmailFormatter(path_to_users, date_string, save_path) 

    formatter.saveToJSON(emails)

    # it saves a dict to a json file
    expected_file_path = save_path
    assert os.path.exists(expected_file_path) == True, f"{expected_file_path} must exist"

    with open(expected_file_path, 'r') as json_file:
        saved_emails = json.load(json_file)

    assert emails == saved_emails 

    # it overwrites any json file with same name
    new_emails = {
        "bob@example.com": "\n2024-02-01\nbob@example.com\n\nDear Bob,\n\nI hope this email finds you well and that your tuna consumption has been satisfactory!\nWe're reaching out to let you know that the warranty on your last can of tuna is about to expire. Yes, that's right, your extended tuna warranty is coming to an end. Don't panic just yet, though! You still have time to renew and ensure your peace of mind when it comes to enjoying delicious tuna meals."
    }   

    formatter.saveToJSON(new_emails)

    # it saves a dict to a json file
    expected_file_path = save_path
    assert os.path.exists(expected_file_path) == True, f"{expected_file_path} must exist"

    with open(expected_file_path, 'r') as json_file:
        saved_new_emails = json.load(json_file)

    assert new_emails == saved_new_emails 


