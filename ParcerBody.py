from bs4 import BeautifulStoneSoup
import requests
import openpyxl


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

    def parse_and_load(self, n, url, patch):
        try:
            final = self.parse_data(url)
        except Some_Exeption:
            print("Ощибка в соединении или имени")
            return
        print(final, end='\n\n')

        vk = openpyxl.load_workbook(patch)
        sh = vk.active
        sh.cell(column=1, row=n).value = str(final['name_of_product'])
        sh.cell(column=2, row=n).value = str(final['reference'])
        sh.cell(column=3, row=n).value = str(final['price_for_all'])
        sh.cell(column=4, row=n).value = str(final['price_for_registered'])
        sh.cell(column=5, row=n).value = str(final['url'])

        vk.save(patch)

    def parse_and_save(self, patch):
        patch = patch.replace('\ ', ' \\ ')

        vk = openpyxl.Workbook()
        sh = vk.active
        sh.title = "Цены"
        sh.cell(column=1, row=1).value = "Название"
        sh.cell(column=2, row=1).value = "Номер"
        sh.cell(column=3, row=1).value = "Оптовая цена"
        sh.cell(column=4, row=1).value = "Цена розничного магазина"
        sh.cell(column=5, row=1).value = "Ссылка на товар"
        vk.save(patch)
        list_of_urls = self.get_all_urls()

        for idx, item in enumerate(list_of_urls):
            self.parse_and_load(idx + 2, item, patch)


def main():
    print('Good')


if __name__ == "__main__":
    main()
