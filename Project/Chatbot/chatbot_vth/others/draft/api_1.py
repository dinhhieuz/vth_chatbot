from asyncio.windows_events import NULL
from matplotlib import image
from selenium import webdriver
from time import sleep
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json


# Không hiển thị
option = webdriver.ChromeOptions()
option.add_argument('headless')
#turn off log of selenium

# option.add_experimental_option("excludeSwitches", ["enable-logging"])

#Chạy chương trình giả lập Chrome

#Truy cập trang web
def product(path, name_j):
    print("[Crawl] Product ->")
    catagory = {
                "sen-da" : "SEN ĐÁ",
                "dung-cu" : "DỤNG CỤ LÀM VƯỜN",
                "hat-giong-cu-qua" : "HẠT GIỐNG CỦ QUẢ",
                "hat-giong" : "HẠT GIỐNG RAU XANH"
            }
    data ={ 
        "type": catagory.get(path), 
        "time" : date.today().isoformat(),
        "data": []
    } 
    for num_page in range(1,100):
        browser = webdriver.Chrome(executable_path="D:\\Năm 4 - Thực tập tốt nghiệp\\Project\\Chatbot\\chatbot_vth\\others\\chromedriver", options=option)
        browser.get(f"https://vutruhat.com/danh-muc/{path}/page/{num_page}/")
        if browser.title.find("Không tìm thấy trang") > -1:
            break
        else:
            # list_item = browser.find_element_by_class_name("col-inner")
            # list_item = browser.find_elements_by_xpath("//div[@class='col-inner'")
            # driver.find_element_by_xpath("//form[@id='loginForm']")
            sleep(1.5)
            list_item = browser.find_elements(By.XPATH, "//div[@class='product-small box ']")

            for i in list_item:
                item = i.text.split("\n")
                
                #! IMAGE
                IMAGE = i.find_element(By.CLASS_NAME, "image-none").get_attribute('innerHTML')
                #! LINK
                j = 1 if len(item) == 5 else 0

                img = IMAGE[IMAGE.find('srcset="')+8:]
                data["data"].append(
                    {
                        "name" : item[j+1],
                        "price" : item[j+2],
                        "link" : IMAGE[IMAGE.find('href="')+6:IMAGE.find('">')],
                        "image" : img[:(img.find('jpg') if img.find('jpg') > -1 else img.find('png')) +3],
                        "status" :  "Hết hàng" if len(item) == 5 else "Còn hàng",
                    }
                )
                print("\t 1+ data: "+  catagory.get(path))
            # Đóng trình duyệt
            browser.close()

    with open(f"{name_j}.json","w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# product("sen-d
#---------------------------------------------------------------------------
catagory = {
        "sen-da" : "CHĂM SỐC CÂY TRỒNG",
        "dung-cu" : "CÔNG DỤNG CỦA CÁC LOẠI RAU QUẢ",
        "hat-giong-cu-qua" : "VÀO BẾP CÙNG VŨ TRỤ HẠT",
        "hat-giong" : "Ý NGHĨA LOẠI CÂY"
    }

data ={ 
    "type": "Ý NGHĨA LOẠI CÂY", 
    "time" : date.today().isoformat(),
    "data": []
} 

browser = webdriver.Chrome(executable_path="D:\\Năm 4 - Thực tập tốt nghiệp\\Project\\Chatbot\\chatbot_vth\\others\\chromedriver", options=option)
browser.get(f"https://vutruhat.com/category/y-nghia-loai-cay/")
#Đợi load
sleep(2)

num = 1
for i in browser.find_elements(By.XPATH, "//a[@class='plain']"):
    #---> IMAGE
    IMAGE = i.find_element(By.CLASS_NAME, "image-cover").get_attribute('innerHTML')
    IMAGE = IMAGE[IMAGE.find('srcset="')+8:]
    # Tìm loại thích hợp vs đui ảnh
    if IMAGE.find('jpg') > -1:
        f = IMAGE.find('jpg') + 3
    elif IMAGE.find('png') > -1:
        f = IMAGE.find('png') + 3
    elif IMAGE.find('jpeg') > -1:
        f = IMAGE.find('jpeg') + 4
    #!

    data["data"].append(
        {
            "stt" : num,
            "title" : i.find_element(By.TAG_NAME, "h5").text,
            "desc" : i.find_element(By.TAG_NAME, "p").text.replace("[...]","...").rstrip(),
            "link" : i.get_attribute('href'),
            "image" : IMAGE[:f]
        }
    )
    num += 1

browser.close()
with open(f"dungcu.json","w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

#1 . stt (tăng dần)
#2. Tên tiêu đề
#3. Mô tả
#4. Hình ảnh 
# 5. Link



#----RUN
# """

#         D:\Năm 4 - Thực tập tốt nghiệp\Project\Chatbot\chatbot_vth\others\draft
#         conda activate rasa-chatbot
#         python api_1.py

# """