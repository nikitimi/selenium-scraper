from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests

# Set up Chrome options to allow direct PDF download (for the download step)
download_path = "C:/Users/GCCARRANZA/Downloads/sec_aaer_downloads"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,  # Specify your preferred download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "plugins.always_open_pdf_externally": True,  # Automatically open PDF in browser
    "safebrowsing.enabled": False,  # Disable Chrome’s safe browsing check that can block downloads
    "profile.default_content_settings.popups": 0  # Disable popups
})

# Set up the webdriver with options
driver = webdriver.Chrome(options=chrome_options)

# URLs for pages 1, 2, and 3
urls = [
    "https://www.sec.gov/enforcement-litigation/accounting-auditing-enforcement-releases?page=0",
]

# Initialize an empty list to store the URLs and AAER numbers
pdf_data = []

# Loop through each URL (pages 1, 2, and 3)
for url in urls:
    print(f"Scraping URL: {url}...")
    driver.get(url)

    # Wait for the table rows containing links to be loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="block-uswds-sec-content"]/div/div/div[3]/div/table/tbody/tr[1]')))
    
    # Extract the link and AAER number from each row on the current page
    rows = driver.find_elements(By.XPATH, '//*[@id="block-uswds-sec-content"]/div/div/div[3]/div/table/tbody/tr')
    for row in rows:
        try:
            # Extract the link from the first column (PDF link)
            link_element = row.find_element(By.XPATH, './/td[2]/div[1]/a')
            link_href = link_element.get_attribute('href')
            
            # Extract the AAER number from the second column
            aaer_text_element = row.find_element(By.XPATH, './/td[2]/div[2]/span[2]')
            aaer_text = aaer_text_element.text
            aaer_number = aaer_text.split("AAER-")[1].split()[0]  # Extract the number after AAER-

            # Store the data in a list of dictionaries
            pdf_data.append({'link': link_href, 'aaer_number': aaer_number})
        except Exception as e:
            print(f"Error extracting data from row: {e}")

# Print the scraped data (optional for verification)
for entry in pdf_data:
    print(f"Link: {entry['link']}, AAER Number: {entry['aaer_number']}")
