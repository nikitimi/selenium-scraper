from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

target_resources = ('online courses')
# target_resources = ('online courses', 'product videos')

class WebScrapeHarmanCourses:
    def __init__(self, base_url='https://training.harmanpro.com/'):
        self.is_for_termination = False

        chrome_options=webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless=new')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 3)
        self.base_url = base_url
        self.goto_home_page()

        self.__locate_brands()


    def goto_home_page(self):
        self.browser.get(self.base_url)

    def get_resources_links_from_brands(self):
        self.brand_names:list[str] = []
        self.brand_resources_title_and_url_tuple:list[tuple[str, str]]= []
        for brand_link in self.brand_links_set:
            self.browser.get(brand_link) # Visits every brand in Harman.
            region_main = self.wait.until(EC.presence_of_element_located((By.ID, 'region-main')))
            header_two = region_main.find_element(By.TAG_NAME, 'h2')
            print('%s is appended in `brand_names`' % header_two.text)
            self.brand_names.append(header_two.text)
            anchors = region_main.find_elements(By.CLASS_NAME, 'gridboxlink')
            for a in anchors:
                self.brand_resources_title_and_url_tuple.append((a.text, a.get_attribute('href')) )
            self.goto_home_page()
            
    def get_contents_from_resources_links(self):
        """Get contents from resources: `Online Courses`, `Instructor Led`, `Certifications`, `Webinars`, `Product Videos`.\n
        Adjust scope be adding in the tuple `target_resources` above in lowercase."""
        global target_resources
        is_unavailable = 'coming soon'
        print('Resources title and URL has length of: %i' % len(self.brand_resources_title_and_url_tuple))
        for title, url in self.brand_resources_title_and_url_tuple:
            title_cased = title.lower()
            if title_cased.find(is_unavailable) > 0: # Skip to next iteration if resource is coming soon...
                continue
            
            print('Result count: %i with title: %s' % (target_resources.count(title_cased), title_cased))

            try:
                if target_resources.count(title_cased) > 0:
                    print('%s: %s' % (title, url))
                    self.browser.get(url)
                    courseboxes = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'coursebox')))
                    for coursebox in courseboxes:
                        course_anchor = coursebox.find_element(By.TAG_NAME, 'a')
                        course_tuple = course_anchor.text, course_anchor.get_attribute('href')
                        print(course_tuple)
                        
                else:
                    continue
            except Exception as e:
                print(e)

            self.browser.back() # Go back to visit other unvisited resources.

    def terminate_session(self):
        self.browser.quit()

    def get_details(self):
        counter = 0
        for link in self.brand_links_set:
            print('%s\t%s\t%i' % (link, self.brand_names[counter], len(self.brand_resources_title_and_url_tuple)))
            print(self.brand_resources_title_and_url_tuple)
            counter+=1

    def __locate_brands(self):
        self.brand_links_set = set()
        fpgrid = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fpgrid')))
        fpgridblocks = fpgrid.find_elements(By.CLASS_NAME, 'fpgridblock')
        
        # for index in range(len(fpgridblocks)):
        for index in range(1):
            brand_anchor_element = fpgridblocks[index].find_element(By.TAG_NAME, 'a')
            brand_link = brand_anchor_element.get_attribute('href')
            self.brand_links_set.add(brand_link)

if __name__ == '__main__':
    web_scrapper = WebScrapeHarmanCourses()

    try:
        web_scrapper.get_resources_links_from_brands()
        web_scrapper.get_contents_from_resources_links()
        web_scrapper.get_details()
    except Exception as err:
        print(err)


    web_scrapper.terminate_session()
        

  

