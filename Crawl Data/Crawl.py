import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os

def Edit(weather):
    weather = weather.split(' ')
    weather[0] = weather[0][:-2]
    weather[1] = weather[1][:-1]
    weather[2] =  weather[2][:-3]
    weather[3] =  weather[3][:-3]
    return weather

def extract_row(values):
    result = []
    for value in values:
        result.append(value.text)
    result.pop(0)
    return result

def request_WEB(browser, Stations):
    '''browser là cái driver 
       date mặc định là 0: hôm nay 1: hôm qua 2: hôm kia 
    '''
    #Stations = ['Cao Bằng: Trạm khí TTQT phường Sông Hiến (KK)','Phú Thọ: đường Hùng Vương - Tp Việt Trì (KK)','Thái nguyên: Đường Hùng Vương - Tp Thái Nguyên (KK)','Hà Nội: 556 Nguyễn Văn Cừ (KK)','Bắc Ninh: gần KCN Quế Võ - Tp Bắc Ninh (KK)','Hưng Yên: Sở TNMT - 437 Nguyễn Văn Linh, Tp Hưng Yên (KK)','Quảng Ninh: Phường Cẩm Thịnh - Cẩm Phả (KK)']
    select = Select(browser.find_element_by_id('cbbStations'))
    data_per_date = []
    for stat in Stations: 
        data_per_hour = []
        select.select_by_visible_text(stat)
        time.sleep(10)
        
        Province = browser.find_element_by_id('station_province').text.split(':')[-1].strip()
        data_per_hour.append(Province)
        longlat = browser.find_element_by_id('longlat').text.split(' ')
        data_per_hour.append((longlat[2],longlat[6]))
        weather = browser.find_element_by_class_name('weather').text
        data_per_hour.extend(Edit(weather))
        
        soup=BeautifulSoup(browser.page_source,'html.parser')
        table= soup.find('table',{'id': 'custom_datatable_1'})
        body = table.find('tbody')
        lastest_hour = body.find('tr')
        values = lastest_hour.find_all('td')
        data_per_hour.extend(extract_row(values))
        
        data_per_date.append(data_per_hour)
        
        
    return data_per_date
def ba_mien(Mien):
    the_file = 0
    Stations = []
    
    if Mien == 1:
        name = "aqi_MienBac.txt"
        if os.path.exists('./aqi_MienBac.txt') == False:
            the_file = open(name,'a',encoding='utf-8')
            the_file.write("Tỉnh\tVị trí\tNhiệt độ\tĐộ ẩm\tTốc độ gió\tÁp suất\tNgày giờ\tVN_AQI\tNO2\tO3\tPM-10\tPM-2-5\tSO2" + '\n')
        the_file = open(name,'a',encoding='utf-8')
        Stations = ['Gia Lai: TTQT TN&MT - P.Thống Nhất - TP Pleiku (KK)','Đà Nẵng: 41 đường Lê Duẩn (KK)','Cao Bằng: Trạm khí TTQT phường Sông Hiến (KK)','Phú Thọ: đường Hùng Vương - Tp Việt Trì (KK)','Thái nguyên: Đường Hùng Vương - Tp Thái Nguyên (KK)','Hà Nội: 556 Nguyễn Văn Cừ (KK)','Bắc Ninh: gần KCN Quế Võ - Tp Bắc Ninh (KK)','Hưng Yên: Sở TNMT - 437 Nguyễn Văn Linh, Tp Hưng Yên (KK)','Quảng Ninh: Phường Cẩm Thịnh - Cẩm Phả (KK)']
        
    if Mien == 2:
        name = "aqi_MienTrung.txt"
        if os.path.exists('./aqi_MienTrung.txt') == False:
            the_file = open(name,'a',encoding='utf-8')
            the_file.write("Tỉnh\tVị trí\tNhiệt độ\tĐộ ẩm\tTốc độ gió\tÁp suất\tNgày giờ\tVN_AQI\tPM-10\tPM-2-5" + '\n')
        the_file = open(name,'a',encoding='utf-8')
        Stations = ['Nghệ An: Trường Thi, Thành phố Vinh - KTTV (KK)']
    
    if Mien == 3:
        name = "aqi_MienNam.txt"
        if os.path.exists('./aqi_MienNam.txt') == False:
            the_file = open(name,'a',encoding='utf-8')
            the_file.write("Tỉnh\tVị trí\tNhiệt độ\tĐộ ẩm\tTốc độ gió\tÁp suất\tNgày giờ\tVN_AQI\tPM-10\tPM-2-5" + '\n')
        the_file = open(name,'a',encoding='utf-8')
        Stations = ['Tp Hồ Chí Minh: Đường Nguyễn Văn Tạo, Ấp 3, Nhà Bè - KTTV (KK)','Cần Thơ: Ninh Kiều - KTTV (KK)']
    
    data_all_station = request_WEB(browser,Stations)
    for data in data_all_station:
        the_file.write('\t'.join(str(v) for v in data) + '\n')
    the_file.close()

#Vào trang
URL = 'http://enviinfo.cem.gov.vn/'
browser = webdriver.Chrome(executable_path='./chromedriver.exe') 
browser.maximize_window()
browser.get(URL)
time.sleep(7)
browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[3]/div[1]/div[1]/div/div[1]/div/div[1]/div[1]').click()
container = browser.find_element_by_id("cbbStations")
browser.execute_script("arguments[0].style.display = 'block';", container)

ba_mien(1)
ba_mien(2)
ba_mien(3)

browser.close()