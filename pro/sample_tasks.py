import time
import requests
from celery import shared_task



@shared_task
def get_call(task_type):
    url="https://reqres.in/api/users?page=2"
    resp = requests.get(url)
    return resp.json()

@shared_task
def adding_task(x, y):
    print(x,y)
    return x + y

@shared_task
def send_otp(phone_number,otp):
    requests.get("http://sms.textmysms.com/app/smsapi/index.php?key=35FD9ADAC248D5&campaign=0&routeid=13&type=text&contacts={}&senderid=SOFTEC&msg=Welcome+to+ClassFly%2C+Your+otp+is+{}.".format(phone_number,otp))
    return