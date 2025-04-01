from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')  # Открываем HTML
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

@app.route("/")
def home():
    return "Hello, world!"  # Проверь, есть ли что-то здесь

if __name__ == "__main__":
    app.run()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Reģistrācija veiksmīga!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user'] = user.username
        return jsonify({"message": "Pieslēgšanās veiksmīga!", "role": user.role})
    return jsonify({"message": "Nepareizs lietotājvārds vai parole!"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Atslēgšanās veiksmīga!"})

@app.route('/facilities')
def get_facilities():
    facilities = Facility.query.all()
    return jsonify([{ "id": f.id, "name": f.name, "capacity": f.capacity } for f in facilities])

@app.route('/book', methods=['POST'])
def book_facility():
    data = request.json
    new_booking = Booking(facility_id=data['facility_id'], date=data['date'], time=data['time'])
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Rezervācija veiksmīga!"})

@app.route('/bookings')
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([{ "facility_id": b.facility_id, "date": b.date, "time": b.time } for b in bookings])

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)
    
