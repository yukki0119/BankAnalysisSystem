from flask import Flask, render_template, request, redirect, url_for, session,Markup
import neo4jQuery as neo4jDB
import mysqlQuery as mysqlDB
import mongoQuery as mongoDB
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
account_id = 9307

# configuration for mysql
app.config['MYSQL_USER']= 'adbfinal'
app.config['MYSQL_PASSWORD']='111111'
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_DB']='adb_final'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['MYSQL_PORT']= 8889
mysql = MySQL(app)

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
            return redirect(url_for('admin_query'))


@app.route('/customer')
def customer_query():
    return render_template('customer_query.html')


@app.route('/admin')
def admin_query():
    district = neo4jDB.get_district()
    region = neo4jDB.get_region()
    # print(district)
    return render_template('admin_query.html', district=district, region=region)


@app.route('/customer/search', methods=['POST'])
def customer_search():
    year = int(request.form.get('year'))
    month = int(request.form.get('month'))
    searchType = int(request.form.get('searchType'))
    db = int(request.form.get('db'))
    account = str(session["account_id"])
    print(db, year, month, searchType, account)
    if db == 1:
        account = int (account)  # In mongoDB, account_id -> int. So data conversion needed here
        print ('db is 1')
        # res = neo4jDB.customer_query(year, month, searchType, account)
        # print('res is :', res)
        if searchType == 1:  # Number of transactions
            res = mongoDB.get_user_trans_amount_mongo (account, month, year)  # res: A aggregated number
            print (res)
            return render_template ('customer_query.html', account=account, trans_count=res)
        if searchType == 2:  # Transactions information
            print ('type=2')
            res = mongoDB.get_user_trans_info_mongo (account, month, year)  # res: A list
            print (res)
            return render_template ('customer_query.html', account=account, trans_info=res)
    if db == 2: # 1:mongodb, 2:neo4j, 3:mysql
        print('db is 2')
        res = neo4jDB.customer_query(year, month, searchType, account)
        print('res is :', res)
        if searchType == 1: # num of trans
            return render_template('customer_query.html', account=account, trans_count=res)
        if searchType == 2:
            return render_template('customer_query.html', account=account, trans_info=res)
    if db == 3:
        if searchType == 1:
            res = mysqlDB.sqlcustomer_query1(year, month, searchType, account, mysql)
            print(res)
            return render_template('customer_query.html', account=account, trans_count=res)
        if searchType == 2:
            res = mysqlDB.sqlcustomer_query2(year, month, searchType, account,mysql)
            print('search type = 2: ',res)
            return render_template('customer_query.html', account=account, trans_info=res)


@app.route('/admin/search', methods=['POST'])
def admin_search():
    req = request.form
    db = int(req.get('db'))
    query_id = int(req.get('queryID'))
    district = neo4jDB.get_district()
    region = neo4jDB.get_region ()
    print(db)
    if db == 1: # neo4j
        res = neo4jDB.admin_query(req)
        print('res in app.py', res)
        return render_template('admin_query.html', query_id=query_id, req=req, res=res, district=district, region=region)
    if db == 2: # mysql
        res = mysqlDB.sqladmin_query(req,mysql)
        print('res in app.py', res)
        return render_template('admin_query.html', query_id=query_id, req=req, res=res, district=district, region=region)
    if db == 3: # MongoDB -> 3; In customer page: MongoDB -> 1
        print(db)
        if query_id == 1:
            #  year = str(year) # year month 是数字的情况
            year = int(req.get('year'))
            month = int(req.get('month'))
            district_id = req['dist']
            res = mongoDB.get_district_trans_amount_mongo(district_id, month, year)
            print(res)
            return render_template("admin_query.html", query_id=query_id, res=res, district=district, region=region, req=req)
        elif query_id == 2:
            account = int(req.get('account_id'))  # account_id
            res = mongoDB.get_admin_trans_amount_mongo(account)
            print(res)
            return render_template("admin_query.html", query_id=query_id, res=res, district=district, region=region, req=req)
        elif query_id == 3:
            status = req['status']
            age_range = int(req['age_range'])
            if age_range == 1:
                age_range = "0-25"
            elif age_range == 2:
                age_range = "26-50"
            elif age_range == 3:
                age_range = "51-75"
            else: age_range = "75+"
            res = mongoDB.get_user_loan_info_mongo(age_range, status)
            print(res)
            return render_template("admin_query.html", query_id=query_id, res=res, district=district, region=region, req=req)
        elif query_id == 4:
            reg = req['region']
            res = mongoDB.get_region_trans_amount_mongo(reg)
            print(res)
            return render_template("admin_query.html", query_id=query_id, res=res, district=district, region=region, req=req)
        elif query_id == 5:
            dist_id = int(req['dist'])
            gender = req['gender']
            res = mongoDB.get_district_gender_amount_mongo(dist_id, gender)
            return render_template("admin_query.html", query_id=query_id, res=res, district=district, region=region, req=req)
        else:
            reg = req['region']
            res = mongoDB.get_user_region_amount_mongo(reg)
            print(res)
            return render_template("admin_query.html", query_id=query_id, res=res, district=district, region=region, req=req)
    return render_template('admin_query.html', district=district, region=region)


@app.route('/bar')
def show_bar():
    bar_labels = ['A', 'B', 'C', 'D']
    values_range_1 = neo4jDB.get_customer_num(1)
    values_range_2 = neo4jDB.get_customer_num(2)
    values_range_3 = neo4jDB.get_customer_num(3)
    #values_range_4 = neo4jDB.get_customer_num(4)
    # bar_values = values
    return render_template('barchart.html', para=bar_labels, values_range_1=values_range_1, values_range_2=values_range_2, values_range_3=values_range_3)


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


