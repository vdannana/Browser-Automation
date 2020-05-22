import random
import subprocess
import time
import urllib.request
from datetime import datetime
from http import HTTPStatus
from sys import platform

import requests
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys

import Configuration as conf


'''
    This Script is use to click a clear button in alert box in firefox browser to clear cache.
'''
accept_dialog_script = (
    f"const browser = document.getElementsByClassName('dialogFrame')[0];" +
    "browser.contentDocument.querySelector('#clearButton').click();"
)


'''
    clear_chrome_cache function clears the chrome browser cache.
    the argument driver is a webdriver object of the browser.
'''
def clear_chrome_cache(driver):
    driver.get('chrome://settings/clearBrowserData')
    driver.find_element_by_xpath('//settings-ui').send_keys(Keys.ENTER)
    url = 'chrome://settings/clearBrowserData'
    while (url == 'chrome://settings/clearBrowserData'):
        url = driver.current_url
    print(driver.current_url)


'''
    clear_firefox_cache function clears the firefox browser cache.
    the argument driver is a webdriver object of the browser.
'''
def clear_firefox_cache(driver, timeout=10):
    driver.get('about:preferences#privacy')
    # Click the "Clear Data..." button under "Cookies and Site Data".
    driver.find_element_by_css_selector('#clearSiteDataButton').click()
    time.sleep(2)
    driver.execute_script(accept_dialog_script)
    time.sleep(2)
    alert = Alert(driver)
    alert.accept()


'''
    fetch_urls function gets the 100 urls from the github link.
'''
def fetch_urls():
    read_data = requests.get(conf.url_path).content
    urls = read_data.decode("utf-8")
    conf.web_url_list = urls.split('\n')
    print(len(conf.web_url_list))


'''
    Rand function selects a number (num) of random number from the range [satrt, end].
    the arguments
        start range starting number.
        end   range ending number.
        num   number of random numbers to get.
'''
def Rand(start, end, num):
    res = []
    for j in range(num):
        res.append(random.randint(start, end))
    return res


'''
    selectList function selects a conf.number_of_sites number of random sites from 100 sites fetched from github
'''
def selectList():
    conf.selectList = []
    lst = Rand(0, len(conf.web_url_list) - 1, conf.number_of_sites)
    for i in lst:
        conf.selectList.append(conf.web_url_list[i])


'''
    openBrowser function performs following tasks
        1. open the required browser.
        2. clears the web cache.
        3. opens list of sites/urls.
        4. get the satus code, amount of bytes loaded, time taken to load the site are calculated.
    The argumntes
        sitelist takes list of site urls
        browsercode takes a integer which represents a specific browser
            ex: 0 for Chrome
                1 for Firefox
                other values open Internet Explorer
'''
def openBrowser(sitelist, browsercode):
    if platform == "linux" or platform == "linux2":
        if browsercode == '0':
            try:
                subprocess.check_output(['google-chrome', '--version'])
                print("Google Chrome is installed")
                driver = webdriver.Chrome('Requirements/Linux/chromedriver')
            except:
                print("Google Chrome is not install")
                return
        if browsercode == '1':
            try:
                subprocess.check_output(['firefox', '--version'])
                print("Firefox is installed")
                driver = webdriver.Firefox(executable_path='Requirements/Linux/geckodriver')
            except:
                print("Firefox is not install")
                return
    if platform == 'win32':
        if browsercode == '0':
            try:
                driver = webdriver.Chrome('Requirements\\Windows\\chromedriver.exe')
                print("Google Chrome is installed")
                valid = True
            except:
                print("Google Chrome is not install")
                return
            if(valid):
                clear_chrome_cache(driver)
        if browsercode == '1':
            try:
                driver = webdriver.Firefox(executable_path='Requirements\\Windows\\geckodriver.exe')
                valid = True
                print("Firefox is installed")
            except:
                print("Firefox is not install")
                return
            if(valid):
                clear_firefox_cache(driver)
    f = open(conf.Log_Directory+'/'+conf.File_Name, 'a')

    for site in sitelist:
        driver.execute_script("window.open('" + site + "' ,'_blank')")

    for site in sitelist:
        try:
            start_time = time.time()
            temp = urllib.request.urlopen(site)
            end_time = time.time()
            timetaken = end_time - start_time
            print('Time taken by ' + site + ' is ' + str(timetaken) + 'sec' + " | " + str(datetime.now()))
            f.write('Time taken by ' + site + ' is ' + str(timetaken) + 'sec' + " | " + str(datetime.now()))
            print('Data loaded by ' + site + ' is ' + str(len(temp.read())) + 'bytes' + " | " + str(datetime.now()))
            f.write('Time taken by ' + site + ' is ' + str(len(temp.read())) + 'bytes' + " | " + str(datetime.now()))
            print('Response Code: ' + site + " : " + HTTPStatus(temp.getcode()).phrase + " | " + str(datetime.now()))
            f.write('Response Code: ' + site + " : " + str(HTTPStatus(temp.getcode()).phrase) + " | " + str(datetime.now()) + '\n')
        except Exception as e:
            print(site + " : " + str(e) + " | " + str(datetime.now()))
            f.write(site + " : " + str(e) + " | " + str(datetime.now()) + '\n')

    f.close()
    return driver
