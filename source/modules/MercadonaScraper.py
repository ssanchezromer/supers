import csv
import os
from WebScraper import WebScraper


class MercadonaScraper(WebScraper):
    """
    MercadonaScraper class
    """
    def __init__(self):
        """
        Constructor MercadonaScraper class
        """
        super().__init__(supermarket_name="Mercadona")
        self.products_data_Mercadona = []
        self.supermarket_url = "https://tienda.mercadona.es/"
        self.categories_url = "api/categories/"
        self.super_folder = "mercadona"
        self.output_path = os.path.join(os.getcwd(), self.path_csv, self.super_folder, self.name_csv)

    def load_content(self):
        """
        Load content from supermarket
        """
        self.print_message(f"Loading products from {self.supermarket_name}...", "INFO")
        create = True
        if self.check_exists_products():
            self.products_data_Mercadona = self.get_product_data_from_csv()
            self.print_total(len(self.products_data_Mercadona))
            if not self.remove_products():
                create = False

        if create:
            self.load_products()
        self.print_added_products(len(self.products_data_Mercadona), self.supermarket_name)
        self.all_products[self.supermarket_name] = self.products_data_Mercadona
        self.close_browser()

    def load_products(self):
        """
        Load all product from supermarket
        :return: none
        """
        self.products_data_Mercadona = []
        # Get url for principal categories
        principal_categories_url = self.supermarket_url + self.categories_url
        # Get json file from url
        code_json = self.get_json(principal_categories_url)
        if "results" in code_json:
            with open(self.output_path, 'w', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
                header = self.get_header_product()
                writer.writerow(header)
                for principal_category_json in code_json["results"]:
                    self.print_message(f"- Principal category name: {principal_category_json['name']}", "SUCCESS")
                    principal_category_json["url"] = "" # no url
                    for category_json in principal_category_json["categories"]:
                        self.print_message(f"  - Category name: {category_json['name']}", "SUCCESS")
                        category_json["url"] = self.supermarket_url + "categories/" + str(category_json["id"])
                        categories_api_url = self.supermarket_url + self.categories_url + str(category_json['id'])
                        # Get code from webpage
                        code_json_categories = self.get_json(categories_api_url)
                        if "categories" in code_json_categories:
                            # save all subcategories (categories)
                            for subcategory_json in code_json_categories["categories"]:
                                self.print_message(f"    - Subcategory name: {subcategory_json['name']}", "SUCCESS")
                                subcategory_json["url"] = "" # no url subcategory
                                products_json = subcategory_json["products"]
                                for product_json in products_json:
                                    self.print_message(f"      - Product name: {product_json['display_name']}", "")
                                    product = self.get_product_list(principal_category_json,
                                                                    category_json,
                                                                    subcategory_json,
                                                                    product_json)
                                    writer.writerow(product)
                                    self.products_data_Mercadona.append(product)
                self.print_total(len(self.products_data_Mercadona))

        else:
            self.print_message("Categories not founded...", "WARNING")

    def get_product_list(self, principal_category_json, category_json, subcategory_json, product_json):
        """
        Get product list
        :param principal_category_json: principal category json
        :param category_json: category json
        :param subcategory_json: subcategory json
        :param product_json: product json
        :return: product list
        """
        return [self.supermarket_name,
                principal_category_json["id"], principal_category_json["name"], principal_category_json["url"],
                category_json["id"], category_json["name"], category_json["url"],
                subcategory_json["id"], subcategory_json["name"], subcategory_json["url"],
                product_json["id"], product_json["display_name"], product_json["share_url"],
                product_json["thumbnail"], product_json["packaging"],
                product_json["price_instructions"]["unit_size"],
                product_json["price_instructions"]["unit_price"].replace(",", "."),
                product_json["price_instructions"]["size_format"],
                product_json["price_instructions"]["bulk_price"].replace(",", ".")]


