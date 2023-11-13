from bs4 import BeautifulSoup
from modules.WebScraper import WebScraper
import re
import os
import csv


class CapraboScraper(WebScraper):
    """
    Caprabo scraper class
    """
    def __init__(self):
        """
        Constructor MercadonaScraper class
        """
        super().__init__(supermarket_name="Caprabo")
        self.products_data_Caprabo = []
        self.supermarket_url = "https://www.capraboacasa.com/"
        self.language_selector = "es/"
        self.categories_url = ""
        self.super_folder = "caprabo"
        self.output_path = os.path.join(os.getcwd(), self.path_csv, self.super_folder, self.name_csv)

    def load_content(self):
        """
        Load content from supermarket
        """
        self.print_message(f"Loading products from {self.supermarket_name}...", "INFO")
        create = True
        if self.check_exists_products():
            self.products_data_Caprabo = self.get_product_data_from_csv()
            self.print_total(len(self.products_data_Caprabo))
            if not self.remove_products():
                create = False
        if create:
            self.load_products()
        self.print_added_products(len(self.products_data_Caprabo), self.supermarket_name)
        self.all_products[self.supermarket_name] = self.products_data_Caprabo
        self.close_browser()

    def load_products(self):
        """
        Load all product from supermarket
        :return: none
        """
        self.products_data_Caprabo = []
        # First save language options
        language_url = self.supermarket_url + self.language_selector
        # get page source
        self.content_html = self.get_page_source(language_url)
        # Get initial url
        initial_url = self.supermarket_url + self.categories_url + self.language_selector
        # get page source
        self.content_html = self.get_page_source(initial_url)
        # self.save_html(self.content_html)
        # scrape principal categories
        categories = self.scrape_categories()
        self.products_data_Caprabo = self.scrape_products(categories)
        self.print_total(len(self.products_data_Caprabo))
        self.close_browser()

    def scrape_categories(self):
        """
        Get all categories on page
        """
        level1 = []
        level2 = []
        level3 = []
        categories = []
        excluded_categories = ["Ofertas", "De la nostra terra"]
        # parse the html
        parsed_html = BeautifulSoup(self.content_html, 'html.parser')
        # save parsed_html to file (just to check)
        # self.save_html(parsed_html.prettify())
        # get content unique div class="nav-bottom nav scrollable"
        div_menu = parsed_html.find('div', class_="nav-bottom nav scrollable")
        if div_menu is not None:
            # Get unique ul inside div_menu
            ul_menu = div_menu.find('ul', class_="nav-level-1")
            # get all category_containers (li) inside ul_menu
            l1_cat_containers = ul_menu.find_all('li', class_=re.compile("^secondary-color nav-item"))
            if l1_cat_containers is None:
                print("- Not founded level1 categories...")
            else:
                # print(f"Founded {len(l1_cat_containers)} categories")
                for l1_cat_container in l1_cat_containers:
                    l1_cat_link = l1_cat_container.find('a')
                    # find category name inside a tag
                    if l1_cat_link is not None:
                        l1_cat_name = l1_cat_link.text
                        if l1_cat_name not in excluded_categories:
                            # get category link
                            l1_cat_link_href = l1_cat_link['href']
                            l1_cat_link_href = l1_cat_link_href.replace(":443", "")
                            if l1_cat_name not in level1:
                                print(f"Level1 cat name: {l1_cat_name} with link: {l1_cat_link_href}")
                                level1.append(l1_cat_name)
                            # ----------------------
                            # get level 2 categories
                            # ----------------------
                            # search div with class="nav-level-content"
                            div_container = l1_cat_container.find('div', class_="nav-level-content")
                            if div_container is not None:
                                # search ul with class="nav-level-2"
                                ul_level2 = div_container.find('ul', class_="nav-level-2")
                                if ul_level2 is not None:
                                    # get all subcategory_containers (li) inside ul_subcategories
                                    l2_cat_containers = ul_level2.find_all('li')
                                    if l2_cat_containers is None:
                                        print("- Not founded level 2 categories...")
                                    else:
                                        # print(f"Founded {len(level2_category_containers)} subcategories")
                                        for l2_cat_container in l2_cat_containers:
                                            l2_cat_link = l2_cat_container.find('a')
                                            # find subcategory name inside a tag
                                            if l2_cat_link is not None:
                                                l2_cat_name = l2_cat_link.text
                                                if "Ver todo" not in l2_cat_name:
                                                    # get subcategory link (link without supermarket_url in l2)
                                                    if "href" in l2_cat_link.attrs:
                                                        l2_cat_link_href = l2_cat_link['href']
                                                    elif "data-href" in l2_cat_link.attrs:
                                                        l2_cat_link_href = l2_cat_link['data-href']
                                                    else:
                                                        l2_cat_link_href = " "
                                                    l2_cat_link_href = l2_cat_link_href.replace(":443", "")
                                                    if l2_cat_link_href[0:4] == "/es/":
                                                        l2_cat_link_href = self.supermarket_url + l2_cat_link_href[1:]
                                                    self.print_message(f"LINK 2: {l2_cat_link_href}", "SUCCESS")
                                                    if l2_cat_name not in level2 and l2_cat_name not in level3:
                                                        print(f" => Level2 cat name: {l2_cat_name}"
                                                              f" with link: {l2_cat_link_href}")
                                                        level2.append(l2_cat_name)
                                                    # ----------------------
                                                    # get level 3 categories
                                                    # ----------------------
                                                    # search ul with class="nav-level-3"
                                                    ul_level3 = l2_cat_container.find('ul', class_="nav-level-3")
                                                    if ul_level3 is not None:
                                                        # get all subcategory_containers (li) inside ul_subcategories
                                                        l3_cat_containers = ul_level3.find_all('li')
                                                        if l3_cat_containers is None:
                                                            print("- Not founded level 3 categories...")
                                                        else:
                                                            # print(f"Founded {len(level3_category_containers)}"
                                                            #      f" subcategories")
                                                            l1_cat_id = ""
                                                            l2_cat_id = ""
                                                            l3_cat_id = ""
                                                            for l3_cat_container in \
                                                                    l3_cat_containers:
                                                                l3_cat_link = \
                                                                    l3_cat_container.find('a')
                                                                # find subcategory name inside a tag
                                                                if l3_cat_link is not None:
                                                                    l3_cat_name = \
                                                                        l3_cat_link.text
                                                                    if "Ver todo" not in l3_cat_name:
                                                                        # get subcategory link
                                                                        l3_cat_link_href = l3_cat_link['data-href']
                                                                        # get ids from l3_cat_link_href
                                                                        l3_cat_link_href = l3_cat_link_href.replace(":443", "")
                                                                        link_split = l3_cat_link_href.split("/supermercado/")
                                                                        if len(link_split) == 2:
                                                                            ids = link_split[1].split("/")
                                                                            if len(ids) == 3:
                                                                                l1_cat_id = ids[0].split("-")[0]
                                                                                l2_cat_id = ids[1].split("-")[0]
                                                                                l3_cat_id = ids[2].split("-")[0]
                                                                        if l3_cat_name not in level3:
                                                                            print(
                                                                                f"   => Level3 cat name: {l3_cat_name}"
                                                                                f" with link: {l3_cat_link_href}")
                                                                            level3.append(l3_cat_name)
                                                                            categories.append([
                                                                                l1_cat_id,
                                                                                l1_cat_name,
                                                                                l1_cat_link_href,
                                                                                l2_cat_id,
                                                                                l2_cat_name,
                                                                                l2_cat_link_href,
                                                                                l3_cat_id,
                                                                                l3_cat_name,
                                                                                l3_cat_link_href
                                                                            ])

        else:
            print("- Not founded categories...")
        return categories

    def scrape_products(self, categories):
        """
        Get all products inside subcategory
        :param categories: three level categories (name, url)
        :return: all_products
        """
        products = []
        with open(self.output_path, 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
            header = self.get_header_product()
            writer.writerow(header)
            for category in categories:
                l1_cat_id, l1_cat_name, l1_cat_link_href, \
                    l2_cat_id, l2_cat_name, l2_cat_link_href,\
                    l3_cat_id, l3_cat_name, l3_cat_link_href = category
                # go to level3_category_link_href and extract products
                url = l3_cat_link_href
                # get page source
                self.content_html = self.get_page_source(url)
                # go down page to control scroll infinite
                self.scroll_down_page()
                # one the page is fully loaded parse the html
                parsed_html = BeautifulSoup(self.content_html, 'html.parser')
                # save parsed_html to file (just to check)
                # self.save_html(parsed_html.prettify())
                # get content unique div id="productListZone"
                div_products_general = parsed_html.find('div', id="productListZone")
                if div_products_general is not None:
                    # get all divs inside div_product_list with "col border-0 product-item-lineal" in class
                    div_products = div_products_general.find_all(
                        'div', class_=re.compile("^col border-0 product-item-lineal"))
                    for div_product in div_products:
                        product = self.scrape_product(div_product)
                        row = [
                            self.supermarket_name, l1_cat_id, l1_cat_name, l1_cat_link_href,
                            l2_cat_id, l2_cat_name, l2_cat_link_href,
                            l3_cat_id, l3_cat_name, l3_cat_link_href,
                            product["id_product"], product["name_product"],
                            product["url_product"], product["thumbnail"], product["packaging"],
                            product["unit_size"], product["unit_price"], product["size_format"],
                            product["bulk_price"]
                        ]
                        products.append(row)
                        writer.writerow(row)
        return products

    def scrape_product(self, div_product):
        """
        Get product information
        :param div_product: div product
        :return: product information dictionary
            "id_product";"name_product";"url_product";"thumbnail";
            "packaging";"unit_size";"unit_price";"size_format";"bulk_price"
        """
        # get first img into div with class begins with "product-image"
        div_image = div_product.find('div', class_=re.compile("^product-image"))
        product_thumbnail = ""
        if div_image is not None:
            # get img_product
            img_product = div_image.find('img')
            if img_product is not None:
                product_thumbnail = img_product['src']
        # get product_name, product_url
        # description inside div with class "product-description"
        div_description = div_product.find('div', class_="product-description")
        # get first h2 inside div
        h2_product = div_description.find('h2', class_="product-title")
        # get a inside h2
        a_product = h2_product.find('a')
        product_id = ""
        product_name = ""
        product_url = ""
        if a_product is not None:
            product_name = a_product.text.replace("\n", "")
            product_url = self.supermarket_url + a_product['href'][1:]
            # get product_id from url
            product_id = self.get_product_id(product_url)

        # packaging, unit_size & size_format is in product_name
        product_packaging = ""
        product_unit_size = ""
        product_size_format = ""
        if product_name != "":
            product_name_parts = product_name.split(", ")
            # product_name = product_name_parts[0]
            product_packaging, product_unit_size, product_size_format = self.get_details(product_name_parts)

        # get product_price for span with class="price-offer-now"
        product_unit_price = ""
        product_price_span = div_product.find('span', class_="price-offer-now")
        if product_price_span:
            product_unit_price = product_price_span.text.strip()

        # get product_bulk_price in span with class="price-product"
        product_bulk_price = product_unit_price
        product_bulk_price_span = div_product.find('span', class_="price-product")
        if product_bulk_price_span:
            product_bulk_price = product_bulk_price_span.text.replace("€", "").strip()

        # get product data dict
        product_data = dict(
            id_product=product_id,
            name_product=product_name,
            url_product= product_url,
            thumbnail=product_thumbnail,
            packaging=product_packaging,
            unit_size=product_unit_size,
            unit_price=product_unit_price,
            size_format=product_size_format,
            bulk_price=product_bulk_price
        )

        print(f"- Añadido producto: {product_data.values()}")

        return product_data

    @staticmethod
    def save_html(content_html):
        """
        Save html content into file (just to check)
        :param content_html: html content
        :return: none
        """
        with open("../lectura.html", "w", encoding="utf-8") as file:
            file.write(content_html)

    @staticmethod
    def get_product_id(product_url):
        """
        Get product id from url
        :param product_url: product url
        :return: product id
        """
        product_url_parsed = product_url.split("/es/productdetail/")
        return product_url_parsed[1].split("-")[0]

    def get_details(self, full_product_name):
        """
        Get product details
        :param full_product_name: product name
        :return: product details
        """
        product_packaging = ""
        product_unit_size = ""
        product_size_format = ""
        if len(full_product_name) == 3:
            product_packaging = full_product_name[1].strip()
            # into product_name_parts[2] is unit_size & size_format
            # unit size is a number and size_format is equal to g, kg, l, ml, ...
            # use regular expression to get product unit_size and size_format
            patron = r"\s?(\w+)\s(d+)\s(\w+)"
            matches = re.search(patron, full_product_name[2])
            if matches:
                product_unit_size = matches.group(2)
                product_size_format = matches.group(3)
        if len(full_product_name) == 2:
            # first check if have 3 parts
            check_parts = full_product_name[1].split(" ")
            if len(check_parts) == 3:
                product_packaging = check_parts[0]
                product_unit_size = check_parts[1]
                product_size_format = check_parts[2]
                # particular case "60g X 4"
                if product_unit_size.lower() == "x":
                    print("entramos en el caso particular")
                    patron2 = r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)'
                    matches2 = re.search(patron2, product_packaging)
                    if matches2:
                        product_packaging = "pack" # suponemos pack
                        product_unit_size = matches2.group(1) + "x" + product_size_format
                        product_size_format = matches2.group(2)
                # particular case "160+80" in product_unit_size
                if "+" in product_unit_size:
                    product_unit_size_split = product_unit_size.split("+")
                    product_unit_size = product_unit_size_split[0] + product_unit_size_split[1]
                # particular case "5-6 unid. bandeja"
                if "unid." in product_unit_size:
                    product_packaging = check_parts[2]
                    product_unit_size = check_parts[0]
                    product_size_format = check_parts[1]
            else:
                patron = r"\s?(\w+)\s(d+)\s(\w+)"
                matches = re.search(patron, full_product_name[1])
                if matches:
                    product_packaging = matches.group(1)
                    product_unit_size = matches.group(2)
                    product_size_format = matches.group(3)

        # convert unit
        product_unit_size, product_size_format = self.convert_unit_size(product_unit_size, product_size_format)

        return [product_packaging, product_unit_size, product_size_format]

    @staticmethod
    def convert_unit_size(product_unit_size, product_size_format):
        """
        Convert unit size
        :param product_unit_size: product unit size
        :param product_size_format: product size format
        :return: product unit size & product size format
        """
        if product_size_format.lower() == "litro" or product_size_format.lower() == "litros":
            product_size_format = "l"
        if product_size_format.lower() == "kilogramo" or product_size_format.lower() == "kilogramos":
            product_size_format = "kg"
        if product_unit_size != "":
            # check packs option
            patron = r'(\d+)\s*x\s*(\d+)'
            result = re.search(patron, product_unit_size)
            if result:
                number1 = int(result.group(1))
                number2 = int(result.group(2))
                product_unit_size = number1 * number2
            try:
                product_unit_size = float(str(product_unit_size).replace(",", "."))
                if product_size_format == "g":
                    product_unit_size = float(product_unit_size) / 1000
                    product_size_format = "kg"
                if product_size_format == "ml":
                    product_unit_size = float(product_unit_size) / 1000
                    product_size_format = "l"
                if product_size_format == "cl":
                    product_unit_size = float(product_unit_size) / 100
                    product_size_format = "l"
            except ValueError:
                pass
        return [product_unit_size, product_size_format]