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

SENDER_EMAI = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL= os.getenv("RECEIVER_EMAIL")

Folder_goc = r'F:/Databasebackup' 
Folder_backup = r'F:/Baitapvn'

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
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        so_file_backup = 0

        if not os.path.exists(Folder_backup):
            os.makedirs(Folder_backup)

        for ten_file in os.listdir(Folder_goc):
            if ten_file.endswith(".sql") or ten_file.endswith(".sqlite3"):
                duong_dan_nguon = os.path.join(Folder_goc, ten_file)
                ten_file_backup = f"{thoi_gian}_{ten_file}"
                duong_dan_backup = os.path.join(Folder_backup, ten_file_backup)

                shutil.copy2(duong_dan_nguon, duong_dan_backup)
                so_file_backup += 1

        if so_file_backup > 0:
            send_email(SENDER_EMAI, RECEIVER_EMAIL, "Backup Thành Công",
                      f"Đã sao lưu {so_file_backup} file database vào {Folder_backup}", SENDER_PASSWORD)
        else:
            send_email(SENDER_EMAI, RECEIVER_EMAIL, " Không Có File Để Backup",
                      "Không tìm thấy file .sql hoặc .sqlite3 trong thư mục nguồn", SENDER_PASSWORD)
    except Exception as loi:
        send_email(SENDER_EMAI, RECEIVER_EMAIL, " Backup Thất Bại",
                  f"Lỗi khi backup: {loi}", SENDER_PASSWORD)

schedule.every().day.at("09:21").do(backup_files)

print("⏰ Đang chờ đến 00:00 để backup database...")

while True:
    schedule.run_pending()
    time.sleep(1)