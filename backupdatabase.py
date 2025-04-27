import os
import time
import shutil
import schedule
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL= os.getenv("RECEIVER_EMAIL")

Folder_goc = 'F:/Databasebackup'
Folder_backup = 'F:/Baitapvn'

def send_email(sender, receiver, subject, body, password):
    try:
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = message.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        print(f"Đã gửi email đến {receiver}")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

def backup_files():
    try:
        thoi_gian = datetime.now().strftime("%Y%m%d")
        so_file_backup = 0

        if not os.path.exists(Folder_backup):
            os.makedirs(Folder_backup)

        for ten_file in os.listdir(Folder_goc):
            if ten_file.endswith(('.sql', '.sqlite3')):
                duong_dan_goc = os.path.join(Folder_goc, ten_file)
                duong_dan_backup = os.path.join(Folder_backup, f"{thoi_gian}_{ten_file}")
                shutil.copy2(duong_dan_goc, duong_dan_backup)
                so_file_backup += 1

        if so_file_backup > 0:
            send_email(SENDER_EMAIL, RECEIVER_EMAIL, "Backup Thành Công", f"Đã backup {so_file_backup} file database vào {Folder_backup}", SENDER_PASSWORD)
        else:
            send_email(SENDER_EMAIL, RECEIVER_EMAIL, " Không Có File Để Backup", "Kiểm tra lại File .sql hoặc .sqlite3 có tồn tại không", SENDER_PASSWORD)
    except Exception:
        send_email(SENDER_EMAIL, RECEIVER_EMAIL, " Backup Thất Bại", f"Đã xảy ra lỗi khi backup", SENDER_PASSWORD)

schedule.every().day.at("10:35").do(backup_files)

print("Đúng 0h sẽ backup database")

while True:
    schedule.run_pending()
    time.sleep(1)