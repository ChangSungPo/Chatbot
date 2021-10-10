# !/usr/bin/python 
# -*-coding:utf-8 -*-
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(totx,subjecttx,bodytx):

    msg = MIMEMultipart()
    msg['From'] = os.environ['email_account']
    msg['To'] = totx
    msg['Subject'] = subjecttx
    msg.attach(MIMEText(bodytx, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(os.environ['email_account'], os.environ['password'])
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("a email sent.")
    except:
        print("something wrong!\n")
        print("sent:"+ msg.as_string())

