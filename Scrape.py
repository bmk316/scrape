"""
A quick scrape of Indeed.com to fetch Data Analyst job positions
and export results onto a CSV file.
"""

from bs4 import BeautifulSoup as bs
import requests
import time
import csv
import os

#Extraction from one page
pages = [0]

file_name = "job_file.csv"
f = open(file_name, "w")

headers = 'Job-Title,Company Name,Location,Description,Salary\n'
f.write(headers)

for page in pages:
    source = requests.get("https://www.indeed.com/jobs?q=data+analyst&l=Atlanta%2C+GA&start={}".format(page)).text

    soup = bs(source, "html.parser")

    for jobs in soup.findAll(class_='result'):

        try:
            job_title = jobs.h2.a.text.strip()
            # job_title = jobs.find('h2', {'class': 'title'}).text.strip().replace("new", "").rstrip()
        except Exception as e:
            job_title = None
        print('Job-Title: ', job_title)

        try:
            company_name = jobs.find('span', {'class': 'company'}).text.strip()
        except Exception as e:
            company_name = None
        print("Company Name: ", company_name)

        try:
            location = jobs.find('span', {'class': 'location accessible-contrast-color-location'}).text.strip()\
                .replace(",", "|")
        except Exception as e:
            location = None
        print("Location: ", location)

        try:

            summary = jobs.find('div', {'class': 'summary'}).text.strip().replace(",", "|").replace(".", "|").replace(
                '\n', '')  # added the last replace here
        except Exception as e:
            summary = None
        print("Description: ", summary)

        try:
            salary = jobs.find('span', class_="no-wrap").text.strip().replace(",", "")
        except Exception as e:
            salary = None
        print("Salary:", salary)

        f.write(str(job_title) + "," + str(company_name) + "," + str(location) + "," + str(summary) + "," + str(salary) + "\n")
        # csv_print.writerow([job_title, company_name, summary, salary])

        print("-------------------------------------------------------------")

        time.sleep(3)
f.close()
