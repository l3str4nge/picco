from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

"""
    Generate your credentials from Google Api Tutorial
    link: https://developers.google.com/drive/api/v3/quickstart/python


    Note: put your own path's for CREDENTIALS AND TOKEN
"""
CREDENTIALS_PATH = '/home/zawadeusz/credentials.json'
TOKEN_PATH = '/home/zawadeusz/token.json'

SCOPES_FULL_AUTH = 'https://www.googleapis.com/auth/drive'
SCOPES_READ_ONLY = 'https://www.googleapis.com/auth/drive.metadata.readonly'

""" MIMETYPES """
MIMETYPE_ZIP = 'application/zip'

class Uploader:
    def __init__(self, scope):
        self.service = self.authorize(scope)

    def authorize(self, scope):
        store = file.Storage(TOKEN_PATH)
        creds = store.get()

        if not creds or creds.invalid :
            flow = client.flow_from_clientsecrets(CREDENTIALS_PATH, scope)
            flags = tools.argparser.parse_args([])
            creds = tools.run_flow(flow, store, flags)

        service = build('drive', 'v3', http=creds.authorize(Http()))
        return service

    def upload_file(self, path, name, mimetype):
        metadata = {'name': name}
        media = MediaFileUpload(path, mimetype)

        uploaded = self.service.files().create(
                body=metadata, media_body=media, fields='id').execute()

        if not uploaded:
            return False

        return True

