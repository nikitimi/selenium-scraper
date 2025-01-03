import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_event_contacts(base_url, search_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    event_contacts = []

    # Fetch the main search page
    print(f"Scraping page: {search_url}")
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch page: {search_url}, status code: {response.status_code}")
        return event_contacts

    soup = BeautifulSoup(response.content, "html.parser")
    # Select event links
    event_links = soup.select("a.search-results__card-event-name")


    print(f"Found {len(event_links)} events on the page.")

    for link in event_links:
        event_url = link['href']
        event_name = link.text.strip()  # Extract Event Name

        try:
            print(f"Scraping event: {event_url}")
            event_response = requests.get(event_url, headers=headers)
            if event_response.status_code != 200:
                print(f"Failed to fetch event page: {event_url}, status code: {event_response.status_code}")
                continue

            event_soup = BeautifulSoup(event_response.content, "html.parser")

            # Extract contact name and email
            contact_name = event_soup.find("dd", class_="event-details__contact-list-definition")
            email = event_soup.find("a", href=lambda href: href and "mailto:" in href)

            contact_name_text = contact_name.text.strip() if contact_name else "N/A"
            email_address = email['href'].split("mailto:")[1].split("?")[0] if email else "N/A"

            if contact_name or email:
                print(f"Found contact: {contact_name_text}, email: {email_address}")
                event_contacts.append({
                    "Event Name": event_name,
                    "Event URL": event_url,
                    "Event Contact": contact_name_text,
                    "Email": email_address
                })
            else:
                print(f"No contact information found for {event_url}")
        except Exception as e:
            print(f"Error scraping event {event_url}: {e}")

    print(f"Scraped {len(event_contacts)} events.")
    return event_contacts

def save_to_spreadsheet(data, output_file):
    if not data:
        print("No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    base_url = "https://raceroster.com"
    search_url = "https://raceroster.com/search?q=5k&t=upcoming"
    output_file = "/Users/my_name/Documents/event_contacts.xlsx"

    contact_data = scrape_event_contacts(base_url, search_url)
    if contact_data:
        save_to_spreadsheet(contact_data, output_file)
    else:
        print("No contacts were scraped.")
