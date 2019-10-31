from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('signin.html')


@app.route('/register')
def signup():
    return render_template('signup1.html')


@app.route('/benefits')
def benefits():
    return render_template('benefits.html')


@app.route('/eligible')
def eligible():
    return render_template('elegible.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/types')
def bloodtypes():
    return render_template('typeofblood.html')


@app.route('/test')
def base():
    return render_template('temp.html')


if __name__ == '__main__':
    app.run(debug=True)
