
import time, random, os, csv, platform
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui
import csv
from urllib.request import urlopen
from webdriver_manager.chrome import ChromeDriverManager
import re
import yaml
from datetime import datetime, timedelta

# paste your credencials for testing !warning non encrypted 
username = 'utkrishtsharma93@gmail.com'
password = 'bakri@994U'
# Define a set to hold existing profile links
existing_profile_links = set()

with open('linkedin_results.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Check if file is empty to write header only once
    if file.tell() == 0:
        writer.writerow(['Name', 'Profile Link', 'Profile Picture Link', 'Title', 'Company', 'Locations'])


class EasyApplyBot:
    # MAX_SEARCH_TIME is 10 hours by default, feel free to modify it
    MAX_SEARCH_TIME = 10 * 60 * 60
    chromedriver_path = "/Users/utkrisht/Desktop/Linkedin-Jobs-main/chromedriver"

    # Start the Chrome browser with Selenium WebDriver
    #browser = webdriver.Chrome()
    # Set up the service with the executable path
    service = Service(executable_path=chromedriver_path)
    # Initialize the Chrome WebDriver using the service
    driver = webdriver.Chrome(service=service)

    def __init__(self,
                 username,
                 password):

        print("Welcome to Easy Apply Bot")
        dirpath = os.getcwd()
        print("current directory is : " + dirpath)
        #self.options = self.browser_options()
        #self.browser = driver
        #self.wait = WebDriverWait(self.browser, 10)
        self.start_linkedin(username, password)

    def update_link_and_apply(self, new_link_url, location):
        global link_url
        link_url = new_link_url
        self.applications_loop(link_url, location)    


    def start_linkedin(self, username, password):
        print("Logging in.....Please wait :)  ")
        # Start the Chrome browser with Selenium WebDriver
        self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
        # Set an explicit wait of 10 seconds for the login button to be clickable
        # Wait for a few seconds (optional)
        time.sleep(5)
        try:
            user_field = self.browser = self.driver.find_element(By.ID, "username")
            #find_element_by_id("username")
            pw_field = self.browser = self.driver.find_element(By.ID, "password")
            #find_element_by_id("password")
            login_button = self.driver.find_element(by=By.CSS_SELECTOR, value=".btn__primary--large")
            #find_element_by_css_selector(".btn__primary--large")
            user_field.send_keys(username)
            user_field.send_keys(Keys.TAB)
            time.sleep(1)
            pw_field.send_keys(password)
            time.sleep(2)
            login_button.click()
            # Set the implicit wait to 10 seconds
            print("waiting bro ,, shoot its a nap ..")
            for i in range(30, 0, -1):
                print(f"\rTime left: {i} seconds", end='', flush=True)
                time.sleep(1)
        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found")

    def fill_data(self):
        self.driver.set_window_size(1000, 1000)
        self.driver.set_window_position(200, 200)

    def start_apply(self, positions, locations):
        start = time.time()
        self.fill_data()

        combos = []
        while len(combos) < len(positions) * len(locations):
            position = positions[random.randint(0, len(positions) - 1)]
            location = locations[random.randint(0, len(locations) - 1)]
            combo = (position, location)
            if combo not in combos:
                combos.append(combo)
                print(f"Applying to {position}: {location}")
                location = location
                self.applications_loop(position, location)
            if len(combos) > 500:
                break

    # self.finish_apply() --> this does seem to cause more harm than good, since it closes the browser which we usually don't want, other conditions will stop the loop and just break out
    def next_jobs_page(self, position, location, jobs_per_page):
        #self.browser.get(link_url + str(jobs_per_page))
        print(link_url + str(jobs_per_page))
        print("-------------")
        #self.avoid_lock()
        #log.info("Lock avoided.")
        self.load_page()
        return (self.browser, jobs_per_page)

    def applications_loop(self, position, location):

        count_application = 0
        count_job = 0
        jobs_per_page = 0
        start_time = time.time()
        # Check if the file already exists
        if os.path.exists('linkedin_results.csv'):
            with open('linkedin_results.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Add all existing profile links to the set
                existing_profile_links = {row[1] for row in reader if len(row) > 1}
        print("Looking for people.. Please verify bot if any.. 60 secs")
      


        

        while time.time() - start_time < self.MAX_SEARCH_TIME:
            global x
            #put your url here please -------------------- VvvvvvV
            link_url = 'https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102748797%22%5D&keywords=VP%20of%20Land&origin=FACETED_SEARCH&sid=Fp0'
            if x == 0:
                self.driver.get(link_url)
                x = 2
            else:
                y='&page='
                link_url = (link_url+y+str(x))
                self.driver.get(link_url)
                x += 1
            time.sleep(10)    
            element = self.driver.find_element(By.CSS_SELECTOR, '.reusable-search__entity-result-list.list-style-none')
            time.sleep(4)
            # Find all the individual result containers within the list
            results = element.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')    
            print("----------------")
            print(link_url)
            print("----------------")
            
            
            # Iterate through the results and extract the information
            print("--------------going in write csv loop now ----------------------")
            for result in results:
                try:
                    # Get name
                    name_text = result.find_element(By.CSS_SELECTOR, '.entity-result__title-text a').text
                    name = name_text.split('\n')[0] if '\n' in name_text else name_text

                    # Get LinkedIn profile link
                    profile_link = result.find_element(By.CSS_SELECTOR, '.entity-result__title-text a').get_attribute('href')
                    # Get profile picture link (inside try block to catch exceptions)
                    profile_picture_link = result.find_element(By.CSS_SELECTOR, 'img.presence-entity__image').get_attribute('src')
                    # Get title
                    title = result.find_element(By.CSS_SELECTOR, '.entity-result__primary-subtitle.t-14.t-black.t-normal').text
                    # Get company
                    # Get summary text
                    summary_text = result.find_element(By.CSS_SELECTOR, '.entity-result__summary.t-12.t-black--light').text
                    # Extract company name
                    company_name = summary_text.split('at ')[1].strip() if 'at ' in summary_text else 'Company not found'
                    company = company_name # or another appropriate selector based on your HTML structure

                    # Get locations
                    locations = [loc.text for loc in result.find_elements(By.CSS_SELECTOR, '.entity-result__secondary-subtitle.t-14.t-normal')]
                except NoSuchElementException:
                    profile_picture_link = 'No profile picture available'

                # Open the file for appending
                with open('linkedin_results.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Check if the profile link is already in the set
                    if profile_link not in existing_profile_links:
                        writer.writerow([name, profile_link, profile_picture_link, title, company, ', '.join(locations)])
                        # Add the profile link to the set
                        existing_profile_links.add(profile_link)

            try:

                # Find the next button, and click it
                #next_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.artdeco-pagination__button--next')))
                #next_button.click()
                time.sleep(2)
                #current_url = driver.current_url
                self.update_link_and_apply(link_url, location) # Call the method to update url loop 
            except:
                print(f"Could not click next on page , possibly last page.")
                break


if __name__ == '__main__':
    x = 0

    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    assert len(parameters['positions']) > 0
    assert len(parameters['locations']) > 0
    assert parameters['username'] is not None
    assert parameters['password'] is not None

    bot = EasyApplyBot(parameters['username'],parameters['password'])

    locations = [l for l in parameters['locations'] if l != None]
    positions = [p for p in parameters['positions'] if p != None]
    bot.start_apply(positions, locations)
