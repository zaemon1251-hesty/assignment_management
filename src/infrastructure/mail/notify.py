from typing import Dict, Optional
from src.domain.assignment import Assignment
from src.domain.scheduler import Scheduler
from src.domain.user import User
from src.usecase.driver.NotifyDriver import NotifyDriver
from email.mime.text import MIMEText
import smtplib

# SMTP認証情報
account = "hogehoge@gmail.com"
password = "passpass"

# 送受信先
to_email = "送信先@hoge.com"
from_email = "送信元@gmail.com"

# MIMEの作成
subject = "テストメール"
message = "テストメール"
msg = MIMEText(message, "html")
msg["Subject"] = subject
msg["To"] = to_email
msg["From"] = from_email

# メール送信処理
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(account, password)
server.send_message(msg)
server.quit()


class NotifyDriverImpl(NotifyDriver):
    """ notify using mail """

    def __init__(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)

    async def notify(self, user: User, schedule: Scheduler, assignemt: Assignment) -> Optional[Dict]:
        pass
