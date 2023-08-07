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

# search button click
button_element = driver.find_element(By.ID, 'acc-toggle-1')
driver.execute_script("arguments[0].click();", button_element)
# button_wait = WebDriverWait(driver, 20)
# button_element = button_wait.until(EC.element_to_be_clickable((By.ID, 'acc-toggle-1')))
# button_element.click()
time.sleep(5)

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

# for loop for 36 tag select
for select_id in range(len(select_options)):
        
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
    items = int(int(item_number[0])/25)
    time.sleep(3)

    # show more button click
    if items == 0:
        time.sleep(1)
    else:
        show_element = driver.find_element(By.ID, 'load-more')
        for item in range(items):
            driver.execute_script("arguments[0].click();", show_element)
            # wait = WebDriverWait(driver, 20)
            # element = wait.until(EC.element_to_be_clickable((By.ID, 'load-more')))
            # element.click()
            time.sleep(1)

    # collect URLs for the result
    all_result_content = driver.page_source
    urls = BeautifulSoup(all_result_content, 'html.parser')
    lists = urls.select('ul > li > div > span > a')
    scrape_one = []
    for li in lists:
        href = li['href']
        other_driver = webdriver.Chrome()
        other_driver.get(href)
        time.sleep(5)
        other_content = BeautifulSoup(other_driver.page_source, 'html.parser')
        
        # RNCP and intitule
        title = other_content.select('.bl__title')
        real_title = title[0].text.strip()
        split_title = real_title.split(" - ")
        RNCP = split_title[0]
        intitule = split_title[1]
        print('RNCP:', RNCP, 'intitule:', intitule)

        # Niveau
        niveau_data = other_content.select('.nomenclature_niveau > span')
        niveau = niveau_data[0].text.strip()
        print('Niveau:', niveau)
        
        # Certificateur
        certi_data = other_content.select('#collapseOne > div > div > table > tbody > tr > td')
        certi = certi_data[0].text.strip()
        print('Certi:', certi)

        # Date
        date_data = other_content.select('.code > div > span')
        dates = date_data[1].text.strip()
        print('Date:', dates)

        # Fiche
        fiche = other_content.select('.content-liste > div > span')
        real_fiche = fiche[0].text.strip()
        print('fiche:', real_fiche)
        
        # RESUME
        resume_title = other_content.select('#collapseTwo > div > h5')
        resume_content = other_content.select('#collapseTwo > div > div')
        resume = []
        for id in range(len(resume_title)):
            if len(resume_content) > id >=0:
                resume_value = {
                    "title": resume_title[id].text.strip(),
                    'content': resume_content[id].text.strip()
                }
            else:
                resume_value = {
                    "title": resume_title[id].text.strip(),
                    'content': ""
                }
            
            resume.append(resume_value)
        # print('Resume:', resume)

        # SECTEUR
        secteur_title = other_content.select('#collapseFour > div > h5')
        secteur_content = other_content.select('#collapseFour > div > div')
        secteur = []
        for id in range(len(secteur_title)):
            if len(secteur_content) > id >=0:
                secteur_value = {
                    "title": secteur_title[id].text.strip(),
                    'content': secteur_content[id].text.strip()
                }
            else:
                secteur_value = {
                    "title": secteur_title[id].text.strip(),
                    'content': ""
                }
            
            secteur.append(secteur_value)
        # print('Secteur', secteur)

        # VOIES
        voies_data = other_content.select('#collapseFive > div')
        voies = voies_data[0].text.strip()
        print(voies)

        # LIEN
        lien_data = other_content.select('#collapseSix > div')
        lien = lien_data[0].text.strip()
        print(lien)

        # BASE
        base_data = other_content.select('#collapseSeven > div')
        base = base_data[0].text.strip()
        print(base)

        # POUR
        pour_data = other_content.select('#collapseEight > div')
        pour = pour_data[0].text.strip()
        print(pour)

        # quit other driver
        other_driver.quit()

        # collect data
        total_data =  {
            "id" : items + 1,
            "RNCP" : RNCP,
            "Intitule" : intitule,
            "Niveau" : niveau,
            "Certificateur" : certi,
            "Date" : dates,
            "fiche" : fiche,
            "RESUME" : resume,
            "SECTEUR" : secteur,
            "VOIES" : voies,
            "LIEN" : lien,
            "BASE" : base,
            "POUR" : pour,
        }
        scrape_one.append(total_data)
    
    # insert collect data to json
    scrape_data[select_options[select_id]] = scrape_one
    time.sleep(5)

# write json data to data.json file
file_path = "data.json"
with open(file_path, "w") as json_file:
    json.dump(scrape_data, json_file)

time.sleep(5)
driver.quit()
