from modules import *
import subprocess


# Load content supers
bonpreu = BonpreuScraper()
bonpreu.load_content()

mercadona = MercadonaScraper()
mercadona.load_content()

caprabo = CapraboScraper()
caprabo.load_content()

# Get all products from Bonpreu, Mercadona & Caprabo
all_products = bonpreu.all_products["Bonpreu"] + mercadona.all_products["Mercadona"] + caprabo.all_products["Caprabo"]
# save all products
mercadona.save_all_products(all_products)

# Open flash app
mercadona.print_message("\nOpen run.py flash app...\n", "INFO")
subprocess.Popen("python run.py", shell=True)
