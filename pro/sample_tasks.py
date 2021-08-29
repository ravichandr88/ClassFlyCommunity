import time
import requests
from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail



@shared_task
def get_call(task_type):
    url="https://reqres.in/api/users?page=2"
    resp = requests.get(url)
    return resp.json()

@shared_task
def adding_task(x, y):
    print(x,y)
    return x + y

#@shared_task
def send_otp(phone_number,otp):
    requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(phone_number,otp))
    return

@shared_task
def send_student_otp(phone,otp):
    requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+REVA%2C+Your+otp+is+{}.".format(phone,otp))
    return 

@shared_task
def send_email_otp(user,otp):
    subject = 'ClassFly'
    message = f'Hi {user.username}, thank you for registering for ClassFly, Your Email OTP is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return
