from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import json

select_options = [
    'BAC+PRO',
    'BEATEP',
    'BEES',
    'BEP',
    'BEPA',
    'BP',
    'BPA',
    'BPJEPS',
    'BTA',
    'BTn',
    'BTS',
    'BTSA',
    'BTSMarit',
    'BUT',
    'CAP',
    'CAPA',
    'CPJEPS',
    'DEEA',
    'DEJEPS',
    'DESJEPS',
    'DEUST',
    'DNSP',
    'DOCTORAT',
    'DSTS',
    'DUT',
    'Grade_Licence',
    'Grade_Master',
    'LICENCE',
    'Licence+Professionnelle',
    'MASTER',
    'MC4',
    'MC5',
    'Titre+ingénieur',
    'TP',
]

scrape_data = {}
# For Chrome
driver = webdriver.Chrome()
driver.get('https://www.francecompetences.fr/recherche_certificationprofessionnelle/')
time.sleep(5)

# for loop for 36 tag select
for select_id in range(len(select_options)):

    # search button click
    button_element = driver.find_element(By.ID, 'acc-toggle-1')
    driver.execute_script("arguments[0].click();", button_element)
    # button_wait = WebDriverWait(driver, 20)
    # button_element = button_wait.until(EC.element_to_be_clickable((By.ID, 'acc-toggle-1')))
    # button_element.click()
    time.sleep(3)

    # input option click
    input1_element = driver.find_element(By.ID, 'edit-type-directory-RNCP')
    driver.execute_script("arguments[0].click();", input1_element)
    input2_element = driver.find_element(By.ID, 'edit-etat-fiche-active')
    driver.execute_script("arguments[0].click();", input2_element)
    # input1_wait = WebDriverWait(driver, 20)
    # input1_element = input1_wait.until(EC.element_to_be_clickable((By.ID, 'edit-type-directory-RNCP')))
    # input1_element.click()
    # input2_element = input1_wait.until(EC.element_to_be_clickable((By.ID, 'edit-etat-fiche-active')))
    # input2_element.click()
        
    # select tag click
    select_element = driver.find_element(By.ID, 'edit-abrege')
    select = Select(select_element)
    select.select_by_value(select_options[select_id])

    # submit search button
    submit_btn_element = driver.find_element(By.CLASS_NAME, 'footer-submit')
    driver.execute_script("arguments[0].click();", submit_btn_element)
    # submit_btn_wait = WebDriverWait(driver, 20)
    # submit_btn_element = submit_btn_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'footer-submit')))
    # submit_btn_element.click()

    # get page content
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    result_number = soup.select('.label-page')
    item_number = re.findall(r'\d+', result_number[0].text.strip())
    if len(item_number) > 0:
        li = int(int(item_number[0])/25)
        time.sleep(3)

        # show more button click
        if li == 0:
            time.sleep(1)
        else:
            show_element = driver.find_element(By.ID, 'load-more')
            for item in range(li):
                driver.execute_script("arguments[0].click();", show_element)
                # wait = WebDriverWait(driver, 20)
                # element = wait.until(EC.element_to_be_clickable((By.ID, 'load-more')))
                # element.click()
                time.sleep(1)

        # collect URLs for the result
        all_result_content = driver.page_source
        urls = BeautifulSoup(all_result_content, 'html.parser')
        lists = urls.select('ul > li > div > span > a')
        i = 0
        for li in lists:
            i += 1
            href = li['href']
            other_driver = webdriver.Chrome()
            other_driver.get(href)
            time.sleep(3)
            other_content = BeautifulSoup(other_driver.page_source, 'html.parser')
            
            # RNCP and intitule
            title = other_content.select('.bl__title')
            real_title = title[0].text.strip()
            split_title = real_title.split(" - ")
            RNCP = split_title[0].encode("utf-8").decode("utf-8")
            intitule = split_title[1].encode("utf-8").decode("utf-8")
            
            # Niveau
            niveau_data = other_content.select('.nomenclature_niveau > span')
            niveau = niveau_data[0].text.strip().encode("utf-8").decode("utf-8")
            
            # Certificateur
            certi_data = other_content.select('#collapseOne > div > div > table > tbody > tr > td')
            certi = certi_data[0].text.strip().encode("utf-8").decode("utf-8")

            # Date
            date_data = other_content.select('.code > div > span')
            dates = date_data[1].text.strip().encode("utf-8").decode("utf-8")

            # Fiche
            fiche = other_content.select('.content-liste > div > span')
            real_fiche = fiche[0].text.strip().encode("utf-8").decode("utf-8")
            
            # RESUME
            resume_data = other_content.select('#collapseTwo > div')
            resume = str(resume_data[0])

            # SECTEUR
            secteur_data = other_content.select('#collapseFour > div')
            secteur = str(secteur_data[0])

            # VOIES
            voies_data = other_content.select('#collapseFive > div')
            voies = str(voies_data[0])

            # LIEN
            lien_data = other_content.select('#collapseSix > div')
            lien = str(lien_data[0])

            # BASE
            base_data = other_content.select('#collapseSeven > div')
            base = str(base_data[0])

            # POUR
            pour_data = other_content.select('#collapseEight > div')
            pour = str(pour_data[0])

            # quit other driver
            other_driver.quit()

            # collect data
            total_data =  {
                "id" : i,
                "RNCP" : RNCP,
                "Intitule" : intitule,
                "Niveau" : niveau,
                "Certificateur" : certi,
                "Date" : dates,
                "fiche" : real_fiche,
                "RESUME" : resume,
                "SECTEUR" : secteur,
                "VOIES" : voies,
                "LIEN" : lien,
                "BASE" : base,
                "POUR" : pour,
            }
            # read and append data to json
            data = []
            file_path = "data.json"
            with open(file_path, "r") as file:
                data = json.load(file)
            data.append(total_data)

            # write json data to data.json file
            with open('data.json', 'w') as file:
                json.dump(data, file)

        time.sleep(3)
time.sleep(5)
driver.quit()
