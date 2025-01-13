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
    def __init__(self, pop_server, smtp_server, email, password, pop_port = 110, smtp_port=25):
        self.pop_server = pop_server
        self.smtp = smtp_server
        self.email = email
        self.password = password
        self.pop_port = pop_port
        self.smtp_port = smtp_port
        self.pop_conn = None
        self.smtp_conn = None

        #Ruta del archivo SQLite:
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
            conn.commit()
            conn.close()
            print(f"Base de datos inicializada: {self.db_file}")
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")