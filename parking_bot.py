# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 12:18:05 2021

@author: макс

This bot can send complain form to rishonlezion moked site

"""

import time
from datetime import datetime
from time import sleep
from base64 import b64encode
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import random
import os
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# xpath from moked site
url_moked = "https://www.rishonlezion.muni.il/Residents/Moked/Pages/Moked-Open.aspx"
url_with_captcha = 'https://www.rishonlezion.muni.il/_layouts/15/GetSignatureImage.aspx'
xpath_rehov = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedReportStreetText"]'
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
xpath_button_send_form = '/html/body/form/div[5]/main/div[3]/div/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[' \
                         '2]/table/tbody/tr/td[1]/button '
xpath_telefon_nusaf = '//*[@id="ctl00_ctl46_g_44664f40_3971_4a93_9c26_f20dfbc9f66f_txtMokedMobilePhone"]'

# two captcha site key
key = os.environ.get("TWO_CAPTCHA_KEY")


# site form data what would be sended
form_data = {
    'rehov': "החייל האלמוני",
    'house_number': random.randint(6, 8),
    'teur_tluna': "רכבים לא מאזור חונים. מבקש לטפל. תודה",
    'teur_tluna_nikaion': "מעבר מרחוב החייל האלמוני לפארק הבנים לא נקי.מבקש לטפל",
    'surname': "ס",
    'name': "יוסי",
    'rehov_of_complainer': "החייל האלמוני",
    'bait_of_complainer': "7",
    'telefon_of_complainer': TEL_NUMBER,
    'area_code': AREA_CODE,
    'telefon_without_area_code': TEL_ONLY,
    'email_of_complainer': EMAIL_ADDRESS
}


class GetData:

    def log(s, t=None):
        # Logging function
        now = datetime.now()
        if t == None:
            t = "Main"
        print("%s :: %s -> %s " % (str(now), t, s))

    def httpbin(self):
        # func  for checking http headers
        captcha_image_url = 'https://www.rishonlezion.muni.il/_layouts/15/GetSignatureImage.aspx'

        # encoding captcha to b64
        with open('captcha.jpg', 'rb') as f:
            b64 = b64encode(f.read()).decode('utf-8')

        headers = {
            'action': 'http://2captcha.com/in.php',
            'method': 'base64',
            'key': key,
            'body': b64

        }

        response = requests.post('http://httpbin.org/post', headers)
        return response.json()

    def setup_selenium(self, url):
        self.log("setup selenium")
        options = webdriver.FirefoxOptions()
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True

        binary = FirefoxBinary(os.environ.get("FIREFOX_BIN"))
        #binary = FirefoxBinary(r"C:\Users\макс\AppData\Local\Mozilla Firefox\firefox.exe")
        options = Options()
        options.set_headless(headless=False)
        options.binary = binary

        fp = webdriver.FirefoxProfile()
        driver = webdriver.Firefox(firefox_options=options, options=options, capabilities=capabilities,firefox_profile=fp, executable_path=os.environ.get("GECKODRIVER_PATH"))
        #driver = webdriver.Firefox(firefox_binary=binary,firefox_options=options,options=options,capabilities=capabilities,firefox_profile=fp, executable_path = 'geckodriver.exe')
        driver.set_window_size(1280, 1024)
        driver.get(url)

        return driver

    def captcha_bypass(self, driver):

        # func to bypass captcha thru 2captcha.com
        get_site = "https://2captcha.com/in.php"
        responce_site = "https://2captcha.com/res.php"

        # save captcha image from moked site
        driver.find_element_by_xpath(xpath_captcha_code).screenshot('captcha.png')

        # encode image to b64
        with open(r'captcha.png', 'rb') as f:
            b64 = b64encode(f.read()).decode('utf-8')
        headers = {
            'action': 'http://2captcha.com/in.php',
            'method': 'base64',
            'key': key,
            'body': b64

        }

        # example 2captcha site url
        # https://2captcha.com/in.php?key=1abc234de56fab7c89012d34e56fa7b8&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=http://mysite.com/page/with/recaptcha

        # submit url to 2captcha site
        s = requests.Session()
        time.sleep(1)
        self.log("Send Url to 2captcha")
        # r_submit = s.post(url_compile,verify=False)
        r_submit = s.post(get_site, headers, verify=False)

        if 'OK' in r_submit.text:

            id = r_submit.text.strip("OK|")
            action = "get"
            url_responce = responce_site + "?" + "key=" + key + "&action=" + action + "&id=" + id

            # sample url
            # https://2captcha.com/res.php?key=1abc234de56fab7c89012d34e56fa7b8&action=get&id=2122988149
            s = requests.Session()
            time.sleep(90)
            self.log("Send  request to get answer token from 2Captcha ")
            r_get_answer = s.get(url_responce, verify=False)

            if "OK" in r_get_answer.text:
                # self.log("Get answer token")
                answer_token = r_get_answer.text.strip("OK|")
                print(answer_token)
                return answer_token
            else:

                return self.log("2captcha_site_Error")
        else:
            self.log("Submit Url Error ")

    @staticmethod
    def fill_form(driver, token_answer):

        # site form filling
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

        # click on button send form
        # driver.find_element_by_xpath(xpath_button_send_form).click()
        sleep(5)

        # self.log("Complain Form sended to Moked")
        # driver.quit()

    @staticmethod
    def fill_form_nikaion(get_driver):
        # cleaning complain form filling
        driver = get_driver
        driver.find_element_by_xpath(xpath_complain_window).send_keys(form_data['teur_tluna_nikaion'])

    def send_form_setup(self):

        # url_moked = url_moked
        self.log('Setup  SElenium')
        driver = self.setup_selenium(url_moked)
        self.log('Get token captcha')
        captcha_solve = self.captcha_bypass(driver)
        self.log('Fill form site')
        answer_site = self.fill_form(driver, captcha_solve)
        print(answer_site)
        return answer_site

    def __call__(self):
        self.send_form_setup()

'''


if __name__ == '__main__':

    GetData().send_form_setup()
    # sched = BackgroundScheduler(daemon=True)
    # il_timezone = timezone('Asia/Jerusalem')
    # sf = Get_Data()

    # sched.add_job(sf.send_form_setup,'cron',day_of_week='0-4,6',hour = '11,15',timezone = il_timezone)
    # sched.start()
else:
    print('File not executed')


#driver = Get_Data().setup_selenium(url_moked)
#driver.quit()    
driver = Get_Data().setup_selenium(url_moked)
#captcha_solve = Get_Data().captcha_bypass(driver,url_with_captcha,key)
#Get_Data().fill_form(driver,captcha_solve)     

       
'''
# driver = Get_Data().setup_selenium(url_moked)
