from flask import Flask, render_template, request, redirect, url_for, session, flash
import neo4jQuery as neo4jDB
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
account_id = 9307

# app._static_folder = './static'


@app.route('/')
def index():
    if isLoggedIn():
        print(session['logged_in'])
        return redirect(url_for('userIndex'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = str(request.form.get('Email'))
        passwd = str(request.form.get('Password'))
        # user = confi_set.find_one({'ID': id, 'passwd': str(passwd)})
        print('email is: ',email)
        if email == 'customer@bank.com' and passwd == '123456':
            session['user_type'] = 1#1 for customer
            session['account_id'] = account_id#default client_id
            session['logged_in'] = True
            print(session)
            return redirect(url_for('userIndex'))
        elif email == 'admin@bank.com' and passwd == '123456':
            session['user_type'] = 0 # 0 for admin
            session['logged_in'] = True
            print(session)
            return redirect(url_for('userIndex'))
        # flash('Email and password must match!', category='error')
        error = 'email and password must match!'
        return render_template('login.html', error=error)
        # return redirect(url_for('home'))


@app.route('/userIndex')
def userIndex():
    print('route to userIndex')
    if isLoggedIn():
        return render_template('userIndex.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    # session.pop('client_id', None)
    if isLoggedIn():
        session['logged_in'] = None
        session['user_type'] = None
        session['client_id'] = None
        session['account_id'] = None
    return redirect(url_for('index'))


@app.route('/query')
def query():
    if session is not None:
        if session['user_type'] == 1: # stand for customer
            return redirect(url_for('customer_query'))
        if session['user_type'] == 0: # stand for admin
            return redirect(url_for('admin'))


@app.route('/customer')
def customer_query():
    return render_template('customer_query.html')


@app.route('/admin')
def admin_query():
    return render_template('admin_query.html')


@app.route('/customer/search', methods=['POST'])
def customer_search():
    year = int(request.form.get('year'))
    month = int(request.form.get('month'))
    searchType = int(request.form.get('searchType'))
    db = int(request.form.get('db'))
    account = str(session["account_id"])
    print(db, year, month, searchType, account)
    if db == 2: # 1:mongodb, 2:neo4j, 3:mysql
        print('db is 2')
        res = neo4jDB.customer_query(year, month, searchType, account)
        print ('res is :', res)
        if searchType == 1: # num of trans
            return render_template('customer_query.html', account=account, trans_count=res)
        if searchType == 2:
            return render_template('customer_query.html', account=account, trans_info=res)
    # if db == 3:
    #     res = mysqlQuery.customer_query(year, month, searchType, account)
    #     if searchType == 1:


def isLoggedIn():
    logged_in = False
    if session is not None:
        print('session is : ',session)
        if not session.get('logged_in') is None:
            logged_in = session['logged_in']
            print('login status is: ', session['logged_in'])
    print(logged_in)
    session['logged_in'] = logged_in
    return logged_in


