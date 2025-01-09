from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.common.exceptions as SEExceptions

target_resources = ('online courses')
# target_resources = ('online courses', 'product videos')

class WebScrapeHarmanCourses:
    def __init__(self, base_url='https://training.harmanpro.com/'):
        self.is_for_termination = False

        chrome_options=webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless=new')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 1)
        self.base_url = base_url
        self.goto_home_page()

        self.__locate_brands()


    def goto_home_page(self):
        self.browser.get(self.base_url)

    def get_resources_links_from_brands(self):
        self.brand_names:list[
            dict[
                'brand_name': str, 
                'contents': list[
                    dict[
                        'title': str, 
                        'url': str, 
                        'courses': list[
                            tuple(str, str, str)
                        ]
                    ]
                ]
            ]] = []
        for brand_link in self.brand_links_set:
            self.browser.get(brand_link) # Visits every brand in Harman.
            region_main = self.wait.until(EC.presence_of_element_located((By.ID, 'region-main')))
            header_two = region_main.find_element(By.TAG_NAME, 'h2')
            print('%s is appended in `brand_names`' % header_two.text)
            self.brand_names.append({'brand_name': header_two.text})
            anchors = region_main.find_elements(By.CLASS_NAME, 'gridboxlink')

            contents_holder = []
            for a in anchors:
                brand_names_dict_generator = (entry for entry in self.brand_names if entry.get('brand_name') == header_two.text)
                brand_names_dict = brand_names_dict_generator.send(None)
                contents_holder.append({'title': a.text, 'url': a.get_attribute('href')})

            brand_names_dict.update({'contents': contents_holder})
            brand_names_dict_generator.close()
            self.goto_home_page()
            
    def get_contents_from_resources_links(self):
        """Get contents from resources: `Online Courses`, `Instructor Led`, `Certifications`, `Webinars`, `Product Videos`.\n
        Adjust scope be adding in the tuple `target_resources` above in lowercase."""
        global target_resources
        is_unavailable = 'coming soon'
        for brand_names_dictionary in self.brand_names:
            brand_name:str = brand_names_dictionary.get('brand_name')
            print('Resources title and URL has length of: %i' % len(brand_names_dictionary.get('contents')))
            for brand_name_contents_dict in brand_names_dictionary.get('contents'):
                title:str = brand_name_contents_dict.get('title')
                url:str = brand_name_contents_dict.get('url')

                title_cased = title.lower()
                if title_cased.find(is_unavailable) > 0: # Skip to next iteration if resource is coming soon...
                    continue

                try:
                    if target_resources.count(title_cased) > 0:
                        print('%s: %s' % (title, url))
                        self.browser.get(url)
                        courseboxes = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'coursebox')))
                        course_content_holder = []
                        for coursebox in courseboxes:
                            course_anchor = coursebox.find_element(By.TAG_NAME, 'a')
                            summary_element  = coursebox.find_element(By.CLASS_NAME, 'summary')
                            course_tuple = course_anchor.text, summary_element.text, course_anchor.get_attribute('href')
                            course_content_holder.append(course_tuple)

                        # This blocks will perform update to the dictionary second level through the contents.
                        brand_name_dict_generator = (entry for entry in self.brand_names if entry.get('brand_name') == brand_name)
                        brand_name_dict = brand_name_dict_generator.send(None)
                        brand_contents_dict_generator = (entry for entry in brand_name_dict.get('contents') if entry.get('title') == title)
                        brand_contents_dict:dict = brand_contents_dict_generator.send(None)
                        brand_contents_dict.update({'courses': course_content_holder})
                            
                        brand_contents_dict_generator.close()
                        brand_name_dict_generator.close()
                            
                    else:
                        continue
                except Exception as e:
                    print(e)

                self.browser.back() # Go back to visit other unvisited resources.

        self.goto_home_page()

    def get_topic_outlines(self):
        global target_resources
        xpath_nav, xpath_tabs_tree = '//nav[@id="courseindex"]', '//div[@id="tabs-tree-start"]'
        for entry in self.brand_names:
            brand_name = entry.get('brand_name')
            print(brand_name)
            resource_dict_generator = (resource for resource in entry.get('contents') if target_resources.count(resource.get('title').lower()) > 0)
            resource_dict:dict = resource_dict_generator.send(None)
            for title, _, url in resource_dict.get('courses'):
                print('Visiting: %s\nURL:%s' % (title,url))
                self.browser.get(url)

                try:
                    nav_element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_nav)))
                    anchors = nav_element.find_elements((By.TAG_NAME, 'a'))
                    anchor_generator = ((anchor.text, anchor.get_attribute('href')) for anchor in anchors)
                    anchor_tuple = anchor_generator.send(None)
                    print('Title: %s\nURL: %s' % anchor_tuple)
                    
                except SEExceptions.TimeoutException:
                    print('No navigation detected.')
                    pass
                except Exception as err:
                    error_template = 'Exeption Name: {0}\tArguments: {1!r}'
                    print(error_template.format(type(err).__name__, err.args))
                    pass

                self.browser.back()

            self.goto_home_page()

                


    def terminate_session(self):
        self.browser.quit()

    def get_details(self):
        counter = 0
        for link in self.brand_links_set:
            print('%s\t%s\t%i' % (link, self.brand_names[counter].get('brand_name'), len(self.brand_names)))
            print(self.brand_names)
            counter+=1

    def __locate_brands(self):
        self.brand_links_set = set()
        fpgrid = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fpgrid')))
        fpgridblocks = fpgrid.find_elements(By.CLASS_NAME, 'fpgridblock')
        
        # for index in range(len(fpgridblocks)):
        for index in range(2):
            brand_anchor_element = fpgridblocks[index].find_element(By.TAG_NAME, 'a')
            brand_link = brand_anchor_element.get_attribute('href')
            self.brand_links_set.add(brand_link)

if __name__ == '__main__':
    web_scrapper = WebScrapeHarmanCourses()

    try:
        web_scrapper.get_resources_links_from_brands()
        web_scrapper.get_contents_from_resources_links()
        web_scrapper.get_details()
        web_scrapper.get_topic_outlines()
    except Exception as err:
        print(err)


    web_scrapper.terminate_session()
        

  

