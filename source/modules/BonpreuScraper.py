import time

from bs4 import BeautifulSoup
from modules.WebScraper import WebScraper
from urllib.parse import urlparse, parse_qs
import re
import os
import csv


class BonpreuScraper(WebScraper):
    """
    Bonpreu scraper class
    """

    def __init__(self):
        """
        Constructor MercadonaScraper class
        """
        super().__init__(supermarket_name="Bonpreu")
        self.products_data_Bonpreu = []
        self.supermarket_url = "https://www.compraonline.bonpreuesclat.cat/"
        self.language_selector = "&language=es-ES"
        self.categories_url = "products/"
        self.super_folder = "bonpreu"
        self.output_path = os.path.join(os.getcwd(), self.path_csv, self.super_folder, self.name_csv)
        self.principal_category_init = "Parafarmacia"
        self.category_init = "Salud deportiva"
        self.subcategory_init = ""

    def load_content(self):
        """
        Load content from supermarket
        """
        self.print_message(f"Loading products from {self.supermarket_name}...", "INFO")
        create = True
        if self.check_exists_products():
            self.products_data_Bonpreu = self.get_product_data_from_csv()
            self.print_total(len(self.products_data_Bonpreu))
            if not self.remove_products():
                create = False

        if create:
            self.load_products()
        self.print_added_products(len(self.products_data_Bonpreu), self.supermarket_name)
        self.all_products[self.supermarket_name] = self.products_data_Bonpreu
        self.close_browser()

    def load_products(self):
        """
        Load all product from supermarket
        :return: none
        """
        self.products_data_Bonpreu = []
        # First save language options
        language_url = self.supermarket_url + "?" + self.language_selector
        # get page source
        self.content_html = self.get_page_source(language_url)
        # Get initial url
        initial_url = self.supermarket_url + self.categories_url + "?" + self.language_selector
        # get page source
        self.content_html = self.get_page_source(initial_url)
        # scrape principal categories
        principal_categories = self.scrape_categories()
        search_init_l1 = False
        search_init_l2 = False
        search_init_l3 = False
        if self.principal_category_init != "": search_init_l1 = True
        if self.category_init != "": search_init_l2 = True
        if self.subcategory_init != "": search_init_l3 = True
        with open(self.output_path, 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
            header = self.get_header_product()
            writer.writerow(header)
            for principal_category in principal_categories:
                if search_init_l1:
                    if principal_category[0] == self.principal_category_init:
                        search_init_l1 = False
                    else:
                        continue
                # get category url
                category_url = self.supermarket_url + principal_category[1]
                # get page source
                self.content_html = self.get_page_source(category_url + self.language_selector)
                # scrape categories
                categories = self.scrape_categories()
                for category in categories:
                    if search_init_l2:
                        if category[0] == self.category_init:
                            search_init_l2 = False
                        else:
                            continue
                    # get category url
                    subcategory_url = self.supermarket_url + category[1]
                    # get page source
                    self.content_html = self.get_page_source(subcategory_url + self.language_selector)
                    # scrape subcategories
                    subcategories = self.scrape_categories()
                    # scrape products
                    if len(subcategories) == 0:
                        subcategory = ("", "")
                        self.scrape_products(principal_category, category, subcategory, writer)
                    else:
                        for subcategory in subcategories:
                            if search_init_l3:
                                if subcategory[0] == self.subcategory_init:
                                    search_init_l3 = False
                                else:
                                    continue
                            self.print_message(f"\n"
                                               f"{principal_category[0]} -> "
                                               f"{category[0]} -> "
                                               f"{subcategory[0]}...", "INFO")
                            self.scrape_products(principal_category, category, subcategory, writer)
        self.print_total(len(self.products_data_Bonpreu))
        self.close_browser()

    def scrape_categories(self):
        """
        Get all categories on page
        :return: categories
        """
        categories = []
        # parse the html
        parsed_html = BeautifulSoup(self.content_html, 'html.parser')
        # get content unique div with role="menu"
        div_menu = parsed_html.find('div', attrs={'role': 'menu'})
        if div_menu is not None:
            # Get unique ul inside div_menu
            ul_menu = div_menu.find('ul')
            # get all category_containers (li) inside ul_menu
            category_containers = ul_menu.find_all('li')
            if category_containers is None:
                self.print_message("Not founded categories...", "WARNING")
            else:
                for category_container in category_containers:
                    link = category_container.find('a')
                    # find category name inside a tag
                    category_name = link.text
                    # get category link (remove "/" from link)
                    category_link = link['href'].replace("/", "")
                    categories.append((category_name, category_link))
        else:
            self.print_message("- Not founded categories...", "WARNING")
        return categories

    def load_page_product(self, product_url, sum_height, total_height, max_retries=3):
        """"
        Load page product
        :param product_url: product url
        :param sum_height: sum height
        :param total_height: total height
        :return: parsed html & actual height
        """
        retries = 0
        while retries < max_retries:
            try:
                # get page source with go down
                self.content_html = self.get_page_source(product_url + self.language_selector)
                # go down page to load more content
                actual_height = self.go_height_page(sum_height, total_height)
                # get page source with go down
                self.content_html = self.refresh_driver()
                # check height
                # actual_height_check = self.get_actual_height()
                # parse html
                parsed_html = BeautifulSoup(self.content_html, 'html.parser')
                # save html
                # self.save_html(content_html=parsed_html.prettify())

                return parsed_html, actual_height
            except Exception as e:
                print(f"Error: {e}")
                retries += 1
                if retries < max_retries:
                    print(f"Retrying (Attempt {retries + 1})...")
                    time.sleep(2)
                else:
                    raise

    def scrape_products(self, principal_category, category, subcategory, writer):
        """
        Get all products inside subcategory
        :param principal_category: principal category information
        :param category: category information
        :param subcategory: subcategory information
        :param writer: csv writer
        :return: none
        """
        parsed_html = None
        # get product url
        if subcategory[1] == "":
            product_url = self.supermarket_url + category[1]
        else:
            product_url = self.supermarket_url + subcategory[1]
        try:
            parsed_html, actual_height = self.load_page_product(product_url, 0, 0)
        except Exception as e:
            print(f"Max tries reached in {product_url}.\nError: {e}")
        if parsed_html is not None:
            # get content unique div product-list data-synthetics="product-list"
            div_product_list = parsed_html.find('div', attrs={'data-synthetics': 'product-list'})
            # get all products inside div_product_list
            product_containers_all = div_product_list.find_all('div', class_=re.compile("^base__Wrapper-sc"))
            product_ids = []
            interval_height = 1000
            sum_height = interval_height
            # Get scroll height
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            actual_height = self.go_height_page(0, total_height)
            while len(product_ids) != len(product_containers_all) and actual_height < total_height:
                # get all product_containers (div) inside div_product_list
                # all divs with attribute data-test="fop-wrapper:...."
                product_containers = div_product_list.find_all('div', attrs={'data-test': re.compile("^fop-wrapper:")})
                if product_containers is not None:
                    for product_container in product_containers:
                        product_id = self.read_product_container(
                            product_container, principal_category, category, subcategory, writer, product_ids)
                        if product_id not in product_ids:
                            product_ids.append(product_id)
                else:
                    print("Not product containers found, go down page...")

                # we have to load again page
                # because inside product load product detail page
                try:
                    parsed_html, actual_height = self.load_page_product(product_url, sum_height, total_height)
                except Exception as e:
                    print(f"Max tries reached in {product_url}.\nError: {e}")
                sum_height += interval_height
                # get content unique div product-list data-synthetics="product-list"
                div_product_list = parsed_html.find('div', attrs={'data-synthetics': 'product-list'})
                if div_product_list is None:
                    print("Not product list found, existing...")
                    break

    def read_product_container(self, product_container, principal_category, category, subcategory, writer, product_ids):
        """
        Read product container
        :param product_container: product containers
        :param principal_category: principal category information
        :param category: category information
        :param subcategory: subcategory information
        :param writer: csv writer
        :param product_ids: product ids
        :return: none
        """
        # get id from attribute data-test="fop-wrapper:...."
        product_id = product_container['data-test'].split(":")[1]
        if product_id not in product_ids:
            div_product = product_container.find('div', class_=re.compile("^box__Box-sc"))
            # save content html to file (just to check)
            # self.save_html(div_product.prettify())
            # get product data
            product = self.scrape_product(principal_category, category, subcategory, div_product)
            # save product data
            writer.writerow(product)
        return product_id

    def scrape_product(self, principal_category, category, subcategory, div_product):
        """
        Get product information
        :param principal_category: principal category information
        :param category: category information
        :param subcategory: subcategory information
        :param div_product: div product
        :return: product information array
        """
        url_cat_principal = principal_category[1]
        # get sublocationId from url
        id_cat_principal = parse_qs(urlparse(url_cat_principal).query).get('sublocationId', [None])[0]
        name_cat_principal = principal_category[0]
        url_category = category[1]
        # get sublocationId from url
        id_category = parse_qs(urlparse(url_category).query).get('sublocationId', [None])[0]
        name_category = category[0]
        url_subcategory = subcategory[1]
        # get sublocationId from url
        id_subcategory = parse_qs(urlparse(url_subcategory).query).get('sublocationId', [None])[0]
        name_subcategory = subcategory[0]
        # get product url without first char "/"
        product_url = div_product.find('a', {'data-test': 'fop-product-link'})['href'][1:]
        # get product id
        product_id = "0"
        match = re.search(r'products/(\d+)/details', product_url)
        if match:
            product_id = match.group(1)
        # get product name
        product_name = div_product.find('a', {'data-test': 'fop-product-link'}).text
        # get product thumbnail
        product_thumbnail_img = div_product.find('img')
        product_thumbnail = ""
        if product_thumbnail_img is not None:
            product_thumbnail = product_thumbnail_img['src']
        # get product packaging (inside info product url), go inside url
        product_packaging = self.get_product_packaging(
            self.supermarket_url + product_url + "?" + self.language_selector)
        # get product unit size, size_format & bulk_price inside div with data-test = "fop-size"
        span_size = div_product.find('div', {'data-test': 'fop-size'})
        # thera are 2 spans: unit_size & size format are inside first span and bulk_price inside second span
        spans = span_size.find_all('span')
        product_unit_size = "unidad"
        product_size_format = "unidad"
        # only gets information for bulk price
        product_bulk_price_information = spans[0].text
        product_bulk_price = ""
        if len(spans) == 1:
            product_bulk_price = product_bulk_price_information.split(self.currency)[0].replace("(", "").strip()
            units_available = ["unidad", "artículo"]
            for unit_available in units_available:
                if unit_available in product_bulk_price_information:
                    product_size_format = unit_available
                    product_unit_size = "1"
                    break
            else:
                self.print_message(f"Not found product_size_format (1 span) in: {product_bulk_price_information}",
                                   "WARNING")
        elif len(spans) >= 2:
            # first span text with unit_size & size_format without separation between information
            product_unit_size_information = spans[0].text
            units_available = ["kg", "L", "por envase"]
            for unit_available in units_available:
                if unit_available in product_unit_size_information:
                    product_unit_size = product_unit_size_information.split(unit_available)[0].strip()
                    product_size_format = unit_available
                    if product_size_format == "por envase":
                        product_size_format = "envase"
                    break
            else:
                self.print_message(f"Not found product_size_format (2 span) in: {product_bulk_price_information}",
                                   "WARNING")
            # get last span text with bulk_price
            product_bulk_price_information = spans[len(spans) - 1].text
            # get product_bulk_price, price between "(" and currency
            product_bulk_price = product_bulk_price_information.split(self.currency)[0].replace("(", "").strip()

        # get unit_price
        product_unit_price = "0"
        price_div = div_product.find('div', attrs={'data-test': 'fop-price-wrapper'})
        if price_div is not None:
            product_unit_price = price_div.text.replace(self.currency, "").strip()
        else:
            self.print_message("Not price div found...", "WARNING")
        # product bulk price format
        product_bulk_price = product_bulk_price.replace(",", ".")
        # check if has 2 points or more!
        parts = product_bulk_price.split('.')
        product_bulk_price_cleaned = product_bulk_price
        if len(parts) > 1:
            product_bulk_price_cleaned = ''.join(parts[:-1]) + "." + parts[-1]
        # get product data list, remove invalid chars in product_name
        product_data = [self.supermarket_name,
                        id_cat_principal, name_cat_principal, self.supermarket_url + url_cat_principal,
                        id_category, name_category, self.supermarket_url + url_category,
                        id_subcategory, name_subcategory, self.supermarket_url + url_subcategory,
                        product_id, self.remove_invalid_chars(product_name), self.supermarket_url + product_url,
                        product_thumbnail, product_packaging, product_unit_size, product_unit_price.replace(",", "."),
                        product_size_format, product_bulk_price_cleaned]
        self.print_message(f" - Added product {product_name}", "INFO")
        self.products_data_Bonpreu.append(product_data)
        return product_data

    def get_product_packaging(self, product_url, try_num=1):
        """
        Get product packaging
        :param product_url: product url
        :param try_num: try_num
        :return: packaging information
        """
        packaging_info = ""
        # get page source
        self.content_html = self.get_page_source(product_url)
        # parse the html
        parsed_html = BeautifulSoup(self.content_html, 'html.parser')
        # get content with class "site--content"
        div_site_content = parsed_html.find('div', class_='site--content')
        if div_site_content is not None:
            # get divs with information about product begins with "static-content-wrapper__StaticContentWrapper-sc-"
            divs_information = div_site_content.find_all('div', class_=re.compile(
                "^static-content-wrapper__StaticContentWrapper-sc-"))
            if divs_information is not None:
                # get div with general packaging information (first div)
                div_information_packaging = divs_information[0]
                # get div inside this div
                if div_information_packaging is not None:
                    packaging_text = div_information_packaging.text
                    # get packaging information: word between "en" and "de"
                    packaging_info = self.extract_packaging_text(packaging_text)

        if packaging_info == "" and try_num == 1:
            # get another try to get packaging info
            packaging_info = self.get_product_packaging(product_url, try_num=2)

        return packaging_info

    @staticmethod
    def extract_packaging_text(packaging_text):
        """
        Extract packaging text
        :param packaging_text: packaging text
        :return: packaging information
        """
        packaging_options = ["unidad", "unidades", "bolsa", "bolsas", "pack", "packs",
                             "caja", "cajas", "bandeja", "bandejas", "bandeja familiar",
                             "botella", "botellas", "lata", "latas", "cartón", "cartones",
                             "paquete", "paquetes", "tableta", "tabletas"]
        packaging_info = ""
        # get packaging information: word between "en" and "de"
        if " en " in packaging_text and " de " in packaging_text:
            packaging_info = packaging_text.split(" en ")[1].split(" de ")[0].strip()
        if packaging_info == "":
            # search packaging information in packaging_options
            for packaging_option in packaging_options:
                if packaging_option in packaging_text:
                    packaging_info = packaging_option
                    break

        return packaging_info

    @staticmethod
    def remove_invalid_chars(text):
        """
        Remove invalid chars
        :param text: text
        :return: text without invalid chars
        """
        # Define una expresión regular para eliminar caracteres no válidos
        valid_chars = re.compile(r'[^\x20-\x7E]+')
        return valid_chars.sub('', text)
