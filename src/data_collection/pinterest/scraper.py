# From: https://github.com/xjdeng/pinterest-image-scraper/blob/master/pinterest_scraper/scraper.py
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time,random,socket,unicodedata
import string, copy, os
import pandas as pd
import requests
try:
    from urlparse import urlparse
except ImportError:
    from six.moves.urllib.parse import urlparse

def download(myinput, mydir = "./"):
    if isinstance(myinput, str) or isinstance(myinput, bytes):
        #http://automatetheboringstuff.com/chapter11/
        res = requests.get(myinput)
        res.raise_for_status()
        #https://stackoverflow.com/questions/18727347/how-to-extract-a-filename-from-a-url-append-a-word-to-it
        outfile = mydir + "/" + os.path.basename(urlparse(myinput).path)
        playFile = open(outfile, 'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
    elif isinstance(myinput, list):
        for i in myinput:
            download(i, mydir)
    else:
        pass

def phantom_noimages():
    from fake_useragent import UserAgent
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    ua = UserAgent()
    #ua.update()
    #https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-driver
    caps = DesiredCapabilities.PHANTOMJS
    caps["phantomjs.page.settings.userAgent"] = ua.random
    return webdriver.PhantomJS(service_args=["--load-images=no"], desired_capabilities=caps)
        

def randdelay(a,b):
    time.sleep(random.uniform(a,b))

def u_to_s(uni):
    return unicodedata.normalize('NFKD',uni).encode('ascii','ignore')

class Pinterest_Helper(object):
    
    def __init__(self, login, pw, maxImgCount=1000, scrollThreshold=500, browser = None):
        self.maxImgCount = maxImgCount
        self.scrollThreshold = scrollThreshold

        if browser is None:
            # #http://tarunlalwani.com/post/selenium-disable-image-loading-different-browsers/
            # profile = webdriver.FirefoxProfile()
            # profile.set_preference("permissions.default.image", 2)
            # self.browser = webdriver.Firefox(firefox_profile=profile)
            self.browser = webdriver.Chrome(ChromeDriverManager().install())

        else:
            self.browser = browser

        # self.browser = webdriver.Chrome(executable_path="drivers/chromedriver")

        # self.browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        
        self.browser.get("https://www.pinterest.com/login")
        emailElem = self.browser.find_element_by_name('id')
        emailElem.send_keys(login)
        passwordElem = self.browser.find_element_by_name('password')
        passwordElem.send_keys(pw)
        passwordElem.send_keys(Keys.RETURN)
        randdelay(2,4)
    
    def getURLs(self, urlcsv, threshold = 500):
        tmp = self.read(urlcsv)
        results = []
        for t in tmp:
            tmp3 = self.runme(t, threshold)
            results = list(set(results + tmp3))
        random.shuffle(results)
        return results
    
    def write(self, myfile, mylist):
        tmp = pd.DataFrame(mylist)
        tmp.to_csv(myfile, index=False, header=False)
    
    def read(self,myfile):
        tmp = pd.read_csv(myfile,header=None).values.tolist()
        tmp2 = []
        for i in range(0,len(tmp)):
            tmp2.append(tmp[i][0])
        return tmp2        
        
    
    def runme(self,url, persistence = 120, debug = False):
        threshold = self.scrollThreshold
        scrapeIsDone = False
        maxImagesCount = 2
        final_results = []
        previmages = []
        tries = 0
        try:
            self.browser.get(url)

            # Checking max scroll threshold and if enough or max count
            while threshold > 0 and scrapeIsDone == False:
                try:
                    results = []
                    images = self.browser.find_elements_by_tag_name("img")
                    if images == previmages:
                        tries += 1
                    else:
                        tries = 0
                    if tries > persistence:
                        if debug == True:
                            print("Exitting: persistence exceeded")
                        return final_results
                    for i in images:
                        src = i.get_attribute("src")
                        if src:
                            if src.find("/236x/") != -1:
                                src = src.replace("/236x/","/736x/")
                                results.append(u_to_s(src))
                    previmages = copy.copy(images)
                    final_results_new = list(set(final_results + results))

                    # Check if enough images
                    if len(final_results_new) > self.maxImgCount:
                        print(f"Done scraping pinterest because max count reached. Total -> {len(final_results_new)}")
                        scrapeIsDone = True

                    # Check if no new images are found, make sure not first iteration where both 0
                    elif len(final_results) > 0 and len(final_results_new) == len(final_results):
                        print(f"Done scraping pinterest because no new images. Total -> {len(final_results_new)}")
                        scrapeIsDone = True
                    else:
                        dummy = self.browser.find_element_by_tag_name('a')
                        dummy.send_keys(Keys.PAGE_DOWN)
                        randdelay(1,2)
                        threshold -= 1

                    # Set the new images
                    final_results = final_results_new


                except (StaleElementReferenceException):
                    if debug == True:
                        print("StaleElementReferenceException")
                    threshold -= 1
        except (socket.error, socket.timeout):
            if debug == True:
                print("Socket Error")
        except KeyboardInterrupt:
            return final_results
        if debug == True:
            print("Exitting at end")
        return final_results

    def runme_alt(self,url, tol = 10, minwait = 1, maxwait = 2,debug = False):
        threshold = self.scrollThreshold
        final_results = []
        heights = []
        dwait = 0
        try:
            self.browser.get(url)
            while threshold > 0:
                try:
                    results = []
                    images = self.browser.find_elements_by_tag_name("img")
                    cur_height = self.browser.execute_script("return document.documentElement.scrollTop")
                    page_height = self.browser.execute_script("return document.body.scrollHeight")
                    heights.append(int(page_height))
                    if debug == True:
                        print("Current Height: " + str(cur_height))
                        print("Page Height: " + str(page_height))
                    if len(heights) > tol:
                        if heights[-tol:] == [heights[-1]]*tol:
                            if debug == True:
                                print("No more elements")
                            return final_results
                        else:
                            if debug == True:
                                print("Min element: {}".format(str(min(heights[-tol:]))))
                                print("Max element: {}".format(str(max(heights[-tol:]))))
                    for i in images:
                        src = i.get_attribute("src")
                        if src:
                            if src.find("/236x/") != -1:
                                src = src.replace("/236x/","/736x/")
                                results.append(u_to_s(src))
                    final_results = list(set(final_results + results))
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    randdelay(minwait,maxwait)
                    threshold -= 1
                except (StaleElementReferenceException):
                    if debug == True:
                        print("StaleElementReferenceException")
                    threshold -= 1
                except (socket.error, socket.timeout):
                    if debug == True:
                        print("Socket Error. Waiting {} seconds.".format(str(dwait)))
                        time.sleep(dwait)
                        dwait += 1
        #except (socket.error, socket.timeout):
        #    if debug == True:
        #        print("Socket Error")
        except KeyboardInterrupt:
            return final_results
        if debug == True:
            print("Exitting at end")
        return final_results        
 
    def scrape_old(self, url):
        results = []
        self.browser.get(url)
        images = self.browser.find_elements_by_tag_name("img")
        for i in images:
            src = i.get_attribute("src")
            if src:
                if string.find(src,"/236x/") != -1:
                    src = string.replace(src,"/236x/","/736x/")
                    results.append(u_to_s(src))
        return results
            
        
        
        
        
    
    def close(self):
        self.browser.close()
    
    
    