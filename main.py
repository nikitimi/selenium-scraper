from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    chrome_options=webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless=new')
    browser = webdriver.Chrome(options=chrome_options)
    
    try:
        wait = WebDriverWait(browser, 10)

        number_of_brands = 10
        counter = 0
        is_coming_soon = False
        while True:
            browser.get('https://training.harmanpro.com/')
            fpgridblocks = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fpgridblock')))
            for index in range(len(fpgridblocks)):
                if index == counter:
                    anchor = fpgridblocks[index].find_element(By.TAG_NAME, 'a')
                    url = anchor.get_attribute('href')
                    print(url)
                    browser.get(url)
                    anchors = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'gridboxlink')))
                    for a in anchors:
                        print(a.text)
                        if a.text == 'Online Courses':
                            browser.get(a.get_attribute('href'))
                            break
                        elif a.text == 'Online Courses (Coming Soon)':
                            is_coming_soon = True
                            break
                    if is_coming_soon:
                        is_coming_soon = False
                        counter += 1
                        break
                    
                    coursebox = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'coursebox')))
                    for course in coursebox:
                        print(course.text)
                    counter += 1
                    break
                
            if counter == number_of_brands:
                break

    except Exception as e:
        print(e)
    
    browser.quit()

