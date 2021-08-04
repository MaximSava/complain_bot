# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 21:25:48 2021

@author: макс
"""

import parking_bot as pb
import schedule,time
import datetime
from dateutil import tz


def log(s,t=None):
            tzj = tz.gettz('Asia/Jerusalem')
            now = datetime.datetime.now(tz=tzj)
            if t == None :
                    t = "Main"
            print ("%s :: %s -> %s " % (str(now), t, s)) 

if __name__ == '__main__':
    sf = pb.Get_Data()
    schedule.every().sunday.at("13:00").do(sf.send_form_setup)
    schedule.every().sunday.at("15:00").do(sf.send_form_setup)  
    schedule.every().monday.at("12:45").do(sf.send_form_setup)
    schedule.every().monday.at("15:00").do(sf.send_form_setup)
    schedule.every().tuesday.at("13:00").do(sf.send_form_setup)
    schedule.every().tuesday.at("20:30").do(sf.send_form_setup)
    schedule.every().wednesday.at("12:45").do(sf.send_form_setup)
    schedule.every().wednesday.at("17:35").do(sf.send_form_setup)
    schedule.every().thursday.at("13:45").do(sf.send_form_setup)
    schedule.every().thursday.at("15:00").do(sf.send_form_setup)
    schedule.every().friday.at("10:45").do(sf.send_form_setup)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    '''
    sched = BackgroundScheduler(daemon=True)
    il_timezone = timezone('Asia/Jerusalem')
    sf = pb.Get_Data()
    
    sched.add_job(sf.send_form_setup(),'cron',day_of_week='0-4,6',hour = '11,15',timezone = il_timezone)
    sched.start()
    '''
else:
    print('File not executed')  

'''

print(' '.join(country_timezones('il')))
''' 