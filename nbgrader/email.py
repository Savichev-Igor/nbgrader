import logging
import smtplib

from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from os.path import basename

from nbgrader import config

logger = logging.getLogger(__name__)


def send_email(subject, text, send_to, files):
    msg = MIMEMultipart()
    msg["From"] = config.EMAIL_FROM
    msg["To"] = ", ".join(send_to)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)

    if text:
        msg.attach(MIMEText(text))

    for f in files or []:
        try:
            with open(f, "rb") as file:
                part = MIMEApplication(file.read(), Name=basename(f))

            part.add_header('Content-Disposition', 'attachment', filename=basename(f))
            msg.attach(part)
        except IOError:
            logger.warning("Error opening attachment file {}".format(f))

    server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_HOST_USER, config.EMAIL_HOST_PASSWORD)

    server.sendmail(config.EMAIL_FROM, send_to, msg.as_string())

    logger.info("Letter was sent to {}".format(", ".join(send_to)))

    server.quit()
