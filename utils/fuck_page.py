import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = "1224228537"
receivers = ["2533916647@qq.com",]

message = MIMEText('aaaa','plain','utf-8')
message['From'] = Header('from mxt','utf-8')
message['To'] = Header('ceshibiaoti','utf-8')

subject = '1111111111'
message['Subject'] = Header(subject,'utf-8')

# try:
smtpObj = smtplib.SMTP()
smtpObj.connect('smtp.qq.com',25)
print(11111111111)
smtpObj.login(sender,'18235148793a')
print(11111111111)
smtpObj.sendmail(sender,receivers,message.as_string())
smtpObj.quit()
# except smtplib.SMTPException as e:
#     print(e)
