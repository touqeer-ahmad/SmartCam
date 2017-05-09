import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

def email(email_address):
    to = email_address # Email to send to
    gmail_user = 'Email' # Email to send from (MUST BE GMAIL)
    gmail_password = 'password' # Google App Password
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use

    smtpserver.ehlo()  # Says 'hello' to the server
    smtpserver.starttls()  # Start TLS encryption
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)  # Log in to server
    today = datetime.date.today()  # Get current time/date

    # Creates a sentence for each ip address.
    text = 'Door got open on %s' % today.strftime('%b %d %Y')
    #my_ip_b = 'Your %s ip is %s' % (ip_type_b, ipaddr_b)

    # Creates the text, subject, 'from', and 'to' of the message.
    #msg = MIMEText(my_ip_a + "\n" + my_ip_b)
    msg = MIMEText(text)
    msg['Subject'] = 'Smart Camera Controller Notification %s' % today.strftime('%b %d %Y')
    msg['From'] = gmail_user
    msg['To'] = to
    # Sends the message
    smtpserver.sendmail(gmail_user, [to], msg.as_string())
    # Closes the smtp server.
    smtpserver.quit()
