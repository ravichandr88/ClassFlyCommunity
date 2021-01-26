from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from user.models import Phonenumber
from rest_framework import status

from rest_framework import serializers

"""Validation code for all the forms"""

def user_validation(phone_number,email):
    #Check whether the phone number is already present
    if len(phone_number) != 10:
        res = serializers.ValidationError({'message':'Phone number not valid'})
        res.status_code = 203
        raise res
    
    elif Phonenumber.objects.filter(phone_number=phone_number).count() != 0:
        res = serializers.ValidationError({'message':'Phone number already exist'})
        res.status_code = 203
        raise res
    
    elif User.objects.filter(username=email).count() != 0:
        res = serializers.ValidationError({'message':'Email already exists'})
        res.status_code = 203
        raise res
    return




    '''{"name":"ravi","phone_number": "8095988717", "email": "ekaljnkjnK@kjnkjn"}'''