import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_test_email():
    smtp_server = "simmon.jp"
    port = 587  # または適切なポート番号
    sender_email = "saito_kouki@simmon.jp"
    receiver_email = "saito_kouki@simmon.jp"
    password = "aru3BA$8"

    message = MIMEText('This is a test email.', 'plain', 'utf-8')
    message['Subject'] = Header('Test Email', 'utf-8')
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.set_debuglevel(1)  # デバッグ出力を有効化
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_test_email()