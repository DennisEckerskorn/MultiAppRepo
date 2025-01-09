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

    def fetch_unread_count(self):
        """Obtener el número de correos no leidos"""
        self.imap_conn.select("INBOX")
        status, response = self.imap_conn.search(None, "UNSEEN")
        return len(response[0].split())

    def list_emails(self, limit=10):
        """Lista de correos más recientes"""
        self.imap_conn.select("INBOX")
        status, response = self.imap_conn.search(None, "ALL")
        email_ids = response[0].split()[-limit:]
        emails = []
        for email_id in email_ids:
            status, msg_data = self.imap_conn.fetch(email_id, "(RFC822)")
            emails.append(msg_data[0][1].decode("utf-8"))
        return emails

    def send_mail(self, to_address, subject, body):
        """Permite enviar un correo electronico"""
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        self.smtp_conn.sendmail(self.email, to_address, msg.as_string())

    def close_connections(self):
        """Cierra las conexiones IMAP y SMTP"""
        if self.imap_conn:
            self.imap_conn.logout()
        if self.smtp_conn:
            self.smtp_conn.quit()
