from asyncio.windows_events import NULL
from matplotlib import image
from selenium import webdriver
from time import sleep
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
#mutil stream
import asyncio

# Không hiển thị
option = webdriver.ChromeOptions()
option.add_argument('headless')
#turn off log of selenium
option.add_experimental_option("excludeSwitches", ["enable-logging"])
#Chạy chương trình giả lập Chrome
class crawl:
    async def product(path, name_j):
        try:
            await asyncio.sleep(5)
            print("[class Crawl/product ->")
            catagory = {
                "sen-da" : "SEN ĐÁ",
                "dung-cu" : "DỤNG CỤ LÀM VƯỜN",
                "hat-giong-cu-qua" : "HẠT GIỐNG CỦ QUẢ",
                "hat-giong" : "HẠT GIỐNG RAU XANH"
            }.get(path)
            data ={ 
                "type": catagory, 
                "time" : date.today().isoformat(),
                "data": []
            } 
            for num_page in range(1,100):
                browser = webdriver.Chrome(
                    # executable_path="D:\\Năm 4 - Thực tập tốt nghiệp\\Project\\Chatbot\\chatbot_vth\\others\\chromedriver", 
                    executable_path="D:\\HieuCali\\File of Hieu\\Project\\DSA Company\\Project\\ChatBox_RASA\\Chatbot_Vutruhat\\vth_chatbot\\Project\\\Chatbot\\chatbot_vth\\others\\serv\\chromedriver", 
                    options=option)
                browser.get(f"https://vutruhat.com/danh-muc/{path}/page/{num_page}/")
                if browser.title.find("Không tìm thấy trang") > -1:
                    browser.close()
                    break
                else:
                    sleep(2)
                    for i in browser.find_elements(By.XPATH, "//div[@class='product-small box ']"):
                        #get value
                        item = i.text.split("\n")
                        
                        #! IMAGE
                        img = i.find_element(By.CLASS_NAME, "image-none").find_element(By.TAG_NAME, "img").get_attribute('src')
                        if img.find('jpg') > -1:
                            img[img.find("https://")+8::img.find('jpg') + 3]
                        elif img.find('png') > -1:
                            img[img.find("https://")+8::img.find('png') + 3]
                        elif img.find('jpeg') > -1:
                            img[img.find("https://")+8::img.find('jpeg') + 4]

                        #! LINK
                        j = 1 if len(item) == 5 else 0

                        # img = IMAGE[IMAGE.find('srcset="')+8:]
                        data["data"].append(
                            {
                                "name" : item[j+1].title(),
                                "price" : item[j+2],
                                "link" : i.find_element(By.CLASS_NAME, "image-none").find_element(By.TAG_NAME, "a").get_attribute('href'),
                                "image" : img,

                                "status" :  "Hết hàng" if len(item) == 5 else "Còn hàng",
                            }
                        )
                        print("\t 1+ data: "+  catagory)
                    # Đóng trình duyệt
                    browser.close()

            with open(f"./assets/data/product/{name_j}.json","w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)
                
            print("[class: crawl/product] -> Done")
        except Exception as error:
            print(error)
            print("[class: crawl/product] -> Lỗi crawl dữ liệu ")


    ''' Crawl BLOGS'''
    async def blogs(name_j):
        try:
            await asyncio.sleep(5)
            print("[class Crawl/blogs ->")
            #Lấy loại blogs
            catagory = {
                    "cham-soc-cay-trong" : "CHĂM SỐC CÂY TRỒNG",
                    "cong-dung-cua-cac-loai-rau-qua" : "CÔNG DỤNG CỦA CÁC LOẠI RAU QUẢ",
                    "vao-bep-cung-vu-tru-hat" : "VÀO BẾP CÙNG VŨ TRỤ HẠT",
                    "y-nghia-loai-cay" : "Ý NGHĨA LOẠI CÂY"
                }.get(name_j)
            #Tạo nơi lưu dữ liệu
            data ={ 
                "type": catagory, 
                "time" : date.today().isoformat(),
                "data": []
            } 
            print(catagory)
            browser = webdriver.Chrome(executable_path="D:\\Năm 4 - Thực tập tốt nghiệp\\Project\\Chatbot\\chatbot_vth\\others\\chromedriver", options=option)
            browser.get(f"https://vutruhat.com/category/{name_j}/")
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
                #thêm dữ liệu
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
                print("\t 1+ data: "+  catagory)

            browser.close()
            with open(f"./assets/data/blog/{name_j}.json","w", encoding='utf-8') as jsonfile:
                    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

            print("[class: crawl/blogs] -> Done")
        except Exception as error:
            print(error)
            print("[class: crawl/blogs] -> Lỗi crawl dữ liệu ")