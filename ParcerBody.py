from bs4 import BeautifulStoneSoup
import requests

class Some_Exeption(Exception):
    pass
class Connection_Exception(Some_Exeption):
    pass
class Format_Exeption(Some_Exeption):
       pass
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
    print('Good')


if __name__ == "__main__":
    main()
