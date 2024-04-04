import tempfile
import os
from images.emailSender.scripts.send_emails import checkPath, initializeSender, EmailSender

def test_checkPath():
    temp_path = tempfile.TemporaryDirectory()
    temp_file = tempfile.NamedTemporaryFile()
    nonExistentPath = "/non/existent/path/"
    existentPath = temp_path.name
    nonExistentFilePath = "/non/existent/file/this.json"
    existentFilePath = temp_file.name 

    # exists with code 1 if path or file does not exist
    try:
        checkPath(nonExistentPath)
    except SystemExit as e:
        assert True 
        assert e.code == 1
    else:
        assert False 

    try:
        checkPath(nonExistentFilePath)
    except SystemExit as e:
        assert True 
        assert e.code == 1
    else:
        assert False 

    # does not exist if path exists
    try:
        checkPath(existentPath)
    except SystemExit as e:
        assert False
    else:
        assert True

    try:
        checkPath(existentFilePath)
    except SystemExit as e:
        assert False
    else:
        assert True

def test_initializeSender():
    ds = "2024-02-01"
    path_to_emails = "/path/to/emails"
    path_to_logs = "/path/to/logs"

    args = [ds, path_to_emails, path_to_logs]
    sender = initializeSender(args)

    # returns an instance of EmailSender
    assert isinstance(sender, EmailSender)

    assert sender.ds == ds
    assert sender.path_to_emails == path_to_emails
    assert sender.path_to_logs == path_to_logs

def test_run_1(mocker):
    temp_path = tempfile.TemporaryDirectory()

    ds = "2024-02-01"
    expected_log_path = temp_path.name + f"/{ds}_logs.log"
    path_to_logs = temp_path.name
    path_to_emails = "/path/to/emails"

    sender = EmailSender(ds, path_to_emails, path_to_logs)
    mock_load_emails = mocker.patch.object(sender, 'load_emails')
    mock_send_emails = mocker.patch.object(sender, 'send_emails')

    sender.run()

    mock_load_emails.assert_called_once()
    mock_send_emails.assert_called_once()

    # outputs a log file with format ds_logs.log
    assert os.path.exists(expected_log_path) == True