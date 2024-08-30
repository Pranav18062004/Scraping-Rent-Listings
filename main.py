from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import time


class RentListing:
    def __init__(self) -> None:
        url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url=url, headers=header)
        self.soup = BeautifulSoup(response.text, "html.parser")
        self.address_list = []
        self.link_list = []
        self.price_list = []

    def zillow_scraper(self):
        listing_scrape = self.soup.find_all(name="article")
        for listing in listing_scrape:
            try:
                address_text = listing.select_one(
                    'address[data-test="property-card-addr"]'
                ).get_text()
                self.address_list.append(address_text)
                link = listing.select_one("div.property-card-data a")
                link_text = link["href"]
                if "https" not in link_text:
                    self.link_list.append(f"https://www.zillow.com{link_text}")
                else:
                    self.link_list.append(link_text)
                price = listing.select_one("div div div div span")
                self.price_list.append(price.get_text())
            except:
                continue
        print(len(self.address_list))
        print(len(self.link_list))
        print(len(self.price_list))
        # print(self.address_list)
        # print(self.link_list)
        # print(self.price_list)
        self.form_fill()

    def form_fill(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        for i in range(len(self.address_list)):
            driver.get(
                "https://docs.google.com/forms/d/e/1FAIpQLSeUo9L0MDwNdVuItAXZcucMDp3ziN6dmoWyktynG0LKlqsr5Q/viewform"
            )
            time.sleep(1)
            price_input = driver.find_element(
                by=By.XPATH,
                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
            price_input.send_keys(self.price_list[i])
            link_input = driver.find_element(
                by=By.XPATH,
                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
            link_input.send_keys(self.link_list[i])
            address_input = driver.find_element(
                by=By.XPATH,
                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
            address_input.send_keys(self.address_list[i])
            submit_button = driver.find_element(
                by=By.XPATH,
                value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div',
            )
            submit_button.click()


rent = RentListing()
rent.zillow_scraper()
