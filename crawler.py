from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
import csv
import os
from tqdm import tqdm
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time

START = 157
END = 1000
# service = r"C:\Users\Admin\Documents\code\crawler\geckodriver-v0.32.0-win32\geckodriver.exe"
service = r'C:\Users\Admin\Documents\code\crawler\chromedriver_win32\chromedriver.exe'
columns = [
    "Diện tích đất:",
    "Số phòng ngủ:",
    "Số phòng vệ sinh:",
    "Giấy tờ pháp lý:",
    "Loại hình nhà ở:",
    "Chiều ngang:",
    "Diện tích sử dụng:",
    "Giá/m2",
    "Hướng cửa chính:",
    "Tổng số tầng:",
    "Đặc điểm nhà/đất",
    "Tình trạng nội thất:",
    "Chiều dài",
    "Location",
    "Name",
    "URL",
    "Price",
]
locations = {
    'Ha Noi':"https://www.nhatot.com/mua-ban-nha-dat-ha-noi",
    # 'Ho Chi Minh':"https://www.nhatot.com/mua-ban-nha-dat-tp-ho-chi-minh",
    # "https://www.nhatot.com/mua-ban-nha-dat-da-nang",
}


# class House:
#     def __init__(self):
#         super()
#         # self.location:str= ''
#         self.name: str = ""
#         self.url: str = ""
#         self.area: str = ""
#         self.price: str = ""
#         self.bedroom_amount: str = ""
#         self.bathroom_amount: stfrom selenium.webdriver.firefox.options import Options


#         self.floor_amount: str = ""
#         self.legal_document: str = ""
#         self.land_feature: str = ""
#         self.type: str = ""
#         self.furnish_status: str = ""
#         self.location: str = ""
#         self.length: str = ""
#         self.width: str = ""
#         self.living_area: str = ""
#         self.main_door_direction: str = ""options = Options()

#         self.house_type: str = ""
#         self.price_per_m2: str = ""

# self.dict =
# def setter(self, label, data):
#     if label == columns[0]:
#         self.area = data
#         return
#     if label == columns[1]:
#         self.bedroom_amount = data
#         return
#     if label == columns[2]:
#         self.bathroom_amount = data
#         return
#     if label == columns[3]:
#         self.legal_document = data
#         return
#     if label == columns[4]:
#         self.house_type = data
#         return
#     if label == columns[5]:
#         self.width = data
#         return
#     if label == columns[6]:
#         self.living_area = data
#         return
#     if label == columns[7]:
#         self.price_per_m2 = data
#         return
#     if label == columns[8]:
#         self.main_door_direction = data
#         return
#     if label == columns[9]:
#         self.floor_amount = data
#         return
#     if label == columns[10]:
#         self.land_feature = data
#         return
#     if label == columns[11]:
#         self.furnish_status = data
#         return
#     if label == columns[12]:
#         self.length = data
#         return
# def getter(self):
#     pass
# if label =


def setter(house, label, data):
    if label in columns:
        house[label] = data

# options = Options()
# options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
# options.binary_location = r'"C:\Program Files\Mozilla Firefox\firefox.exe"'
# options.headless = False

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

for location,url_cho_tot in locations.items():
    print(url_cho_tot)
    path = f'./data/{location}'
    if not os.path.exists(path):
        os.mkdir(path)

    for page in tqdm(range(START, END + 1),position=0):
        # driver = webdriver.Firefox(executable_path=service,options=options)
        driver = webdriver.Chrome(executable_path=service,options=chrome_options)
        driver.get(f"{url_cho_tot}?page={page}")
        items = driver.find_elements(By.CLASS_NAME, "AdItem_adItem__gDDQT")
        urls = [str(item.get_attribute("href")) for item in items]
        driver.close()
        csv_file = open(path+f'/page_{page}.csv','w',encoding='utf8')
        writer = csv.DictWriter(csv_file,columns)
        writer.writeheader()
        for url in tqdm(urls,position=1,leave=False):
            # subdriver = webdriver.Firefox(executable_path=service,options=options)

            subdriver = webdriver.Chrome(executable_path=service,options=chrome_options)
            subdriver.get(url)
            try:
                info = subdriver.find_elements(
                    By.CLASS_NAME, "DetailView_adviewPtyItem__V_sof"
                )[1]
                house = {}
                for c in columns:
                    house[c] = ''
                house["Location"] = location
                house["URL"] = url
                house["Price"] = subdriver.find_elements(
                    By.CLASS_NAME,
                    'AdDecriptionVeh_price__u_N83'
                )[0].text
                house["Name"] = subdriver.find_elements(
                    By.CLASS_NAME, "AdDecriptionVeh_adTitle__vEuKD"
                )[0].text
                
                try:
                    btn = WebDriverWait(info, 3).until(
                EC.element_to_be_clickable((By.TAG_NAME, "button"))
            )       
                    btn.click()
                    # print(element)
                except:
                    pass
                finally:
                    pass


                try:
                    details = WebDriverWait(info, 3).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "AdParam_adMediaParam__3epxo"))
        )       
                    # details = subdriver.find_elements(
                    #     By.CLASS_NAME, "AdParam_adMediaParam__3epxo"
                    # )
                    if len(details) > 0:
                        for detail in details:
                            _, label, data = detail.find_elements(By.TAG_NAME, "span")
                            setter(house, label.text, data.text)
                except:
                    pass
                finally:
                    writer.writerow(house)
            except:
                print(url)
            finally:    
                subdriver.close()
            # print(house)
            # break
        csv_file.close()
