from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urls import urls

if __name__ == '__main__':
    url_counter = 0
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=chrome_options)

    for url in urls:
        browser.get(url)
        try:

            wait = WebDriverWait(browser, .5)
            element = wait.until(EC.presence_of_element_located((By.ID, 'contact-information')))
            _, name, email = element.text.splitlines()
            clean_name = name.strip('Event contact ')
            clean_email = email.strip('Email ')
            print(clean_name, clean_email)
        except Exception as e:
            print(e)
            print('No contact information extracted.')

        url_counter += 1

    browser.quit()
    print('Processed URL(s):%i.' % url_counter)

