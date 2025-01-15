import os
import poplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime


class EmailClientPOP:
    def __init__(self, pop_server, smtp_server, email, password, pop_port=110, smtp_port=25):
        self.pop_server = pop_server
        self.smtp_server = smtp_server
        self.email = email
        self.password = password
        self.pop_port = pop_port
        self.smtp_port = smtp_port
        self.pop_conn = None
        self.smtp_conn = None
        self.running = True

        # Ruta del archivo SQLite:
        self.db_file = os.path.join("resources/db_email", "emails.db")
        self.init_database()

    def init_database(self):
        db_folder = os.path.dirname(self.db_file)
        if not os.path.exists(db_folder):
            os.makedirs(db_folder, exist_ok=True)
            print(f"Carpeta creada: {db_folder}")
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    subject TEXT,
                    body TEXT,
                    received_at DATETIME
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sent_emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient TEXT NOT NULL,
                    subject TEXT,
                    body TEXT,
                    sent_at DATETIME
                )
            """)
            conn.commit()
            conn.close()
            print(f"Base de datos inicializada: {self.db_file}")
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")

    def connect_pop(self):
        """Conexión al servidor POP"""
        try:
            self.pop_conn = poplib.POP3(self.pop_server, self.pop_port, timeout=10)
            self.pop_conn.user(self.email)
            self.pop_conn.pass_(self.password)
            print("Conexión POP exitosa")
        except Exception as e:
            print(f"Error al conectar al servidor POP: {e}")
            self.pop_conn = None

    def connect_smtp(self):
        """Conexión al servidor SMTP"""
        try:
            self.smtp_conn = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10)
            self.smtp_conn.login(self.email, self.password)
            print("Conexión SMTP exitosa")
        except Exception as e:
            print(f"Error al conectar al servidor SMTP: {e}")
            self.smtp_conn = None

    def is_connected(self):
        """Verifica si hay una conexión válida tanto de POP como de SMTP"""
        return self.pop_conn is not None and self.smtp_conn is not None

    def reconnect(self):
        """Intenta reconectar a los servidores POP y SMTP"""
        print("Intentando reconectar al servidor de correo...")
        if not self.running:
            return
        if self.pop_conn is None:
            self.connect_pop()
        if self.smtp_conn is None:
            self.connect_smtp()

    def fetch_unread_count(self):
        """Obtener el número de correos (POP3 no distingue entre leídos y no leídos)"""
        try:
            if not self.pop_conn:
                self.connect_pop()
            num_messages = len(self.pop_conn.list()[1])
            return num_messages  # Total de mensajes
        except Exception as e:
            print(f"Error al obtener el conteo de correos: {e}")
            return 0

    def fetch_emails(self, save_to_db=True):
        """Obtiene correos desde el servidor POP"""
        try:
            if not self.pop_conn:
                self.connect_pop()

            emails = []
            num_messages = len(self.pop_conn.list()[1])
            for i in range(1, num_messages + 1):
                raw_messages = b"\n".join(self.pop_conn.retr(i)[1])
                msg = email.message_from_bytes(raw_messages)
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                sender = msg.get("From")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                email_data = {
                    "sender": sender,
                    "subject": subject,
                    "body": body,
                    "received_at": datetime.now().isoformat()
                }
                emails.append(email_data)

                if save_to_db:
                    self.save_email_to_db(email_data)

            return emails
        except Exception as e:
            print(f"Error al obtener los correos: {e}")
            return []

    def fetch_folders(self):
        """POP3 no tiene carpetas, devuelve un mensaje indicando esto"""
        print("El protocolo POP3 no soporta carpetas. Devuelve solo la bandeja de entrada.")
        return ["INBOX"]

    def save_email_to_db(self, email_data):
        """Guarda un correo recibido en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO emails (sender, subject, body, received_at)
                VALUES (?, ?, ?, ?)
            """, (email_data["sender"], email_data["subject"], email_data["body"], email_data["received_at"]))
            conn.commit()
            conn.close()
            print("Correo recibido guardado en la base de datos.")
        except sqlite3.Error as e:
            print(f"Error al guardar correo recibido: {e}")

    def send_mail(self, recipient, subject, body, save_to_db=True):
        """Envía un correo usando SMTP"""
        try:
            if not self.smtp_conn:
                self.connect_smtp()

            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            self.smtp_conn.sendmail(self.email, recipient, msg.as_string())
            print(f"Correo ha sido enviado a {recipient}")

            if save_to_db:
                self.save_sent_mail_to_db({
                    "recipient": recipient,
                    "subject": subject,
                    "body": body,
                    "sent_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Error al enviar correo: {e}")

    def save_sent_mail_to_db(self, email_data):
        """Guarda un correo enviado en la base de datos."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sent_emails (recipient, subject, body, sent_at)
                VALUES (?, ?, ?, ?)
            """, (email_data["recipient"], email_data["subject"], email_data["body"], email_data["sent_at"]))
            conn.commit()
            conn.close()
            print("Correo enviado guardado en la base de datos.")
        except sqlite3.Error as e:
            print(f"Error al guardar correo enviado: {e}")

    def list_emails(self, limit=10):
        """Lista correos recientes (máximo `limit`)"""
        emails = self.fetch_emails()
        return emails[:limit]

    def close_connections(self):
        """Cierra las conexiones POP y SMTP"""
        try:
            if self.pop_conn:
                self.pop_conn.quit()
                self.pop_conn = None
                print("Conexión POP cerrada.")
        except Exception as e:
            print(f"Error al cerrar conexión POP: {e}")

        try:
            if self.smtp_conn:
                self.smtp_conn.quit()
                self.smtp_conn = None
                print("Conexión SMTP cerrada.")
        except Exception as e:
            print(f"Error al cerrar conexión SMTP: {e}")
