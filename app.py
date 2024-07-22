from flask import Flask, redirect, render_template,request,session, url_for, jsonify
import requests
import json
import base64  
from datetime import date,datetime
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/image'
app.secret_key = 'supersecretkey'

def get_db_connection():
    conn = sqlite3.connect('ecommerce.db',check_same_thread=False)
    conn.row_factory = sqlite3.Row  
    return conn

conn = get_db_connection()
row = conn.execute("""SELECT * FROM tblProduct""")
products = []
for item in row:
    product = {
        'id': item[0],
        'title': item[1],
        'cost': item[2],
        'price': item[3],
        'description': item[4],
        'image': item[5]
    }
    products.append(product)




@app.route('/')
@app.route('/home')
def home():
    return render_template('user/home.html', module='home')





# product_list = [
#         {
#             'id' : '1',
#             'title' : 'Jordan',
#             'price' : '200',
#             'description' : "Some quick example text to build on the card title and make up the bulk of the card's content.",
#             'image': 'shoe2.jpg'
#         },
#         {
#             'id' : '2',
#             'title' : 'Nike',
#             'price' : '150',
#             'description' : "Some quick example text to build on the card title and make up the bulk of the card's content.",
#             'image': 'shoe3.jpg'
#         },
#         {
#             'id' : '3',
#             'title' : 'Adidas',
#             'price' : '150',
#             'description' : "Some quick example text to build on the card title and make up the bulk of the card's content.",
#             'image': 'shoe.jpg'
#         }
#     ]


# respone = requests.get('https://fakestoreapi.com/products')
# product_list = respone.json()


# @app.get('/product')
# def product():
#     return render_template('user/product.html', product_list = product_list)



@app.get('/product')
def product():
    row = conn.execute("""SELECT * FROM tblProduct""")
    products = []
    
    for item in row:
        image = ''
        if item[6] == None:
            image = 'no_image'
        else:
            image = item[6]
        product = {
            'id': item[0],
            'title': item[1],
            'cost': item[2],
            'price': item[3],
            'category': item[4],
            'description': item[5],
            'image': image
        }
        products.append(product)
        
    return render_template('user/product.html', products=products ,module="product")



@app.route('/cart')
def cart():
    if 'items' not in session:
        session['items'] = []

    cart_products = []
    added_items = set()  # To keep track of already added items

    for item_id in session['items']:
        for product in products:
            if item_id == str(product['id']):
                if item_id not in added_items:
                    product['qty'] = session['items'].count(item_id)
                    cart_products.append(product)
                    added_items.add(item_id)
                break
    return render_template('user/cart.html', cart_products=cart_products)





@app.route('/add_item', methods=['POST'])
def add_item():
    item_id = request.form['item_id']
    if 'items' not in session:
        session['items'] = []
    
    session['items'].append(item_id)
    session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
    
    return redirect(url_for('product'))







@app.route('/clear')
def clear_items():
    session.pop('items', None)
    return redirect(url_for('cart'))


@app.route('/clear_selected')
def clear_selected():
    product_id = request.args.get('id')
    
    if 'items' in session:
        session['items'] = [item for item in session['items'] if item != product_id]
        session.modified = True
    
    return redirect(url_for('cart'))
    




@app.get('/product_detail')
def product_detail():
    product_id = request.args.get('id')
    row = conn.execute(f"""SELECT * FROM tblProduct WHERE id={product_id}""")
    current_product = {}
    for item in row:
        image = ''
        if item[6] == None:
            image = 'no_image'
        else:
            image = item[6]
            
        current_product['id']=item[0]
        current_product['title']=item[1]
        current_product['cost']=item[2]
        current_product['price']=item[3]
        current_product['category']=item[4]
        current_product['description']=item[5]
        current_product['image']=image

    return render_template('user/product_detail.html',current_product=current_product)




@app.get('/add_product')
def add_product():
    row = conn.execute("""SELECT * FROM tblProduct""")
    products = []
    
    for item in row:
        image = ''
        if item[6] == None:
            image = 'no_image'
        else:
            image = item[6]
        product = {
            'id': item[0],
            'title': item[1],
            'cost': item[2],
            'price': item[3],
            'category': item[4],
            'description': item[5],
            'image': image
        }
        products.append(product)
    return render_template('user/add_product.html', products=products)


@app.post('/submit_new_product')
def submit_new_product():
    title = request.form.get('title')
    price = request.form.get('price')
    cost = request.form.get('cost')
    category = request.form.get('category')
    description = request.form.get('description')
    file = request.files['file']
    if file:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'product', filename)
        file.save(file_path)
        
    cropImage = request.files['croppedImage']
    if cropImage:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        cfilename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'crop_image', cfilename)
        cropImage.save(file_path)
    
    
    # Insert into database (adjust as per your database setup)
    res = conn.execute("INSERT INTO tblProduct (title, cost, price, category, description, image) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, float(cost), float(price), category, description, filename))
    conn.commit()
    
    return redirect('/add_product')
 
 
 
 
@app.get('/edit_product')
def edit_product():
    product_id = request.args.get('id')
    row = conn.execute(f"""SELECT * FROM tblProduct WHERE id={product_id}""")
    current_product = {}
    for item in row:
        image = ''
        if item[6] == None:
            image = 'no_image'
        else:
            image = item[6]
            
        current_product['id']=item[0]
        current_product['title']=item[1]
        current_product['cost']=item[2]
        current_product['price']=item[3]
        current_product['category']=item[4]
        current_product['description']=item[5]
        current_product['image']=image
    return render_template('user/edit_product.html',current_product=current_product)
 
 
 
@app.post('/save_update')
def save_update():
    id = request.form.get('pid')
    title = request.form.get('title')
    price = request.form.get('price')
    cost = request.form.get('cost')
    category = request.form.get('category')
    description = request.form.get('description')
    file = request.files['file']
    
    filename = None
    if file:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'product', filename)
        file.save(file_path)
        
        
    res = conn.execute("UPDATE tblProduct SET title = ?, cost = ?, price = ?, category = ?, description = ?, image = ? WHERE id = ?",(title, float(cost), float(price), category, description, filename, id))
    conn.commit()
    
    return redirect('/add_product')

 
    


@app.route('/confirm_delete')
def confirm_delete():
    product_id = request.args.get('id')
    row = conn.execute(f"""SELECT * FROM tblProduct WHERE id={product_id}""")
    current_product = {}
    for item in row:
        image = ''
        if item[6] == None:
            image = 'no_image'
        else:
            image = item[6]
            
        current_product['id']=item[0]
        current_product['title']=item[1]
        current_product['cost']=item[2]
        current_product['price']=item[3]
        current_product['category']=item[4]
        current_product['description']=item[5]
        current_product['image']=image

    return render_template('user/confirm_delete.html',current_product=current_product)
        

@app.post('/delete_product')
def delete_product():
    pid = request.form.get('pid')
    row = conn.execute(f"""DELETE FROM tblProduct WHERE id={pid}""")
    conn.commit()
    
    return redirect('/add_product')







@app.get('/checkout')
def checkout():
    product_id = request.args.get('id')
    row = conn.execute(f"""SELECT * FROM tblProduct WHERE id={product_id}""")
    current_product = {}
    for item in row:
        image = ''
        if item[6] == None:
            image = 'no_image'
        else:
            image = item[6]
            
        current_product['id']=item[0]
        current_product['title']=item[1]
        current_product['cost']=item[2]
        current_product['price']=item[3]
        current_product['category']=item[4]
        current_product['description']=item[5]
        current_product['image']=image
            
    return render_template('user/checkout.html',current_product=current_product)



@app.post('/submit_order')
def submit_order():
    name = request.form.get('fullname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    
    product_id = request.args.get('id')
    row = conn.execute("SELECT * FROM tblProduct WHERE id=?", (product_id,))
    
    current_product = {}
    for item in row:
        image = 'no_image' if item[6] is None else item[6]
        
        current_product = {
            'id': item[0],
            'title': item[1],
            'cost': item[2],
            'price': item[3],
            'category': item[4],
            'description': item[5],
            'image': image,
        }
    
    html_message = (
        "<strong>🧾 INV0001</strong>\n"
        "<code>ឈ្មោះ: {}</code>\n"
        "<code>សរុប: ${:.2f}</code>\n"
        "<code>📆 {}</code>\n"
        "<code>Customer: {}</code>\n"
        "<code>Phone: {}</code>\n"
        "<code>Email: {}</code>\n"
    ).format(
        current_product['title'],
        current_product['price'],
        date.today(),
        name,
        phone,
        email,
    )
    
    image_file_path = f"C:\\Users\\USER\\Python Project\\E-Commerce\\static\\image\\product\\{current_product['image']}"
    
    bot_token = '7142917421:AAEWaepuOdWZGqEixJFUWYw_W27dxTd4t6I'
    chat_id = '@cspshop123'
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(image_file_path, 'rb') as photo:
        files = {'photo': photo}
        data = {'chat_id': chat_id, 'caption': html_message, 'parse_mode': 'HTML'}
        response = requests.post(url, files=files, data=data)
        print(response.status_code)
    
    return redirect(url_for('product'))











if __name__ == '__main__':
    app.run()
