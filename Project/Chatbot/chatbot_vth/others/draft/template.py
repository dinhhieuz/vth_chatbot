class template:
    def generic (data = [], type = ''):
        elements = []
        for i in data:
            subtitle = ""
            if type == 'khuyen_mai':
                subtitle = "Giá: " + i["price"].replace(" ", " giảm -> ") + "\nTrạng thái: " + i["status"]

            elements.append(
                {
                    "title": i["name"],
                    "image_url": i["image"],
                    "subtitle": subtitle,
                    "default_action": {
                        "type": "web_url",
                        "url": i["link"],
                        "webview_height_ratio": "tall",
                    },
                    "buttons":[
                        {
                            "type":"web_url",
                            "url": i["link"],
                            "title":"Xem thêm"
                        },{
                            "type":"postback",
                            "title":"Liên hệ admin để chốt đơn",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                        }              
                    ]      
                }
            )
        return {
                    "attachment":{
                        "type":"template",
                        "payload":{
                            "template_type":"generic",
                            "elements": elements
                        }
                    }
                }