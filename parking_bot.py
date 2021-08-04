# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 12:18:05 2021

@author: макс

Бот жалоб на парковку
"""
import logging
import asyncio
import requests
import time
from datetime import datetime
from time import sleep
import sys
import base64
from base64 import b64encode
import requests
from PIL import Image
from io import BytesIO

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


import time
import random

import sys
import os
from twocaptcha import TwoCaptcha
import urllib

from pytz import utc,timezone,country_timezones



url_moked = "https://www.rishonlezion.muni.il/Residents/Moked/Pages/Moked-Open.aspx"
url_with_captcha = 'https://www.rishonlezion.muni.il/_layouts/15/GetSignatureImage.aspx'
xpath_rehov =  '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedReportStreetText"]'
xpath_house_number = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedReportHouseNumber"]' 
xpath_complain_window = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedDetails"]'
xpath_surname = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedLastName"]'
xpath_rehov_complainer = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedStreetText"]'
xpath_areacode = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtAreaCodesPhoneText"]'
xpath_phone = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedPhone"]'
xpath_firstname_complainer = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedFirstName"]'
xpath_bait_of_complainer = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedHouseNumber"]'
xpath_email = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedEmail"]'
xpath_captcha_code = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_ctl52_Captcha_Image"]'
xpath_captcha_window = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_ctl52_Captcha_Input"]'
xpath_button_send_form = '/html/body/form/div[5]/main/div[3]/div/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/table/tbody/tr/td[1]/button'
xpath_telefon_nusaf = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedMobilePhone"]'

key = "c844c15198652c277892e5f9a4b35028"

form_data = {
        'rehov':"החייל האלמוני",
        'house_number':"6",
        'teur_tluna':"רכבים לא מאזור חונים. מבקש לטפל. תודה",
        'surname':"ס",
        'name':"מקס",
        'rehov_of_complainer':"החייל האלמוני",
        'bait_of_complainer':"7",
        'telefon_of_complainer':"0526180349",
        'area_code':'052',
        'telefon_without_area_code': '6180349',
        'email_of_complainer':"maximbt@gmail.com"
        
        }

class Get_Data:
    
    
    def log(s,t=None):
            now = datetime.now()
            if t == None :
                    t = "Main"
            print ("%s :: %s -> %s " % (str(now), t, s)) 
            
    def httpbin():
        
        api_key = "c844c15198652c277892e5f9a4b35028"
        solver = TwoCaptcha(api_key)
        captcha_image_url = 'https://www.rishonlezion.muni.il/_layouts/15/GetSignatureImage.aspx'
        response = requests.get(captcha_image_url)
        img = Image.open(BytesIO(response.content))
        img_saved = img.save('captcha.jpg')
        
        with open('captcha.jpg', 'rb') as f:
            b64 = b64encode(f.read()).decode('utf-8')
            
        headers = {
                'action' : 'http://2captcha.com/in.php',
                'method' : 'base64',
                'key' : 'c844c15198652c277892e5f9a4b35028',
                'body' : b64
                               
                }
        
        response = requests.post('http://httpbin.org/post', headers) 
        response.json()

                
    
    def twocaptcha():
        api_key = "c844c15198652c277892e5f9a4b35028"
        solver = TwoCaptcha(api_key)
        captcha_image_url = 'https://www.rishonlezion.muni.il/_layouts/15/GetSignatureImage.aspx'
        response = requests.get(captcha_image_url)
        img = Image.open(BytesIO(response.content))
        img_saved = img.save('captcha.jpg')
        captcha_image = Image.open(r'captcha.jpg')
               
        with open('captcha.jpg', 'rb') as f:
            b64 = b64encode(f.read()).decode('utf-8')
        
        try:
            result = solver.normal('C:\temp\captcha.jpg')
            solver.normal(b64)
            solve1 = TwoCaptcha(api_key)
            solve1.solve_captcha(b64,captcha_image_url)
            solver.solve_captcha(b64)
        
        except Exception as e:
            sys.exit(e)
        
        else:
            sys.exit('result: ' + str(result))
        
   
    def setup_selenium(self,url):
        
        self.log("setup selenium")
        options = webdriver.FirefoxOptions()
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True
        
        binary = FirefoxBinary(os.environ.get("FIREFOX_BIN"))
        #binary = FirefoxBinary(r"C:\Users\макс\AppData\Local\Mozilla Firefox\firefox.exe")
        options = Options()
        options.set_headless(headless=False)
        options.binary = binary
        #fp_profile = r"C:\Users\макс\AppData\Local\Mozilla\Firefox\Profiles\v6axkke0.default"
        #fp = webdriver.FirefoxProfile(fp_profile)
        #profile = webdriver.FirefoxProfile(fp) 
        #firefox_profile=fp        
        #driver = webdriver.Firefox(firefox_options=options,options=options,capabilities=capabilities, executable_path = os.environ.get('GECKODRIVER_PATH'))
        driver = webdriver.Firefox(firefox_options=options,options=options,capabilities=capabilities, executable_path ='geckodriver')
        driver.set_window_size(1280, 1024)
        
        driver.get(url)
        
        
        return driver  
    
       
    
    def captcha_bypass(self,driver,url_with_captcha,key):
            
            captcha_image_url = url_with_captcha
            get_site = "https://2captcha.com/in.php"
            responce_site = "https://2captcha.com/res.php"
            
            driver.find_element_by_xpath(xpath_captcha_code).screenshot('captcha.png')

            
            
            with open(r'captcha.png', 'rb') as f:
                b64 = b64encode(f.read()).decode('utf-8')
                
            headers = {
                'action' : 'http://2captcha.com/in.php',
                'method' : 'base64',
                'key' : key,
                'body' : b64
                               
                }    
            
            #example 2captcha site url
            #https://2captcha.com/in.php?key=1abc234de56fab7c89012d34e56fa7b8&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=http://mysite.com/page/with/recaptcha
            
                     
            #submit url to 2captcha site
            s = requests.Session()
            time.sleep(1)
            self.log("Send Url to 2captcha")
            #r_submit = s.post(url_compile,verify=False)
            r_submit = s.post(get_site,headers,verify=False)
                
            #r_submit.text
            
            if 'OK' in r_submit.text:
                
            #get answer 
                
                id = r_submit.text.strip("OK|")
                action = "get"
                url_responce = responce_site + "?" + "key=" + key + "&action=" + action + "&id=" +  id            
                
            
                #sample url
                #https://2captcha.com/res.php?key=1abc234de56fab7c89012d34e56fa7b8&action=get&id=2122988149            
                s = requests.Session()
                time.sleep(90)
                self.log("Send  request to get answer token from 2Captcha ")
                r_get_answer = s.get(url_responce,verify=False)
                
                
                if "OK" in r_get_answer.text:
                    #self.log("Get answer token")
                    answer_token = r_get_answer.text.strip("OK|")
                    print(answer_token)
                    return answer_token
                else:
                    print ("2captcha_site_Error")
                    #answer 03AGdBq27KNwMhE2rOQdJDr39M7f8p7qSQ_QRht9n9qP9rJaSGlf6NUhzIODYjCCg886WS1AibwrhizLe7RuBFoJQv7i6I3TqFAuUXHeWkpoNMi-c21hDid83EfH3YcaveXFr6lhrf_ugci3c_hVK4nDsM7n3WjlhHXDWTrxWca3I0vCvOyX5MmAREB0RurHLD-mBXUWqVozjN7a8OqXiCkBREsvWYo-nV4-v-Y88py3BKtU5sb3CKCel62WG5CFrsRN5pMEIV-f8Aw971qU9yfk1EW3UuQdGLojIxnIH99jFBz4pDbjdEUpDWRKBmxkJdFBVKMjX5WBT_LowjHdWqcdKdeFgG-NTBVjMP0l1NrFp-ZrdHxiTHMCRFn31ot-3BQlYMQ9XQ-kQYqc0tYHppAJYSfNH4ExDKy_gAPIOzj2ecd_4D9M_OaStiV1fd29uLpPVj_yv6H8Ns6BgGFB9todlo0lFWbz2Beg
                    return 'error'
            else:
                self.log("Submit Url Error ")
                
                
                
                
    def fill_form(self,get_driver,token_answer=0):
            
            #url = "https://validate.perfdrive.com/ccb4768f5e2ea98586d13473d71efc83/captcha?ssa=3beefd4f-1d31-41d6-bc9d-bb8c3c0f72f0&ssb=2ih111iimg1cp30bb65mhl6e6&ssc=https%3A%2F%2Fwww.yad2.co.il%2Fapi%2Fpre-load%2FgetFeedIndex%2Frealestate%2Frent%3Fcity%3D8300%26property%3D1%26page%3D2%26rooms%3D2-2%26price%3D2000-4000%26compact-req%3D1%26forceLdLoad%3Dtrue&ssd=124595643431258&sse=bpbbaconnngcekd&ssf=7f7c6c69d4ebdf1a7f421a5b40b29c21eaf24bf7&ssg=a8b0d72d-9181-4008-9945-2b864d61bb0b&ssh=37df8d94-6d76-44c7-9fc9-6504c29822cf&ssi=fd41f73e-bhcz-4b8a-bff2-088667967c28&ssj=a1eacd31-796c-46f7-9cd3-04cb04f0c1f6&ssk=support@shieldsquare.com&ssl=104722949697&ssm=46048851464827762107099549727023&ssn=866c84a8acee2322b66e50f8ca75531917e69245543b-e395-4131-ae6f71&sso=f7cfce49-1a0960bf66d1ce324f24a422c6001376a5e927c6b079b2b4&ssp=05425821621599676097159965843770285&ssq=24911354055125050285240551435594089358110&ssr=MjEyLjIzNS45OC4xNDA=&sss=Chrome/5.0%20(iPhone;%20U;%20CPU%20iPhone%20OS%203_0%20like%20Mac%20OS%20X;%20en-us)%20AppleWebKit/528.18%20(KHTML,%20like%20Gecko)%20Version/4.0%20Mobile/7A341%20Safari/528.16&sst=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/74.0.3729.169%20Safari/537.36&ssu=Mozilla/5.0%20(compatible;%20Yahoo!%20Slurp;%20http://help.yahoo.com/help/us/ysearch/slurp)&ssv=tvvltosnmu@l3rl&ssw=&ssx=633440154012360&ssy=ebhmdbhada@bapfbopfpohpcjbocfeimjfpgbkan&ssz=ac34c7c42aaf0b1"
             
            
            #driver = Get_Data().setup_selenium(url)
            driver = get_driver
            
            #fill form
            
            driver.find_element_by_xpath(xpath_rehov).send_keys(form_data['rehov'])
            driver.find_element_by_xpath(xpath_house_number).send_keys(form_data['house_number'])
            driver.find_element_by_xpath(xpath_complain_window).send_keys(form_data['teur_tluna'])
            
            driver.find_element_by_xpath(xpath_surname).send_keys(form_data['surname'])
            driver.find_element_by_xpath(xpath_rehov_complainer).send_keys(form_data['rehov_of_complainer'])
            driver.find_element_by_xpath(xpath_areacode).clear()
            driver.find_element_by_xpath(xpath_areacode).send_keys(form_data['area_code'])
            driver.find_element_by_xpath(xpath_phone).send_keys(form_data['telefon_without_area_code'])
            driver.find_element_by_xpath(xpath_email).send_keys(form_data['email_of_complainer'])
            driver.find_element_by_xpath(xpath_firstname_complainer).send_keys(form_data['name'])
            driver.find_element_by_xpath(xpath_bait_of_complainer).send_keys(form_data['bait_of_complainer'])
            driver.find_element_by_xpath(xpath_captcha_window).send_keys(token_answer)
            driver.find_element_by_xpath(xpath_telefon_nusaf).send_keys('1111111')
            
            #click on button send form
            driver.find_element_by_xpath(xpath_button_send_form).click()
            sleep(5)
            driver.close


              
    def send_form_setup(self):
            
            #url_with_captcha = Get_Data().yad2(url)
            #url_moked = url_moked 
            self.log('Setup  SElenium')
            driver = self.setup_selenium(url_moked)
            self.log('Get token captcha')               
            captcha_solve = self.captcha_bypass(driver,url_with_captcha,key)
            self.log('Fill form site')
            answer_site = self.fill_form(driver,captcha_solve)
            print(answer_site)
            return answer_site
        
    def __call__(self):
        self.send_form_setup()
             
'''
if __name__ == '__main__':
    
    sched = BackgroundScheduler(daemon=True)
    il_timezone = timezone('Asia/Jerusalem')
    sf = Get_Data()
    
    sched.add_job(sf.send_form_setup,'cron',day_of_week='0-4,6',hour = '11,15',timezone = il_timezone)
    sched.start()
else:
    print('File not executed')    
    
'''    
#driver = Get_Data().setup_selenium(url_moked)
#captcha_solve = Get_Data().captcha_bypass(driver,url_with_captcha,key)
            
