import sqlite3

DB = None
CONN = None

class Melon(object):
    """A wrapper object that corresponds to rows in the melons table."""
    def __init__(self, id, melon_type, common_name, price, imgurl, flesh_color, rind_color, seedless):
        self.id = id
        self.melon_type = melon_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        return "$%.2f"%self.price

    def __repr__(self):
        return "<Melon: %s, %s, %s>"%(self.id, self.common_name, self.price_str())

class Customer(object):
    """A class for customers."""
    def __init__(self, givenname, surname, email):
      self.first_name = givenname
      self.last_name = surname
      self.email = email

def connect():
  global DB, CONN
  CONN = sqlite3.connect("melons.db")
  DB = CONN.cursor()


def get_melons():
    """Query the database for the first 30 melons, wrap each row in a Melon object"""
    connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE imgurl <> ''
               LIMIT 30;"""

    DB.execute(query)
    melon_rows = DB.fetchall()

    melons = []

    for row in melon_rows:
        melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                      row[6], row[7])

        melons.append(melon)

    print melons

    return melons

def get_melon_by_id(id):
    connect()
    """Query for a specific melon in the database by the primary key"""
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE id = ?;"""

    DB.execute(query, (id,))

    row = DB.fetchone()
    
    if not row:
        return None

    melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7])
    
    return melon

def get_customer_by_email(email):
  connect()
  query = """SELECT givenname, surname, email FROM customers WHERE email = ?"""
  DB.execute(query, (email,))
  row = DB.fetchone()
  if row == None:
    return None
  else:
    customer = Customer(row[0], row[1], row[2])
    return customer

def add_customer_to_db(email, first_name, last_name, password):
  connect()
  query = """INSERT INTO customers (email, givenname, surname, password) VALUES (?, ?, ?, ?)"""
  DB.execute(query, (email, first_name, last_name, password))
  CONN.commit()
  message = "Welcome to Ubermelon!"
  return message
