import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


class Email_Sender:
    def __init__(self, send_from, send_to, send_to_cc, subject, text, server, port):
        msg = MIMEMultipart()
        msg["From"] = send_from
        msg["To"] = send_to
        msg["Cc"] = send_to_cc
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject
        msg.attach(MIMEText(text))

        # part = MIMEBase("application", "octet-stream")
        # part.set_payload(open("Query OPD Data.xlsx", "rb").read())
        # encoders.encode_base64(part)
        # part.add_header(
        #     "Content-Disposition", 'attachment; filename="Query OPD Data.xlsx"'
        # )
        # msg.attach(part)

        # context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        # SSL connection only working on Python 3+
        smtp = smtplib.SMTP(server, port)
        smtp.sendmail(send_from, [send_to, send_to_cc], msg.as_string())
        smtp.quit()


if __name__ == "__main__":
    send_email = Email_Sender(
        "Sarika Jadhav <sarika.jadhav@kokilabenhospitals.com>",
        "kdahpfs@gmail.com",
        "sarika.jadhav@kokilabenhospitals.com",
        "OPD Data via API",
        "",
        "172.20.200.29",
        25,
    )
