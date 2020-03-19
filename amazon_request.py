import requests
import json
from lxml import html
import pandas as pd


class Amazon(object):
    @staticmethod
    def parse_product(div):
        page = html.fromstring(div)
        name = page.xpath('string(//a[@class="a-link-normal a-text-normal"]/span/text())')
        price = page.xpath('string(//span[@class="a-price"]/span/text())')
        return name, price

    def run(self, search):
        url = 'https://www.amazon.com.br/s/query'
        params = {
            '__mk_pt_BR': 'ÅMÅŽÕÑ',
            'i': 'aps',
            'k': search,
            'ref': 'nb_sb_noss',
            'url': 'search-alias=aps',
            'page': '1'
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        response = requests.get(url=url, params=params, headers=headers)
        products = list()
        for element in response.text.split("&&&"):
            try:
                obj = json.loads(element)
                if 'data-search-results:search-result' in obj[1]:
                    div = obj[2].get('html')
                    name, price = self.parse_product(div)
                    if price:
                        products.append({
                            'name': name.encode('utf-8').decode(),
                            'price': price
                        })
            except Exception:
                continue

        print('Crawler finalizado!')
        print(f'Produtos capturados: {len(products)}')

        df = pd.DataFrame(products)
        writer = pd.ExcelWriter('products.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Productss')
        writer.save()


if __name__ == '__main__':
    amazon = Amazon()
    amazon.run('iphone')
