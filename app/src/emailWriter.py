import base64
import os
from email.mime.text import MIMEText
from oauth2client.client import AccessTokenCredentials
from googleapiclient.discovery import build
from oauth2client import client, tools
from oauth2client.file import Storage

import app.src.config

USER_AGENT = "LabSupport"

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class EmailWriter:

    def __init__(self, settings):

        self.CLIENT_SCERET_PATH = settings.settings[app.src.config.PATH_TO_CLIENT_SECRET]
        self.settings = settings
        store = Storage(os.path.join(self.settings.settings[app.src.config.MAIL_ACCOUNT_CREDS]))
        credentials = store.get()
        self.credentials = credentials

    def auth(self):
        return build('gmail', 'v1', credentials=self.credentials)

    def send_message(self, message):
        message = (self.auth().users().messages().send(userId="me", body=message).execute())

    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {"raw": base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    def send_message_with_link(self, address, link):
        message_file = self.settings.settings[app.src.config.INVITE_MSG_BODY]
        with open(message_file) as f:
            message_body = f.read()
        message_text = message_body + link
        message = self.create_message("labsupportcs", address, 'LAB SUPPORT', message_text)
        self.send_message(message)

    def authorize_new_account(self):
        store = Storage(os.path.join(self.settings.settings[app.src.config.MAIL_ACCOUNT_CREDS]))
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.CLIENT_SCERET_PATH,
                SCOPES)
            flow.user_agent = USER_AGENT
            credentials = tools.run_flow(flow, store)


if __name__ == '__main__':
    _store = Storage(os.path.join('../credentials/mail_account_secret.json'))
    _credentials = _store.get()
    if not _credentials or _credentials.invalid:
        flow = client.flow_from_clientsecrets(
            '../credentials/client_secret_637398666132-j8s19q7egap0u79l894jmuhauiv39ec7.apps.googleusercontent.com.json',
            ['https://www.googleapis.com/auth/gmail.send'])
        flow.user_agent = "LabSupport"
        _credentials = tools.run_flow(flow, _store)
    flow = AccessTokenCredentials('../credentials/mail_account_secret.json',
                                  ['https://www.googleapis.com/auth/gmail.send'])
    # creds = ServiceAccountCredentials.from_json_keyfile_name('.gmail-api.json', ['https://www.googleapis.com/auth/gmail.send'])
    # creds = flow.run_local_server(port=0)
    # mail = EmailWriter(credentials)
    # mail.send_message(
    #     mail.create_message("labsupport@cs.huji.ac.il", "avinoam.hershler@mail.huji.ac.il", "TEST", "TEST"))
