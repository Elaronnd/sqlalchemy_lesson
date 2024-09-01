from flask import Flask, render_template, redirect, url_for
from models import Students
from forms import StudentForm
from database import db
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config['WTF_CSRF_ENABLED'] = False
db.init_app(app=app)


@app.before_request
def create_tables():
    if not os.path.exists("database.db"):
        db.create_all()


@app.route(rule="/")
def index():
    students = Students.query.all()
    return render_template(template_name_or_list="index.html", students=students)


@app.route(rule="/add", methods=["GET", "POST"])
def add_student():
    students_form = StudentForm()
    if students_form.validate_on_submit():
        student = Students(name=students_form.name.data, age=students_form.age.data, major=students_form.major.data)
        db.session.add(student)
        db.session.commit()
        return redirect(location=url_for(endpoint="index"))
    return render_template(template_name_or_list="add_student.html", form=students_form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Students.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.age = form.age.data
        student.major = form.major.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', form=form, student=student)


@app.route(rule="/delete/<int:id>")
def delete_student(id: int):
    student = Students.query.get_or_404(id)
    db.session.delete(instance=student)
    db.session.commit()
    return redirect(location=url_for(endpoint="index"))
