import email
import tempfile
import os
from unittest import mock
from images.emailSender.scripts.send_emails import checkPath, initializeSender, EmailSender
from unittest.mock import call

def test_checkPath(mocker):
    temp_path = tempfile.TemporaryDirectory()
    nonExistentPath = "/non/existent/path/"
    existentPath = temp_path.name

    # exists with code 1 if path or file does not exist
    mock_loggingError = mocker.patch("logging.error")
    mock_sysExit = mocker.patch("sys.exit")
        
    checkPath(nonExistentPath)
    mock_loggingError.assert_called_once_with(f"Path {nonExistentPath} does not exit, ending program")
    mock_sysExit.assert_called_once_with(1)

    checkPath(existentPath)
    mock_loggingError.assert_called()
    mock_sysExit.assert_called()


def test_initializeSender(mocker):
    ds = "2024-02-01"
    path_to_emails = "/path/to/emails.json"
    path_to_logs = "/path/to/logs.log"

    checkPath_importPath = "images.emailSender.scripts.send_emails.checkPath" 
    mocker.patch(checkPath_importPath)

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
    path_to_logs = temp_path.name + f"/{ds}_logs.log"
    path_to_emails = "/path/to/emails.json"

    sender = EmailSender(ds, path_to_emails, path_to_logs)
    mock_load_emails = mocker.patch.object(sender, 'load_emails')
    mock_send_emails = mocker.patch.object(sender, 'send_emails')

    sender.run()

    mock_load_emails.assert_called_once()
    mock_send_emails.assert_called_once()

    # outputs a log file with format ds_logs.log
    assert os.path.exists(expected_log_path) == True

def test_load_emails(mocker):
    temp_dir = tempfile.TemporaryDirectory()

    ds = "2024-02-01"
    path_to_emails = os.path.join(temp_dir.name, f"{ds}_emails.json") 
    path_to_logs = f"path/to/{ds}_logs.log"

    f = open(path_to_emails, "w")

    try:
        expected_emails = {
            "email1": "email message",
            "email2": "email message"
        }
        mock_jsonLoad = mocker.patch('json.loads', return_value = expected_emails)

        sender = EmailSender(ds, path_to_emails, path_to_logs)
        emails = sender.load_emails()

        assert isinstance(emails, dict)
    finally:
        f.close()
    
def test_send_emails(mocker):
    ds = "2024-02-01"
    path_to_logs = "path/to/logs.log"
    path_to_emails = "/path/to/emails.json"

    sender = EmailSender(ds, path_to_emails, path_to_logs)    

    user1 = "user1@email.com"
    user2 = "user2@email.com"
    message = "email message",
    emails = {
        user1: message,
        user2: message
    }

    mock_logging = mocker.patch('logging.info')

    sender.send_emails(emails)

    assert mock_logging.call_args_list == [call(f"Sent email to {user1}"), call(f"Sent email to {user2}")]
    assert mock_logging.call_count == 2