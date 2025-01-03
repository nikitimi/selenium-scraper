from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


search_url='https://raceroster.com/search?q=5k&t=upcoming'
next_indicator='Next »'
urls = []

def sanitize_string_number(value:str) -> int:
    """
        returns -1 if failed to parse into integer.
    """
    remove_list = (",", "results!", " ")
    for rm in remove_list:
        value = value.replace(rm, "")

    try:
        return int(value)
    except:
        return -1

def get_number_of_results(browser:webdriver.Firefox) -> int:
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-results__metrics")))
    result = element.find_element(By.CLASS_NAME, "text-end")
    return sanitize_string_number(result.text)

def get_anchors(browser:webdriver.Firefox):
    wait = WebDriverWait(browser, 10)
    anchors = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search-results__card-event-name")))
    for a in anchors:
        urls.append(a.get_attribute("href"))

def next_page(browser:webdriver.Firefox):
    wait = WebDriverWait(browser, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-link")))
    for e in elements:
        if next_indicator == e.text:
                posY = 0
                y = e.location_once_scrolled_into_view.values()
                while (posY != y):
                    posY = y

                button = wait.until(EC.element_to_be_clickable(e))
                button.click()

                    

if __name__ == "__main__":
    browser = webdriver.Firefox()
    browser.get(search_url)
    assert 'Race Roster' in browser.title
    
    try:
        results = get_number_of_results(browser)
        while len(urls) < results:
            get_anchors(browser)
            next_page(browser)
    except Exception as e:
        print(e)
        
    # Iterate this list into spreadsheet.
    print(urls)
    browser.quit()

