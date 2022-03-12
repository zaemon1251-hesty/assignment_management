from src.settings import logger
from datetime import datetime
import os
from typing import Dict, Optional
from src.domain.assignment import ASSIGNMENT_STATE, Assignment
from src.domain.scheduler import Scheduler
from src.domain.submission import SUBMISSION_STATE
from src.domain.user import User
from src.usecase.driver.NotifyDriver import NotifyDriver
from email.mime.text import MIMEText
import smtplib

# SMTP認証情報


class NotifyDriverImpl(NotifyDriver):
    """ notify using mail """

    def __init__(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.account = os.getenv("GMAIL_ACCOUNT")
        self.password = os.getenv("GMAIL_PASSWORD")

    async def notify(self, user: User, assignemt: Assignment, state: SUBMISSION_STATE) -> None:
        subject = self.create_subject(assignemt.title)
        message = self.create_message(
            user.name,
            assignemt.title,
            assignemt.end_at,
            state
        )
        msg = MIMEText(message, "html")
        msg["Subject"] = subject
        msg["To"] = user.email
        msg["From"] = self.account

        self.server.starttls()
        self.server.login(self.account, self.password)
        err = self.server.send_message(msg)
        self.server.quit()
        logger.info(err)

    def create_subject(self, assignment_title: str) -> str:
        return "{} のお知らせです。".format(assignment_title)

    def create_message(
            self,
            name: str,
            assignment_title: str,
            end_at: datetime,
            state: SUBMISSION_STATE) -> str:
        msg = "[{}]".format(state.name)
        msg = "\n" + "{} さん、".format(name)
        msg = "\n" + "{} の期限が近づいています.".format(assignment_title)
        msg = "\n" + "終了日は, {} です.".format(end_at)
        return msg
