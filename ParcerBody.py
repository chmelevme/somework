from bs4 import BeautifulStoneSoup
import requests


class SuperParser():
    """Класс содержащий базовые инструменты"""
    def __init__(self, headers, urls):
        self.headers = headers
        self.urls = urls
        self.session = requests.session()

    def get_all_urls(self):
        """Возвращает список url"""
        list_of_urls = []
        for url in self.urls:
            request = self.session.get(url, headers=self.headers)
            soap = BeautifulStoneSoup(request.content)
            urls = soap.find_all('loc')
            list_of_urls += [url.next_element for url in urls]
        return list_of_urls


def main():
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    base_urls_navigator = ["https://www.navigator-63.ru/sitemap-shop-1.xml",
                           "https://www.navigator-63.ru/sitemap-shop-2.xml"]

    a = SuperParser(headers, base_urls_navigator)


if __name__ == "__main__":
    main()
