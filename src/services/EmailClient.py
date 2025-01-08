import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailClient:
    def __init__(self, imap_server, smtp_server, email, password, imap_port=993, smtp_port=587):
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
        self.imap_port = imap_port
        self.smtp_port = smtp_port
        self.imap_conn = None
        self.smtp_conn = None
        self.connect_imap()
        self.connect_smtp()

    def connect_imap(self):
        """Conexión del servidor IMAP"""
        self.imap_conn = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        self.imap_conn.login(self.email, self.password)

    def connect_smtp(self):
        """Conexión del servidor SMTP"""
        self.smtp_conn = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.smtp_conn.starttls()
        self.smtp_conn.login(self.email, self.password)


