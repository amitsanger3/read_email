#!/usr/bin/env python
# coding: utf-8

# In[2]:


import imaplib, email
from bs4 import BeautifulSoup
import smtplib, ssl


# In[3]:


class Read_Email(object):
    """
    Read gmail emails and fetch useful data
    from it by using beautiful soup. 
    """
    
    def __init__(self, username, password):
        """
        username = Your gmail id if full. for e.g., 
            example@gmail.com
            
        password = password of your gmail id.
            Note: its case sensitive
        """
        
        self.user = username
        self.pwd = password
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        
        
    def server_connection(self):
        """
        Establish connections to gamil server
        and return server connection.
        """
        
        server = imaplib.IMAP4_SSL("imap.gmail.com")
        server.login(self.user, self.pwd)
        print("Connection establish")
        
        return server
    
    
    def inbox_mails(self):
        """
        Go into the gmail's inbox(default) and read all mails
        and return inbox's mails ids list.
        """
        
        msr = self.server_connection()
        msr.select("INBOX") # Selecting inbox: can select any other folder from gmail
        print("I m in inbox")
        # data: is a set of all emails number in a specific binary number
        result, data = msr.uid('search', None, 'ALL')
        print("I got email binary dataset")
        # inbox_item_list: carries latest 5 new email's binary numbers from inbox in a list
        inbox_item_list = data[0].split()
        print("I got latest 5 email binary numbers")
        
        return inbox_item_list
    
    
    def email_message(self, email_id):
        """
        Go into perticular email and fetch its raw data and
        decode it readable utf-8 form to perform further
        functions.
        
        email_id = unique_id of email
        
        return string form of email message
        """
        
        result, data = msr.uid('fetch', email_id, '(RFC822)')
        raw_data = data[0][1].decode('utf-8')
        email_msg = email.message_from_string(raw_data)
        
        return email_msg
    
    
    def email_html(self, email_msg):
        """
        Convert string form of email message to BeautifulSoup
        object to get useful data.
        
        return BeautifulSoup object to soup further
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
        
        receiver_email = to whome you want to send email
        subject = subject of email
        message = message body of email
        """
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server2:
            server2.login(self.user, self.pwd)
            server.sendmail(self.user, receiver_email, subject+message)
    
    
    def __str__(self):
        return self.user +' with password '+ self.pwd


# In[ ]:




