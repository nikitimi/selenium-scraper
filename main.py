from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests

if __name__ == "__main__":
    # Set up Chrome options to allow direct PDF download (for the download step)
    username = "GCCARRANZA"
    download_path = f"C:/Users/{username}/Downloads/sec_aaer_downloads"
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

    # URLs for pages
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

    # Loop through each entry in the pdf_data list
    for entry in pdf_data:
        try:
            # Extract the PDF link and AAER number
            link_href = entry['link']
            aaer_number = entry['aaer_number']

            # Send a GET request to download the PDF
            pdf_response = requests.get(link_href, headers={
                "Host": "www.sec.gov",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Connection": "keep-alive",
                "Cookie": "ak_bmsc=B54F8502510EA1D2BA19FE36EDFF0699~000000000000000000000000000000~YAAQByYxoWqVM72TAQAAVc+FPxrQZhbEsEqELkak6jhjXuRx3ld89/0wF5dZ5LeyPJf1HMumukuZ2zvDwFBco9ySVvp14YIYeRNh4zcJhfhnqLXnSD5pHxK+XlLRevxIYz5Pl9+IeazziSoiVuDiAALvl674iq6f/Y/nU1p3AdAzhA6OJpdlkQjeCluXrtCFA12aw4bAfPdKz86jpyek74NLbX+SVVUmzYgb8m9tXJ2pYdoUkmbFCnf0o/VgoV/waZkt6v5+xN1kgbm0JOrXaSter15CiEJ9IniFQp7Lp+HUEWQUP/CzClOjkGs6S0WlIKU7pdNv+aHXK/K+vnz03jJi6TqFEYJqjriRX3dMfhPqQZoQOpjRGFyTLSV72OFy0rclNhABdw==; bm_mi=B9E73E90815D3B25FB60115319DF3C70~YAAQxb0oF/U48b+TAQAAKTerPxqsCI4W//JZpedkrQ2FgwJ5Hxp+5f9ZyvznX9640i1ovusuw8wsJ0mrHjX2JdRtSaP3nYVnLEUVuEnhtZTryd5SlZEEgs+Vj6SU0oM3XyxHwMfA9olBG2E7mpvYCAVjdnoiefoqK97qzQm4Id4eqBt6UyFxL/f+ecI2cmlQ4bEluR8BAOmT3xabNnAkbomJZ09LmrXwMqLK4bJjCRUZjGPTuv2JBG/45Vj4UTqgITADGvNyD6oe3tMPMLhgs22DW82Ge9VrhiVLPaDylqsmVh6oHKhUoPYb0CHSaQs3QwaOZiuBsNwvjGkjgmEmOfEMpGNSPN8sMiY+h3sfWT0CJ7cW5nf2njFJWcS+xS4TGoe+W3TGPvA+vw==~1; bm_sv=ED632B90B8C410B8BC27370C80C23552~YAAQxb0oF/Y48b+TAQAAKTerPxr1qbLXYWfZE4q1uWnLHNPwc4ve2mCRoR+TwCANKyMGygFnRrskvJD/ykpP5ORNMQBelNBB0fxD/lI4FJIsrJQ7t1z23xJJZMoQuwulDokL+lFZq6sOAxEy9hFpachjV4VEirj02ufNJ13l0z0YplYvFJyfJ+L79wqFQFPMtYDvaTWtf0q2Ji2qCuLWAjlc5vg0gwGnJ7LEo1xx0RXhNPwVovlA3zqhhdTL~1",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Priority": "u=0, i",
                "Pragma": "no-cache",
            })

            # Check if the request was successful
            if pdf_response.status_code == 200:
                # Save the PDF to the download folder, using the AAER number as the filename
                pdf_file_path = os.path.join(download_path, f"{aaer_number}.pdf")
                with open(pdf_file_path, "wb") as pdf_file:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        pdf_file.write(chunk)
                print(f"Downloaded: {aaer_number}.pdf")
            else:
                print(f"Failed to download the file from {link_href}, status code: {pdf_response.status_code} {pdf_response.reason}")
                # print(pdf_response.json())
        
        except Exception as e:
            print(f"Error downloading the PDF for AAER {aaer_number}: {e}")
