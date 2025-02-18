from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import configparser
import csv
import os

class Check24Crawler:
    def __init__(self):
        config = configparser.ConfigParser()
        with open("input.ini", "r", encoding="utf-8") as f:
            config.read_file(f)
        self.pincode = config['check24']['pincode']
        self.street = config['check24']['street']
        self.house_no = config['check24']['house_no']
        self.url = config['check24']['url']
        self.input_csv_file = config['check24']['input_csv_file']
        self.output_csv_file = config['check24']['output_csv_file']
        self.current_time = time.strftime("%d.%m.%Y")

    def start_browser_engine(self):
        options = webdriver.ChromeOptions()
        
        # Run Chrome in headless mode (no GUI)
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu")  
        options.add_argument("--window-size=1920x1080")  # Ensures proper page loading
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  
        options.add_argument("--disable-blink-features=AutomationControlled")  
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        # Specify the path to the ChromeDriver service
        service = Service(r'C:\chromedriver-win64\chromedriver-win64\chromedriver.exe')
        
        # Pass the service object when initializing the WebDriver
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.url)

    def accepet_cookies(self):
        try:
            self.wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
            cookie_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick=\"Check24.cookieBanner.c24consent.giveConsent('fam')\"]")))
            cookie_button.click()
            # print("Accepted cookies successfully.")
            time.sleep(2)
        except Exception as e:
            print("Cookie button not found or could not be clicked:", e)

    def click_checkboxes(self):
        try:
            radio_button = self.wait.until(EC.element_to_be_clickable((By.ID, "selectCustomerType-new")))
            radio_button.click()
            # print("Clicked the checkbox/radio button successfully.")
        except Exception as e:
            print("Radio button not found or could not be clicked:", e)
        time.sleep(1)

        # Click the checkbox
        # try:
        #     checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, "P0-0")))
        #     checkbox.click()
        #     print("Clicked the checkbox successfully.")
        # except Exception as e:
        #     print("Checkbox not found or could not be clicked:", e)

        # Click the "Optionen" button to open the options modal
        try:
            options_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Button to open options modal']")))
            options_button.click()
            # print("Clicked the 'Optionen' button successfully.")
        except Exception as e:
            print("Optionen button not found or could not be clicked:", e)

        time.sleep(1)

        # Locate and uncheck the checkbox (if it's checked)
        try:
            checkbox = self.wait.until(EC.presence_of_element_located((By.ID, "P0-0")))
            
            # Check if the checkbox is selected
            if checkbox.is_selected():
                checkbox.click()  # Uncheck it
                # print("Unchecked the checkbox successfully.")
        except Exception as e:
            print("Checkbox not found or could not be interacted with:", e)

    def enter_address(self,pincode,street_name,house_number):
        try:
            options_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Button to open address modal']")))
            options_button.click()
            # print("Clicked the 'Optionen' button successfully.")
        except Exception as e:
            print("Optionen button not found or could not be clicked:", e)

        # Enter ZIP Code using class and press Enter
        try:
            zip_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='sc-dcJtft hHWbhe']")))  # XPath for class
            zip_input.click()
            time.sleep(1)  # Small pause before typing
            zip_input.clear()
            zip_input.send_keys(pincode)
            time.sleep(3)
            zip_input.send_keys(Keys.ENTER)
            time.sleep(1)
            # print("Entered ZIP code and pressed Enter successfully.")
        except Exception as e:
            print("ZIP code input field not found or could not be interacted with:", e)

        # Enter Address using class and press Enter
        try:
            addr_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='sc-dcJtft ctfhec']")))  # XPath for class
            addr_input.click()
            time.sleep(1)  # Small pause before typing
            addr_input.clear()
            addr_input.send_keys(street_name)
            time.sleep(3)
            addr_input.send_keys(Keys.ENTER)
            time.sleep(1)
            # print("Entered Addresss and pressed Enter successfully.")
        except Exception as e:
            print("Addresss input field not found or could not be interacted with:", e)

        # Enter house no. after Address field and press Enter
        try:
            # We assume the cursor is already in the address field
            current_field = self.driver.switch_to.active_element  # Get the currently active (focused) element
            current_field.send_keys(house_number)  # Append ' 41' to the current field (after the address)
            time.sleep(1)  # Wait before sending Enter
            current_field.send_keys(Keys.ENTER)  # Press Enter
            # print("Entered '41' and pressed Enter successfully.")
        except Exception as e:
            print("Could not input '41' or press Enter:", e)

        time.sleep(2)

        # Click the 'Search' button to submit the form
        try:
            search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(text(), 'vergleichen')]")))
            search_button.click()  # Click the search button
            # print("Clicked the 'Search' button successfully.")
        except Exception as e:
            print("Search button not found or could not be clicked:", e)

        time.sleep(10)  

    def filter_speed(self):
        try:
            sort_dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "tko-sort-select")))
            select = Select(sort_dropdown)
            select.select_by_value("downstream")
            # print("Selected 'Geschwindigkeit' successfully.")
        except Exception as e:
            print("Sort dropdown or option not found:", e)

        time.sleep(8)

    def filter_glassfiber(self):
        # Check the "Glasfaser" checkbox
        try:
            fiberglass_checkbox = self.wait.until(EC.presence_of_element_located((By.NAME, "c24api_transfertype_fiberglass")))
            self.driver.execute_script("arguments[0].click();", fiberglass_checkbox)
            # print("Checked the 'Glasfaser' checkbox successfully.")
        except Exception as e:
            print("Checkbox not found or could not be clicked:", e)

        time.sleep(8) 

    def fetch_results(self):
        output_list = []
        network_provider_list = []
        note_months = []
        # Fetch all result divs inside the main container
        try:
            result_container = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-bam-element-identifier='tileContainer']")))
            result_divs = result_container.find_elements(By.XPATH, "./div/div/div")  # Adjusted to navigate inside the container

            result_class_names = [div.get_attribute("class") for div in result_divs]
            # print("Class names of result divs:", result_class_names)
        except Exception as e:
            print("Could not fetch result divs:", e)

        # Loop through each result div and extract the title from the span tag
        try:
            result_container = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-bam-element-identifier='tileContainer']")))
            result_divs = result_container.find_elements(By.XPATH, "./div/div/div")  # Locate all result divs
            
            for div in result_divs:
                try:
                    connection_speed = div.find_element(By.XPATH, ".//div[@class='tko-flatrate-value']")
                    title_span = div.find_element(By.XPATH, ".//span[@class='tko-tariffname-text']")
                    network_provider_div = div.find_element(By.XPATH, ".//div[@class='tko-providerlogo']")
                    img_element = network_provider_div.find_element(By.TAG_NAME, "img")
                    network_provider = img_element.get_attribute("title")
                    title_text = title_span.text
                    connection_speed_text = connection_speed.text
                    if connection_speed_text == "1.000 MBit/s":
                        network_provider_list.append(network_provider)
                        try:
                            # Locate the div with class "tko-tariff-note"
                            tariff_note_div = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tko-tariff-note")))

                            # Extract text from span and the div
                            span_text = tariff_note_div.find_element(By.TAG_NAME, "span").text  # Get text from span
                            cleaned_span_text = span_text.replace("Note:verfügbar ab", "").replace(":", "")
                            div_text = tariff_note_div.find_element(By.TAG_NAME, "div").text  # Get text from the div

                            # Combine the extracted text
                            # final_text = f"{span_text} {div_text}"
                            final_text = f"{cleaned_span_text} "
                            # print("Tariff Note:", final_text)
                        except Exception as e:
                            final_text = ""
                            print("Tariff note div not found or could not be accessed:", e)

                        # formatted_result = "Network Provider: " + network_provider + " | Tariff Title:" + title_text + "| Speed:" + connection_speed_text + "| Note:" +final_text
                        # formatted_result = str(self.current_time) + " ES: Laut check24 von " +  network_provider
                        # 06.02.2025 ES: Laut check24 in Kurfürstenstraße 41 GF von Vodafone, 1&1, Maingau... verfügbar.
                        note_months.append(final_text)
                        # output_list.append(formatted_result)    
 
                except Exception as e:
                    print("Title span not found in this div")
        except Exception as e:
            print("Could not fetch result divs:", e)

        formatted_result = str(self.current_time) + " ES: Laut check24 von " +  ", ".join(network_provider_list) + ". Note: (" + ", ".join(note_months) + ")" 

        # print(formatted_result, "========================formatted_result")

        return formatted_result

    def execute(self,pincode,street_name,house_number):
        self.start_browser_engine()
        self.accepet_cookies()
        self.click_checkboxes()
        self.enter_address(pincode,street_name,house_number)
        self.filter_speed()
        self.filter_glassfiber()
        formatted_result = self.fetch_results()
        return formatted_result

    def fetch_address(self):
        counter = 0
        # Read the CSV file
        with open(self.input_csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                if len(row) >= 3:  # Ensure the row has enough columns
                    pincode = row[0].strip() + " Berlin"
                    street_name = row[1].strip()
                    house_number = row[2].strip()
                    
                    # print(pincode,street_name,house_number,"\n")
                    if pincode and street_name and house_number: 
                        formatted_result = self.execute(pincode,street_name,house_number)
                        self.driver.quit()
                        self.write_to_csv(pincode,street_name,house_number,formatted_result)
                        counter+=1
                    
                    # if counter>4:
                    #     break
                
    def write_to_csv(self,pincode,street_name,house_number,formatted_result):
        # Check if file exists
        file_exists = os.path.isfile(self.output_csv_file)

        # Open the file in append mode (or create it if it doesn’t exist)
        with open(self.output_csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write headers only if file doesn't exist
            if not file_exists:
                writer.writerow(["pincode", "street_name", "house_number", "results"])  # Header

            # Append new row (joining list values with a separator, e.g., `|`)
            writer.writerow([pincode, street_name, house_number, formatted_result])

        print("Data written successfully!")

if __name__=="__main__":
    Check24Crawler_obj = Check24Crawler()
    # Check24Crawler_obj.execute()
    Check24Crawler_obj.fetch_address()