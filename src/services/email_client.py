import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import message_from_bytes
from email.header import decode_header

class EmailClient:
    def __init__(self, imap_server, smtp_server, email, password, imap_port=143, smtp_port=25):
        self.imap_server = imap_server
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
        self.imap_port = imap_port
        self.smtp_port = smtp_port
        self.imap_conn = None
        self.smtp_conn = None


    def connect_imap(self):
        """Conexión del servidor IMAP"""
        try:
            self.imap_conn = imaplib.IMAP4(self.imap_server, self.imap_port)
            self.imap_conn.login(self.email, self.password)
            print("Conexión IMAP exitosa")
        except Exception as e:
            print(f"Erro al conectar al servidor IMAP: {e}")
            self.imap_conn = None

    def connect_smtp(self):
        """Conexión del servidor SMTP"""
        try:
            self.smtp_conn = smtplib.SMTP(self.smtp_server, self.smtp_port)
            #self.smtp_conn.starttls()
            self.smtp_conn.login(self.email, self.password)
            print("Conexión SMTP exitosa")
        except Exception as e:
            print(f"Error al conectar al servidor SMTP: {e}")
            self.smtp_conn = None

    def is_connected(self):
        """Verifica si hay una conexión valida tanto de IMAP como de SMTP"""
        return self.imap_conn is not None and self.smtp_conn is not None

    def reconnect(self):
        """Intenta reconectar a los servidores IMAP y SMTP"""
        print("Intentando reconectar al servidor de correo...")
        self.connect_imap()
        self.connect_smtp()

    def fetch_unread_count(self):
        """Obtener el número de correos no leidos"""
        self.imap_conn.select("INBOX")
        status, response = self.imap_conn.search(None, "UNSEEN")
        return len(response[0].split())

    def fetch_folders(self):
        """Obtiene la lista de carpetas disponibles en el servidor"""
        status, folders = self.imap_conn.list()
        if status == "OK":
            return [folder.decode().split(' "/" ')[-1] for folder in folders]
        return []

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
