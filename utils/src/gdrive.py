from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def renameFile(drive, fileId, newTitle):
    a = drive.auth.service.files().get(fileId=id).execute()
    a["title"] = newTitle
    update = drive.auth.service.files().update(fileId=id, body=a).execute()
    return update
