import find_1 as cf
import json

catagory = cf.catagory.get("ask_khuyenmai_dungcu_details")

with open(f'D:/Năm 4 - Thực tập tốt nghiệp/Project/Chatbot/chatbot_vth/assets/data/discount/{catagory}.json', encoding='utf-8') as json_file:
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

message = "Hôm nay bình xịt có giảm giá không nhỉ"
found_i = []
a = cf.item_dungcu
for item in a:
    # Vì đang mang là mãng key dict k phải string nên vì thế nhóm lại bằng join để biến thành chuổi
    if message.find("".join(item.keys())) > -1:
        for inf_i in data["data"]:
            if inf_i["name"] == "".join(item.values()):
                print(inf_i)


    