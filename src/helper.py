from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from atscheck import get_resume_text,check
import datetime
import os
import time


class Filter:
    def __init__(self, driver):
        self.driver = driver
        self.file = open("data.log","w")
        self.file.write("")
        self.JOB_TITLE_SEARCH_BAR_XPATH = "/html/body/main/section[1]/div/section/div[2]/" \
                                          "section[2]/form/section[1]/input"
        self.LOCATION_SEARCH_BAR_XPATH = "/html/body/main/section[1]/div/section/div[2]/" \
                                         "section[2]/form/section[2]/input"
        self.COMPANY_FILTER_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form[1]" \
                                           "/ul/li[3]/div/div/button"
        self.COMPANY_FILTER_NAME_XPATH = "/html/body/div[1]/section/div/div/div/form[1]/ul" \
                                         "/li[3]/div/div/div/section/input"
        self.EXPERIENCE_LEVEL_INTERNSHIP_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]" \
                                                        "/div/div/div/div/div/div[1]"
        self.EXPERIENCE_LEVEL_ENTRY_LEVEL_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]" \
                                                         "/div/div/div/div/div/div[2]"
        self.EXPERIENCE_ASSOCIATE_LEVEL_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]" \
                                                       "/div/div/div/div/div/div[3]"
        self.EXPERIENCE_MID_SENIOR_LEVEL_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]" \
                                                        "/div/div/div/div/div/div[4]"
        self.EXPERIENCE_DIRECTOR_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]" \
                                                "/div/div/div/div/div/div[5]"
        self.EXPERIENCE_EXECUTIVE_BUTTON_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]" \
                                                 "/div/div/div/div/div/div[6]"
        self.EXPERIENCE_LEVEL_XPATH = "/html/body/div[1]/section/div/div/div/form/ul/li[6]/div/div/button"

    """
    Enter the job title and location and search for jobs
    @:param title - Job Title
    @:parameter location - Location
    """
    def filter_job_title_search(self, title, location):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, self.JOB_TITLE_SEARCH_BAR_XPATH))
            ).send_keys(title)
            location_bar = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((
                By.XPATH, self.LOCATION_SEARCH_BAR_XPATH)))
            location_bar.clear()
            location_bar.send_keys(location)
            location_bar.send_keys(Keys.RETURN)
        except:
            self.file.write("ERROR FILTERING JOB TITLE \n")
            print("ERROR FILTERING JOB TITLE")

    """
    Filter experience level
    @:param levels - List of all levels to filter
    """
    def filter_experience_levels(self, levels):
        if len(levels) == 0:
            return
        done_button_path = "/html/body/div[1]/section/div/div/div/form/ul/li[6]/div/div/div/button"
        experience_level_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((
            By.XPATH, self.EXPERIENCE_LEVEL_XPATH)))
        experience_level_button.click()
        done_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((
            By.XPATH, done_button_path)))

        for level in levels:
            try:
                if level.lower() == 'internship':
                    internship_button = self.driver.find_element(By.XPATH, self.EXPERIENCE_LEVEL_INTERNSHIP_BUTTON_XPATH)
                    internship_button.click()
                    done_button.click()

                if level.lower() == 'entry level':
                    entry_level_button = self.driver.find_element(By.XPATH, self.EXPERIENCE_LEVEL_ENTRY_LEVEL_BUTTON_XPATH)
                    entry_level_button.click()
                    done_button.click()

                if level.lower() == "associate":
                    entry_level_button = self.driver.find_element(By.XPATH, self.EXPERIENCE_ASSOCIATE_LEVEL_BUTTON_XPATH)
                    entry_level_button.click()
                    done_button.click()

                if level.lower() == "mid_senior":
                    entry_level_button = self.driver.find_element(By.XPATH, self.EXPERIENCE_MID_SENIOR_LEVEL_BUTTON_XPATH)
                    entry_level_button.click()
                    done_button.click()

                if level.lower() == "director":
                    entry_level_button = self.driver.find_element(By.XPATH, self.EXPERIENCE_DIRECTOR_BUTTON_XPATH)
                    entry_level_button.click()
                    done_button.click()

                if level.lower() == "executive":
                    entry_level_button = self.driver.find_element(By.XPATH, self.EXPERIENCE_EXECUTIVE_BUTTON_XPATH)
                    entry_level_button.click()
                    done_button.click()
            except:
                self.file.write("ERROR FILTERING LEVELS \n")
                print("ERROR FILTERING LEVELS")
                continue

    """
    Filter experience level
    @:param levels - List of all companies for filter
    """
    def filter_companies(self, companies):
        try:
            if len(companies) == 0:
                return
            self.driver.find_element(By.XPATH, self.COMPANY_FILTER_BUTTON_XPATH).click()
            class_name = "typeahead-input__dropdown-item"
            for company in companies:
                text = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((
                    By.XPATH, self.COMPANY_FILTER_NAME_XPATH)))
                text.send_keys(company)
                time.sleep(1.5)
                text.send_keys(" ")
                time.sleep(1.5)
                text.send_keys(" ")
                res = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located(
                            (By.CLASS_NAME, class_name)
                        ))
                if len(res) > 0:
                    text.send_keys(Keys.ARROW_DOWN)
                    text.send_keys(Keys.RETURN)
        except:
            self.file.write(company.upper()+" NOT FOUND \n")
            print(company+" NOT FOUND")

    def filter_companies_and_experience_levels(self, levels, companies):
        try:
            self.filter_experience_levels(levels)
            self.filter_companies(companies)
            done = "/html/body/div[1]/section/div/div/div/form[1]/ul/li[3]/div/div/div/button"
            self.driver.find_element(By.XPATH, done).click()
        except:
            self.file.write("ERROR APPLYING FILTERS \n")
            print("ERROR APPLYING FILTERS")


class Jobs:
    curr_dir = os.getcwd()
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.headless = True
        self.driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.filter_helper = Filter(self.driver)
        self.URL = "https://www.linkedin.com/jobs"
        self.JOB_RESULTS_XPATH = "/html/body/div[1]/div/main/section[2]/ul"
        self.DESCRIPTION_CLASS = "show-more-less-html__markup"
        self.COMPANY_CLASS = "base-search-card__subtitle"
        self.file = open("data.log","w")

    """
    Direct the chromedriver to linked.com/jobs 
    """
    def direct(self):
        self.driver.minimize_window()
        self.driver.get(self.URL)
        
    """
    Close the chromedriver
    """
    def close(self):
        self.driver.quit()
        self.file.close()

    """
    Filter the jobs based on title, location, levels and companies
    @:param job_title : Title of job
    @:param location : Prefered location
    @:param levels : Experience level
    @:param companied : Filtered Companies
    """
    def filter(self,job_title,location,levels,companies):
        self.filter_helper.filter_job_title_search(job_title,location)
        self.filter_helper.filter_companies_and_experience_levels(levels,companies)

    """
    Fetch all the jobs on the website
    @:return list([link, description, company, role]) 
    """
    def get_jobs(self):
        try:
            job_results = self.driver.find_element(By.XPATH, self.JOB_RESULTS_XPATH)
            results = job_results.find_elements(By.CLASS_NAME, "base-search-card__title")
            ans = []
            run = True
            count = 1
            Y = 0
            while run:
                try:
                    print("PROCESSING JOB"+str(count))
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    res = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
                        (By.XPATH,"/html/body/div[1]/div/main/section[2]/ul/li[" + str(count) + "]/div/a")))
                    res.click()
                except:
                    run = False
                    continue
                
                time.sleep(2.25)
                try:
                    description = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                        (By.CLASS_NAME,self.DESCRIPTION_CLASS)))
                    company = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                        (By.CLASS_NAME, self.COMPANY_CLASS)))
                    role = self.driver.find_element(By.XPATH,
                                            "//html/body/div[1]/div/main/section[2]/ul/li[" + str(count) + "]/div/a/span")
                    try:
                        link = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[1]/div/section/div[2]/"
                                                "section/div/div[1]/div/div/a").get_attribute('href')

                        ans.append([link, description.text, company.text, role.text.replace(",", "")])
                    except:
                        link = self.driver.current_url
                        ans.append([link, description.text, company.text, role.text])
                        continue
                except:
                    self.file.write("ERROR PROCESSING JOB "+str(count)+" \n")
                    print("ERROR PROCESSING JOB "+str(count))
                count += 1   

            print("PROCESSED "+str(count)+ " JOBS")
            self.file.write("SUCCESS \n")
            print("SUCCESS \n")
            return ans
        except:
            self.file.write("SUCCESS \n")
            print("ERROR PROCESSING JOBS")
            return []


class Export:
    def __init__(self,resume_path):
        self.RESUME_PATH = resume_path
        self.curr_dir = os.getcwd()

    """
    Reads the resume and get the ATS similarity score
    @:param jobs : list of jobs cotaining link, description, name, role
    @:return : list of ATS scores.
    """
    def get_ats_score(self, jobs):
        resume = get_resume_text(self.RESUME_PATH)
        ats = []
        for link, des, company, role in jobs:
            ats.append(check([des, resume]))
        return ats

    """
    Export the essential information to a CSV file to ./results 
    the results are grouped by daily
    The fields are 
    * Link
    * Description
    * Company Name
    * Role Name
    * ATS Score
    """
    def export(self,jobs,ats):
        today = datetime.date.today()
        date = today.strftime("%m-%d-%y")
        RESULT_PATH = os.path.join(self.curr_dir, "results")
        FILE_NAME = os.path.join(RESULT_PATH, "jobs_" + date + ".csv")
        text = ""
        count = 0
        for i in range(0, len(jobs)):
            # print(jobs[i])
            link, description, company, role = jobs[i]
            if len(link) > 0:
                count += 1
                text += str(company) + "," + str(role).replace(",", " ") + "," + str(link) + "," + ats[i] + "\n"
        # print(count)
        if not os.path.exists(FILE_NAME):
            f = open(FILE_NAME, "w")
            f.write("Company Name,Role,Job link, Similarity Score \n")
            f.close()
        f = open(FILE_NAME, "a")
        f.write(text)
        f.close()

# INTERNSHIP = 'internship'
# ENTRY_LEVEL = 'entry level'

# jobs = Jobs()
# jobs.direct()
# jobs.filter("software engineering","united states",["internship"],["Amazon"])
# all_jobs = jobs.get_jobs()

# export = Export("/Users/srinivaskoushik/Documents/resumes/resume.pdf")
# ats = export.get_ats_score(all_jobs)
# export.export(all_jobs,ats)
# jobs.close()