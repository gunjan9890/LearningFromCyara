from __future__ import print_function

import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = 'D:\\SpearlineQA\\playwirght_repo\\spearline_qa_automation\\token.json'
    credential_path = 'D:\\SpearlineQA\\playwirght_repo\\spearline_qa_automation\\credential.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service: Resource = build('gmail', 'v1', credentials=creds)
        service.users().labels()
        print(type(service.users()))
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        # print('Labels:')
        # for label in labels:
        #     print(label['name'])

        msg_list = service.users().messages().list(userId='me', q='Top Level Layered Report 001', includeSpamTrash=True).execute()
        print(msg_list['messages'][0]['id'])
        msg = service.users().messages().get(userId='me', id=msg_list['messages'][0]['id']).execute()
        data_set = msg['payload']['parts']
        print(len(data_set))
        data = msg['payload']['parts'][0]['body']['data']
        print(base64.b64decode(data))
        attachment = msg['payload']['parts'][1]['body']
        fname = msg['payload']['parts'][1]['filename']
        print(fname)
        attachment_id = (attachment['attachmentId'])

        attachment_obj = service.users().messages().attachments().get(userId='me', messageId=msg_list['messages'][0]['id'], id=attachment_id).execute()
        decoded_txt = base64.urlsafe_b64decode(attachment_obj['data'])
        with open(f'D:\\SpearlineQA\\{fname}','wb') as f:
            f.write(decoded_txt)


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()