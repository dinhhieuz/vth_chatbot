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

from actions.act_help import conf as cf 
import json
from datetime import datetime, date, timedelta
import asyncio
import random

from actions.act_help.crawl import crawl


#!------------------------------------- BLOGS
''' MENU VỀ BLOGS'''
class act_blogs(Action):

    def name(self) -> Text:
        return "act_blogs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
            #----->

            button = [
                {
                    "type":"postback",
                    "title": "chăm sốc cây trồng",
                    "payload": "/ask_blog_care"
                },
                {
                    "type":"postback",
                    "title":"Công dụng của các loại rau quả",
                    "payload":"/ask_blog_use"
                },
                {
                    "type":"postback",
                    "title":"Vào bếp cùng Vũ Trụ Hạt",
                    "payload": "/ask_blog_cook"
                }
            ]

            dispatcher.utter_message(
                text = "Các gợi ý nhóm bài viết của Vũ Trụ Hạt: "
                , buttons = button
            )
            #--->
            button = [
                {
                    "type":"postback",
                    "title": "Ý nghĩa loại cây",
                    "payload": "/ask_blog_mean"
                },
                {
                    "type":"postback",
                    "title": "Bài viết mới nhất",
                    "payload": "/ask_blog_new"
                }
            ]

            dispatcher.utter_message(
                text = "đặt biệt hơn hết là..."
                , buttons = button
            )

            del button
            gc.collect()
            return []
        except Exception as error:
            print("-->Error<--")
            print(error)
            dispatcher.utter_message(text="Xin lỗi bạn, hiện tại hệ thông đang bị lỗi 😓😓😓")
            return [FollowupAction("act_accept_buy")]



'''ĐƯA DANH SÁCH CÁC BLOGS'''
class act_blogs_web(Action):

    def name(self) -> Text:
        return "act_blogs_web"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
            print(tracker.latest_message['intent']['name'])
            # Opening JSON file
            # returns JSON object as
            v_new = False
            catagory = None
            for item in cf.ctg_blog.keys():
                if tracker.latest_message['text'].lower().replace("?","").find(item) > -1:
                    catagory = cf.ctg_blog.get(item)
                    break
                elif tracker.latest_message['intent']['name'] == item:
                    catagory = cf.ctg_blog.get(item)
                    #--> Tìm tin mới nhất
                    if tracker.latest_message['intent']['name'] in ["ask_blog_use_new", "ask_blog_mean_new",  "ask_blog_cook_new",  "ask_blog_care_new"]:
                        v_new = True
                    break
                elif tracker.latest_message['intent']['name'] == "ask_blog_new":
                    # initializing list 
                    list = ["cong-dung-cua-cac-loai-rau-qua", "y-nghia-loai-cay", "vao-bep-cung-vu-tru-hat", "cham-soc-cay-trong"]
                    catagory = list[random.randint(0, len(list)-1)]
                    v_new = True
                    del list
                    break

            if catagory is not None:
                with open(f'./assets/data/blog/{catagory}.json', encoding='utf-8') as json_file:
                    data = json.load(json_file) #type: dict
                    """{
                        "type": "DỤNG CỤ LÀM VƯỜN",
                        "time": "2022-04-26",
                        "data": [{
                            "stt": 1,
                            "title": "Chuột Ăn Sen Đá? Top 5 Cách Phòng Chống Chuột Ăn Sen Đá Cực Hiệu Quả",
                            "desc": "Sen đá với vẻ đẹp nhỏ nhắn, đa dạng màu sắc cùng nhiều ý nghĩa...",
                            "link": "https://vutruhat.com/chuot-an-sen-da/",
                            "image": "https://vutruhat.com/wp-content/uploads/2021/11/sen_da_dot_bien_var_vu_tru_hat-min-711x400.jpg"
                        },
                            {...}
                    }"""

                #Kiểm tra cần call dữ liệu không

                # Nếu: ngày hiện tại = ngày crawl + 1 ngày thì mới crawl lại lần 2
                if data["time"] != date.today().isoformat():
                    # crawl dữ liệu (Chạy asynce)
                    # open mutual stream to crawl data
                    loop = asyncio.get_event_loop()
                    loop.create_task(crawl.blogs(name_j=catagory))

                #--> Tạo Template
                if len(data["data"]) > 0:
                    elements = []

                    for item in data["data"]:
                        elements.append(
                            {
                                "title": item["title"],
                                "image_url": item["image"],
                                "subtitle": item["desc"],
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
                                    }            
                                ]      
                            }
                        )
                        #--> Chỉ lấy 1 bài mới nhất
                        if v_new == True:
                            break

                    #Respond to user
                    dispatcher.utter_message(
                        text ='BÀI VIẾT VỀ "'+ data["type"].upper() + '"'
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
                    catagory = {
                        "cham-soc-cay-trong" : "CHĂM SỐC CÂY TRỒNG",
                        "cong-dung-cua-cac-loai-rau-qua" : "CÔNG DỤNG CỦA CÁC LOẠI RAU QUẢ",
                        "vao-bep-cung-vu-tru-hat" : "VÀO BẾP CÙNG VŨ TRỤ HẠT",
                        "y-nghia-loai-cay" : "Ý NGHĨA LOẠI CÂY"
                    }.get(catagory)
                    dispatcher.utter_message(
                        text = f"Rất tiết hiện chúng tôi không có bài viết cho {catagory.lower()} ☹️"
                    )

                if 'data' in locals(): del data

            else:
                dispatcher.utter_message(
                    text = "Rất tiết, loại bài viết bạn tìm không có :("
                )
            
            del catagory, v_new
            gc.collect()
            return []

        except Exception as error:
            print("-->Error<--")
            print(error)
            dispatcher.utter_message(text="Xin lỗi bạn, hiện tại hệ thông đang bị lỗi 😓😓😓")
            return [FollowupAction("act_accept_buy")]