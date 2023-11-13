from app import app
from flask import render_template, request as request_flask
import csv


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search():
    # get the query
    query = request_flask.form['query']
    if len(query.strip()) <= 2:
        return render_template('search.html')
    # Print the results
    results = f"<h3>Results for: <strong>'{query}'</strong></h3>"
    results_final = ""
    products_found = 0

    # search product into csv file
    with open('csv/products.csv', newline='') as csvfile:
        # first row in csv file is the header
        reader = csv.DictReader(csvfile, delimiter=';')
        results_final += ""
        counter = 0
        query_words = query.lower().split()
        for row in reader:
            name_product = row["name_product"].lower()
            if all(word in name_product for word in query_words):
                if counter == 0:
                    results_final += '<div class="row">'
                results_final += create_div_product(row)
                counter += 1
                if counter == 5:
                    results_final += '</div><p style="line-height: 0px; font-size:8px">&nbsp;</p>'
                    counter = 0
                products_found += 1

        if counter > 0:
            results_final += '</div><p style="line-height: 0px; font-size:8px">&nbsp;</p>'
        #results_final += "</div>"
    results += f"<p>Products found: <strong>{products_found}</strong></p>" + results_final

    return render_template('search.html', results=results, query=query)


def create_div_product(row):
    """
    Creates div element with product data
    :param row: row data element for each product
    :return: html div element
    """
    if row["thumbnail"] == "":
        row["thumbnail"] = "../static/product.png"
    link = row["url_product"]
    div = '<div class="column">\
            <div class="card">\
                <div class="image-container">'
    div += f'<img class="corner-image" src="../static/logo-{row["supermarket"].lower()}.png" ' \
           f'alt="{row["supermarket"]}">'
    div += '</div>'
    description = f'{row["packaging"]} {convert_to_int(row["unit_size"])} {row["size_format"].upper()}'
    div += f'<a href="{link}" target="blank"><img src="{row["thumbnail"]}" ' \
           f'alt="{row["name_product"]}" style="width: 100%; max-width: 200px;"></a>\
             <div id="title"><span class="title"><a href="{link}" target="blank">{row["name_product"]}</a></span></div>\
             <span class="description">{description}</span>\
             <span class="price">{row["unit_price"]} €</span><br />\
             (<span class="price">1 {row["size_format"].upper()} {row["bulk_price"]} €</span>)\
            </div>\
          </div>'
    return div


def convert_to_int(num):
    """"
    Convert num to int
    :param num: number to convert
    :return: int
    """
    if num != "":
        try:
            if "x" in num:
                # convert text 3 x 0.048 to float
                num_split = num.split("x")
                num = "{:.2f}".format(float(num_split[0]) * float(num_split[1]))
            else:
                num = float(num)
                if num == int(num):
                    return int(num)
        except ValueError:
            pass

    return num
