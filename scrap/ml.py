from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import uniform
import csv

class MercadoLibre:

    _pathw = r'C:\Users\Cristian\Documents\Programacion\Proyectos\slenium-scraping\scrap\chromedriver.exe'
    _path = r'./chromedriver'

    def __init__(self, link):
        self.__link = link
        self.__pathw = r'C:\Users\Cristian\Documents\Programacion\Proyectos\slenium-scraping\scrap\chromedriver.exe'
        self.__driver = webdriver.Chrome(self.__pathw)


    def __pagination(self):
        next_buttom = self.__driver.find_element_by_xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]/a').get_attribute('href')
        sleep(uniform(3, 5))
        self.__driver.get(next_buttom)

    def __products_links(self):
        products = self.__driver.find_elements_by_xpath('//section[@class="ui-search-results"]/ol/li/div/div/div[2]/div/a[1]')
        clean = lambda x: x.get_attribute('href')
        links = list(map(clean, products))
        return links

    def item_title(self):
        title = self.__driver.find_element_by_xpath('//div[@class="ui-pdp-header__title-container"]/h1').text
        return title

    def item_price(self):
        enter_price = self.__driver.find_element_by_xpath('//div[@class="ui-pdp-price__second-line"]/span/span[2]/span[2]').text
        try:
            cents_price = self.__driver.find_element_by_xpath('//div[@class="ui-pdp-price__second-line"]/span/span[2]/span[4]').text
            return float(enter_price + '.' + cents_price)
        except Exception:
            return float(enter_price)
    
    def item_status(self):
        status = self.__driver.find_element_by_xpath('//div[@class="ui-pdp-header__subtitle"]/span').text
        if 'Nuevo' in status:
            return 'Nuevo'
        elif 'Usado' in status:
            return 'Usado'

    def item_sales(self):
        sales = self.__driver.find_element_by_xpath('//div[@class="ui-pdp-header__subtitle"]/span').text
        clean = lambda x: x.replace('Nuevo  |  ', '').replace(' vendidos', '').replace('Usado  |  ', '').replace('Nuevo', '').replace('Usado', '')
        clean_sales = clean(sales)
        if clean_sales == '':
            return 0
        elif clean_sales == '1 vendido':
            return 1
        return int(clean_sales)

    def seller_name(self):
        try:
            name = self.__driver.find_element_by_xpath('//div[@class="ui-pdp-seller__header__title"]').text
            return name
        except Exception:
            return 'N/A'

    def seller_rates(self):
        try:
            rate = self.__driver.find_element_by_xpath('//li[@class="ui-pdp-seller__item-description"][1]/strong').text
            return rate
        except Exception:
            return 'N/A'

    def seller_age(self):
        try:
            age = self.__driver.find_element_by_xpath('//li[@class="ui-pdp-seller__item-description"][2]/strong').text
            return age
        except Exception:
            return 'N/A'

    def seller_sales(self):
        try:
            age = self.__driver.find_element_by_xpath('//li[@class="ui-pdp-seller__item-description"][3]/strong').text
            return int(age)
        except Exception:
            return 'N/A'

    def item_data(self):
        product_info = []
        title = self.item_title()
        price = self.item_price()
        status = self.item_status()
        sales = self.item_sales()
        seller_name = self.seller_name()
        seller_rate = self.seller_rates()
        seller_age = self.seller_age()
        seller_sales = self.seller_sales()
        product_info.append(title)
        product_info.append(price)
        product_info.append(status)
        product_info.append(sales)
        product_info.append(seller_name)
        product_info.append(seller_rate)
        product_info.append(seller_age)
        product_info.append(seller_sales)
        return product_info

    def csv(self, products):
        etiquetas = ['Titulo', 'Precio', 'Estado', 'Vendidos', 'Vendedor', 'Puntuacion', 'Edad', 'Ventas']
        with open('mercado_libre.csv', 'a', newline='') as file:
            spamwriter = csv.writer(file, delimiter=';')
            spamwriter.writerow(etiquetas)
            spamwriter.writerows(products)

    def run(self):
        self.__driver.get(self.__link)
        total_links = []
        products = []
        np = 1
        for i in range(5):
            links = self.__products_links()
            total_links += links
            self.__pagination()

        ntp = len(total_links)
        for url in total_links:
            product_info = []
            sleep(uniform(3, 6))
            self.__driver.get(url)
            title = self.item_title()
            price = self.item_price()
            status = self.item_status()
            sales = self.item_sales()
            seller_name = self.seller_name()
            seller_rate = self.seller_rates()
            seller_age = self.seller_age()
            seller_sales = self.seller_sales()
            product_info.append(title)
            product_info.append(price)
            product_info.append(status)
            product_info.append(sales)
            product_info.append(seller_name)
            product_info.append(seller_rate)
            product_info.append(seller_age)
            product_info.append(seller_sales)
            product_info.append(url)
            products.append(product_info)
            print(f'{np}/{ntp}')
            np += 1

        self.csv(products)
        self.__driver.close()


if __name__ == '__main__':
    link = r'https://listado.mercadolibre.com.ve/bombillos-led-50w#D[A:bombillos%20led%2050w]'
    cosa = MercadoLibre(link)
    cosa.run()








