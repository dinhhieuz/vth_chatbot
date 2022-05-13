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
from requests import delete


class act_chat_greating(Action):

    def name(self) -> Text:
        return "act_chat_greating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        #----->

        button = [
            {
                "type":"postback",
                "title": "Chính Sách",
                "payload": "làm sao để hiểu được chính sách của VTH"
            },
            {
                "type":"postback",
                "title":"📞 Liên hệ nhân sự",
                "payload":" Liên hệ phòng nhân sự"
            },
            {
                "type":"postback",
                "title":"Khuyến Mãi",
                "payload": "/ask_khuyenmai_menu"
            }
        ]

        dispatcher.utter_message(
            text = "Xin chào Vũ Trụ Hạt rất vui được nói chuyện với bạn!!!\nChúng tôi có thể giúp gì cho bạn nào"
            , buttons = button
        )
        # #---> Generic Template 
        # res = {
        #     "attachment":{
        #         "type":"template",
        #         "payload":{
        #             "template_type":"generic",
        #             "elements":[
        #                 {
        #                     "title":"cái ni là gì 1",
        #                     "image_url":"https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
        #                     "subtitle":"Đây là tiêu đề 1",
        #                     "default_action": {
        #                         "type": "web_url",
        #                         "url": "https://www.originalcoastclothing.com/",
        #                         "webview_height_ratio": "tall",
        #                     },
        #                     "buttons":[
        #                         {
        #                             "type":"web_url",
        #                             "url":"https://www.originalcoastclothing.com/",
        #                             "title":"button 1"
        #                         },{
        #                             "type":"postback",
        #                             "title":"số button 2",
        #                             "payload":"DEVELOPER_DEFINED_PAYLOAD"
        #                         }              
        #                     ]      
        #                 },
        #                 {
        #                     "title":"cái ni là gì 2",
        #                     "image_url":"https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
        #                     "subtitle":"Đây là tiêu đề 2.",
        #                     "default_action": {
        #                         "type": "web_url",
        #                         "url": "https://www.originalcoastclothing.com/",
        #                         "webview_height_ratio": "tall",
        #                     },
        #                     "buttons":[
        #                         {
        #                             "type":"web_url",
        #                             "url":"https://www.originalcoastclothing.com/",
        #                             "title":"View Website"
        #                         },{
        #                             "type":"postback",
        #                             "title":"Start Chatting",
        #                             "payload":"DEVELOPER_DEFINED_PAYLOAD"
        #                         }              
        #                     ]      
        #                 }
        #             ]
        #         }
        #     }
        # }
        # dispatcher.utter_message(json_message = res)

        # #--> Receipt template
        # res = {
        #     "attachment":{
        #         "type":"template",
        #         "payload":{
        #             "template_type":"receipt",
        #             "recipient_name":"Stephane Crozatier",
        #             "order_number":"12345678902",
        #             "currency":"USD",
        #             "payment_method":"Visa 2345",        
        #             "order_url":"http://originalcoastclothing.com/order?order_id=123456",
        #             "timestamp":"1428444852",         
        #             "address":{
        #                 "street_1":"1 Hacker Way",
        #                 "street_2":"",
        #                 "city":"Menlo Park",
        #                 "postal_code":"94025",
        #                 "state":"CA",
        #                 "country":"US"
        #             },
        #             "summary":{
        #             "subtotal":75.00,
        #             "shipping_cost":4.95,
        #             "total_tax":6.19,
        #             "total_cost":56.14
        #             },
        #             "adjustments":[
        #                 {
        #                     "name":"New Customer Discount",
        #                     "amount":20
        #                 },
        #                 {
        #                     "name":"$10 Off Coupon",
        #                     "amount":10
        #                 }
        #             ],
        #             "elements":[
        #             {
        #                 "title":"Classic White T-Shirt",
        #                 "subtitle":"100% Soft and Luxurious Cotton",
        #                 "quantity":2,
        #                 "price":50,
        #                 "currency":"USD",
        #                 "image_url":"http://originalcoastclothing.com/img/whiteshirt.png"
        #             },
        #             {
        #                 "title":"Classic Gray T-Shirt",
        #                 "subtitle":"100% Soft and Luxurious Cotton",
        #                 "quantity":1,
        #                 "price":25,
        #                 "currency":"USD",
        #                 "image_url":"http://originalcoastclothing.com/img/grayshirt.png"
        #             }
        #             ]
        #         }
        #     }
        # }
        # dispatcher.utter_message(json_message = res)

        # #--> Feedback
        # res = {
        #     "attachment": {
        #         "type": "template",
        #         "payload": {
        #             "template_type": "customer_feedback",
        #             "title": "Rate your experience with Original Coast Clothing.",
        #             "subtitle": "Let Original Coast Clothing know how they are doing by answering two questions",
        #             "button_title": "Rate Experience",
        #             "feedback_screens": [{
        #             "questions":[{
        #                 "id": "hauydmns8",
        #                 "type": "csat",
        #                 "title": "How would you rate your experience with Original Coast Clothing?",
        #                 "score_label": "neg_pos",
        #                 "score_option": "five_stars",
        #                 "follow_up":
        #                 {
        #                 "type": "free_form", 
        #                 "placeholder": "Give additional feedback"
        #                 }
        #             }]
        #             }],
        #             "business_privacy": 
        #             {
        #                 "url": "https://www.google.com.vn/?hl=vi"
        #             },
        #             "expires_in_days" : 3
        #         }
        #     }
        # }
        # res ={
        #     "attachment":{
        #     "type":"template",
        #     "payload":{
        #         "template_type":"generic",
        #         "elements":[
        #         {
        #             "title":"Welcome!",
        #             "image_url":"https://raw.githubusercontent.com/fbsamples/original-coast-clothing/main/public/styles/male-work.jpg",
        #             "subtitle":"We have the right hat for everyone.123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789",
        #             "default_action": {
        #             "type": "web_url",
        #             "url": "https://www.originalcoastclothing.com/",
        #             "webview_height_ratio": "tall",
        #             },
        #             "buttons":[
        #             {
        #                 "type":"web_url",
        #                 "url":"https://www.originalcoastclothing.com/",
        #                 "title":"View Website"
        #             },{
        #                 "type":"postback",
        #                 "title":"Start Chatting",
        #                 "payload":"DEVELOPER_DEFINED_PAYLOAD"
        #             }              
        #             ]      
        #         }
        #         ]
        #     }
        #     }
        # }
        # dispatcher.utter_message(json_message = res)
        gc.collect()
        return []



#!-------------------------------------FALL BACK
class act_unknown(Action):

    def name(self) -> Text:
        return "act_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
 
        #--> Không hiểu tra Google
        messeger_user = tracker.latest_message['text']
        url = "https://www.google.com.vn/search?q='" + messeger_user.replace(" ", "%20") + "'"
        search = {
            "type": "web_url",
            "url": f"{url}",
            "title": "Search Google",
        }
        dispatcher.utter_message(
            text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để tôi nhờ chị Google giải đáp nhé: "
            , buttons= [search])
        
        del url, search, messeger_user

        gc.collect()
        return []
