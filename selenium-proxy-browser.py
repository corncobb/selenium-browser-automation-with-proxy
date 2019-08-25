'''
Python Selenium browser proxy for logging into Instagram accounts

Author: Cameron Cobb
'''

import os
import zipfile
import time
from sys import platform as p_os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

p1 = "ip:port@username:password"

insta_username = ""         #instagram username
insta_password = ""         #instagram password

use_proxy = False        #change to "False" to turn off proxy

proxy = p1      #choose proxy from above (Ex: "proxy = p30")

if use_proxy:
    ip = proxy.split(':')[0]
    port = int(proxy.split(':')[1])
    login = proxy.split(':')[2]
    password = proxy.split(':')[3]

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (ip, port, login, password)

def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath("C:\\webdriver\\chromedriver.exe"))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver

def login(driver):

    driver.find_element_by_xpath("//article/div/div/p/a[text()='Log in']").click()

    time.sleep(2)
    #username
    input_username_XP = "//input[@name='username']"
    
    input_username = driver.find_element_by_xpath(input_username_XP)

    ActionChains(driver).move_to_element(input_username). \
        click().send_keys(insta_username).perform()
    time.sleep(1)

    #password
    input_password = driver.find_elements_by_xpath(
        "//input[@name='password']")
    ActionChains(driver).move_to_element(input_password[0]). \
        click().send_keys(insta_password).perform()

    login_button = driver.find_element_by_xpath(
        "//*[contains(text(),'Log In')]")
    ActionChains(driver).move_to_element(login_button).click().perform()

def main():
    driver = get_chromedriver(use_proxy)
    time.sleep(2)
    driver.get('https://www.instagram.com/')
    login(driver)
    
if __name__ == '__main__':
    main()
