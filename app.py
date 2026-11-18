from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

# Create Flask application
app = Flask(__name__)

app.config["SECRET_KEY"] = "green-valley-secret-2026"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tuition.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)


# Batch table
class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    total_fee = db.Column(db.Numeric(10, 2), nullable=False)

    batch_id = db.Column(
        db.Integer,
        db.ForeignKey("batch.id"),
        nullable=False
    )

    batch = db.relationship("Batch", backref="students")


# Payment table
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )


# Create database tables
with app.app_context():
    db.create_all()

# Student Management

@app.route("/students")
def students():
    all_students = Student.query.all()
    return render_template(
        "students.html",
        students=all_students
    )


# Add students
@app.route("/add_student", methods=["POST"])
def add_student():
    from flask import request, redirect, url_for, flash

    # Check duplicate email
    email = request.form["email"].strip().lower()

    existing_email = Student.query.filter_by(
        email=email
    ).first()

    if existing_email:
        flash("Email already exists! Please use another email.", "error")
        return redirect(url_for("students"))

    # Check batch capacity
    batch_id = int(request.form["batch_id"])

    batch = Batch.query.get(batch_id)

    if not batch:
        flash("Please select a valid batch.", "error")
        return redirect(url_for("students"))

    student_count = Student.query.filter_by(
        batch_id=batch_id
    ).count()

    if student_count >= 20:
        flash(
            "This batch is full! Maximum capacity is 20 students.",
            "error"
        )
        return redirect(url_for("students"))

    # Create new student
    new_student = Student(
        name=request.form["name"],
        email=email,
        phone=request.form["phone"],
        total_fee=Decimal(request.form["total_fee"]),
        batch_id=batch_id
    )

    db.session.add(new_student)
    db.session.commit()

    flash("Student added successfully!", "success")

    return redirect(url_for("students"))


# Fee Payment Management
@app.route("/payments", methods=["GET", "POST"])
def payments():

    students = Student.query.all()

    if request.method == "POST":

        student_id = request.form.get("student_id", type=int)
        amount_text = request.form.get("amount", "").strip()

        student = Student.query.get(student_id)

        if not student:
            flash("Please select a valid student.", "error")
            return redirect(url_for("payments"))

        try:
            amount = Decimal(amount_text)

            if amount <= 0:
                flash("Payment must be greater than zero.", "error")
                return redirect(url_for("payments"))

            total_paid = db.session.query(
                db.func.coalesce(db.func.sum(Payment.amount), 0)
            ).filter_by(student_id=student.id).scalar()

            balance = Decimal(str(student.total_fee)) - Decimal(str(total_paid))

            if amount > balance:
                flash("Payment exceeds the remaining balance.", "error")
                return redirect(url_for("payments"))

            new_payment = Payment(
                amount=amount,
                student_id=student.id
            )

            db.session.add(new_payment)
            db.session.commit()

            flash("Payment recorded successfully!", "success")

            return redirect(url_for("payments"))

        except Exception:
            db.session.rollback()
            flash("Invalid payment amount.", "error")
            return redirect(url_for("payments"))

    
    payment_records = Payment.query.order_by(
        Payment.payment_date.desc()
    ).all()

    # Calculate fee summary for every student
    fee_summaries = {}

    for student in students:
        total_paid = db.session.query(
            db.func.coalesce(db.func.sum(Payment.amount), 0)
        ).filter(
            Payment.student_id == student.id
        ).scalar()

        total_fee = Decimal(str(student.total_fee))
        paid_amount = Decimal(str(total_paid))
        balance = total_fee - paid_amount

        if balance <= 0:
            status = "Paid"
        elif paid_amount > 0:
            status = "Partially Paid"
        else:
            status = "Unpaid"

        fee_summaries[student.id] = {
            "total_fee": total_fee,
            "paid_amount": paid_amount,
            "balance": balance,
            "status": status
        }

    return render_template(
        "payments.html",
        students=students,
        payment_records=payment_records,
        fee_summaries=fee_summaries
    )



# Edit Student
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    from flask import request, redirect, url_for, render_template, flash

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        existing_email = Student.query.filter(
            Student.email == request.form["email"],
            Student.id != id
        ).first()

        if existing_email:
            flash("Email already exists! Please use another email.", "error")
            return redirect(url_for("edit_student", id=id))

        student.name = request.form["name"]
        student.email = request.form["email"]
        student.phone = request.form["phone"]
        student.total_fee = Decimal(request.form["total_fee"])
        student.batch_id = int(request.form["batch_id"])

        db.session.commit()

        flash("Student updated successfully!", "success")
        return redirect(url_for("students"))

    return render_template("edit_student.html", student=student)



# Delete Student
@app.route("/delete_student/<int:id>", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)

   
    # Calculate total payments made by the student
    total_paid = db.session.query(
        db.func.coalesce(db.func.sum(Payment.amount), 0)
    ).filter(
        Payment.student_id == student.id
    ).scalar()

    # Calculate remaining balance
    total_fee = Decimal(str(student.total_fee))
    paid_amount = Decimal(str(total_paid))
    balance = total_fee - paid_amount

    # Prevent deletion if pending balance exists
    if balance > 0:
        flash(
            f"Cannot delete student! Pending balance is ₹{balance}. Please clear the fees first.",
            "error"
        )
        return redirect(url_for("students"))

    # Delete payment records
    Payment.query.filter_by(student_id=student.id).delete()

    # Delete student
    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "success")
    return redirect(url_for("students"))


# Run application
@app.route("/")
def home():
    total_students = Student.query.count()
    total_batches = Batch.query.count()

    total_fees = db.session.query(
        db.func.coalesce(db.func.sum(Student.total_fee), 0)
    ).scalar()

    total_payments = db.session.query(
        db.func.coalesce(db.func.sum(Payment.amount), 0)
    ).scalar()

    pending_fees = total_fees - total_payments

    return render_template(
        "index.html",
        total_students=total_students,
        total_batches=total_batches,
        total_fees=total_fees,
        total_payments=total_payments,
        pending_fees=pending_fees
    )\
    
if __name__ == "__main__":
   app.run(debug=True)
    