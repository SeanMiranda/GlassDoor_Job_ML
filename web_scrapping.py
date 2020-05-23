from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.glassdoor.co.in/Job/new-york-machine-learning-engineer-jobs-SRCH_IL.0,8_IC1132348_KO9,34.htm')

    jobs = []

    while len(jobs) < num_jobs:
        time.sleep(20)

        try:
            driver.find_element_by_xpath("//span[@alt='Close']").click()
        except:
            pass

        jobs_containers = driver.find_elements_by_xpath("//div[@class='jobContainer']")

        for job_container in jobs_containers:

            if len(jobs) >= num_jobs:
                break

            job_container.click()

            collected_successfully = False

            try:
                company_name = driver.find_element_by_xpath("(//div[@class='employerName'])[1]").text
                location = driver.find_element_by_xpath('(//div[@class="location"])[1]').text
                job_title = driver.find_element_by_xpath('(//div[contains(@class, "title")])[1]').text
                job_description = driver.find_element_by_xpath('//div[@class="jobDescriptionContent desc"]').text
                collected_successfully = True
            except:
                time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('//span[@class="gray salary"]').text
            except NoSuchElementException:
                salary_estimate = -1

            try:
                rating = driver.find_element_by_xpath('(//span[@class="rating"])[1]').text
            except NoSuchElementException:
                rating = -1

            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))


            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
                time.sleep(10)

                try:
            
                    headquarters = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element_by_xpath(
                        './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})

        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
    
    driver.close()
    return pd.DataFrame(jobs)


if __name__ == '__main__':
    df = get_jobs("data scientist", 5, True)
    df.to_csv('data.csv')
