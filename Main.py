import os
import time
from random import randint

import Common_Function as cf
import Configuration as conf

cf.fetch_urls()
cf.selectList()
print(conf.selectList)

# Creating a Directory to store Log Files
if not os.path.exists(conf.Log_Directory):
    os.mkdir(conf.Log_Directory)
    print("Directory ", conf.Log_Directory,  " Created ")
else:
    print("Directory ", conf.Log_Directory,  " already exists")

f = open(conf.Log_Directory+'/'+conf.File_Name, 'w')
f.close()

# Open Browser repatedly and open the sites.
driver = cf.openBrowser(conf.selectList, conf.browsercode)
time.sleep(conf.browser_close_time)
driver.quit()

while True:
    value = randint(1, 10)
    print(value)
    seconds = (value * 60)
    time.sleep(seconds)
    cf.selectList()
    print(conf.selectList)
    driver = cf.openBrowser(conf.selectList, conf.browsercode)
    time.sleep(conf.browser_close_time)
    driver.quit()
