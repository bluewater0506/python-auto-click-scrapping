from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re

# For Chrome
driver = webdriver.Chrome()
driver.get('https://www.francecompetences.fr/recherche_certificationprofessionnelle/')
time.sleep(3)

# search button click
button = driver.find_element(By.ID, 'acc-toggle-1')
button.click()
time.sleep(3)

# input option click
input1 = driver.find_element(By.ID, 'edit-type-directory-RNCP')
input1.click()
input2 = driver.find_element(By.ID, 'edit-etat-fiche-active')
input2.click()
time.sleep(3)

# select tag click
select_element = driver.find_element(By.ID, 'edit-abrege')
select = Select(select_element)
select.select_by_value('BAC+PRO')
time.sleep(3)

# submit search button
submit_btn = driver.find_element(By.CLASS_NAME, 'footer-submit')
submit_btn.click()
time.sleep(10)

# get page content 
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
result_number = soup.select('.label-page')
item_number = re.findall(r'\d+', result_number[0].text.strip())
items = int(int(item_number[0])/25)

# show more button click
for item in range(items):
    more_btn = driver.find_element(By.ID, 'load-more')
    more_btn.click()
    time.sleep(10)

# collect URLs for the result
all_result_content = driver.page_source
urls = BeautifulSoup(all_result_content, 'html.parser')
lists = urls.find_all('ul > li')
print(urls)
for li in lists:
    atag = li.find('a')
    href = atag['href']
    print(href)

time.sleep(5)
driver.quit()
