import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init
import os
import csv
from random import randrange


class WebScraper:
    # Versión 119.0.6045.105 (Build oficial) (64 bits) - https://googlechromelabs.github.io/chrome-for-testing/#stable
    # https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win64/chromedriver-win64.zip
    chrome_driver_path = r"C:\GITHUB\Python\supers\chromedriver\chromedriver.exe"
    supermarkets = ["Mercadona", "Bonpreu", "Caprabo"]

    def __init__(self, supermarket_name):
        if supermarket_name not in self.supermarkets:
            raise Exception("Supermarket not found")
        self.supermarket_name = supermarket_name
        self.supermarket_url = ""
        self.path_csv = "csv"
        self.all_products = {}
        self.postal_code = "08960"
        self.currency = "€"
        self.name_csv = "products.csv"
        self.image_path = 'images'
        self.content_html = ""
        self.output_path_final = os.path.join(os.getcwd(), self.path_csv, "products.csv")
        chrome_options = webdriver.ChromeOptions()
        # don't show browser
        chrome_options.add_argument("--headless")
        # disable notifications log level
        # options INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3
        # chrome_options.add_argument("--log-level=3")
        # silent output true
        chrome_options.add_argument("--silent")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # chrome_options.add_argument("--disable-notifications")
        # init driver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        # self.driver = webdriver.Chrome(self.chrome_driver_path)
        # init colorama
        init(autoreset=True)

    def add_supermarket_products(self, supermarket_name, products):
        """
        Add supermarket products
        :param supermarket_name: supermarket name
        :param products: products
        :return: none
        """
        self.all_products[supermarket_name] = products

    def get_supermarket_products(self, supermarket_name):
        """
        Get supermarket products
        :param supermarket_name: supermarket name
        :return: products
        """
        return self.all_products[supermarket_name]

    def get_page_source(self, url):
        """
        Get page source from url
        :param url: url string
        :return: page source
        """
        # Obtiene el código fuente de la página
        self.driver.get(url)
        # wait to load page (presence of body element) 10 seconds
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(randrange(1, 3))

        return self.driver.page_source

    def refresh_driver(self):
        """
        Refresh driver
        :return: none
        """
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(randrange(1, 3))
        
        return self.driver.page_source

    def check_exists_products(self):
        """
        Check if exists products.csv file
        :return: boolean exists
        """
        # check if file exist
        return os.path.exists(self.output_path)

    @staticmethod
    def get_header_product():
        """
        Get header product
        :return: header product
        """
        return ["supermarket", "id_cat_principal", "name_cat_principal", "url_cat_principal",
                "id_category", "name_category", "url_category",
                "id_subcategory", "name_sub_category", "url_sub_category",
                "id_product", "name_product", "url_product",
                "thumbnail", "packaging", "unit_size", "unit_price", "size_format", "bulk_price"]

    def remove_products(self):
        """
        Remove products.csv file
        :return:
        """
        remove = False
        if input(
                f"File {self.output_path} exists!\nDo you want to refresh {self.supermarket_name} products? (y/n): ") == "y":
            try:
                os.remove(self.output_path)
                remove = True
            except OSError as e:
                self.handle_error("Error: %s : %s" % (self.output_path, e.strerror))
        return remove

    def print_total(self, num_products):
        self.print_message(f"\nTotal products in {self.supermarket_name}: {num_products}", "")

    def get_product_data_from_csv(self):
        """
        Get product data from csv file
        :return: product data
        """
        products_data_csv = []
        with open(self.output_path, newline='') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)  # Esto omite la primera línea (cabecera)
            for row in reader:
                products_data_csv.append(row)
        return products_data_csv

    @staticmethod
    def get_json(url):
        """
        Get json file from url
        :param url: url string
        :return: json
        """
        json_data = {}
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
        time.sleep(1)
        return json_data

    def get_content_html(self, url):
        """
        Get content html from url
        :param url: url string
        :return: content html
        """
        content_html = ""
        response = requests.get(url)
        if response.status_code == 200:
            content_html = response.text
        self.save_html(content_html)
        time.sleep(1)
        return content_html

    def get_actual_height(self):
        """
        Get actual height scroll page
        """
        # Get scroll height
        actual_height = self.driver.execute_script(
            f"return (window.pageYOffset !== undefined) ? window.pageYOffset : "
            f"(document.documentElement || document.body.parentNode || document.body)"
            f".scrollTop")
        return actual_height

    def go_height_page(self, height, total_height):
        """
        Go down page
        :param height: height
        :param total_height: total height
        :return: height
        """
        if height > total_height:
            self.driver.execute_script(f"window.scrollTo(0, {total_height});")
            actual_height = total_height
        else:
            # go to specific height
            self.driver.execute_script(f"window.scrollTo(0, {height});")
            # Get scroll height
            actual_height = self.get_actual_height()
        return actual_height

    def close_browser(self):
        self.driver.quit()

    def handle_error(self, error_message):
        self.print_message(error_message, "ERROR")

    @staticmethod
    def print_message(message, type_message):
        # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
        if type_message == "ERROR":
            print(Fore.RED + message)
        elif type_message == "WARNING":
            print(Fore.YELLOW + message)
        elif type_message == "INFO":
            print(Fore.BLUE + message)
        elif type_message == "SUCCESS":
            print(Fore.GREEN + message)
        else:
            print(Fore.WHITE + message)

    @staticmethod
    def price_by_unit(quantity, product_price):
        """
        Calculate price by unit
        :param quantity: quantity
        :param product_price: product price
        :return: price by unit
        """
        quantity = quantity.strip().replace(',', '.')
        quantity_num, quantity_unit = quantity.split()
        quantity_num = float(quantity_num)
        conversions = {
            "L": (1, "L"),  # Litros
            "cl": (0.01, "L"),  # Centilitros a litros (1 cl = 0.01 L)
            "ml": (0.001, "L"),  # Mililitros a litros (1 ml = 0.001 L)
            "Kg": (1, "Kg"),  # Kilogramos
            "g": (0.001, "Kg"),  # Gramos a kilogramos (1 g = 0.001 Kg)
        }
        factor_conversion, ref_unit = conversions.get(quantity_unit, (0, None))
        if factor_conversion > 0:
            quantity_ref = float(quantity_num) * factor_conversion
            # Calculate price in Kg/L
            price_by_unit = "{:.2f}".format(float(product_price.replace(',', '.')) / quantity_ref)

            return [price_by_unit, ref_unit]

        return [quantity_num, quantity_unit]

    def merge_csvs(self, products_data_all):
        """
        Merge csv files into one
        :return: none
        """
        # merge if not exists products.csv file
        if not os.path.exists(os.path.join(os.getcwd(), "csv", "products.csv")):
            # save into csv file (csv/products.csv)
            self.save_all_products(products_data_all)
            self.print_message(f"\nTOTAL PRODUCTS MERGED: {len(products_data_all)}", "SUCCESS")

    def save_all_products(self, product_data_all):
        """
        Save products into csv file (sorted by bulk price, last column)
        :param product_data_all: product data
        :return: none
        """

        try:
            if os.path.exists(self.output_path_final):
                # remove existent products.csv file
                os.remove(self.output_path_final)
        except OSError as e:
            self.handle_error("Error: %s : %s" % (self.output_path_final, e.strerror))
        # sort by bulk_price (last column)
        product_data_all.sort(key=lambda x: float(x[-1].replace(',', '.')))

        # save into csv file (csv/products.csv)
        with open(self.output_path_final, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            # write header
            writer.writerow(self.get_header_product())
            # write rows
            for row in product_data_all:
                writer.writerow(row)

        self.print_message(f"\nMerged file '{self.name_csv}' created with {len(product_data_all)} products!", "SUCCESS")

    def print_added_products(self, num_products, supermarket_name):
        """
        Print added products
        :param num_products: number of products
        :param supermarket_name: supermarket name
        :return: none
        """
        self.print_message(f"\n => {num_products} products from {supermarket_name} will be added!\n", "")

    @staticmethod
    def save_html(content_html):
        """
        Save html content into file (just to check)
        :param content_html: html content
        :return: none
        """
        with open("lectura.html", "w", encoding="utf-8") as file:
            file.write(content_html)
