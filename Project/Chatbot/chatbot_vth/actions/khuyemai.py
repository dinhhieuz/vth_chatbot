# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# package of RASA
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# handle package
import gc
import json
from datetime import datetime, date, timedelta
from requests import delete

import asyncio

#class custome
from actions.act_help.crawl import crawl
from actions.act_help import conf as cf 
from actions.act_help.seek import seek

#!------------------------------------- """ KHUYẾN MÃI """
""" Khuyến mãi chung theo loại """
class act_khuyenmai_web(Action):

    def name(self) -> Text:
        return "act_khuyenmai_web"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        # Opening JSON file
        # returns JSON object as
        catagory = None
        for item in cf.catagory.keys():
            if tracker.latest_message['text'].lower().replace("?","").find(item) > -1:
                catagory = cf.catagory.get(item)
                break
            
        if catagory is not None:
            print(catagory)
            with open(f'./assets/data/product/{catagory}.json', encoding='utf-8') as json_file:
                data = json.load(json_file) #type: dict
                """{
                    "type": "DỤNG CỤ LÀM VƯỜN",
                    "time": "2022-04-26",
                    "data": [
                        {
                            "name": "Bình tưới cây",
                            "price": "25,000₫ 13,000₫",
                            "link": "https://vutruhat.com/san-pham/binh-tuoi-cay/",
                            "image": "https://vutruhat.com/wp-content/uploads/2021/09/binh-tuoi-cay-vu-tru-hat-min-300x300.jpg",
                            "status": "Hết hàng"
                        },
                        {...}
                }"""

            #Kiểm tra cần call dữ liệu không

            # Nếu: ngày hiện tại = ngày crawl + 1 ngày thì mới crawl lại lần 2
            if data["time"] != date.today().isoformat():
                # crawl dữ liệu (Chạy asynce)
                # open mutual stream to crawl data
                loop = asyncio.get_event_loop()
                loop.create_task(crawl.product(path=catagory, name_j=catagory))
            
            #element giới hạn 10 trong 1 lần gửi
            #Kiểm tra xem có tìm được dữ liệu không
            if len(data["data"]) > 0:
                #--> Tạo Template
                elements = []
                num = 0
                for item in data["data"]:
                    if item["price"].find("–") == -1 and item["price"].find(" ") > -1:
                        elements.append(
                            {
                                "title": item["name"],
                                "image_url": item["image"],
                                "subtitle": "Giá: " + item["price"].replace(" ", " giảm -> ") + "\nTrạng thái: " + item["status"],
                                "default_action": {
                                    "type": "web_url",
                                    "url": item["link"],
                                    "webview_height_ratio": "tall",
                                },
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url": item["link"],
                                        "title":"Xem thêm"
                                    },{
                                        "type":"postback",
                                        "title":"Mua ngay 💪",
                                        "payload":"/ask_accept_buy"
                                    }              
                                ]      
                            }
                        )

                #Respond to user
                dispatcher.utter_message(
                    text = "KHUYẾN MÃI " + data["type"].upper()
                )
                # Kiểm tra xem có sản phẩm không
                new_elm = []
                # Vì facebook giới hạn chỉ được 10 elements cho 1 lần gửi
                # Cứ 10 element sẽ được gửi 1 lần, những cái cuối k chia hết cho 10 nữa thì được gửi cuối cùng
                for i in range(1,len(elements)+1):
                    if i%10==0:
                        new_elm.append(elements[i-1])
                        res = {
                            "attachment":{
                                "type":"template",
                                "payload":{
                                    "template_type":"generic",
                                    "elements": new_elm
                                }
                            }
                        }
                        dispatcher.utter_message(
                            json_message = res
                        )
                        new_elm = []
                    else:
                        new_elm.append(elements[i-1])
                    if i == len(elements):
                        res = {
                            "attachment":{
                                "type":"template",
                                "payload":{
                                    "template_type":"generic",
                                    "elements": new_elm
                                }
                            }
                        }
                        dispatcher.utter_message(
                            json_message = res
                        )
                del res, new_elm, elements
            else: 
                dispatcher.utter_message(
                    text = "Rất tiết hiện chúng tôi không có khuyến mãi cho loại này:("
                )

            if 'data' in locals(): del data

        else:
            dispatcher.utter_message(
                text = "Rất tiết, loại khuyến mãi bạn tìm không có :("
            )
        
        del catagory
        gc.collect()
        return []


""" Khuyến mãi theo từng mặt hàng trong loại """
class act_khuyenmai_web_details(Action):

    def name(self) -> Text:
        return "act_khuyenmai_web_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        #1. Get name intent and then set condition to finding catagory 
        
        list_i, seek_i, catagory, time =  seek.product(intent = tracker.latest_message['intent']['name'], 
                                message = tracker.latest_message['text'].lower().replace("?",""))
                #--> Tạo Template
        elements = []
        num = 0
        
        if catagory is not None:
            #2. after looking for kind catagory, we are begin item in custome's string and then get information discounte  
            #Kiểm tra cần call dữ liệu không
            # cộng lên 1 ngày 
            # date_string = (datetime.fromisoformat(time) + timedelta(days=1)).isoformat()
            # Nếu: ngày hiện tại = ngày crawl + 1 ngày thì mới crawl lại lần 2
            if time != date.today().isoformat():
                # crawl dữ liệu (Chạy asynce)
                # open mutual stream to crawl data
                loop = asyncio.get_event_loop()
                loop.create_task(crawl.product(path=catagory, name_j=catagory))
            
            if len(list_i) > 0:
                for item in list_i:
                    if item["price"].find("–") == -1 and item["price"].find(" ") > -1:
                        elements.append(
                            {
                                "title": item["name"],
                                "image_url": item["image"],
                                "subtitle": "Giá: " + item["price"].replace(" ", " giảm -> ") + "\nTrạng thái: " + item["status"],
                                "default_action": {
                                    "type": "web_url",
                                    "url": item["link"],
                                    "webview_height_ratio": "tall",
                                },
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url": item["link"],
                                        "title":"Xem thêm"
                                    },{
                                        "type":"postback",
                                        "title":"Mua ngay 💪",
                                        "payload":"/ask_accept_buy"
                                    }              
                                ]      
                            }
                        )
                    #!
                    #     num += 1
                    # # mười element thì dừng vì fb chỉ cho 10 element
                    # if num == 10: break
                    #!
                
                #Respond to user
                dispatcher.utter_message(
                    text = "KHUYẾN MÃI " + seek_i.upper()
                )

                new_elm = []
                # Vì facebook giới hạn chỉ được 10 elements cho 1 lần gửi
                # Cứ 10 element sẽ được gửi 1 lần, những cái cuối k chia hết cho 10 nữa thì được gửi cuối cùng
                for i in range(1,len(elements)+1):
                    if i%10==0:
                        new_elm.append(elements[i-1])
                        res = {
                            "attachment":{
                                "type":"template",
                                "payload":{
                                    "template_type":"generic",
                                    "elements": new_elm
                                }
                            }
                        }
                        dispatcher.utter_message(
                            json_message = res
                        )
                        new_elm = []
                    else:
                        new_elm.append(elements[i-1])
                    if i == len(elements):
                        res = {
                            "attachment":{
                                "type":"template",
                                "payload":{
                                    "template_type":"generic",
                                    "elements": new_elm
                                }
                            }
                        }
                        dispatcher.utter_message(
                            json_message = res
                        )
                del res, new_elm
                #!
                # res = {
                #     "attachment":{
                #         "type":"template",
                #         "payload":{
                #             "template_type":"generic",
                #             "elements": elements
                #         }
                #     }
                # }
                # dispatcher.utter_message(
                #     json_message = res
                # )
                # del res
                #!

            else: 
                dispatcher.utter_message(
                    text = "Rất tiết hiện chúng tôi tìm thấy sản phẩm hay khuyến mãi cho sản phẩm này :("
                )
        else:
            dispatcher.utter_message(
                text = "Rất tiết, loại khuyến mãi bạn tìm không có :("
            )
        
        del elements, num, seek_i, list_i, time
        gc.collect()
        return []


'''
    Task today
        - tư vấn sản phẩm
        - 
'''

