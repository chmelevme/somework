from bs4 import BeautifulStoneSoup
from ParcerBody import SuperParser
from ParcerBody import Format_Exeption, Connection_Exception


class Navigator(SuperParser):
    def __init__(self, headers, urls):
        SuperParser.__init__(self, headers, urls)

    def parse_data(self, url):
        '''Собирает данные в словарь'''
        request = self.session.get(url, headers=self.headers)
        if request.status_code == 200:
            soup = BeautifulStoneSoup(request.content)
            if not (bool(soup.find('div', {"class": 'error404__text'})) or bool(
                    soup.find('div', {"class": 'nothing-search'})) or bool(
                soup.find('div', {"id": 'productList'}))):

                try:
                    name_of_product = soup.find('h1').next_element
                except Exception:
                    raise Format_Exeption('name', url)

                try:
                    price_for_all = soup.find('span',
                                              {"class": "item__price item__price--normal-left"}).next_element.replace(
                        " ",
                        "").replace(
                        "\n", "")
                except Exception:
                    price_for_all = "Нет в наличии"
                try:
                    price_for_registered = soup.find('span',
                                                     {
                                                         "class": "item__price item__price--red-bold"}).next_element.replace(
                        " ",
                        "").replace(
                        "\n", "")
                except Exception:
                    price_for_registered = "Нет в наличии"

                try:
                    reference = soup.findAll('div', {"class": "item__card-info-articul"})
                    reference = reference[1].next_element
                    reference = str(reference).split()[2].replace("-", '')
                except Exception:
                    reference = "Нет номера"
                final = {"name_of_product": name_of_product, "price_for_all": price_for_all,
                         "price_for_registered": price_for_registered, "reference": reference, "url": url}
                return final
            else:
                print("Не тот формат, вот ссылка {0}".format(url))
                raise Format_Exeption
        else:
            raise Connection_Exception


def main():
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    base_urls_navigator = ["https://www.navigator-63.ru/sitemap-shop-1.xml",
                           "https://www.navigator-63.ru/sitemap-shop-2.xml"]

    Navigator_ = Navigator(headers, base_urls_navigator)
    Navigator_.parse_and_save(r'C:\work\Navigator.xlsx')


if __name__ == "__main__":
    main()
