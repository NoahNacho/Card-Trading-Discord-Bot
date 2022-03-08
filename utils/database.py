import sqlite3
import random

def pc_random():
    pc_list = pc_getall()
    (name,link) = random.choice(pc_list)
    return name, link


def create_users_table():
    """ Create table for users """
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute("""CREATE TABLE users (
            user_id text,
            photcard_list blob
        )""")
    connection.commit()
    connection.close()


def create_pc_table():
    """ Create table for photocards """
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute("""CREATE TABLE photocards (
            name text,
            link blob
    )""")
    connection.commit()
    connection.close()

def pc_insert(name,link):
    """ Insert New photocard into database """
    pc_list = []
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute("SELECT link FROM photocards")
    all = c.fetchall()
    for item in all:
        card = item[0]
        pc_list.append(card)
    if  link in pc_list:
        return "Already added to database."
    else:
        c.execute(f"""INSERT INTO photocards VALUES ('{name}','{link}') """)
        connection.commit()
        connection.close()
        return f"Added {name} successfully to database."

def u_update(ID, pc):
    """ Update a record in database """
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute(f"""UPDATE users SET photocard_list = '{pc}'
                WHERE user_id = '{ID}'
        """)
    connection.commit()
    connection.close()

def pc_getall():
    """ Get everything from database """
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute("SELECT * FROM photocards")
    all = c.fetchall()
    connection.commit()
    connection.close()
    return all


def u_insert(ID):
    """ Insert new user when !regiser command gets called """
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute(f"""INSERT INTO users VALUES ('{ID}','None None')""")
    connection.commit()
    connection.close()

def u_getall():
    """ Get everything from users databases table """
    connection = sqlite3.connect('data.db')
    c = connection.cursor()
    c.execute("SELECT * FROM users")
    all = c.fetchall()
    connection.commit()
    connection.close()
    return all