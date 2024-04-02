import tempfile

def test_checkPath():
    temp_path = tempfile.TemporaryDirectory()
    nonExistentFilePath = "/non/existent/path/"
    existentFilePath = temp_path.name

    # exists with code 1 if path does not exist
    try:
        checkPath(nonExistentFilePath)
    except SystemExit as e:
        assert True 
        assert e.code == 1
    else:
        assert False 

    # does not exist if path exists
    try:
        checkPath(existentFilePath)
    except SystemExit as e:
        assert False
    else:
        assert True

def test_initializeSender():
    ds = "2024-02-01"
    path_to_emails = "/path/to/emails/"
    path_to_logs = "/path/to/logs"

    args = [ds, path_to_emails, path_to_logs]
    sender = initializeSender(args)

    assert isinstance(sender, EmailSender)

    assert sender.ds == ds
    assert sender.path_to_emails == path_to_emails
    assert sender.path_to_logs == path_to_logs

