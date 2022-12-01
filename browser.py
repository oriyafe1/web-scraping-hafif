import os
import base64
import json

from urllib.parse import urlparse
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


def get_hosts_from_requests(requests):
    return [request.host for request in requests]


class WebScraper:
    def __init__(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)

    def scrape_url(self, url):
        print(f'Scraping "{url}"...')

        self.driver.get(url)
        content = self.driver.page_source

        url_requests = self.driver.requests

        url_output_dir = f"output/{urlparse(url).hostname}"

        os.makedirs(url_output_dir, exist_ok=True)

        screenshot_path = f"{url_output_dir}/screenshot.png"

        self.driver.save_screenshot(screenshot_path)

        output_dict = {
            "html": content,
            "resources": get_hosts_from_requests(url_requests),
            "screenshot": str(image_to_base64(screenshot_path))
        }

        output_json = json.dumps(output_dict)

        with open(f"{url_output_dir}/browse.json", "w") as output_json_file:
            output_json_file.write(output_json)

        print(f'Finished scraping "{url}"...')


def scrape_url(url):
    web_scraper = WebScraper()
    web_scraper.scrape_url(url)


def scrape_urls(urls):
    print('Starting scraping:')

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(scrape_url, urls)

    print(f'Finished scraping all {len(urls)} urls.')


def get_input_urls():
    input_urls_path = 'input/urls.input'
    input_urls_file = open(input_urls_path, "r")
    input_urls_string = input_urls_file.read()

    return input_urls_string.split('\n')


def main():
    input_urls = get_input_urls()

    scrape_urls(input_urls)


if __name__ == "__main__":
    main()
