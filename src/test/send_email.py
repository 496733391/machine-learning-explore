#! /usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '496733391@qq.com'  # 发件人邮箱账号
my_pass = 'tfqyucjemdpvcabc'  # 发件人邮箱密码
my_user = '496733391@qq.com'  # 收件人邮箱账号

msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
msg['From'] = formataddr(("private_test", my_sender))  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
msg['To'] = formataddr(("private_test", my_user))  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
msg['Subject'] = "发送邮件测试"  # 邮件的主题，标题

server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口
server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
server.sendmail(my_sender, [my_user], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
server.quit()  # 关闭连接
