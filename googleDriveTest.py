from __future__ import print_function

import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials as ServiceAccountCredentials

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
    credentials_key = {
            "type": "service_account",
            "project_id": "pln-luccaki-llsh",
            "private_key_id": "c20631f3c1887ddd68d20bfc743f03e6fc8daed4",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDC5J2obieLpgek\n3UrRN+kDOJ/iAQdbcQx4yOYXXZBv666QgihkbFMnHcu2Rzq4KB+sNT7cJE5FIXYZ\npKp6exuV0PmIEBCdzv65dy2Bdrp7XCv7b3XMp3LAjsuFbed0poaxjMp4HFexYLel\n+EO/1hqaZ9/oBtHFJB2lmsJOz/FvFqEngBscMnZkFu53YbJk4pD+Du4vMcnofihF\nGGwgrI2FVdviJo8iaKrWzJplY/hSPKNyR3mSUlYs/UzWepnv/5e+oGmMR+0gH0wD\n2Q3ArkESxM89uJyIFR+Q81F/+lu5PUyxWlzn5iEAQ8YQewV8QHyhukdKF6Em8AND\nvEB/OBJZAgMBAAECggEABFvw+2FOyyFDajh05mA6ewCtqIaVporxxlONvDxXXtl8\nzxHKNuzPDsDHtvYneDdMY8YaQNVsMi432QYg2pp44jH3G/78kCjDhhNPVkGLcNKi\nPTVWlZxEDmCH1tUtepEtP4H5qV08Wpu9n9STl1tLCC30CSKxV08PoiAwvUZBH3ul\nGO2+B20D5XLBQLCqRBvFG9Ht2zr48ZYazjAHB5Nq3nxtfuD14LaEy/1J4CNijWIr\npccpGxI4tLqcxtJN06VpbpsKQAtMT3plRgJs4Y7TCXIfTiKMlItMSq0zNYvK9Muz\n1X9i3xrN6p4uVjYM5vVbpvKc+ncM15q0OWJaBIl5HQKBgQDl4lJk6S6IJ6DKHT3j\nWIzPyb8erCPgOduTSbP16wCsaxtugdfbZqXuCrmYkQwNiw9W8SqnJHpDCro7IYvq\nLJ9d6isLnC+7o/NinzzvW4R3Q9qVCicxHellLXpGkCcHGjUY+dqSxNzVxFa35EsD\nVfPz5d1VaSQh5XFYTTiyAbooxwKBgQDZCKfeXMwDj7OrDEn2lOxuxSh5D7IlQx9B\n+d/yDNOx3cAU1EPKxLKuY0YzZzJZKsvRfZp1rcF1yklkiTU6fMdmj2R6EMGvBEs3\nSZFo65bPhjYQvc9eDQIXmhMljTo06IQc2ont4K3aSrQhSi7qcljzqTrXGE7BlI3K\ntRjnrUIL3wKBgFMG+OdFaO74ERSulwmjk8gAf6yeU57Khsmdlwe8xtN/I7s33jR5\n0Hg3G21FBetmTDYEiHkxrY7FMxnkNdpwH2cWClH5KSxGPMNj6+gvT5qbwTiPIDSX\nLxLB6CXQLqhcCM1qgEz+GRyD+yYTqBweUSvH27bbcJdlfRh9W3q/MPNFAoGACI6m\nz8Wo5ZsM4nmhkO9eQx/S8LMFuyJiYR+RDOIklqa/pBKaeaw3v1h6tBwliA5/6sqh\nBHLNZe+L5ULjrmKtGgYdWBLBED2DGbL04MYpNBV+nDpfqr2oj3Wru5dN7DgevWSA\ne7iYIjs/zvA12ViY2UKa51A2Crvou01YpgnWyNECgYApf3KLTSLTiq0l1OksXC43\nhAqU5Z6WPTbgHKMBI+XhpxyKEBCOv+rVBK9qsFcOGU424YVYFck6DTkHiKBdrcGR\nGivoAN67pNPSgOQYxb8PM2g3jaUUYGYUhVPAeGhADnLOY2axbgQ5HdVkqp6zkpI4\nU50yaHdlrb9H7gg7InMOMw==\n-----END PRIVATE KEY-----\n",
            "client_email": "pgc-google-drive@pln-luccaki-llsh.iam.gserviceaccount.com",
            "client_id": "105439926672532049788",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pgc-google-drive%40pln-luccaki-llsh.iam.gserviceaccount.com"
        }
    credentials = ServiceAccountCredentials.from_service_account_info(credentials_key)

    try:
        service = build('drive', 'v3', credentials=credentials)

        from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

        ## Create a MediaFileUpload object for the file you want to upload
        #file = open('image.jpeg', 'rb')
        ##fd = io.BytesIO(b"data goes here")
        #media = MediaIoBaseUpload(fd=file, mimetype="application/octet-stream", resumable=True)
#
        ## Insert the file into the specified folder
        #file_metadata = {'name': 'image.jpeg', 'parents':None}
        #file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        #print(F'File ID: {file.get("id")}')

        #1Gx-TbeSkP2fcWSdbeSSFFm1R8OWHUfRG

        from googleapiclient.http import MediaIoBaseDownload

        file_name = 'test_image.jpeg'
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
        #service.files().delete(fileId=file_id).execute()
        #print(f'File with ID: {file_id} was deleted successfully')
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()