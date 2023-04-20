import os, sys
import sqlite3
from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask_cors import CORS

app = Flask(__name__)
app.db = "sqlitedb.db"
CORS(app)

if(sys.argv[1] == 'host'):
	ACC_NO = 11007818
	USR_NAME = 'Victim'
	PORT = 3000
	
if(sys.argv[1] == 'attacker'):
	ACC_NO = 11007816
	USR_NAME = 'Hacker'
	PORT = 8080
	
# Method to connect to database
def get_dbconn():
    return sqlite3.connect(app.db)
    
#get login user's bank balance
def get_balance():
	g.db = get_dbconn()
	query = g.db.execute("SELECT SUM(amount) FROM wallets WHERE receiver=?", [ACC_NO])
	balance = query.fetchone()[0]
	query = g.db.execute("SELECT SUM(amount) FROM wallets WHERE sender=?", [ACC_NO])
	sent = query.fetchone()[0]
	balance -= sent if sent else 0
	g.db.close()
	return balance
	
# Bind account number and balance of the active user
@app.context_processor
def bind_balancedetails():
    balance = get_balance()
    return dict(
        balance=balance,
        account_no=ACC_NO,
        user_name=USR_NAME,
    )

# Default index page
@app.route('/')
def index():
    g.db = get_dbconn()
    query = g.db.execute(
        "SELECT * FROM wallets WHERE sender=? OR receiver=?",
        (ACC_NO, ACC_NO))
    records = query.fetchall()
    results = []
    total_deposit=0
    total_withdraw=0
    for row in records:
        is_sender = int(row[0]) == int(ACC_NO)
        if is_sender:
        	total_withdraw+=row[2]
        else:
        	total_deposit+=row[2]
        results.append(
            dict(
                account=(row[1] if is_sender else row[0]),
                amount_deposit=(0) if is_sender else row[2],
                amount_withdraw= (row[2]) if is_sender else 0,
                reason=row[3],
            ))
    g.db.close()
    return render_template('index.html', transactions=results,total_withdraw=total_withdraw,total_deposit=total_deposit)

# Method to transfer Wallet amount
@app.route('/transfer', methods=['POST', 'GET'])
def transfer():
    if request.method == 'POST':
        to_account, amount, reason = (request.form['account'],
        			request.form['amount'],
                                request.form['reason'])
        g.db = get_dbconn()
        g.db.execute(
            "INSERT INTO wallets (sender, receiver, amount, reason) VALUES (?, ?, ?, ?)",
            [ACC_NO, to_account, amount, reason])
        g.db.commit()
        g.db.close()
        return render_template('wallet_transfer.html', msg="Transfer successful")

    return render_template('wallet_transfer.html')

# Method to create database and insert values
if __name__ == "__main__":
    if not os.path.exists(app.db):
        conn = sqlite3.connect(app.db)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE wallets(sender TEXT, receiver TEXT, amount INT, reason TEXT)'
        )
        c.execute(
            'INSERT INTO wallets VALUES("11007816", "11007817", 1000, "Shopping")')
        c.execute(
            'INSERT INTO wallets VALUES("11007815", "11007818", 10000, "College fees")'
        )
        c.execute(
            'INSERT INTO wallets VALUES("11007817", "11007818", 100, "Grocery")'
        )
        c.execute(
            'INSERT INTO wallets VALUES("11007820", "11007816", 20, "Recharge")'
        )
        conn.commit()
        conn.close()

    app.run(host='0.0.0.0', port=PORT)
