from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from title_and_url import data

def save_to_spreadsheet(data, output_file):
    if not data:
        print("No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")


if __name__ == '__main__':
    url_counter = 0
    user_name = "GCCARRANZA" # Edit to your PC User.
    data_length = len(data)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=chrome_options)
    output_file = f"/Users/{user_name}/Documents/event_contacts.xlsx"
    event_contacts = []

    for title, url in data:
        browser.get(url)
        try:
            wait = WebDriverWait(browser, .5)
            element = wait.until(EC.presence_of_element_located((By.ID, 'contact-information')))
            items = element.find_elements(By.CLASS_NAME, 'event-details__contact-list-item')
            contact, email, *args =  items
            clean_name = contact.text.strip("Event contact ")
            clean_email = email.text.strip("Email ")
            print(clean_name, clean_email, title, url)
            event_contacts.append({
                "Event Name": title,
                "Event URL": url,
                "Event Contact": clean_name,
                "Email": clean_email
            })
        except Exception as e:
            print(e)
            print('No contact information extracted.', title, url)
            event_contacts.append({
                "Event Name": title,
                "Event URL": url,
                "Event Contact": '',
                "Email": ''
            })

        url_counter += 1

        print('Percentage: %i' % (url_counter / data_length * 100))

    browser.quit()
    print('Processed URL(s):%i.' % url_counter)

    save_to_spreadsheet(event_contacts, output_file)

