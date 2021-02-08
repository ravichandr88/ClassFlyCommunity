# import requests

# resp = requests.get('http://localhost:8000/fileurl',{'filename':'test'})

#             GET /my-image.jpg HTTP/1.1
#             Host: bucket.s3.<Region>.amazonaws.com
#             Date: Mon, 3 Oct 2016 22:32:00 GMT
#             Authorization: authorization string
         
# print(resp.json())


import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import requests
import json

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
        print(response)
    except ClientError as e:
        print(e)
    return response

#for a single download
# url = generate_presigned_url('project0videos','classfly2.png')
# print(url)


#initiate multipart upload
def initiate_multipart_upload(bucket,key):
        
    # s3 = boto3.client('s3')
    s3 = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))
    
    response = s3.create_multipart_upload(
        Bucket=bucket, 
        Key=key
    )

    return response['UploadId']

# print(initiate_multipart_upload('project0videos','classfly.mp4'))



def presigned_url_multipart(bucket,key,upload_id,part_no):
    s3 = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))

    signed_url = s3.generate_presigned_url(
    ClientMethod ='upload_part',
    Params = {
       'Bucket': bucket,
       'Key': key, 
       'UploadId': upload_id, 
       'PartNumber': part_no
    })
    return signed_url

upload_id = "E.dk1Tm6MWgde6vn9kBU2SkeKwNtFO2LBmMset7T4aSBJpBXLfsxwXL9eFSWI4lvZB2Ja062_K73WxXnoy9NlKaAF67doy3bPJBDTKkCRBwmlXOxwNQ6suhV8R1xyOAC"

# print(presigned_url_multipart('project0videos','classfly.mp4',upload_id,0))

def complete_multipart_upload():
    s3 = boto3.client("s3",region_name="ap-south-1",
                          aws_access_key_id="AKIAS6UIIOP5B476WEOF",
                          aws_secret_access_key="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",
                          config=Config(signature_version="s3v4"))
    upload_id='4GKI8b.VxTHfSzIeiXfYp49RzycvutXAq0BMNcO97MYqtZpvvH3eKp3zpyDhniarMQn_XQ9Ocb3bqnRefWt7Vy376wt4FL3RJ8Dr917.kJ4MKt5IN8XIvGsbba9h2MOR'
    response = s3.complete_multipart_upload(
        Bucket= 'project0videos',
        MultipartUpload={
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
    },
       Key= '15.xlsx', 
       RequestPayer='requester',
       UploadId = 'Nio5fFgPHZiEhzk1_Qs4W5hoWKN1AAbqCJuJEbhSCNRii00CX9Y1_FhNmgeScakMP2JRiiJ2Xp7a_kuPjqOaIiTh24o26LUwMgZq4CazLruWKfSFD32fS2anIEtaCma5')

    return response


def upload_to_mux(v_url,):
    video_url = v_url
    url = 'https://api.mux.com/video/v1/assets'
    data={
        'input':video_url,
        'playback_policy':'signed'
    }
    headers = {
        'Content-Type':'application/json'
    }
    response = requests.post(url,json.dumps(data),headers=headers,auth=('d17ad52c-a7cd-4d0f-baeb-096038163452','oKSHDGrS3rdKPZ0QFCScAbJrJ/duZVaceyTVkIBFn7SgHb3e7H3qzADLIN3V+mQiG6qe99q/Q9B'))
    return response.json()


def get_upload_status(asset_id):

    url = 'https://api.mux.com/video/v1/assets/'+asset_id
    response = requests.get(url,auth=('d17ad52c-a7cd-4d0f-baeb-096038163452','oKSHDGrS3rdKPZ0QFCScAbJrJ/duZVaceyTVkIBFn7SgHb3e7H3qzADLIN3V+mQiG6qe99q/Q9B'))
    return response.json()


def create_url_signing_key():
    url = 'https://api.mux.com/video/v1/signing-keys'
    headers = {
        'Content-Type':'application/json'
    }
    response = requests.post(url,headers=headers,auth=('d17ad52c-a7cd-4d0f-baeb-096038163452','oKSHDGrS3rdKPZ0QFCScAbJrJ/duZVaceyTVkIBFn7SgHb3e7H3qzADLIN3V+mQiG6qe99q/Q9B'))
    return response.json()


print(generate_presigned_url(bucket_name='project0videos', object_key='djnago_angular.mp4', expiry=3600))

# print(upload_to_mux('https://project0videos.s3.amazonaws.com/classfly.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS6UIIOP5B476WEOF%2F20210206%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20210206T103631Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=4933e62fbeeac5b6b9dc55dea01ff2747083e308ac674e4345f2e0c1d092b1f5'))

# print(get_upload_status('4TkA93Gh800AyFliyckPL4Bs1T01u6jZCyu5U42s88cAM'))

# print(create_url_signing_key())






# https://project0videos.s3.amazonaws.com/classfly.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS6UIIOP5B476WEOF%2F20210129%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20210129T133546Z&X-Amz-Expires=36000&X-Amz-SignedHeaders=host&X-Amz-Signature=e34e24569f1f6bc9c6faa3befb5804b1170f95ab444e6c467ba4a636e8bbb463&X-Amz-Server-Side​-Encryption​-Customer-Algorithm=AES256
'''
Bucket, IfMatch, IfModifiedSince, IfNoneMatch, IfUnmodifiedSince, Key, Range, ResponseCacheControl, ResponseContentDisposition, ResponseContentEncoding, ResponseContentLanguage, ResponseContentType, ResponseExpires, VersionId, SSECustomerAlgorithm, SSECustomerKey, SSECustomerKeyMD5, RequestPayer, PartNumber
'''


'''
{
    "Version": "2012-10-17",
    "Id": "PutObjectPolicy",
    "Statement": [
        {
            "Sid": "DenyIncorrectEncryptionHeader",
            "Effect": "Deny",
            "Principal": "*",
            "Action": ["s3:PutObject","s3:GetObject"],
            "Resource": "arn:aws:s3:::project0videos/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": "AES256"
                }
            }
        },
        {
            "Sid": "DenyUnencryptedObjectUploads",
            "Effect": "Deny",
            "Principal": "*",
            "Action":  ["s3:PutObject","s3:GetObject"],
            "Resource": "arn:aws:s3:::project0videos/*",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption": "true"
                }
            }
        }
    ]
}
'''


"""
{
    "Version": "2012-10-17",
    "Id": "PutObjectPolicy",
    "Statement": [
        {
            "Sid": "DenyIncorrectEncryptionHeader",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::project0videos/*",
            "Condition": {
                "StringNotEquals": {
                    "s3:x-amz-server-side-encryption": "AES256"
                }
            }
        },
        {
            "Sid": "DenyUnencryptedObjectUploads",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::project0videos/*",
            "Condition": {
                "Null": {
                    "s3:x-amz-server-side-encryption": "true"
                }
            }
        }
    ]
}
"""
'''
https://softwareontheroad.com/aws-s3-secure-direct-upload/
'''