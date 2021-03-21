import requests
import json
# import jwt
import base64
import time



headers = {
            'Content-Type':'application/json'
                }
auth = ('24484635-ee3e-4633-977a-88679bbb0551','jqDGptsyBdyh3bQa6NuqnWgEgwFkadLNQm6lJ6ryF1t59GfRcFBy3ZvY6NzuBBgI+fGhBJsolBM')


def upload_to_mux():
    url = 'https://api.mux.com/video/v1/assets'

    data = {
        'input':'https://project0videos.s3.amazonaws.com/classfly.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAS6UIIOP5B476WEOF%2F20210319%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20210319T141121Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c1d8323d7022a43580d1f2dc754566dfde3697727cde4a727432ec67dbecb5f8',
        "playback_policy": [
        "signed"
            ]
            }

    response = requests.post(url,json.dumps(data),headers=headers,auth=auth)

    print(response.json())

# upload_to_mux()
'''
{'data': 
{'status': 'preparing',
 'playback_ids': 
 [{'policy': 'signed', 
 'id': 'o6NfTUyXvdbIoZcDXvgKom02RIcEIU5MB01jjKEnv6OSM'}], 
 'mp4_support': 'none', 
 'master_access': 'none',
  'id': 's6QoHe6oTDRPcwILgwn1i46i6PQr800vHvhccXFI8BDU', 
  'created_at': '1616163124'}}
'''


#Retrive an asset
def retreive():
    url = 'https://api.mux.com/video/v1/assets/s6QoHe6oTDRPcwILgwn1i46i6PQr800vHvhccXFI8BDU'

   
    response = requests.get(url,headers=headers,auth=auth)
    
    print(response.json())
# retreive()

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

    url = 'https://api.mux.com/video/v1/assets/s6QoHe6oTDRPcwILgwn1i46i6PQr800vHvhccXFI8BDU/playback-ids'

    data = { "policy": "signed" }

    response = requests.post(url,json.dumps(data),headers=headers,auth=auth)

    print(response.json())
# playbackid()


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


import jwt
#Generate JWT web token
def JWT_token():
    playback_id     =   "o6NfTUyXvdbIoZcDXvgKom02RIcEIU5MB01jjKEnv6OSM"
    signing_key_id  =   "N5DDgTWOO15rS5ZDQcEX7K37SoLOacb3cbhmxeMNg8Q"
    private_key_base64 = "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb2dJQkFBS0NBUUVBcCs2Sm1lS3Z1dnhqUW1Sc0Z5ZnEzWWEvcGd1cDFQRXZraDZTdE91aHo0cE5HcHlPCnFYMlFMUXIxZlcwWkRCanU5Z3FqYk9vM3I0d0gvT2ZDWHFkVFVUZHBWMlRzTUo0U0tmTWJ2QXZQRWZ2NCtLWUcKMnIybW4wNzQ1TFE0KzJGcWkvNkIrZ3F6eEk4VEVsZXhFbWNtMEpsaHFqUVBBSG5rNDNqcGtDU2tCdjgrYWV0SQppUktvSlZsdjRzaXUvUGt1THV4dHBKNlRCRXVmWlFoRUlEZnc5TGR2YmJkNVpzYXgyenJJdHhiWGJseUF1UCtXCjJvWlJYb2c4WUFjaHFjemdZOUNyZ1ljWWZsLy9HSTZwLzQ4ZlorU1VVcHQwekJrSmRiTWhvaEhRTGR2dEt3Z3UKV1o4aVhVZzAwR2JQczdFU3MxTUJIYXRFWnJWVlBkQS83RWIzYXdJREFRQUJBb0lCQUFUQ0pKSUFzMXdJQk1QLwoxblE5aEZFc25VZVdNd1MrcE10dUpGZ09DVEs1UjRBR2lhQlIxNEQvTzMrSFZOdGI1WUdCUWFvM1pNYUxvRHBSClV0ZWR4Q1diL1ZjbG0rK3d1dkVIVzNUVG5OVjBuMVJrVi9OZ3hsVGpSdmdzQnlWUVdGV0pLNk9ySS9iZzJ2aDkKRlo1ZzM5K3ZTTzRxdFhZYy9oaFg5NzVHMjRMN01zR1VDb05hMUZ1Uk8zWGk2amwxb3Ryc0R4VDU4S0h6aE83RApDM0tYeStobmJxanpOdzZZYTlwSWhsT3IzSHRyR1FaUzhGUld3QWQrNGZ1L280Y0g0bDNjOTd5SUpjanQ2QXZZCldxd2hKNGRlaE5ybEpCeDV0V09tVVJkTjFyMWYwa1JoUW9sWnVhVER1Z09ZSzRlbXBOTXVsbUVrS2RaNjdJbFIKVkp6NlZrRUNnWUVBd2NWdlZWT2N5dlRSbGg3UmFBNTUzaHRad0NTWWRIVWtrSlRJTVU1ZTV3K3NjQk1RaW1wRgpjNXFBeDB4YVphTTBRZmZ0MGhJTmtRMWV1cjR5K0J3THJMcytJUTlxYmFEV3Nyb2kwYmg1M0tYRHp6MFhyWjFvCkhsRkg1NGtDeWhIcmoyU0x6MVFqNDdsWE5NaWRqNlhGTngzbEk4azVzMU9lUllCanYvajdlSXNDZ1lFQTNkekIKOS9xdnFtZFErdFd5bS9BSWI5Z3JKWkdIV0ZZUEZqZ1BQa3RuWUNwV2lMNmRqdTBqQm5ZcHVTY3BEZkpkejNJVgpJQUdJamRQY3lyOCtqTGZoMGExWjc5Ym11TWMrL3pRTFJoVXo2WDRvZFh2T0ZQeUpQQVBKam9TOEJ5Ni9lZ0lhCjZ2L3VXeHYycnNuYzhsUHR1TjRwSW03NW9sc1Zpdk5ZRzBXOWVLRUNnWUFBdkhoTTBiR0J6K1pQOUxRRStqRWEKVis1Q1hhRTZxQXRJaFZneFg4UGFpdU96MVU2MXgrdVZvZHVsWmpQZHVQNEUxaVZRTEFOakxyTFNjTkNPd3NTRQpsbjJJOEo4TjVaT0xRRXZMa2pEY1ZzRGtzNjI0V2lYQUg3enZNMFVRY1hyOG8zd29nSUJXYUNqZHFYbDN4MEIxCmtpYUJ1VXovMG15Q2hSZGI3bDArT3dLQmdFQWdzaFE2YXBJbm9ObVA4VHR2aXhEQSs5KzFDOWoxcnhDdURZSGwKQzdGWks0QUZFTWVpTlpDRmtSUEtoT3hhRk5HRVdTVFNMS1ZLQ3JTenlLR2wrT2pCWVpDWW5rSGtuWW5vZ2lXMAp0VGVWVnA1MnRaK05TeUdFdXJxdUZTZENWT2d3T1pXWmVrenRiVVVpWmZISlhwb2o1T0htRDlQazNmbzIwazIzCnY4ZGhBb0dBSDVWcWNKV0xoaW1SamFPNjVaTTlWLzNRM2JUVEgrWE1Fa3RUbVpkNHQxdEcrbHNocjRsMWN0VWoKc29EWHNJSE11Y0pQOWFvTmx1QnI4RUpqREhGZ0ZDeEEzUFpHYndwT2lWWUdsVnVEdlU1aGcrSjN2L0w4MDkyagp1TTRseDV6NStnY0sxdGZLWVpGaE0vV1VLRFU2eGZtNjVmMEhLTlFBWmpZYW5Zb0dCRUE9Ci0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg=="
    private_key = base64.b64decode(private_key_base64)

    token = {
        'sub': playback_id,
        'exp': int(time.time()) + 3600, # 1 hour
        'aud': 'v'
    }
    headers = {
        'kid': signing_key_id
    }

    json_web_token = jwt.encode(token, private_key, algorithm="RS256", headers=headers)

    # You need to decode the token, otherwise you'll get a `b'` at the start of the string.
    print(json_web_token.decode('UTF-8'))
JWT_token()

'''
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJlblhJdjNJbEMwMGc2N2xQb3NUMDFCT3FzRUc5VW1oYUx5Nm1yc0RKcFI3VSJ9.eyJzdWIiOiJzRWRXOWlpOEt2SmRqemZlUzNLQW5DcjF5c2tWTHNUck9jV3pJb21jbldrIiwiZXhwIjoxNjE1NjQzNTA5LCJhdWQiOiJ2In0.UO80apSLdGGeiONwv2Xom0onQOaDZDTpZnDnn7NXwSsdO9m3xkD_L5-0-VcddDoQXmr35EqJYYcdVoJNqWlv-Beg5tSm0A4AsgqCWxF0XIM96uajKjYWiiHTpwjL8jY1ArLglEuRuS3TSDNyBznOrBcQtGq2I1PcV1DyvVvuHGL_uORgNctXxajJtGRV5d4wfamGOMo-Rx8jn6Ndcg8gZvjUkVuKf8INhdaAe8cZkNL0eg7a5N1Q9BvSj_BhxY1WNVN1oSFboCoVoO7mx-thRnqajXBB4WWxWitlFxCsNfSlU28YxBgqA5wBsyEN1zUiBIh2xcfsg26xk2cAdIC-BA
'''













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

