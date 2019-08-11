from bs4 import BeautifulStoneSoup
import requests
from ParcerBody import SuperParser
from ParcerBody import Format_Exeption, Some_Exeption, Connection_Exception


class Mars(SuperParser):
    def __init__(self, headers, urls):
        SuperParser.__init__(self, headers, urls)

    def parse_data(self, url):
        '''Собирает данные в словарь'''
        request = self.session.get(url, headers=self.headers)
        if request.status_code == 200:
            soap = BeautifulStoneSoup(request.content)
            if not (bool(soap.find('table', {"class": 'map-columns'})) or bool(
                    soap.find('div', {"class": 'col-md-12 catalog-items'}))):
                try:
                    name_of_product = soap.find('h1', {'class': 'title'}).next_element
                except Exception:
                    raise Format_Exeption('name', url)

                try:
                    price_for_all = soap.find('div', {"class": "price"}).next_element.replace(
                        " ",
                        "").replace(
                        "\n", "")[:-1]
                except Exception:
                    price_for_all = "Нет в наличии"
                try:
                    price_for_rozn = soap.find('div', {"class": "rozn-price"}).next_element.replace(
                        " ",
                        "").replace(
                        "\n", "")[:-1]
                    price_for_rozn = ''.join(filter(str.isdigit, price_for_rozn))
                except Exception:
                    price_for_rozn = "Нет в наличии"
                try:
                    reference = soap.find('div', {'class': 'article'}).next_element.replace("-", '')[9:]
                except Exception:
                    reference = "Нет номера"

                final = {"name_of_product": name_of_product, "price_for_all": price_for_all,
                         "price_for_registered": price_for_rozn, "reference": reference, "url": url}
                return final
            else:
                print("Не тот формат, вот ссылка {0}".format(url))
        else:
            print("ERROR", url, sep='    ')
            raise Connection_Exception


def main():
    pass

if __name__ == "__main__":
    main()
