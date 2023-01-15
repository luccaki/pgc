from __future__ import print_function

import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        from googleapiclient.http import MediaFileUpload

        # Create a MediaFileUpload object for the file you want to upload
        #file = open('image.jpeg', 'rb')
        #media = MediaFileUpload('image.jpeg', mimetype='image/jpeg')
#
        ## Insert the file into the specified folder
        #file_metadata = {'name': 'image.jpeg', 'parents':None}
        #file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        #print(F'File ID: {file.get("id")}')

        #1Gx-TbeSkP2fcWSdbeSSFFm1R8OWHUfRG

        from googleapiclient.http import MediaIoBaseDownload

        file_name = 'image.jpeg'
        file_id = ''
        query =  f"name='{file_name}'"

        results = service.files().list(q=query,fields="nextPageToken, files(id, name)").execute()
        items = results.get("files", [])

        # Iterate through the files and print the ID of the desired file
        for item in items:
            if item['name'] == file_name:
                print(item['id'])
                file_id = item['id']

        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

        with open(f"/home/luccaki/Desktop/pgc/{file_name}", "wb") as f:
            fh.seek(0)
            f.write(fh.read())

        #delete file
        service.files().delete(fileId=file_id).execute()
        print(f'File with ID: {file_id} was deleted successfully')
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()