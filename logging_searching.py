from selenium import webdriver
from time import sleep
from parameters import * 
from parsel import Selector
from selenium.webdriver.common.keys import Keys
import csv

# open csv file to write data out
writer = csv.writer(open(result_file,'a',encoding = 'utf-8'))
writer.writerow(['name','job','location','education','LinkedIn Url'])


# open driver
driver = webdriver.Chrome('d:/Scrapy/chromedriver_win32/chromedriver.exe')
driver.maximize_window()
sleep(0.5)

# log in to linked in
driver.get('https://www.linkedin.com/')
sleep(2)
driver.find_element_by_xpath('//a[text() = "Sign in"]').click()
sleep(2)
username_input = driver.find_element_by_name('session_key')
username_input.send_keys(username)
sleep(2)
password_input = driver.find_element_by_name('session_password')
password_input.send_keys(password)
sleep(2)
sign_in_btn =driver.find_element_by_xpath('//button[text()="Sign in"]')
sign_in_btn.click()
sleep(5)


# I have 2-step verification enabled, so next step is to get OTP
print('Enter OTP sent to your registered mobile number ...')
otp = input().strip()
    
otp_input = driver.find_element_by_name('pin')

otp_input.send_keys(otp)
sleep(2)


#click submit
driver.find_element_by_xpath('//button[text()="Submit"]').click()
print('You have successfully logged in ...')
sleep(1)

#get linked in search bar
search_box = driver.find_element_by_xpath("//input[contains(@class,'search-global-typeahead__input')]")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)
sleep(1)
while True :
    try :
        url = driver.current_url.split('/')
        url[5] = 'people'
        url = '/'.join(url)
    except:
        continue
    break


driver.get(url)
sleep(2)
while True:
    try:
        #get list of profiles
        profiles = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
    except:
        continue
    break
profile_urls = []
for profile in profiles:
    name = profile.find_element_by_xpath('.//a/span/span').text
    try:
        profile.find_element_by_xpath('.//button/span[text()="Connect"]').click()
        try:
            sendBtn = driver.find_element_by_xpath("//div[@role='dialog']//button/span[text()='Send']")
            sendBtn.click()
        except:
            continue
    except:
        continue
    profile_urls.append([name,profile.find_element_by_xpath('.//a').get_attribute('href')])

for profile_url in profile_urls:
    driver.get(profile_url[1])
    sleep(5)
    sel  = Selector(text=driver.page_source)
    desg = sel.xpath('//main//section//div/h1/../following-sibling::div[1]/text()').extract_first()
    if desg :
        desg = desg.strip()
    location= sel.xpath('//div[@class="pb2"]/span[1]/text()').extract_first()
    if location :
        location = location.strip()
    education = sel.xpath('//*[contains(@class,"pv-entity__school-name")]/text()').extract()

    writer.writerow([profile_url[0],desg,location,education,driver.current_url])
    
driver.quit()

