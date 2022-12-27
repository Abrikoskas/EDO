from pathlib import Path
import os
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def get_files_list(folder_path):
    return [p for p in Path(folder_path).iterdit() if p.is_file()]


def get_files(folder):
    files = []
    for file in Path(folder).iterdir():
        if file.is_file():
            files.append(file)
    return files


def delete_file(folder, file_name):
    os.remove(os.path.join(folder, file_name))


def send_mail(send_from, send_to, subject, text,
              gmail_user, gmail_password,
              files=None, host='smtp.gmail.com', port=587):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    smtp = smtplib.SMTP(host, port)
    smtp.ehlo()
    smtp.login(gmail_user, gmail_password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
