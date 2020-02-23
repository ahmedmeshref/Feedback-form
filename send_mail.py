import smtplib
from email.mime.text import MIMEText


def send_email(customer, dealer, rating, comments, email):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'd06be1a416919e'
    password = 'b12cda0164818f'
    message = f"<h3> New Feedback Submission</h3>" \
              f"<ul><li>Customer: {customer}</li>" \
              f"<li>Dealer: {dealer}</li>" \
              f"<li>Rating: {rating}</li>" \
              f"<li>Comments: {comments}</li></ul>"

    sender_email = "a.meshref@alustudent.com"
    receiver_email = email
    msg = MIMEText(message, 'html')
    msg['Subject'] = "Feedback"
    msg['From'] = sender_email
    msg['to'] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
