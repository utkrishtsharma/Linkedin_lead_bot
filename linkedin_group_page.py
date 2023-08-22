
from intro import display_large_message
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

with open('linkedin_group_results.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Check if file is empty to write header only once
    if file.tell() == 0:
        writer.writerow(['Name', 'Profile Link', 'Title'])


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
        if os.path.exists('linkedin_group_results.csv'):
            with open('linkedin_group_results.csv', mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Add all existing profile links to the set
                existing_profile_links = {row[1] for row in reader if len(row) > 1}
        print("Looking for people.. Please verify bot if any.. 60 secs")
      


        

        while time.time() - start_time < self.MAX_SEARCH_TIME:
            global x
            #put your url here please -------------------- VvvvvvV put link here please , PUT LINK HERE PLEASE
            link_url = 'https://www.linkedin.com/groups/87188/members/'
            self.driver.get(link_url)

            time.sleep(5)
            # Wait for the main element to be present
            element = WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.artdeco-list__item.groups-members-list__typeahead-result')))
            # Find all elements with the class 'ui-entity-action-row' directly
            results = self.driver.find_elements(By.CSS_SELECTOR, '.ui-entity-action-row')

            # Extract and print the names and titles from each result
            for result in results:
                name = result.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__title').text
                title = result.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__subtitle').text
                profile_link = result.find_element(By.CSS_SELECTOR, 'a.ui-conditional-link-wrapper').get_attribute('href')
                print(f"Name: {name}, Title: {title}, Profile Link: {profile_link}")


            # Initialization before the loop
            data_to_write = []

            print("--------------going in write csv loop now ----------------------")

            for result in results:
                try:
                    name = result.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__title').text
                except NoSuchElementException:
                    name = 'Name not available'

                try:
                    profile_link = result.find_element(By.CSS_SELECTOR, 'a.ui-conditional-link-wrapper').get_attribute('href')
                except NoSuchElementException:
                    profile_link = 'Profile link not available'

                try:
                    title = result.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__subtitle').text
                except NoSuchElementException:
                    title = 'Title not available'

                # If the profile link isn't in the existing links, add the data to the list to write
                if profile_link not in existing_profile_links:
                    data_to_write.append([name, profile_link, title])
                    existing_profile_links.add(profile_link)

            # Write all the gathered data to the CSV, opening the file just once
            with open('linkedin_group_results.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data_to_write)
            #wait for 5 sec
            time.sleep(5)
            print("--- scrollin down.. -----  ")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)
            # If the profile link isn't in the existing links, add the data to the list to write
            if profile_link not in existing_profile_links:
                data_to_write.append([name, profile_link, title])
                existing_profile_links.add(profile_link)
            while True:
                try:
                    # Wait for the load more button to be present and clickable, but only for a short duration.
                    wait = WebDriverWait(self.driver, 5)
                    load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.scaffold-finite-scroll__load-button')))
                    load_more_button.click()
                except (TimeoutException, StaleElementReferenceException):  
                    # If "load more" button isn't found or if it's stale, we'll scroll down
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # After scrolling, give some delay to let the content load
                    time.sleep(10)
                    # If the profile link isn't in the existing links, add the data to the list to write
                    if profile_link not in existing_profile_links:
                        data_to_write.append([name, profile_link, title])
                        existing_profile_links.add(profile_link)
                except NoSuchElementException:
                    # If there's no such element exception, it means the "load more" button isn't present, hence break the loop
                    break



            # Find all the individual result containers within the list
            """
            results = element.find_elements(By.CSS_SELECTOR, '.ui-entity-action-row')    
            print("----------------")
            print(link_url)
            print("----------------")
            # Print the text of each result
            for result in results:
                print(result.text)
                print("----------------")
            
            
            # Iterate through the results and extract the information
            print("--------------going in write csv loop now ----------------------")
            for result in results:
                try:
                    name = result.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__title').text
                except NoSuchElementException:
                    name = 'Name not available'

                try:
                    profile_link = result.find_element(By.CSS_SELECTOR, 'a.ui-entity-action-row__link').get_attribute('href')
                except NoSuchElementException:
                    profile_link = 'Profile link not available'

                try:
                    profile_picture_link = result.find_element(By.CSS_SELECTOR, 'img.presence-entity__image').get_attribute('src')
                except NoSuchElementException:
                    profile_picture_link = 'No profile picture available'

                try:
                    title = result.find_element(By.CSS_SELECTOR, '.artdeco-entity-lockup__subtitle').text
                except NoSuchElementException:
                    title = 'Title not available'

                # Open the file for appending
                with open('linkedin_group_results.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    # Check if the profile link is already in the set
                    if profile_link not in existing_profile_links:
                        writer.writerow([name, profile_link, profile_picture_link, title])
                        # Add the profile link to the set
                        existing_profile_links.add(profile_link)

            try:
                # Scroll to the bottom of the page to ensure the "Show more results" button is in view.
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Replace with your actual CSS selector for the button
                button_css_selector = '.artdeco-button.artdeco-button--muted.scaffold-finite-scroll__load-button'

                # Wait for the "Show more results" button to be clickable.
                show_more_button = WebDriverWait(self.driver, 7).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector))
                )


                show_more_button.click()

                # Wait for elements to load after the click.
                time.sleep(5)
                #  sself.applications_loop(position, location)
                
            except TimeoutException:
                print("Waited too long for the 'Show more results' button to be clickable.")
                break
            except StaleElementReferenceException:
                print("Encountered StaleElement error. Will continue to next iteration.")
                continue
            except Exception as e:
                print(f"Unexpected error: {e}. Could not click next, possibly last person.")
                break
            """    


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
    display_large_message()
    bot.start_apply(positions, locations)
