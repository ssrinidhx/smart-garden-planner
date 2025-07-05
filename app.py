from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['garden_planner_project']
users_collection = db['users']

app = Flask(__name__)
app.secret_key = '0845f8ccaa59beee226866a920b8ca8f'

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    modal_title = None
    modal_message = None
    modal_button_text = None

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            modal_title = "Error"
            modal_message = "Passwords do not match."
            modal_button_text = "Try Again"
            return render_template(
                'create_account.html',
                name=name, email=email, country=country,
                state=state, city=city,
                modal_title=modal_title,
                modal_message=modal_message,
                modal_button_text=modal_button_text
            )

        hashed_password = generate_password_hash(password)

        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            modal_title = "Error"
            modal_message = "Email address is already registered."
            modal_button_text = "Try Again"
            return render_template(
                'create_account.html',
                modal_title=modal_title,
                modal_message=modal_message,
                modal_button_text=modal_button_text
            )

        users_collection.insert_one({
            'name': name,
            'email': email,
            'country': country,
            'state': state,
            'city': city,
            'password': hashed_password
        })

        modal_title = "Success"
        modal_message = "Account created successfully!"
        modal_button_text = "Done"
        return render_template(
            'create_account.html',
            modal_title=modal_title,
            modal_message=modal_message,
            modal_button_text=modal_button_text
        )

    return render_template('create_account.html')

@app.route('/login', methods=['POST'])
def handle_login():
    modal_title = None
    modal_message = None
    modal_button_text = None

    email = request.form['email']
    password = request.form['password']

    user = users_collection.find_one({'email': email})

    if user:
        if check_password_hash(user['password'], password):
            session['user_email'] = user['email']
            return redirect(url_for('mainpage'))
        else:
            modal_title = "Error"
            modal_message = "Incorrect password."
            modal_button_text = "Try Again"
    else:
        modal_title = "Error"
        modal_message = "This email has not been registered."
        modal_button_text = "Try Again"

    return render_template(
        'login.html',
        modal_title=modal_title,
        modal_message=modal_message,
        modal_button_text=modal_button_text
    )

@app.route('/mainpage', methods=['GET'])
def mainpage():
    return render_template('main_page.html')

@app.route('/userdetails')
def userdetails():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    user_email = session['user_email']

    user = users_collection.find_one({'email': user_email}, {
        '_id': 0,  
        'name': 1,
        'email': 1,
        'country': 1,
        'state': 1,
        'city': 1
    })

    if user:
        return render_template('user_details.html', user=user)
    else:
        flash("User details not found.", "error")
        return redirect(url_for('mainpage'))

@app.route('/search')
def search():
    query = request.args.get('plant', '').lower()
    
    if query:
        search_results = [plant for plant in plants if query in plant['name'].lower()]
    else:
        search_results = []

    return render_template('main_page.html', plants=plants, search_results=search_results)

plants = [
    {'name': 'Apples', 'category': 'Fruits', 'image': 'Apple.webp'},
    {'name': 'Blueberries', 'category': 'Fruits', 'image': 'Blueberries.jpg'},
    {'name': 'Grapes', 'category': 'Fruits', 'image': 'Grapes.jpg'},
    {'name': 'Oranges', 'category': 'Fruits', 'image': 'Orange.jpg'},
    {'name': 'Strawberries', 'category': 'Fruits', 'image': 'Strawberry.jpeg'},
    {'name': 'Beetroot', 'category': 'Vegetables', 'image': 'Beetroot.jpg'},
    {'name': 'Carrots', 'category': 'Vegetables', 'image': 'Carrot.jpg'},
    {'name': 'Onions', 'category': 'Vegetables', 'image': 'Onions.jpg'},
    {'name': 'Potatoes', 'category': 'Vegetables', 'image': 'Potato.jpg'},
    {'name': 'Tomatoes', 'category': 'Vegetables', 'image': 'Tomatoes.jpg'},
    {'name': 'Basil', 'category': 'Greens', 'image': 'Basil.jpg'},
    {'name': 'Lettuce', 'category': 'Greens', 'image': 'Lettuce.jpg'},
    {'name': 'Mint', 'category': 'Greens', 'image': 'Mint.jpg'},
    {'name': 'Parsley', 'category': 'Greens', 'image': 'Parsley.jpg'},
    {'name': 'Spinach', 'category': 'Greens', 'image': 'Spinach.jpg'},
    {'name': 'Daffodils', 'category': 'Flowers', 'image': 'Daffodils.jpg'},
    {'name': 'Lilies', 'category': 'Flowers', 'image': 'Lilies.jpg'},
    {'name': 'Rose', 'category': 'Flowers', 'image': 'Rose.jpg'},
    {'name': 'Sunflower', 'category': 'Flowers', 'image': 'Sunflower.jpg'},
    {'name': 'Tulip', 'category': 'Flowers', 'image': 'Tulips.jpg'},
]

@app.route('/logout')
def logout():
    session.pop('user_email', None)  
    return redirect(url_for('homepage'))  

@app.route('/garlic')
def garlic():
    return render_template('garlic.html')

@app.route('/onions')
def onions():
    return render_template('onions.html')

@app.route('/broccoli')
def broccoli():
    return render_template('broccoli.html')

@app.route('/cabbage')
def cabbage():
    return render_template('cabbage.html')

@app.route('/cauliflower')
def cauliflower():
    return render_template('cauliflower.html')

@app.route('/cosmos')
def cosmos():
    return render_template('cosmos.html')

@app.route('/daffodils')
def daffodils():
    return render_template('daffodils.html')

@app.route('/lavender')
def lavender():
    return render_template('lavender.html')

@app.route('/lilies')
def lilies():
    return render_template('lilies.html')

@app.route('/marigold')
def marigold():
    return render_template('marigold.html')

@app.route('/rose')
def rose():
    return render_template('rose.html')

@app.route('/sunflower')
def sunflower():
    return render_template('sunflower.html')

@app.route('/tulip')
def tulip():
    return render_template('tulip.html')

@app.route('/apple')
def apple():
    return render_template('apple.html')

@app.route('/blueberries')
def blueberries():
    return render_template('blueberries.html')

@app.route('/grapes')
def grapes():
    return render_template('grapes.html')

@app.route('/orange')
def orange():
    return render_template('orange.html')

@app.route('/strawberries')
def strawberries():
    return render_template('strawberries.html')

@app.route('/lettuce')
def lettuce():
    return render_template('lettuce.html')

@app.route('/spinach')
def spinach():
    return render_template('spinach.html')

@app.route('/basil')
def basil():
    return render_template('basil.html')

@app.route('/ginger')
def ginger():
    return render_template('ginger.html')

@app.route('/mint')
def mint():
    return render_template('mint.html')

@app.route('/mustard')
def mustard():
    return render_template('mustard.html')

@app.route('/parsley')
def parsley():
    return render_template('parsley.html')

@app.route('/rosemary')
def rosemary():
    return render_template('rosemary.html')

@app.route('/beans')
def beans():
    return render_template('beans.html')

@app.route('/peanut')
def peanut():
    return render_template('peanut.html')

@app.route('/peas')
def peas():
    return render_template('peas.html')

@app.route('/cucumber')
def cucumber():
    return render_template('cucumber.html')

@app.route('/pumpkin')
def pumpkin():
    return render_template('pumpkin.html')

@app.route('/watermelon')
def watermelon():
    return render_template('watermelon.html')

@app.route('/bellpepper')
def bellpepper():
    return render_template('bellpepper.html')

@app.route('/tomatoes')
def tomatoes():
    return render_template('tomatoes.html')

@app.route('/asparagus')
def asparagus():
    return render_template('asparagus.html')

@app.route('/corn')
def corn():
    return render_template('corn.html')

@app.route('/beetroot')
def beetroot():
    return render_template('beetroot.html')

@app.route('/carrots')
def carrots():
    return render_template('carrots.html')

@app.route('/potatoes')
def potatoes():
    return render_template('potatoes.html')

@app.route('/radish')
def radish():
    return render_template('radish.html')

if __name__ == '__main__':
    app.run(debug=True)