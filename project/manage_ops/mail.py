#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import smtplib
import time
from email.message import Message
from time import sleep
import email.utils
import sys

class mysendmail(threading.Thread):
    def __init__(self, address,sub,content):
        threading.Thread.__init__(self)
        self.address = address
        self.sub = sub
        self.content = content




    def run(self):
        address = self.address
        sub = self.sub
        content = self.content
        mail_from = 'ops@wexin.com'
        smtpserver = 'smtp.exmail.qq.com'
        user = 'ops@wexin.com'
        pwd = 'wexin.com'
        t = email.utils.formatdate(time.time(), True)
        message = Message()
        message['Subject'] = sub
        message['From'] = mail_from
        message['To'] = address
        message.set_payload(content + "\n\n\n" + "系统程序发送, 不要回复此邮件 www.linuxqq.net")
        msg = message.as_string()
        sm = smtplib.SMTP(smtpserver, port=25, timeout=20)
        sm.set_debuglevel(1)
        sm.ehlo()
        sm.ehlo()
        sm.login(user, pwd)
        sm.sendmail(mail_from, address, msg)
        sm.quit()


