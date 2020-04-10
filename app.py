from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# app._static_folder = './static'

@app.route('/')
def index():
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
        if email == 'yxmtest@yxm.com' and passwd == '123456':
            # session['client_id'] = 2
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
        session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/customer_query')
def customer_query():
    # remove the username from the session if it's there
    # session.pop('client_id', None)
    return render_template('userIndex.html')


def isLoggedIn():
    logged_in = False
    if session is not None:
        if session['logged_in'] is not None:
            logged_in = session['logged_in']
    print(logged_in)
    session['logged_in'] = logged_in
    return logged_in