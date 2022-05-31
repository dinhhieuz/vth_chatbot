# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# package of RASA
from gettext import ngettext
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction

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
#data product
from assets.data.product import details as product_details

#!------------------------------------- """ TƯ VẤN """
""" Tư vấn theo loại sản phẩm """
class act_tuvan_web(Action):

    def name(self) -> Text:
        return "act_tuvan_web"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

            # Opening JSON file
            # returns JSON object as
            catagory = None
            for item in cf.catagory.keys():
                if tracker.latest_message['text'].lower().replace("?","").find(item) > -1:
                    catagory = cf.catagory.get(item)
                    break
                
            if catagory is not None:
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
                if data["time"] != date.today().isoformat(): #Ngày lưu gần nhất có bằng với hiện tại không, nếu k thì call
                    # crawl dữ liệu (Chạy asynce)
                    # open mutual stream to crawl data
                    loop = asyncio.get_event_loop()
                    loop.create_task(crawl.product(path=catagory, name_j=catagory))
                
                #--> Tạo Template
                if len(data["data"]) > 0:
                    elements = []
                    for item in data["data"]:
                        #Mô tả giá
                        if item["price"].find("–") == -1 and item["price"].find(" ") > -1:
                            #Giá giảm
                            item["price"] = item["price"].replace(" ", " giảm còn ")
                        elif item["price"].find("–") > -1 and item["price"].find(" ") > -1:
                            #Trong khoảng
                            item["price"] = item["price"].replace("-", "đến")
                        #Mô tả sản phẩm
                        desc = {
                            "sen-da" : product_details.sen_da.get(item["name"]),
                            "dung-cu" : product_details.dung_cu.get(item["name"]),
                            "hat-giong-cu-qua" : product_details.cu_qua.get(item["name"]),
                            "hat-giong" : product_details.rau_xanh.get(item["name"])
                        }.get(catagory, "")

                        elements.append(
                            {
                                "title": item["name"],
                                "image_url": item["image"],
                                "subtitle": "Giá: " + item["price"] + " | Trạng thái: " + item["status"] + "| "+ desc,
                                "default_action": {
                                    "type": "web_url",
                                    "url": item["link"],
                                    "webview_height_ratio": "tall",
                                },
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url": item["link"],
                                        "title":"Xem thêm ..."
                                    },{
                                        "type":"postback",
                                        "title":"Mua ngay 🔥",
                                        "payload":"/ask_buy"
                                    }              
                                ]
                            }
                        )
                
                    #Respond to user
                    dispatcher.utter_message(
                        text = "THÔNG TIN SẢN PHẨM " + data["type"]
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
                        text = "Rất tiết hiện chúng tôi không có thông tin sản phẩm này:("
                    )
                if 'data' in locals(): del data

            else:
                dispatcher.utter_message(
                    text = "Rất tiết, loại sản phẩm bạn tìm không có :("
                )
            
            del catagory
            gc.collect()
            return []
        except Exception as error:
            print("-->Error<--")
            print(error)
            dispatcher.utter_message(text="Xin lỗi bạn, hiện tại hệ thông đang bị lỗi 😓😓😓")
            return [FollowupAction("act_accept_buy")]





""" Tư vấn chi tiết theo từng sản phẩm """
class act_tuvan_web_details(Action):

    def name(self) -> Text:
        return "act_tuvan_web_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # try:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        #1. Get name intent and then set condition to finding catagory 
        
        list_i, seek_i, catagory, time =  seek.product(intent = tracker.latest_message['intent']['name'], 
                                message = tracker.latest_message['text'].lower().replace("?",""))
        #--> Tạo Template
        elements = []
        
        if catagory is not None :
            if time != date.today().isoformat(): #Ngày lưu gần nhất có bằng với hiện tại không, nếu k thì call
                # crawl dữ liệu (Chạy asynce)
                # open mutual stream to crawl data
                loop = asyncio.get_event_loop()
                loop.create_task(crawl.product(path=catagory, name_j=catagory))
                
            if len(list_i) > 0:
                for item in list_i:
                    #Mô tả giá
                    if item["price"].find("–") == -1 and item["price"].find(" ") > -1:
                        #Giá giảm
                        item["price"] = item["price"].replace(" ", " giảm còn ")
                    elif item["price"].find("–") > -1 and item["price"].find(" ") > -1:
                        #Trong khoảng
                        item["price"] = item["price"].replace("-", "đến")
                    #Mô tả sản phẩm
                    desc = {
                        "sen-da" : product_details.sen_da.get(item["name"]),
                        "dung-cu" : product_details.dung_cu.get(item["name"]),
                        "hat-giong-cu-qua" : product_details.cu_qua.get(item["name"]),
                        "hat-giong" : product_details.rau_xanh.get(item["name"])
                    }.get(catagory, "")
                    
                    elements.append(
                        {
                            "title": item["name"],
                            "image_url": item["image"],
                            "subtitle": "Giá: " + item["price"] + "| Trạng thái: " + item["status"] + "| "+ desc,
                            "default_action": {
                                "type": "web_url",
                                "url": item["link"],
                                "webview_height_ratio": "tall",
                            },
                            "buttons":[
                                {
                                    "type":"web_url",
                                    "url": item["link"],
                                    "title":"Xem thêm ..."
                                },{
                                    "type":"postback",
                                    "title":"Mua ngay 🔥",
                                    "payload":"/ask_buy"
                                }              
                            ]      
                            #NOTE: Gửi API tới zalo cho mua ngay
                        }
                    )
                #Respond to user
                dispatcher.utter_message(
                    text = "THÔNG TIN SẢN PHẨM " + seek_i.upper()
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
            else: 
                    dispatcher.utter_message(
                        text = "Rất tiết hiện chúng tôi không có thông tin sản phẩm này:("
                    )
        else:
            dispatcher.utter_message(
                text = "Rất tiết, loại sản phẩm bạn tìm không có :("
            )
        
        del elements, seek_i, list_i, time
        gc.collect()
        return []
        # except Exception as error:
        #     print("-->Error<--")
        #     print(error)
        #     dispatcher.utter_message(text="Xin lỗi bạn, hiện tại hệ thông đang bị lỗi 😓😓😓")
        #     return [FollowupAction("act_accept_buy")]

