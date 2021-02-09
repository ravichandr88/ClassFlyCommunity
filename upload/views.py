from django.shortcuts import render
import boto3 
from botocore.client import Config
from botocore.exceptions import ClientError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import datetime
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files import File
import os
import requests
from django.contrib.auth.models import User
# Create your views here.
 
from .models import Contact_number


def generate_presigned_url(bucket_name, object_key, expiry=600):

    client = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))
    try:
        response = client.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name,'Key': object_key},
                                                  ExpiresIn=expiry
                                                  )
        # print(response)
    except ClientError as e:
        print(e)
    return response



@csrf_exempt
@api_view(["POST","GET"])
def fileupload(request):

        #request params {'sessioin_id','filename'}
        #when u get the code or when ready change add userid to the file name

        data=request.data
        imgurl = 'classfly2.png'
        s3 = boto3.client(
        "s3",
        region_name="ap-south-1",
        aws_access_key_id="AKIAS6UIIOP5B476WEOF",
        aws_secret_access_key="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",
        # amz_server_side​_encryption​_customer_algorithm="AES256",
        config=Config(signature_version="s3v4")
        )
        
        # session = boto3.Session(aws_access_key_id="AKIAS6UIIOP5B476WEOF", aws_secret_access_key="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")
        # s3client = s3.client('s3')
        url = s3.generate_presigned_url('put_object', Params={'Bucket':'project0videos', 'Key':imgurl}, ExpiresIn=36000, HttpMethod='PUT')
        # print(url)
        # imgurl="https://classfly.s3.ap-south-1.amazonaws.com/"+imgurl
        return Response(data={'code':200,'url':url})

@csrf_exempt
@api_view(['POST','GET'])
def create_presigned_url(request,filename):
        # print(request.data)
        count = Contact_number()
        count.save()
        filename = 'contact'+str(count.id)+filename
        count.filename = filename
        count.save()

        url = generate_presigned_url('project0videos',filename)
        return Response(data={'url':url})


def upload(request):
        return render(request,'amazon.html')

def upload_raw(request):
        return render(request,'final.html')


@csrf_exempt
@api_view(['POST','GET'])
def initiate_upload(request):
        print('Inititate Upload 0000000000',request.data)
        s3 = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))
     
        response = s3.create_multipart_upload(
        Bucket='project0videos', 
        Key=dict(request.data)['file_name'],
        Expires=3600
        )
        print(response)

        return Response(data={'upload_id':response['UploadId']})



#function to generate pre signed url for multipart upload 

@csrf_exempt
@api_view(['POST'])
def presigned_url_multipart(request):
        data = dict(request.data)
        print(data)
        key = data['key']
        part_no = data['part_no']
        upload_id = data['upload_id']
        s3 = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))

        signed_url = s3.generate_presigned_url(
        ClientMethod ='upload_part',
        Params = {
        'Bucket': 'project0videos',
        'Key': key, 
        'UploadId': upload_id, 
        'PartNumber': int(part_no)
        })
        return Response(data={'url': signed_url})


#function to complete multipart upload
@csrf_exempt
@api_view(['POST'])
def complete_upload(request):
        ''' {'upload_id',file_name,'multi_part_etags} '''
        data = request.data

        s3 = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))
        try:
                response = s3.complete_multipart_upload(
                Bucket= 'project0videos',
                MultipartUpload=data['multi_part_etags'],
                Key= data['file_name'], 
                RequestPayer='requester',
                UploadId = data['upload_id'])
                 
                print(response)
        except ClientError as e:
                print(e)
        return Response(data={'code':200})


'''
    {
        'Parts': [
            {
               'ETag': '"\"c1fafcc7d581d7749b7a90116ec75649\""',
                   'PartNumber': 1
            },
            {
                'ETag': '"\"ae317bd373d37bca702785fabac7196a\""',
                'PartNumber': 2
            },
            {
                'ETag': '"\"93b885adfe0da089cdf634904fd59f71\""',
                'PartNumber': 3
            }
        ]
    }
'''

def initiate(request):
        return render(request,'temp1.html')

