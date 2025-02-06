from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Set up the Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled") 


options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Specify the path to chromedriver
service = Service(r'C:\chromedriver-win64\chromedriver-win64\chromedriver.exe')

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(options=options)

# Open the URL
driver.get("https://www.check24.de/internet/")

try:
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick=\"Check24.cookieBanner.c24consent.giveConsent('fam')\"]")))
    cookie_button.click()
    print("Accepted cookies successfully.")
except Exception as e:
    print("Cookie button not found or could not be clicked:", e)

time.sleep(2)
    
try:
    radio_button = wait.until(EC.element_to_be_clickable((By.ID, "selectCustomerType-new")))
    radio_button.click()
    print("Clicked the checkbox/radio button successfully.")
except Exception as e:
    print("Radio button not found or could not be clicked:", e)

# Wait before closing the browser
time.sleep(1)  # Keeps the browser open for 5 seconds before closing

# Click the checkbox
try:
    checkbox = wait.until(EC.element_to_be_clickable((By.ID, "P0-0")))
    checkbox.click()
    print("Clicked the checkbox successfully.")
except Exception as e:
    print("Checkbox not found or could not be clicked:", e)

# Click the "Optionen" button to open the options modal
try:
    options_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Button to open options modal']")))
    options_button.click()
    print("Clicked the 'Optionen' button successfully.")
except Exception as e:
    print("Optionen button not found or could not be clicked:", e)

# Wait for the options modal to open
time.sleep(1)

# Locate and uncheck the checkbox (if it's checked)
try:
    checkbox = wait.until(EC.presence_of_element_located((By.ID, "P0-0")))
    
    # Check if the checkbox is selected
    if checkbox.is_selected():
        checkbox.click()  # Uncheck it
        print("Unchecked the checkbox successfully.")
    else:
        print("Checkbox was already unchecked.")
except Exception as e:
    print("Checkbox not found or could not be interacted with:", e)

# Click the "Optionen" button to open the options modal
try:
    options_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Button to open address modal']")))
    options_button.click()
    print("Clicked the 'Optionen' button successfully.")
except Exception as e:
    print("Optionen button not found or could not be clicked:", e)

# ✅ Enter ZIP Code using class and press Enter
try:
    zip_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='sc-dcJtft hHWbhe']")))  # XPath for class
    zip_input.click()
    time.sleep(1)  # Small pause before typing
    zip_input.clear()
    zip_input.send_keys("10785 Berlin")
    time.sleep(2)
    zip_input.send_keys(Keys.ENTER)
    print("Entered ZIP code and pressed Enter successfully.")
except Exception as e:
    print("ZIP code input field not found or could not be interacted with:", e)


# ✅ Enter Address using class and press Enter
try:
    addr_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='sc-dcJtft ctfhec']")))  # XPath for class
    addr_input.click()
    time.sleep(1)  # Small pause before typing
    addr_input.clear()
    addr_input.send_keys("Kurfürstenstraße")
    time.sleep(2)
    addr_input.send_keys(Keys.ENTER)
    print("Entered Addresss and pressed Enter successfully.")
except Exception as e:
    print("Addresss input field not found or could not be interacted with:", e)

# ✅ Enter "41" after Address field and press Enter
try:
    # We assume the cursor is already in the address field
    current_field = driver.switch_to.active_element  # Get the currently active (focused) element
    current_field.send_keys(" 41")  # Append ' 41' to the current field (after the address)
    time.sleep(1)  # Wait before sending Enter
    current_field.send_keys(Keys.ENTER)  # Press Enter
    print("Entered '41' and pressed Enter successfully.")
except Exception as e:
    print("Could not input '41' or press Enter:", e)

time.sleep(2)

# ✅ Click the 'Search' button to submit the form
try:
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(text(), 'vergleichen')]")))
    search_button.click()  # Click the search button
    print("Clicked the 'Search' button successfully.")
except Exception as e:
    print("Search button not found or could not be clicked:", e)

time.sleep(10)  



title = driver.title

# Print the title
print("Title of the webpage is:", title)

time.sleep(30)

# Wait for the desired div to be pr

# driver.quit()
