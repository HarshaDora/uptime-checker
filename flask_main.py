from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is the home page. <a href="/front">Go to Front Page</a>'

@app.route('/front')
def front_page():
    return render_template('front.html')

@app.route('/mmmm')
def mmmm_page():
    return render_template('mmmm.html')

@app.route('/sign_in')
def sign_in_page():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)
