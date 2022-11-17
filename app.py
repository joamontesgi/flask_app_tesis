from flask import Flask, jsonify, request, render_template
from products import products
import os

#from interfaces import get_connection_name_from_guid
import netifaces as ni
#from getTraffic import captureTraffic

from pprint import pprint

app = Flask(__name__)

#Render form in HTML
@app.route('/')
def template():
    return render_template('form.html')

# Get all
@app.route('/products')
def getProducts():
    return jsonify({'products': products})

# Get one
@app.route('/products/<int:id>')
def getProduct(id):
    productsFound = [product for product in products if product['id'] == id]
    return productsFound

# Create
@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        'id': request.json['id'],
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': request.json['quantity']
    }
    products.append(new_product)
    return jsonify({'message': "Gg", 'products': products})

# Update
@app.route('/productsEdit/<int:id>' , methods=['PUT'])
def editProduct(id):
    productFound = [product for product in products if product['id'] == id]
    productFound[0]['name'] = request.json['name']
    productFound[0]['price'] = request.json['price']
    productFound[0]['quantity'] = request.json['quantity']
    return jsonify({'message': "Product Updated", 'product': productFound[0]})

# Delete
@app.route('/productsDelete/<int:id>' , methods=['DELETE'])
def deleteProduct(id):
    productFound = [product for product in products if product['id'] == id]
    products.remove(productFound[0])
    return jsonify({'message': "Product Deleted", 'products': products})

@app.route('/algoritmo', methods=['POST'])
def algoritmo():
    algoritmo = request.form['algoritmo']
    trafico=request.form['trafico']
    if(trafico=="1"):
        a=os.system("sudo python getTraffic.py")
        os.system("sudo pkill -f getTraffic.py")

        return jsonify({'message': "Tráfico capturado: "})
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)