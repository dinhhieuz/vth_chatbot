from actions.act_help import conf as cf
import json
from collections import Counter
import numpy as np

class seek:
    def khuyenmai(intent='', message = ''):
        catagory = cf.catagory.get(intent)
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
            cart = []
            
            list_i = {
                "sen-da" : cf.item_senda,
                "dung-cu" : cf.item_dungcu,
                "hat-giong-cu-qua" : cf.item_cuqua,
                "hat-giong-rau-xanh" : cf.item_rauxanh
            }.get(catagory)

            seek_i = ''
            # Lấy list danh sách đã thiết lập từ trước lấy key ra tìm trong message xem có bao nhiêu keys được tìm thấy
            for item in list_i:
                # Vì đang mang là mãng key dict k phải string nên vì thế nhóm lại bằng join để biến thành chuổi
                if message.find("".join(item.keys())) > -1:
                    cart.append("".join(item.values()))
                    if seek_i == '': seek_i = "".join(item.keys())
            # Khi đã có tên sản phẩm, t unique để tránh trùng lập lại sản phẩm
            cart = np.array(cart)
            # Lấy thông tin sản phẩm trong file từ tên đã tìm được 
            found_i = []
            for item in np.unique(cart):
                for inf_i in data["data"]:
                    if inf_i["name"] == item:
                        found_i.append(inf_i)
            return found_i, seek_i, catagory, data["time"]
        else:
            return [], '', None, ''

    ''' Tìm sản phẩm '''
    def tuvan():
        '''
                *hỏi theo sản phẩm*
            - khi khách hàng hỏi 1 sản phẩm cụ thể, ví dụ mình sẽ xuất hết thông tin như khuyến mãi
            có điều sẽ được thêm vài thông tin như đánh giá và v.v 
            (Vẫn làm như khuyến mãi sản phẩm và chi tiết sản phẩm)

                *hỏi chi tiết theo sản phẩm*
            - Khách hàng hỏi chi tiết thì sẽ lấy cái link sản phẩm đấy (Truyền cái link vào bên trong button để xác định sản phẩm)
            sau đó lấy link để crawl thông tin chi tiết của sản phẩm về cái ni sẽ giống khuyến mãi
                
                *hỏi chi tiết sa (So sánh chuỗi) (TÌm cách)
            - sử dụng thông tin chi tiết ứng với sản phẩm để tư vấn dựa trên câu hỏi sản phẩm mình tư vấn (bỏ chung thông tin vào 1 mãng để dể join())
            - Nhứ bỏ phần đánh giá để dể hình dung tăng số sao the for ()
            - khi lấy được sản phẩm thì 
                * Chia ra thành nhiều nhóm câu hỏi liên quan đến nhóm sản phẩm
                (Sử lý từng câu hỏi)
                ** Tư vấn ** chưa biết nên mua loại cây nào
                ** tư vấn ** chưa biết nên mua dụng cụ nào
                Các loại tư vấn này sữ dụng [https://developers.facebook.com/docs/messenger-platform/reference/buttons/quick-replies]
                Thu thập dữ liệu đủ cho 1 cái cây rồi từ đó xem các thuộc tính trùng với nhóm cây nào thì lấy ra
                
        '''
        return None
                    