import json
from xmlrpc.client import FastParser
import yaml
import requests

''' Other functions'''
def inf_user(id_user):
    ''' Lấy tên người dùng '''
    # Đọc file YAML để lấy access token
    with open(r".//h.yml") as fh:
        rd_acstoken = yaml.load(fh, Loader=yaml.FullLoader)
    response = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(id_user, rd_acstoken["facebook"]["page-access-token"]))
    if response.ok:
        response = response.json()
        print(response)
        return response['last_name']
    else: 
        return "bạn"

''' GỬI YÊU CẦU MUA HÀNG ĐẾN NHÀ QUẢN LÝ'''
def send_manager(id_user):
    ''' Lấy tên người dùng tại Facebook'''
    # Đọc file YAML để lấy access token
    with open(r".//h.yml") as fh:
        rd_acstoken = yaml.load(fh, Loader=yaml.FullLoader)
    response = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic,link&access_token={}".format(id_user, rd_acstoken["facebook"]["page-access-token"]))
    if response.ok:
        response = response.json()
        print(response)
        '''Gửi yêu cầu tới Zalo'''
        headers = { "access_token": rd_acstoken["zalo"]["access_token"] }
        payload = {
            "recipient": {
                "user_id": "8668477534363029464"
            },
            "message": {
                "text": response
            }
        }
        response = requests.post("https://openapi.zalo.me/v2.0/oa/message", data=json.dumps(payload), headers = headers)
        
        if response.ok: return True
        else: return False
    else: 
        return False
