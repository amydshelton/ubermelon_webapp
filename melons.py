from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    current_cart = {}
    total = 0
    if 'cart' in session:
        for key in session['cart']:
            melon = model.get_melon_by_id(key)
            #current_cart[key] = [melon.common_name, melon.price]
            #current_car[key] = melon so that the melon can be accessed
            current_cart[key] = {'common_name': melon.common_name, 'price': melon.price}
            total += melon.price * session['cart'][key]
        return render_template("cart.html",current_cart = current_cart, total = total)
    else:
        flash('You have nothing in your cart. Keep shopping')
        return redirect("/melons")

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
   # session.clear()
    id = str(id)
    if 'cart' in session:
        if id in session['cart']:
            session['cart'][id] += 1
        else:
            session['cart'][id] = 1
    else:
        session['cart'] = {id: 1}

    melon = model.get_melon_by_id(id)
    flash("Successfully added %s to cart!" % str(melon.common_name))
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    #if sesssion has customer, go to process_login
    if 'customer' in session:
        flash("You're already logged in. Shop away!")
        return redirect ("/melons")
    else: 
       return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    email = request.form.get("email")
    if model.get_customer_by_email(email) is None:
        flash("You aren't a customer yet!")
    else:
        customer = model.get_customer_by_email(email)
        #next line is redundant, but not egregious - Lindsay
        first_name, last_name, email = customer.first_name, customer.last_name, customer.email
        session['customer'] = email
        flash("Logged in. Shop away!")
    return redirect ("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

@app.route("/logout")
def logout():
    """Logs the user out, clears the session"""
    session.clear()
    flash("You are logged out. See you soon!")
    return redirect("/melons")

@app.route("/newcustomer")
def new_customer():
    """Where users can sign up to join ubermelon."""
    return render_template("customer_signup.html")

@app.route("/newcustomer", methods=["POST"])
def new_customer_welcome():
    """Welcomes new user"""
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    message = model.add_customer_to_db(email,first_name,last_name,password)
    session['customer'] = email
    flash(message)
    return redirect("/melons")

 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
