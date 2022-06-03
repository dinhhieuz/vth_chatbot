# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# package of RASA
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

# handle package
import gc
from requests import delete

import json
from xmlrpc.client import FastParser
import yaml
import requests

from datetime import datetime, date

##inf Zalo
secret_key = "WAWCLyzhGJ1McGPc6prN"
app_id = "1882365302811688917"

#!-------------------> XIN CHÀO

class act_chat_greating(Action):

    def name(self) -> Text:
        return "act_chat_greating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
            #----->
            button_main = [
                {
                    "type":"postback",
                    "title": "Tư vấn",
                    "payload": "/ask_tuvan_menu"
                },
                {
                    "type":"postback",
                    "title":"Khuyến mãi",
                    "payload": "/ask_khuyenmai_menu"
                },
                {
                    "type":"postback",
                    "title":"Blogs",
                    "payload":"/ask_blog_menu"
                },
            ]
            dispatcher.utter_message(
                text = "Xin chào Vũ Trụ Hạt rất vui được nói chuyện với bạn 🖐️🖐️!!!\nChúng tôi có thể giúp gì cho bạn nào"
                , buttons = button_main
            )
            res = {
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":"Các trợ giúp khác: ",
                        "buttons":[
                            {
                                "type":"postback",
                                "title": "Chính Sách",
                                "payload": "/ask_plc_menu"
                            },
                            {
                                "type":"postback",
                                "title":"Thông tin Page",
                                "payload":"/ask_page_menu"
                            },
                            {
                                "type":"phone_number",
                                "title":"📞 Liên hệ admin",
                                "payload":"+84763792207"
                            },
                        ]
                    }
                }
            }
            dispatcher.utter_message(json_message=res)

            del button_main, res
            gc.collect()
            return []
        except Exception as error:
            print("-->Error<--")
            print(error)
            dispatcher.utter_message(text="Xin lỗi bạn, hiện tại hệ thông đang bị lỗi 😓😓😓")
            return [FollowupAction("act_accept_buy")]

#!------------------------------------ CHẤP NHẬN MUA HÀNG

class act_accept_buy(Action):

    def name(self) -> Text:
        return "act_accept_buy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
    
            #--> Không hiểu tra Google
            result = send_manager(tracker.sender_id)

            if result == True: text = "Cảm ơn bạn đã liên hệ 🥰\nchúng tôi sẽ lên đơn cho bạn, hãy đợi chút nhé 😍"
            else: text = "Cảm ơn bạn đã liên hệ 🥰\nhiện tại hệ thông đang bận, mình sẽ chủ động liên lạc cho bạn trong thời gian sớm nhất, chân thành xin lỗi 😔"
            
            dispatcher.utter_message(
                text = text
            )

            del text, result
            gc.collect()
            return []
        except:
            print("-->Error<--")
            return []

#---> Handle Function


''' GỬI YÊU CẦU MUA HÀNG ĐẾN NHÀ QUẢN LÝ'''
def send_manager(id_user):
    ''' Lấy tên người dùng tại Facebook'''
    # Đọc file YAML để lấy access token
    with open(r"credentials.yml") as fh:
        rd_acstoken = yaml.load(fh, Loader=yaml.FullLoader)
    profile = requests.get(
        "https://graph.facebook.com/{}?fields=first_name,last_name,middle_name, name, name_format, short_name,profile_pic,location&access_token={}".format(id_user, rd_acstoken["facebook"]["page-access-token"]))
    #Kiểm tra lấy được profile người dùng chưa
    if profile.ok:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        profile = profile.json()
        #đọc file zalo
        with open(f'./assets/other/zalo.json', encoding='utf-8') as json_file:
            data = json.load(json_file)

        if data["time"] != date.today().isoformat():
            #call new access 
            headers = { 
                "Content-Type": "application/x-www-form-urlencoded",
                "secret_key": secret_key
            }
            payload = {
                "refresh_token" : data["refresh_token"],
                "app_id" : app_id,
                "grant_type" : "refresh_token"
            }
            response = requests.post("https://oauth.zaloapp.com/v4/oa/access_token", data=payload, headers = headers).json()
            #Save into file
            get_acs = {
                "time": date.today().isoformat(),
                "access_token": response["access_token"],
                "refresh_token":  response["refresh_token"],
            }
            with open(f"./assets/other/zalo.json","w", encoding='utf-8') as jsonfile:
                json.dump(get_acs, jsonfile, ensure_ascii=False, indent=4)

            #đọc access lần mới nhất
            with open(f'./assets/other/zalo.json', encoding='utf-8') as json_file:
                data = json.load(json_file)

        '''Gửi yêu cầu tới Zalo'''
        headers = { "access_token": data["access_token"] }
        payload = {"recipient": {
            "user_id": "8668477534363029464"
            },
            "message": {
                "text": "YÊU CẦU MUA HÀNG: "+ profile["name"] + " | " + now,
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [{
                            "media_type": "image",
                            # "attachment_id": response.json()["data"].get("attachment_id"),
                            "url": profile["profile_pic"]
                        }]
                    }
                }
            }
        }
        response = requests.post("https://openapi.zalo.me/v2.0/oa/message", data=json.dumps(payload), headers = headers)
        if response.ok: return True
        else: return False
    else: 
        return False

#!-------------------------------------FALL BACK
class act_unknown(Action):

    def name(self) -> Text:
        return "act_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
    
            #--> Không hiểu tra Google
            messeger_user = tracker.latest_message['text']
            url = "https://www.google.com.vn/search?q='" + messeger_user.replace(" ", "%20") + "'"

            dispatcher.utter_message(
                text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì!"
            )
            
            res = {
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":"Các lựa chọn khác: ",
                        "buttons":[
                            {
                                "type": "web_url",
                                "url": "https://vutruhat.com/",
                                "title": "🛒 Website",
                            },
                            {
                                "type":"phone_number",
                                "title":"📞 Liên hệ admin",
                                "payload":"+84763792207"
                            },
                            {
                                "type": "web_url",
                                "url": f"{url}",
                                "title": "🔎 Search Google",
                            },
                        ]
                    }
                }
            }
            
            dispatcher.utter_message(json_message=res)
            del url, res, messeger_user
            gc.collect()
            return []

        except Exception as error:
            print("-->Error<--")
            print(error)
            dispatcher.utter_message(text="Xin lỗi bạn, hiện tại hệ thông đang bị lỗi 😓😓😓")
            return [FollowupAction("act_accept_buy")]


