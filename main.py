from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from save_file import save_as_text_file


search_url='https://raceroster.com/search?q=5k&t=upcoming'
next_indicator='Next »'

def sanitize_string_number(value:str) -> int:
    '''
        returns -1 if failed to parse into integer.
    '''
    remove_list = (',', 'results!', ' ')
    for rm in remove_list:
        value = value.replace(rm, '')

    try:
        return int(value)
    except:
        return -1

def get_number_of_results(browser:webdriver.Chrome) -> int:
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search-results__metrics')))
    result = element.find_element(By.CLASS_NAME, 'text-end')
    return sanitize_string_number(result.text)

def get_anchors(browser:webdriver.Chrome):
    wait = WebDriverWait(browser, 10)
    anchors = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-results__card-event-name')))
    for a in anchors:
        urls.append(('%s%s' % (a.get_attribute('href'), '\n'), '%s%s' % (a.text, '\n')))

def next_page(browser:webdriver.Chrome):
    global next_indicator
    wait = WebDriverWait(browser, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-link')))
    for e in elements:
        if next_indicator == e.text:
            pos_y_indicator = 460 # Firefox - 505, Chrome - 460
            while (e.location_once_scrolled_into_view['y'] > pos_y_indicator):
                if (e.location_once_scrolled_into_view['y'] <= pos_y_indicator):
                    e.click()
                    break

if __name__ == '__main__':
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(search_url)
    assert 'Race Roster' in browser.title
    
    page_counter = 0
    urls = []
    
    try:
        results = get_number_of_results(browser)
        while len(urls) < results:
            page_counter += 1
            print('Page: %i,\tTotal URL(s): %i' % (page_counter, len(urls)))
            get_anchors(browser)
            next_page(browser)
    except Exception as e:
        print(e)
    

    # Iterate this list into spreadsheet.
    retrieved_urls = [url[0] for url in urls]
    retrieved_titles = [title[1] for title in urls]
    save_as_text_file(retrieved_urls, "urls.txt")
    save_as_text_file(retrieved_titles, "titles.txt")

    print("Total number of result is %i, got %i urls" % (results, len(urls)))
    browser.quit()

