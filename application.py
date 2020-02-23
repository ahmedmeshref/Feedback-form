from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_email
app = Flask(__name__)

ENV = 'dev'

# we are in the development phase
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:250787388219@' \
                                            'localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# create a model
class Feedback(db.Model):
    __tablename__ = "Feedback"
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text())

    def __init__(self, customer, email, dealer, rating, comment):
        self.customer = customer
        self.email = email
        self.dealer = dealer
        self.rating = rating
        self.comment = comment


@app.route('/')
def hello_world():
    return render_template("index.html", message='')


@app.route("/submit", methods=['POST', 'GET'])
def submit():
    if request.method == "POST":
        customer = request.form['cname']
        email = request.form['email']
        dealer = request.form['dname']
        rating = request.form['rate']
        comment = request.form['message']
        if (not customer) or (not dealer) or (not email):
            return render_template("index.html", message="Please enter "
                                                         "required fields")
        if db.session.query(Feedback).filter(Feedback.email == email).count() == 0:
            data = Feedback(customer, email, dealer, rating, comment)
            db.session.add(data)
            db.session.commit()
            send_email(customer, dealer, rating, comment, email)
            return render_template("success.html")
        return render_template("index.html", message="You have already submitted")
    else:
        redirect(url_for('hello_world'), message='')


if __name__ == "__main__":
    app.run()
