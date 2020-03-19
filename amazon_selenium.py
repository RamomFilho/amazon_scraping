from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from lxml import html
import pandas as pd


class Amazon(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='bin/chromedriver')

    def wait(self, time_wait, type_by, query):
        WebDriverWait(self.driver, time_wait).until(
            ec.visibility_of_element_located((type_by, query)))

    @staticmethod
    def parse_html(page):
        page = html.fromstring(page)
        divs = page.xpath('//div[@class="s-result-list s-search-results sg-row"]/div')
        products = list()
        for div in divs:
            name = div.xpath('string(.//a[@class="a-link-normal a-text-normal"]/span/text())')
            price = div.xpath('string(.//span[@class="a-price"]/span/text())')

            if not price:
                price = div.xpath('string(.//span[@class="a-color-base"]/text())')

            if price:
                products.append({
                    'name': name.encode('utf-8').decode(),
                    'price': price
                })
        print('Crawler finalizado!')
        print(f'Produtos capturados: {len(products)}')

        df = pd.DataFrame(products)
        writer = pd.ExcelWriter('products.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Productss')

        writer.save()

    def run(self, search):
        self.driver.get('https://www.amazon.com.br/')
        self.wait(5, By.ID, 'twotabsearchtextbox')

        input_search = self.driver.find_element_by_id('twotabsearchtextbox')
        input_search.click()
        input_search.send_keys(search)
        input_search.submit()

        self.wait(5, By.CLASS_NAME, 'a-spacing-medium')
        self.parse_html(self.driver.page_source)
        self.driver.close()


if __name__ == '__main__':
    amazon = Amazon()
    amazon.run('iphone')
