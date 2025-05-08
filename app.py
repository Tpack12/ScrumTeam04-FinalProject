from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'deb8d75a806dee95d9d659cbf853c8ea086bf69f82912910'

db = SQLAlchemy(app)

class reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passengerName = db.Column(db.String(100), nullable=False)
    seatRow = db.Column(db.Integer, nullable=False)
    seatColumn = db.Column(db.Integer, nullable=False)
    eTicketNumber = db.Column(db.String(50), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

class admins(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        row = int(request.form['seat_row'])
        col = int(request.form['seat_column'])

        existing = reservations.query.filter_by(seatRow=row, seatColumn=col).first()
        if existing:
            return render_template('reserve.html', error="Seat already reserved.")

        full_name = f"{fname} {lname}"
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        new_res = reservations(passengerName=full_name, seatRow=row, seatColumn=col, eTicketNumber=code)
        db.session.add(new_res)
        db.session.commit()
        return render_template('reserve.html', reservation_code=code)

    return render_template('reserve.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        
        print(f"Attempting login with username: '{user}' and password: '{pw}'")
        
        admin = admins.query.filter_by(username=user).first()
        
        if admin:
            print(f"Found admin: {admin.username}, password: {admin.password}")
            
            if admin.password == pw:
                session['admin'] = user
                print(f"Login successful for admin: {user}")
                return redirect(url_for('admin_dashboard'))
            else:
                print("Incorrect password for admin.")
                return render_template('admin_login.html', error="Invalid credentials.")
        else:
            print("Admin not found in the database.")
            return render_template('admin_login.html', error="Invalid credentials.")
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    reservations = reservations.query.all()
    cost_matrix = get_cost_matrix()

    reserved_seats = {(r.seatRow, r.seatColumn) for r in reservations}
    
    total_sales = sum(
        cost_matrix[r.seatRow][r.seatColumn] for r in reservations
    )

    return render_template('admin_dashboard.html',
                           reservations=reservations,
                           reserved_seats=reserved_seats,
                           total_sales=total_sales)

@app.route('/delete/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    reservation = reservations.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5010)
