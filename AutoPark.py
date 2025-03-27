import os
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

def automate_web_interaction(url, license_plate):
    """Automate the web interaction with correct workflow order"""
    # Set up Firefox options
    opts = FirefoxOptions()
    opts.add_argument("--width=1200")
    opts.add_argument("--height=800")
    opts.binary_location = "/snap/bin/firefox"  # Explicit path for GitHub Actions
    
    # Use webdriver-manager to handle geckodriver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=opts)
    
    try:
        # Open the URL directly
        print(f"Opening URL: {url}")
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 1. Find and fill license plate field
        print("Entering license plate...")
        num_plate_field = driver.find_element(By.NAME, "Rego")
        num_plate_field.clear()
        num_plate_field.send_keys(license_plate)
        
        # 2. Find and click "Start Session" button
        print("Clicking 'Start Session' button...")
        start_session_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
            "//button[contains(@class, 'btn-primary')]//span[contains(@class, 'btn-label')]/span[contains(@class, 'fa-sign-in')]")))
        start_session_button.click()
        
        # Wait for confirmation section to load
        time.sleep(2)  # Adjust based on page load time
        
        # 3. Find and tick confirmation box
        print("Ticking confirmation box...")
        confirmation_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, 
        "//input[@type='checkbox' and (@id='dddd' or @name='ss' or @ng-model='tickagree')]"))
        )
        if not confirmation_box.is_selected():
            confirmation_box.click()
        
        # 4. Find and click final "Start" button
        print("Clicking final 'Start' button...")
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "//button[contains(text(), 'Start') and not(contains(text(), 'Start Session'))]"))
        )
        start_button.click()
        
        print("Process completed successfully!")
        
        # Keep browser open for observation
        time.sleep(10)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    # The URL you already have
    target_url = "https://vpermit.com.au/parkcity/ClaimableEvents/Claim?code=32440"  # Replace with your actual URL
    
    # License plate to enter
    license_plate = os.environ.get("LICENSE_PLATE", "DEFAULT_PLATE")
    
    automate_web_interaction(target_url, license_plate)
