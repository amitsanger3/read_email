import imaplib, email
from bs4 import BeautifulSoup
import smtplib, ssl
# for today's date check
from dateutil.parser import parse
import datetime


class Read_Email(object):
    """
    Read gmail's emails and fetch useful data
    from it by using beautiful soup.
    """

    def __init__(self, username, password):
        """
        Initialize with username & password.

        :param username: Your gmail id if full. for e.g.,
            example@gmail.com
        :param password: password of your gmail id.
            Note: its case sensitive
        """

        self.user = username
        self.pwd = password
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.server = None

    def get_server(self):
        """
        Get recently connecting server. If not connecting
        its return None.

        :return: server connection
        """
        return self.server

    def server_connection(self):
        """
        Establish connections to gamil server
        and return server connection.

        :return: server connection
        """
        server = imaplib.IMAP4_SSL("imap.gmail.com")
        server.login(self.user, self.pwd)
        self.server = server
        print("Connection establish")

        return server

    def inbox_mails(self):
        """
        Go into the gmail's inbox(default) and read all mails
        and return inbox's mails ids list.

        :return: Inbox's mails ids list.
        """
        msr = self.get_server()
        msr.select("INBOX")  # Selecting inbox: can select any other folder from gmail
        print("I m in inbox")
        # data: is a set of all emails number in a specific binary number
        result, data = msr.uid('search', None, 'ALL')
        print("I got email binary dataset")
        # inbox_item_list: carries latest 5 new email's binary numbers from inbox in a list
        inbox_item_list = data[0].split()
        print("I got latest 5 email binary numbers")

        return inbox_item_list

    def email_message(self, email_uid):
        """
        Go into particular email and fetch its raw data and
        decode it readable utf-8 form to perform further
        functions.

        :param email_uid: unique_id of email

        :return: string form of email message
        """
        msr = self.get_server()
        result, data = msr.uid('fetch', email_uid, '(RFC822)')
        raw_data = data[0][1].decode('utf-8')
        email_msg = email.message_from_string(raw_data)

        return email_msg

    def email_from(self, email_msg):
        """
        Sender of email

        :param email_msg: string form of email message

        :return: string of sender's email id
        """
        email_from = email_msg['From']
        m = email_from.find('<')
        n = email_from.find('>')

        return email_from[m + 1:n]

    def email_date(self, email_msg):
        """
        date of email

        :param email_msg: string form of email message

        :return: datetime object of email's date
        """
        email_date = email_msg['Date'][:-5]

        return parse(email_date).date()

    def email_msg_id(self, email_msg):
        """
        Message-ID of email

        :param email_msg: string form of email message

        :return: string of email's Message-ID
        """
        email_id = email_msg['Message-ID']
        m = email_id.find('<')
        n = email_id.find('>')

        return email_id[m + 1:n]

    def email_html(self, email_msg):
        """
        Convert string form of email message to BeautifulSoup
        object to get useful data.

        :param email_msg: string form of email message

        :return: BeautifulSoup object to soup further
        """
        for part in email_msg.walk():

            if part.get_content_maintype() == "multipart":
                continue
            content_type = part.get_content_type()

            if 'html' in content_type:
                html_content = part.get_payload()
                soup = BeautifulSoup(html_content, 'html.parser')

        return soup

    def send_email(self, receiver_email, subject, message):
        """
        Send simple text email

        :param receiver_email: to whom you want to send email
        :param subject: subject of email
        :param message: message body of email

        :return: None
        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server2:
            server2.login(self.user, self.pwd)
            server.sendmail(self.user, receiver_email, subject + message)

        return None

    def __str__(self):
        return self.user + ' with password ' + self.pwd



