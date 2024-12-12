import datetime
from datetime import datetime
from tokenize import String

import requests
import json
from selenium.webdriver.common.by import By
import time
from random import randint
from extract_skills import extract_skills

class Extract:

    def __init__(self,driver,wait,ec):
        self.driver = driver
        self.wait = wait
        self.ec = ec

        # Posted_date,Job Title,Company,Company Logo URL,Location,Skills,Salary Info
        self.job_titles=[]
        self.company_names=[]
        self.skills=[]
        self.logo_urls=[]
        self.salaries=[]
        self.posted_dates=[]
        self.locations=[]
        self.current_url =""


    def page_load(self,title,country):
        pagination_num=2
        self.current_url = f"https://www.indeed.com/jobs?q={title}&l={country}&radius=25&start=0&vjk=1141da45d537702b"
        # self.current_url = f"https://www.indeed.com/jobs?q={title}&l={country}&from=searchOnDesktopSerp&vjk=63d19ad35cb6472d"
        while True:

            time.sleep(randint(2,7))

            if self.driver.current_url != self.current_url:
                self.driver.get(self.current_url)


            job_elements = self.driver.find_elements(By.XPATH, "//a[starts-with(@id, 'job_')]")
            job_ids = [element.get_attribute("id").replace("job_", "") for element in job_elements]

            for job_id in job_ids:
                self.__get_json(job_id)

            try:

                time.sleep(randint(1,3))
                self.driver.get(self.current_url)

                pagination_button = self.wait.until(self.ec.element_to_be_clickable(
                    (By.XPATH, f'/html/body/main/div/div[2]/div/div[5]/div/div[1]/nav/ul/li[{pagination_num}]')))
                time.sleep(randint(1, 5))
                pagination_button.click()
                pagination_num=pagination_num+1
                self.current_url = self.driver.current_url
            except:

                try:
                    pagination_button = self.wait.until(self.ec.element_to_be_clickable(
                        (By.XPATH, f'/html/body/main/div/div[2]/div/div[5]/div/div[1]/nav/ul/li[7]')))
                    time.sleep(randint(1, 5))
                    pagination_num=3
                    pagination_button.click()
                    self.current_url = self.driver.current_url
                except:
                    try:
                        pagination_button = self.wait.until(self.ec.element_to_be_clickable(
                            (By.XPATH, f'/html/body/main/div/div[2]/div/div[5]/div/div[1]/nav/ul/li[6]')))
                        time.sleep(randint(1, 5))
                        pagination_num=3
                        pagination_button.click()
                        self.current_url = self.driver.current_url
                    except:
                        break


    def __get_json(self, job_id):
        try:
            job_url = f"https://www.indeed.com/viewjob?jk={job_id}&from=vjs&viewtype=embedded&spa=1&hidecmpheader=0'"

            time.sleep(randint(1,15))
            self.driver.get(job_url)

            # Get the full page source
            page_source = self.driver.page_source

            # Locate the full JSON embedded in the page
            json_start = page_source.find('{"status":"success"')
            json_end = page_source.rfind('}') + 1
            full_json_string = page_source[json_start:json_end]
            # Parse the JSON
            try:
                full_json_data = json.loads(full_json_string)
                self.__extract_details(full_json_data)  # Process the data

            except Exception as e:
                print( e)
        except:
            pass

    def __extract_details(self, json_data):

        job_title = company = skill = square_logo = posted_date = location = salary = 'NA'

        try:
            # Safely extracting job title
            job_path =['body','hostQueryExecutionResult','data','jobData','results',0,'job','title']
            job_title = self.__get_text_or_nan(json_data,job_path)

            posted_date_path =['body','hostQueryExecutionResult','data','jobData','results',0,'job','datePublished']
            posted_date = self.__get_text_or_nan(json_data,posted_date_path)
            if type(posted_date)== int:
                posted_date = posted_date / 1000
                posted_date = datetime.utcfromtimestamp(posted_date)
                posted_date = posted_date.strftime('%m-%d-%Y')


            location_path = ['body','hostQueryExecutionResult','data','jobData','results',0,'job','location','formatted','short']
            location = self.__get_text_or_nan(json_data,location_path)

            company_name_path =['body','hostQueryExecutionResult','data','jobData','results',0,'job','source','name']
            company = self.__get_text_or_nan(json_data,company_name_path)

            skill_path = ['body','mosaicData','serverContextData','request','data','metaData',"js-match-insights-provider-job-details",'judyResponse','taxonomyEntityMatch','taxonomyEntity',1,'customClasses']
            skill = self.__get_text_or_nan(json_data,skill_path)
            if type(skill)== list:
                skill = self.__extract_raw_names(skill)
                skill= extract_skills(skill)

            salary_raw = ['body', 'salaryInfoModel','salaryText']
            salary = self.__get_text_or_nan(json_data,salary_raw)
            if not salary.startswith("NA"):
                salary = salary.replace("a year", "")

            square_logo_url_path =['body','hostQueryExecutionResult','data','jobData','results',0,'job','employer','dossier','images','squareLogoUrls','url256']
            square_logo = self.__get_text_or_nan(json_data,square_logo_url_path)

            print(
                f"ID:{len(self.job_titles)}  Job Title: {job_title}, Company Name: {company}, Skills: {skill}, Salary: {salary}, Posted Date: {posted_date}, Location: {location}, Logo URL: {square_logo}")

        except Exception as e:
            print( e)

        self.job_titles.append(job_title)
        self.company_names.append(company)
        self.skills.append(skill)
        self.logo_urls.append(square_logo)
        self.posted_dates.append(posted_date)
        self.locations.append(location)
        self.salaries.append(salary)



    def __get_text_or_nan(self,json_data,path):
        try:
            current_data = json_data
            for key in path:
                current_data = current_data[key]  # Navigate deeper at each step
            return current_data  # Return the final value after traversing all keys
        except (KeyError, TypeError, IndexError):
            return "NA"


    def __extract_raw_names(self,custom_classes):
        """ Extracts the 'rawName' from each entry in the customClasses list. """
        raw_names_list = []
        for item in custom_classes:
            # Check if 'rawName' exists and if so, append to the list
            if 'rawName' in item:
                raw_names_list.append(item['rawName'])

        # Return list of raw names
        raw_names=", ".join(raw_names_list)
        return raw_names

    def get_job_titles(self):
        return self.job_titles

    # Getter for company_names
    def get_company_names(self):
        return self.company_names

    # Getter for skills
    def get_skills(self):
        return self.skills

    # Getter for logo_urls
    def get_logo_urls(self):
        return self.logo_urls

    # Getter for salaries
    def get_salaries(self):
        return self.salaries

    # Getter for posted_dates
    def get_posted_dates(self):
        return self.posted_dates

    # Getter for locations
    def get_locations(self):
        return self.locations