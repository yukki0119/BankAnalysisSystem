from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# app._static_folder = './static'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = str(request.form.get('Email'))
        passwd = str(request.form.get('Password'))

        # user = confi_set.find_one({'ID': id, 'passwd': str(passwd)})
        print('email is: ',email)
        if email == 'yxmtest@yxm.com' and passwd == '123456':
            session['client_id'] = 2
            session['logged_in'] = True
            print(session)
            return render_template('index.html')
        return render_template('login.html')
        # return redirect(url_for('home'))


