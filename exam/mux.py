import requests
import json
import jwt
import base64
import time



headers = {
            'Content-Type':'application/json'
                }
auth = ('24484635-ee3e-4633-977a-88679bbb0551','jqDGptsyBdyh3bQa6NuqnWgEgwFkadLNQm6lJ6ryF1t59GfRcFBy3ZvY6NzuBBgI+fGhBJsolBM')


def upload_to_mux():
    url = 'https://api.mux.com/video/v1/assets'

    data = {
        'input':'https://project0videos.s3.amazonaws.com/classfly.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS6UIIOP5B476WEOF%2F20210313%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20210313T110955Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=9e35d48c0fce25c789c4bf49cf22132ba75bafb842520c238988aa511ec5c602',
        "playback_policy": [
        "signed"
            ]
            }

    response = requests.post(url,json.dumps(data),headers=headers,auth=auth)

    print(response.json())

'''
{'data':
 {'test': True,
  'status': 'preparing', 
  'playback_ids': [{'policy': 'signed', 'id': 'sEdW9ii8KvJdjzfeS3KAnCr1yskVLsTrOcWzIomcnWk'}], 
  'mp4_support': 'none', 
  'master_access': 'none', 
  'id': 'bM00r4GVEXJG1U8NMMQwO01H6602ODrw3jxQsjUQSLD5yg',
   'created_at': '1615634264'}}
'''


#Retrive an asset
def retreive():
    url = 'https://api.mux.com/video/v1/assets/bM00r4GVEXJG1U8NMMQwO01H6602ODrw3jxQsjUQSLD5yg'

   
    response = requests.get(url,headers=headers,auth=auth)
    
    print(response.json())


'''
{'data': 
{'tracks':[
    {'type': 'video', 
    'max_width': 1920, 
    'max_height': 910, 
    'max_frame_rate': 24,
     'id': 'NmKHyEVnqavgdjAmh1MBLQ026pBDKLUNA6S029jglhUvQ',
      'duration': 118.958333}, 

      {'type': 'audio',
       'max_channels': 2, 
       'max_channel_layout': 'stereo', 
       'id': '3D6Yn9lNIAbiU3lTSTPgTJA00ZpaPHIB02KcZHLvIAlEw', 
       'duration': 119.039}
       ], 
       'test': True,
        'status': 'ready',
         'playback_ids': [
             {'policy': 'signed', 
             'id': 'sEdW9ii8KvJdjzfeS3KAnCr1yskVLsTrOcWzIomcnWk'}],
              'mp4_support': 'none',
               'max_stored_resolution': 'HD', 
               'max_stored_frame_rate': 24,
                'master_access': 'none',
                 'id': 'bM00r4GVEXJG1U8NMMQwO01H6602ODrw3jxQsjUQSLD5yg', 
                 'duration': 10.291667,
                  'created_at': '1615634264', 
                  'aspect_ratio': '192:91'}}
'''



#Create playbackID for uploaded Asset
def playbackid():

    url = 'https://api.mux.com/video/v1/assets/bM00r4GVEXJG1U8NMMQwO01H6602ODrw3jxQsjUQSLD5yg/playback-ids'

    data = { "policy": "signed" }

    response = requests.post(url,json.dumps(data),headers=headers,auth=auth)

    print(response.json())


'''
{'data': 
{'policy': 'public',
'id': 'VPpTImjbTC2bAPdBgmXwQK01ebd4stm5iuuApuwJcANg'}
}
'''


#Create a URL signing key
def create_url():
    url = 'https://api.mux.com/video/v1/signing-keys'

    response = requests.post(url,headers=headers,auth=auth)

    print(response.json())

create_url()

'''
{'data': 
{'private_key': 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJ
    QkFBS0NBUUVBd0xjcW1mWnVIQ2dranJ1dkFqcXNqVm1ScDFmcVhJMDZ0Nll4dUliSUtZ
    elJTWnpzCnVzTUN0c0UrSGJxbTRtdkcweWRnUnZZaDM4eFk2Z3JLUm1HQVJMSnlrR2w5YU9MZ
    kZBTjByT2hmaG9iS0tKeDgKVGl3QVUvNURyMUlVV2Rpc3hab2ljVWJVNTNyQ0Nhd3BSTCtWTkJ
    EN0dHdzJLVUI4Rlk2MmlEYWdOM0xEa1hvcApzNHdVUVlHNHlyTWFjT2JyUlF2bVhvZEtSNXYrc
    WROYlVSMXNlbURGT0R5OWR0VmJiSy93ZnIxRUhrbFA5SmNECjc5M1FzcEhmeFYwZHAwVlhXNG1L
    dFh1c2Y5aW1RYjRxUTc4NEh1LzN1ZFk1RlBCTUJvckt6V21ldFJoY1RNZEcKS2JiTzRyMXhTUGs5R
    itqNjZvM2grSDlXRHowRHp4Z0NqTGRqclFJREFRQUJBb0lCQUVxSFM2bHBQU0lVZ0RiVwo3SktmSUZZ
    MTJuZHVMNHVGYnJ6UlFBOU55S0VRL1d0TGpkMllSemRvT2w2QzdjRkl6d2FnQnNMS3MwVDZvVFE1CjRn
    b2Y4TndnYXQvZ2ZBaVJISlovMDZKKzUxcCtURFl5ZG54QTFndWxuSVZ6NTd6clo3MnZvenhObVU3QUVjU
    nQKMlRQbUo0eVFPSnMwVmluVDcyamkzVUtHWmFXclIyUEJPTVdiQ01xN3ltSlljZE03a2FnYjJQR3ZhZm
    c0V3liNApnVkJyTHJpU0Z5ZDB4MXZvQXh2Rlk1ZE9Jb2ltbnFLTjc2YVhwbGluTS9td05MNGFIRTdvaU1
    aTllMODJaeW1ZCmZZWGJUMGNOVGNGMm0yTkhpUnY1d0t6clBzdG53VnNMclFUUlEzczl3YW9IS1JFS0V0
    WjJuSGNIRkw0MkwrTFkKYkw1ZzNYMENnWUVBMHlUTHJNRVoyL2lJWkF4L2VSM2hJYnYvQ2RRRnhuV3Yzc
    U1pMzRlaFdySzY4QWJteTlacAo1L0dROTRURW1SR3RJR0hLY2xzNEkyaFhLTFJRdExHaVg0elptRzF0R3
    g1RkI5SWgyaXVObUFRL28zRm5weVVwCkUxTTFBVnRlZG1ldjJteGxHZVRTVnY3UmV4ZE9iVlM4ekprUzd
    rWGJxUURDd1h3RlFIanhMd3NDZ1lFQTZhZ2oKUVlSTkM2eEprYkJPRW1UUTN3cjFqeEJnTk9NdVYwaUV2
    cmw5aUZwN2RxZlRvS3hsTXR3QzJVcytYOFdGTy83VQpXQlVuZXdHTXhyYXFsMkQ2THNFbmNKbnpmTmMwO
    DhGLzhHWFd4T0IrU0Z0QmU0RWJTUEorNFRTWG5wTHZid2ZnClprMWZ4Z2lkWm15UXo4ZlQyakhwVFVZUD
    k0dXM1SGdqcmtnelN5Y0NnWUVBaVJuOGN2bVVUQVNPczhCMXlYU0EKYWtKRGNlTk51TGRVY3BHbHBGWFN
    qUzAvTzNxUHhNNCtTSkRRSEJrRys0bkJ6Q1FUcTd2VnNSQWdnRnJOaVBkTApReFlYZU9XZEVoM09ueXh3
    Tk5WUkJPUEZXdURaZUd3bHh0bWhzbmJjMksrdFBYeGpEYlJLYkpqYjl6eUQvWFFuCmdBYnBodlN2bEliY
    zczd1RnUERIVTA4Q2dZQlEwaXpudzZpV3loQmtpWFJuM21GMVZTZ2RSVS9SMjJjekg4MXkKMzF4eHBzS2
    dCMnNuWDVwZG5rYUovUUhsUk1CU1FWSVg2YkZQVmZqbzMxUmdxbFcvaUdacEI0ZDJma1k5cm9mZgprb3B
    ZYlVLaEtwZWE3Y3lQVGZuZlVqN0R4aFYxOVdhRVhHMHRaZHQwQzBlSDU1bjdGbHFadFF0ZTEveUV4cDJv
    CjhpWno3d0tCZ0NmYzE4ZFlDYTd1akJKUnpzU0VqUjA5NlNHOEcwbk5PNVhXRS9PaTFyNDZRRG1WNExOd
    VByMkMKVCtPOXVtQ1poWk15Q3haSDdSb29yd3VSMDdBZUUwZGgxcVRwZUVoUSt2UXpobVcwelEwa3MzSE
    NyTXJoVFlZcQpDMFdFNmdTZTRoQUVTSlROd1M2VzVoSjlHZ28yOGVvcXFJbFhTU3hqUDRxaS9JL2VmOEJ
    KCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg==', 
    'id': 'RenXIv3IlC00g67lPosT01BOqsEG9UmhaLy6mrsDJpR7U', 
    'created_at': '1615638177'}}
'''



#Generate JWT web token
def JWT_token():
    playback_id = 'sEdW9ii8KvJdjzfeS3KAnCr1yskVLsTrOcWzIomcnWk'
    signing_key_id = 'RenXIv3IlC00g67lPosT01BOqsEG9UmhaLy6mrsDJpR7U'
    private_key_base64 = """LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBd0xjcW1mWnVIQ2dranJ1dkFqcXNqVm1ScDFmcVhJMDZ0Nll4dUliSUtZelJTWnpzCnVzTUN0c0UrSGJxbTRtdkcweWRnUnZZaDM4eFk2Z3JLUm1HQVJMSnlrR2w5YU9MZkZBTjByT2hmaG9iS0tKeDgKVGl3QVUvNURyMUlVV2Rpc3hab2ljVWJVNTNyQ0Nhd3BSTCtWTkJEN0dHdzJLVUI4Rlk2MmlEYWdOM0xEa1hvcApzNHdVUVlHNHlyTWFjT2JyUlF2bVhvZEtSNXYrcWROYlVSMXNlbURGT0R5OWR0VmJiSy93ZnIxRUhrbFA5SmNECjc5M1FzcEhmeFYwZHAwVlhXNG1LdFh1c2Y5aW1RYjRxUTc4NEh1LzN1ZFk1RlBCTUJvckt6V21ldFJoY1RNZEcKS2JiTzRyMXhTUGs5RitqNjZvM2grSDlXRHowRHp4Z0NqTGRqclFJREFRQUJBb0lCQUVxSFM2bHBQU0lVZ0RiVwo3SktmSUZZMTJuZHVMNHVGYnJ6UlFBOU55S0VRL1d0TGpkMllSemRvT2w2QzdjRkl6d2FnQnNMS3MwVDZvVFE1CjRnb2Y4TndnYXQvZ2ZBaVJISlovMDZKKzUxcCtURFl5ZG54QTFndWxuSVZ6NTd6clo3MnZvenhObVU3QUVjUnQKMlRQbUo0eVFPSnMwVmluVDcyamkzVUtHWmFXclIyUEJPTVdiQ01xN3ltSlljZE03a2FnYjJQR3ZhZmc0V3liNApnVkJyTHJpU0Z5ZDB4MXZvQXh2Rlk1ZE9Jb2ltbnFLTjc2YVhwbGluTS9td05MNGFIRTdvaU1aTllMODJaeW1ZCmZZWGJUMGNOVGNGMm0yTkhpUnY1d0t6clBzdG53VnNMclFUUlEzczl3YW9IS1JFS0V0WjJuSGNIRkw0MkwrTFkKYkw1ZzNYMENnWUVBMHlUTHJNRVoyL2lJWkF4L2VSM2hJYnYvQ2RRRnhuV3YzcU1pMzRlaFdySzY4QWJteTlacAo1L0dROTRURW1SR3RJR0hLY2xzNEkyaFhLTFJRdExHaVg0elptRzF0R3g1RkI5SWgyaXVObUFRL28zRm5weVVwCkUxTTFBVnRlZG1ldjJteGxHZVRTVnY3UmV4ZE9iVlM4ekprUzdrWGJxUURDd1h3RlFIanhMd3NDZ1lFQTZhZ2oKUVlSTkM2eEprYkJPRW1UUTN3cjFqeEJnTk9NdVYwaUV2cmw5aUZwN2RxZlRvS3hsTXR3QzJVcytYOFdGTy83VQpXQlVuZXdHTXhyYXFsMkQ2THNFbmNKbnpmTmMwODhGLzhHWFd4T0IrU0Z0QmU0RWJTUEorNFRTWG5wTHZid2ZnClprMWZ4Z2lkWm15UXo4ZlQyakhwVFVZUDk0dXM1SGdqcmtnelN5Y0NnWUVBaVJuOGN2bVVUQVNPczhCMXlYU0EKYWtKRGNlTk51TGRVY3BHbHBGWFNqUzAvTzNxUHhNNCtTSkRRSEJrRys0bkJ6Q1FUcTd2VnNSQWdnRnJOaVBkTApReFlYZU9XZEVoM09ueXh3Tk5WUkJPUEZXdURaZUd3bHh0bWhzbmJjMksrdFBYeGpEYlJLYkpqYjl6eUQvWFFuCmdBYnBodlN2bEliYzczd1RnUERIVTA4Q2dZQlEwaXpudzZpV3loQmtpWFJuM21GMVZTZ2RSVS9SMjJjekg4MXkKMzF4eHBzS2dCMnNuWDVwZG5rYUovUUhsUk1CU1FWSVg2YkZQVmZqbzMxUmdxbFcvaUdacEI0ZDJma1k5cm9mZgprb3BZYlVLaEtwZWE3Y3lQVGZuZlVqN0R4aFYxOVdhRVhHMHRaZHQwQzBlSDU1bjdGbHFadFF0ZTEveUV4cDJvCjhpWno3d0tCZ0NmYzE4ZFlDYTd1akJKUnpzU0VqUjA5NlNHOEcwbk5PNVhXRS9PaTFyNDZRRG1WNExOdVByMkMKVCtPOXVtQ1poWk15Q3haSDdSb29yd3VSMDdBZUUwZGgxcVRwZUVoUSt2UXpobVcwelEwa3MzSENyTXJoVFlZcQpDMFdFNmdTZTRoQUVTSlROd1M2VzVoSjlHZ28yOGVvcXFJbFhTU3hqUDRxaS9JL2VmOEJKCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg=="""
    private_key = base64.b64decode(private_key_base64)

    token = {
        'sub': playback_id,
        'exp': int(time.time()) + 3600, # 1 hour
        'aud': 'v'
    }
    headers = {
        'kid': signing_key_id
    }

    json_web_token = jwt.encode(
        token, private_key, algorithm="RS256", headers=headers)

    # You need to decode the token, otherwise you'll get a `b'` at the start of the string.
    print(json_web_token)


JWT_token()














# retreive input info, like whether uploaded or not
def uploaded_info():
    url = 'https://api.mux.com/video/v1/assets/bM00r4GVEXJG1U8NMMQwO01H6602ODrw3jxQsjUQSLD5yg/input-info' #Assest ID

    response = requests.get(url,headers=headers,auth=auth)
    print(response.json())

'''
{'data': 
[{'settings': 
{'url': 'https://project0videos.s3.amazonaws.com/classfly.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS6UIIOP5B476WEOF%2F20210313%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20210313T110955Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=9e35d48c0fce25c789c4bf49cf22132ba75bafb842520c238988aa511ec5c602'}, 'file': {'tracks': [{'width': 1920, 'type': 'video',
'height': 910, 'frame_rate': 24, 'encoding': 'h264', 'duration': 118.958333}, {'type': 'audio', 'sample_rate': 48000, 'encoding': 'aac', 'duration': 119.039, 'channels': 2}], 'container_format': 'mov,mp4,m4a,3gp,3g2,mj2'}}, {'settings': {'url': 'https://storage.googleapis.com/muxdemofiles/mux-test-video-watermark.png', 'overlay_settings': {'width': '640px', 'vertical_margin': '100px', 'vertical_align': 'bottom', 'opacity': '100.000000%', 'horizontal_align': 'center'}}, 'file': {'tracks': [{'width': 642, 'type': 'image', 'height': 346, 'encoding': 'png'}], 'container_format': 'png'}}]}
'''

