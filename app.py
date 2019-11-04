from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import mysql.connector

app = Flask(__name__)
app.secret_key = '2147aa348383f7cc243fbb58bd89ebe161e80d69'

db = mysql.connector.connect(host="hostname",
                             user="username",
                             passwd="password",
                             db=""
                             )
curr = db.cursor(buffered=True)


@app.route('/')
def index():
    return render_template('index.html', title='Claret')


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/validate/login', methods=['GET', 'POST'])
def validate_login():
    email = request.form.get('email_id')
    password = hashlib.sha1(request.form.get('password').encode('utf-8')).hexdigest()
    try:
        sql = "select password from user where email ='{}'".format(str(email))
        curr.execute(sql)
        db.commit()
        res = curr.fetchone()
        if res is None:
            return render_template('login.html', error='User does not exist')

        else:
            password_db = res[0]
            if password == password_db:
                sql1 = "select first_name,last_name,phone_number from user where email ='{}'".format(email)
                curr.execute(sql1)
                db.commit()
                res = curr.fetchone()
                f_name = res[0]
                l_name = res[1]
                ph = res[2]
                session['name'] = f_name + " " + l_name
                session['email'] = email
                session['ph'] = ph
                session['logged_in'] = True

                redirect(url_for('user'))
            else:
                return render_template('login.html', error='wrong password')

    except Exception as e:
        return render_template('login.html', error='error logging in.')


@app.route('/register')
def signup():
    return render_template('register.html', title='Register')


@app.route('/validate/register', methods=['GET', 'POST'])
def validate_register():
    f_name = request.form.get('first_name')
    l_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    p_number = request.form.get('phone_number')
    address = request.form.get('address')
    state = request.form.get('state')
    city = request.form.get('city')
    blood_grp = request.form.get('blood_grp')
    age = request.form.get('age')

    try:
        sql = "INSERT INTO user (first_name, last_name, email, password," \
              " phone_number, address, state, city, blood_grp, age) " \
              "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            f_name, l_name, email, password, p_number, address, state, city, blood_grp, age)
        curr.execute(sql)
        session['name'] = f_name + " " + l_name
        session['email'] = email
        session['ph'] = p_number
        session['logged_in'] = True
        db.commit()
        return redirect(url_for('user'))
    except Exception as e:
        return render_template('register.html', error='Error. Try again later.')


@app.route('/benefits')
def benefits():
    return render_template('benefits.html', title='Benefits')


@app.route('/eligible')
def eligible():
    return render_template('eligible.html', title='Eligibility')


@app.route('/search')
def search():
    return render_template('search.html', title='Search')


@app.route('/validate/search')
def search_result():
    city = request.form.get('city')
    try:
        sql = "Select first_name,last_name,blood_grp,email,phone_number,age from user where city ='{}'".format(
            str(city))
        curr.execute(sql)
        db.commit()
        res = curr.fetchall()

        return_list = []
        for result in res:
            dic = {'name': result[0] + " " + result[1],
                   'blood_grp': result[2],
                   'email': result[3],
                   'phone': result[4],
                   'age': result[5]
                   }
            return_list.append(dic)

        return render_template('search.html', title='Search', result=return_list)
    except Exception as e:
        return render_template('search.html', title='Search', error="Error. Please try again.")


@app.route('/user')
def user():
    return render_template('user.html', title='User', name=session['name'], email=session['email'], phno=session['ph'])


@app.route('/types')
def bloodtypes():
    return render_template('typeofblood.html', title='Types')


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
