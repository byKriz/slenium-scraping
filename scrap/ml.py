from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import uniform
import csv

class MercadoLibre:

    def __init__(self, link):
        self.__link = link
        self.__driver = webdriver.Chrome('./chromedriver')


    def __pagination(self):
        next_buttom = self.__driver.find_element_by_xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]/a').get_attribute('href')
        sleep(uniform(3, 5))
        self.__driver.get(next_buttom)
        # andes-pagination__button andes-pagination__button--next

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

    def run(self):
        self.__driver.get(self.__link)
        total_links = []

        for i in range(1):
            links = self.__products_links()
            total_links += links
            self.__pagination()

        for url in total_links:
            sleep(uniform(3, 6))
            self.__driver.get(url)
            title = self.item_title()
            price = self.item_price()
            print(title)
            print(price)

        self.__driver.close()


if __name__ == '__main__':
    link = 'https://listado.mercadolibre.com.ve/respuestos-de-carro#D[A:respuestos%20de%20carro]'
    cosa = MercadoLibre(link)
    cosa.run()








