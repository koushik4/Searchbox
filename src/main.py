import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.support import expected_conditions as EC
from atscheck import get_resume_text,check
import time
import datetime,os

curr_dir = os.getcwd()

DRIVE_PATH = os.path.join(curr_dir,"chromedriver 2")
JOB_TITLE_SEARCH_BAR_XPATH = "/html/body/main/section[1]/div/section/div[2]/section[2]/form/section[1]/input"
EXPERIENCE_LEVEL_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]/div/div/button"
LOCATION_XPATH = "/html/body/main/section[1]/div/section/div[2]/section[2]/form/section[2]/input"
EXPERIENCE_LEVEL_INTERNSHIP_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]/div/div/div/div/div/div[1]"
EXPERIENCE_LEVEL_ENTRY_LEVEL_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]/div/div/div/div/div/div[2]"
COMPANY_FILTER_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form[1]/ul/li[3]/div/div/button"
COMPANY_FILTER_NAME_XPATH = "/html/body/div[1]/section/div/div/div/form[1]/ul/li[3]/div/div/div/section/input"

def enter_job_title_search(title,location):
    job_title_searchbar = driver.find_element(By.XPATH,JOB_TITLE_SEARCH_BAR_XPATH)
    job_title_searchbar.send_keys(title)
    location_bar = driver.find_element(By.XPATH,LOCATION_XPATH)
    location_bar.clear()
    location_bar.send_keys(location)
    location_bar.send_keys(Keys.RETURN)
             
def filter_companies(companies):
    driver.find_element(By.XPATH,COMPANY_FILTER_BUTTON_XPATH).click()
    time.sleep(1)
    # text = driver.find_element(By.XPATH,COMPANY_FILTER_NAME_XPATH)
    for company in companies:
        # text = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
        #     COMPANY_FILTER_NAME_XPATH)))
        text = driver.find_element(By.XPATH,COMPANY_FILTER_NAME_XPATH)
        time.sleep(1)
        text.send_keys(company)
        res = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME,"typeahead-input__dropdown-item")
            ))
        # print(len(res))
        if len(res) > 0:
            time.sleep(1)
            text.send_keys(Keys.ARROW_DOWN)
            text.send_keys(Keys.RETURN)
        
    driver.find_element(By.XPATH,"/html/body/div[1]/section/div/div/div/form[1]/ul/li[3]/div/div/div/button").click()


def filter_experience_levels(levels):
    experience_level_button = driver.find_element(By.XPATH,EXPERIENCE_LEVEL_XPATH)
    experience_level_button.click()
    done_button = driver.find_element(By.XPATH,"/html/body/div[1]/section/div/div/div/form/ul/li[6]/div/div/div/button")
    
    for level in levels:
        if level.lower() == 'internship':
            internship_button = driver.find_element(By.XPATH,EXPERIENCE_LEVEL_INTERNSHIP_BUTTON_XPATH)
            internship_button.click()
            done_button.click()

        if level.lower() == 'entry level':
            entry_level_button = driver.find_element(By.XPATH,EXPERIENCE_LEVEL_ENTRY_LEVEL_BUTTON_XPATH)
            entry_level_button.click()
            done_button.click()

def get_all_jobs():
    JOB_RESULTS_XPATH = "/html/body/div[1]/div/main/section[2]/ul"
    SHOW_MORE_XPATH = "/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/button[1]"
    DESCRIPTION_CLASS = "show-more-less-html__markup"
    COMPANY_CLASS = "base-search-card__subtitle"
    APPLY_XPATH = "/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/div/a"
    "/html/body/div[1]/div/main/section[2]/ul/li[1]/div/div[2]/h3"
    job_results = driver.find_element(By.XPATH,JOB_RESULTS_XPATH)
    results = job_results.find_elements(By.CLASS_NAME,"base-search-card__title")
    ans = []
    run = True
    a = 1
    Y = 0
    print("results are ",len(results))
    while run:
        try:
            # res = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[2]/ul/li["+str(a)+"]/div/div[2]/h3")
            res = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,
            "/html/body/div[1]/div/main/section[2]/ul/li["+str(a)+"]/div/a")))
            res.click()
            # driver.execute_script("arguments[0].click();", res)
            time.sleep(2)
            description = driver.find_element(By.CLASS_NAME, DESCRIPTION_CLASS)
            company = driver.find_element(By.CLASS_NAME, COMPANY_CLASS)
            "/html/body/div[1]/div/main/section[2]/ul/li[2]/div/a/span"
            role = driver.find_element(By.XPATH,"//html/body/div[1]/div/main/section[2]/ul/li["+str(a)+"]/div/a/span")
            # role = driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2")
            # print(len(description.text))
            try:
                link = driver.find_element(By.XPATH ,"/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/div/a").get_attribute('href')
                # print(company.text+" "+link)
                ans.append([link,description.text,company.text,role.text.replace(",","")])
                
            except:
                link = driver.current_url
                ans.append([link,description.text,company.text,role.text])
                time.sleep(3)
                a += 1
                continue
        except:
            run = False
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Y += 100

        a += 1 
    return ans


INTERNSHIP = 'internship'
ENTRY_LEVEL = 'entry level'
print(DRIVE_PATH)
driver = webdriver.Chrome(DRIVE_PATH)
driver.get("https://www.linkedin.com/jobs")

enter_job_title_search("software engineering","united states")
time.sleep(1)
filter_experience_levels([INTERNSHIP])
time.sleep(1)
filter_companies(["Amazon "])

jobs =  (get_all_jobs())
RESUME_PATH = "/Users/srinivaskoushik/Documents/resumes/resume.pdf"
resume = get_resume_text(RESUME_PATH)
today = datetime.date.today()
date = today.strftime("%m-%d-%y")
RESULT_PATH = os.path.join(curr_dir,"results")
FILE_NAME = os.path.join(RESULT_PATH,"jobs_"+date+".csv")
ats = []

for link,des,company,role in jobs:
    ats.append(check([des,resume]))
print(len(ats))

text = ""
count = 0
for i in range(0,len(ats)):
    link,description,company,role = jobs[i]
    if len(link) > 0:
        count += 1
        text += str(company) + ","+str(role).replace(","," ") + "," + str(link) +","+ ats[i]+"\n"
print(count)
if not os.path.exists(FILE_NAME):  
    f = open(FILE_NAME,"w")
    f.write("Company Name,Role,Job link, Similarity Score \n")
    f.close()
f = open(FILE_NAME,"a")
f.write(text)
f.close()

driver.quit() 