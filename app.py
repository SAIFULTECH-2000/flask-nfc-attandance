from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(50), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # e.g., "Present" or "Absent"
    student = db.relationship('Student', backref=db.backref('attendances', lazy=True))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['message'] = 'You are successfully logged in'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/registerstudent', methods=['GET', 'POST'])
def register_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        new_student = Student(name=name, age=age, grade=grade)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Student Registered Successfully!', 'success')
            return redirect(url_for('list_students'))
        except:
            db.session.rollback()
            flash('Error in registration!', 'danger')
            return render_template('register_student.html')
    return render_template('register_student.html')

@app.route('/liststudents')
def list_students():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    students = Student.query.all()
    return render_template('list_students.html', students=students)

@app.route('/studentattendance', methods=['GET', 'POST'])
def student_attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        student_id = request.form['student_id']
        status = request.form['status']
        attendance_date = request.form['date']
        new_attendance = Attendance(student_id=student_id, date=attendance_date, status=status)
        try:
            db.session.add(new_attendance)
            db.session.commit()
            flash('Attendance logged successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error logging attendance', 'danger')
    students = Student.query.all()
    return render_template('student_attendance.html', students=students)

@app.route('/viewattendance', methods=['GET', 'POST'])
def view_attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    query = Attendance.query
    if start_date and end_date:
        query = query.filter(Attendance.date.between(start_date, end_date))

    attendance_logs = query.all()

    if request.method == 'POST' and 'export' in request.form:
        data = [{
            'Student Name': log.student.name,
            'Date': log.date,
            'Status': log.status
        } for log in attendance_logs]

        df = pd.DataFrame(data)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Attendance')
        writer.save()
        output.seek(0)

        return send_file(output, attachment_filename='attendance_logs.xlsx', as_attachment=True)

    return render_template('view_attendance.html', attendance_logs=attendance_logs)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/profile/<int:student_id>')
def profile(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return "Student not found", 404
    return render_template('profile.html', student=student)
def save_attendance():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = data.get('name')
    class_name = data.get('class')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    time = datetime.strptime(data.get('time'), '%H:%M:%S').time()

    student = Student.query.filter_by(name=name, grade=class_name).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    new_attendance = Attendance(student_id=student.id, date=date, time=time, status='Present')
    try:
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'message': 'Attendance saved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
