from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def index():
    render_template('index.html')


@app.route('/login')
def login():
    render_template('signin.html')


@app.route('/signup')
def signup():
    render_template('signup1.html')


@app.route('/benefits')
def benefits():
    render_template('benefits.html')


@app.route('/eligible')
def eligible():
    render_template('elegible.html')


@app.route('/search')
def search():
    render_template('search.html')


@app.route('/types')
def bloodtypes():
    render_template('typeofblood.html')


if __name__ == '__main__':
    app.run()
