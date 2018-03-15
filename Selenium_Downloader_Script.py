import re 
import cssselect
import lxml.html
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.support.ui import Select


# START PAGE URL TO START SCRAPING
pageUrl = "https://xyz.zzz.com/v2/search/pageChange?SRCHTYPE=adv&sid=1851930003&actClust=&agentid=&pageNo=1"




# mysql database connection 

def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    rows = tree.cssselect('div.row > a.content')
    return rows

def lxml_link_scraper(html_link):
    tree = lxml.html.fromstring(html_link)
    rows = tree.cssselect('div.tuple')
    return rows


# Logging into forms to reach the actual database 
url = "https://login.recruit.xyz.com/" 

print "Initializing Custom FireFox"
customProfile = FirefoxProfile("C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/zcd5c2sk.selenium")
#customProfile = FirefoxProfile("C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/m3l33or3.selenium2")
browser = webdriver.Firefox(customProfile)
user_input = raw_input("If all set let's go? ")
if user_input:
    pass 
print "Opening " + url
browser.get(url)

print "Fetching and typing in form details"
sleep(1)
myUsername = "**********"
myPassword = "**********"
usernameField = browser.find_element_by_name('username')
passwordField = browser.find_element_by_name('password')
buttonSignIn = browser.find_element_by_xpath("""//*[@id="midCont"]/form/div/div/div/div/div[2]/div[4]/button/div/div""")
usernameField.send_keys(myUsername)
passwordField.send_keys(myPassword)
buttonSignIn.click()

print "LogIn Successfull -> Entering Search Resumes Link"
sleep(2)
browser.get("https://xyz.zzz.com/v2/search/advSearch")
sleep(2)
try:
    optionField = Select(browser.find_element_by_xpath('//*[@id="userNameId"]'))
    optionField.select_by_visible_text('hunterz01')
    submitButton = browser.find_element_by_name('submit')
    sleep(2)
    submitButton.click()
except:
    user_input = raw_input("IF the problem is solved type any char? ")
    if user_input:
        pass
    
print "Getting Search Details From Recent Searches"
SID = "&sid=1851930003"
def download_resume():
    browser.get(pageUrl)
    sleep(15)
    html = browser.page_source
    contents = lxml_link_scraper(html)
    for i in range(0,len(contents)):
        item = contents[i]
        data = item.get('data-uobj')
        uniqID = re.match("""{\'*\"*uniqId\'*\"*\:\'*\"*([\d\w]+)""",data)
        link = "https://xyz.zzz.com/v2/preview/preview?uniqId=" + uniqID.group(1) + SID
        browser.get(link)
        try:
            download = browser.find_element_by_xpath('//*[@id="jump-CV"]/div[1]/div[2]/a')
            download.click()
            sleep(randint(3,6))
        except:
            print "No xpath located for the CV"
            try:
                download = browser.find_element_by_xpath('//*[@id="jump-CV"]/div[1]/div[2]/a')
                download.click()
                sleep(randint(3,6))
            except:
                print "Maybe CapTcha"
                user_input  = raw_input("Enter 'd' to download if captcha solved? ")
                if user_input == 'd':
                    try:
                        download = browser.find_element_by_xpath('//*[@id="jump-CV"]/div[1]/div[2]/a')
                        download.click()
                        sleep(randint(3,6))
                    except:
                        print "error downloading"
                else:
                    print "2nd Try no Xpath Found"
                    print "Moving to next CV"
        cvCount = i
        done = 160 - i
        print "Downloads Left on this page -> " + str(done)
print "Command Executed"
