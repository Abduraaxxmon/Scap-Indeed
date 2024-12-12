import time
import requests
from extract import Extract
from search_req import country_list,job_list
from config import driver,wait,EC
from search import search
from selenium.webdriver.common.by import By
# from extract import Extract
from collect import save_dataframe_to_csv,collect_into_dataframe
from datetime import datetime
# time.sleep(60*60)
data = Extract(ec=EC, wait=wait, driver=driver)

for title in job_list:

    for country in country_list:
        search(title=title,country=country,driver=driver,wait=wait,ec=EC)
        # time.sleep(60*60)
        data.page_load(title=title,country=country)

    save_dataframe_to_csv(df=collect_into_dataframe(
        job=title,
        country="Germany",
        name_companies= data.get_company_names(),
        skills= data.get_skills(),
        location_jobs= data.get_locations(),
        job_titles= data.get_job_titles(),
        logo_urls= data.get_logo_urls(),
        post_dates=data.get_posted_dates(),
        salary_list= data.get_salaries()
    ),file_name=f"{title}data",folder_name=f"{datetime.today().strftime('%Y-%m-%d')} data")





