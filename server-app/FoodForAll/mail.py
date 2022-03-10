#coding: utf-8
import os
import sys
import argparse
import configparser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class mail(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.getenv("apex_server_config"))
        pass

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--subject", dest='subject', type=str, required=True, help="Subject(Title) of mail.")
parser.add_argument("-t", "--text", dest='text', type=str, default="", help="Text of mail. (default: %(default)s)")
parser.add_argument("-f", "--file", dest='file', type=str, nargs='+', default='', help="Attach files of mail. (default: %(default)s)")
parser.add_argument("-F", "--from", dest='sender', type=str, default='task_lty@163.com', help="Sender of mail. (default: %(default)s)")
parser.add_argument("-T", "--to", dest='receiver', type=str, nargs='+', default='ty_liang@foxmail.com', help="Receiver of mail. (default: %(default)s)")
parser.add_argument("-S", "--smtp-server", dest='smtpserver', type=str, default='smtp.163.com', help="Smtp server. (default: %(default)s)")
parser.add_argument("-U", "--username", dest='username', type=str, default='task_lty@163.com', help="Name of user. (default: %(default)s)")
parser.add_argument("-P", "--password", dest='password', type=str, default='CVIIWMJGUUNBONQM', help="Password of user. (default: ********)")
parser.add_argument("-l", "--sslport", dest='sslport', type=int, default=465, help="SSL server port. (default: %(default)d)")
args = parser.parse_args()
if args.subject != '':
  subject = args.subject
else:
  print(sys.argv[0]+" [ERROR] subject is empty!")
  sys.exit(1)
text = args.text
file_attach=args.file
sender = args.sender
receiver = args.receiver
smtpserver = args.smtpserver
username = args.username
password = args.password
sslport = args.sslport

if isinstance(file_attach, str):
  file_attach = file_attach.split()
if isinstance(receiver, str):
  receiver = receiver.split()

receiver.append(sender)

#sender = 'task_lty@163.com'
#receiver = [sender, 'ty_liang@foxmail.com']
#smtpserver = 'smtp.163.com'
#username = 'task_lty@163.com'
#password = 'Lty18811472536'

msg = MIMEMultipart()
msg['Subject'] = Header(subject, 'utf-8')
msg['from'] = sender
msg['to'] = ','.join(receiver)

extra_info=''

for f in file_attach:
  if not os.path.isfile(f):
    print(sys.argv[0]+" [WARNING] no such file : "+f)
    extra_info = extra_info+"\nupload file : "+f+" failed!"
    continue
  elif not os.access(f, os.R_OK):
    print(sys.argv[0]+" [WARNING] read file : "+f+" failed! permission denied!")
    extra_info = extra_info+"\nupload file : "+f+" failed!"
    continue
  file_tmp = MIMEApplication(open(f, 'rb').read())
  file_tmp.add_header('Content-Disposition', 'attachment', filename=os.path.split(f)[1])
  msg.attach(file_tmp)

if not extra_info == '':
  text = text + "\n\nEXTRA INFO:" + extra_info
#text = text + "\n\nFrom " + getpass.getuser() + "(" + socket.gethostname() + ")"
msg.attach(MIMEText(text))

smtp = smtplib.SMTP(smtpserver, sslport)
#smtp.connect(smtpserver)
#smtp=smtplib.SMTP_SSL(smtpserver, sslport)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

#print(sys.argv[0]+" [INFO] send mail success! from ("+sender+") to ("+','.join(receiver[:-1])+")")