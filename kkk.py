# # from datetime import date
# # import requests

# # opt = "y"
# # products = []
# # total_sum = 0

# # while opt == "y":
# #     name = input("Enter Product Name    : ")
# #     qty = int(input("Enter Qty             : "))
# #     price = float(input("Enter Price           : "))
# #     total = qty * price
# #     products.append({"name": name, "qty": qty, "price": price, "total": total})
# #     opt = input("Add more Product? (y/n): ")
# #     print('--------------------------------')

# # discount = float(input('Enter Discount : '))

# # for product in products:
# #     total_sum += product["total"]

# # discounted_total = total_sum * (1 - discount / 100)

# # print("\nProduct List")
# # for product in products:
# #     print("Name:", product["name"])
# #     print("Qty:", product["qty"])
# #     print("Price:", product["price"])
# #     print()

# # print("Total before discount:", total_sum)
# # print("Discount applied:", discount, "%")
# # print("Total after discount:", discounted_total)

# # received_amount = float(input('Received amount: '))
# # change_amount = 0

# # while received_amount < discounted_total:
# #     print("Insufficient amount received. Please re-enter.")
# #     received_amount = float(input('Received amount: '))

# # change_amount = received_amount - discounted_total

# # print("Received Amount:", received_amount)
# # print("Change Amount:", change_amount)

# # image_file_path = "D:\\Setec\\Python\\img.jpg" 

# # html_message = (
# #     "<strong>🧾 INV0001</strong>\n"
# #     "<code>សរុប: ${:.2f}</code>\n"
# #     "<code>ប្រាក់ទទួល: ${:.2f}</code>\n"
# #     "<code>ប្រាក់អាប់: ${:.2f}</code>\n"
# #     "<code>ប្រាក់អាប់: {}៛</code>\n"
# #     "<code>📆 {}</code>\n"
# #     "<code>===Product Lists===</code>\n"
# # ).format(
# #     total_sum,
# #     received_amount,
# #     change_amount,
# #     change_amount * 4100,
# #     date.today(),
# # )


# # for index, product in enumerate(products, start=1):
# #     html_message += "<code>{}. {} {} x {}</code>\n".format(index, product["name"], product["qty"], product["price"])


# # bot_token = '7142917421:AAEWaepuOdWZGqEixJFUWYw_W27dxTd4t6I'
# # chat_id = '@cspshop123'


# # url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
# # files = {'photo': open(image_file_path, 'rb')}
# # data = {'chat_id': chat_id, 'caption': html_message, 'parse_mode': 'HTML'}
# # response = requests.post(url, files=files, data=data)
# # print(response.status_code)



# import requests
# from datetime import date

# app = Flask(__name__)

# @app.post('/submit_order')
# def submit_order():
#     name = request.form.get('fullname')
#     phone = request.form.get('phone')
#     email = request.form.get('email')
    
#     product_id = request.args.get('id')
#     response = requests.get(f'https://fakestoreapi.com/products/{product_id}')
    
#     if response.status_code != 200:
#         return "Error fetching product details", 500
    
#     current_product = response.json()
    
#     html_message = (
#         "<strong>🧾 INV0001</strong>\n"
#         "<code>សរុប: ${:.2f}</code>\n"
#         "<code>📆 {}</code>\n"
#         "<code>Customer: {}</code>\n"
#         "<code>Phone: {}</code>\n"
#         "<code>Email: {}</code>\n"
#     ).format(
#         current_product['price'],
#         date.today(),
#         name,
#         phone,
#         email,
#     )
    
#     image_url = current_product['image']

#     bot_token = '7142917421:AAEWaepuOdWZGqEixJFUWYw_W27dxTd4t6I'
#     chat_id = '@cspshop123'
#     url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
#     data = {'chat_id': chat_id, 'photo': image_url, 'caption': html_message, 'parse_mode': 'HTML'}
    
#     response = requests.post(url, data=data)
#     print(response.status_code)
    
#     return render_template('user/submit_order.html', current_product=current_product)

# if __name__ == '__main__':
#     app.run(debug=True)
