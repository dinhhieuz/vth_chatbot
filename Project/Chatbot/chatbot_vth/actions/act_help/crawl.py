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
# option.add_experimental_option("excludeSwitches", ["enable-logging"])
#Chạy chương trình giả lập Chrome

class crawl:
    async def product(path, name_j):
        try:
            await asyncio.sleep(10)
            print("[class Crawl/product ->")
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
                                "name" : item[j+1].title(),
                                "price" : item[j+2],
                                "link" : IMAGE[IMAGE.find('href="')+6:IMAGE.find('">')],
                                "image" : img[:(img.find('jpg') if img.find('jpg') > -1 else img.find('png')) +3],
                                "status" :  "Hết hàng" if len(item) == 5 else "Còn hàng",
                            }
                        )
                        print("\t 1+ data: "+  catagory.get(path))
                    # Đóng trình duyệt
                    browser.close()

            with open(f"./assets/data/product/{name_j}.json","w", encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)
                
            print("[class: crawl/product] -> Done")
        except:
            print("[class: crawl/product] -> Lỗi crawl dữ liệu ")


    ''' Crawl BLOGS'''
    async def blogs():
        try:
            await asyncio.sleep(10)
            print("[class Crawl/blogs ->")
            #content
            print("[class: crawl/blogs] -> Done")
        except:
            #error
            print("[class: crawl/blogs] -> Lỗi crawl dữ liệu ")