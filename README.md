# Green Valley Tuition Centre Management System

## 1. Project Overview

The Green Valley Tuition Centre Management System is a web-based application developed using Python, Flask, SQLite, SQLAlchemy, HTML and CSS.

The application helps tuition centres manage student records, batch allocation and fee payments through a simple web interface.

## 2. Technologies Used

- Python
- Flask
- SQLite
- Flask-SQLAlchemy
- HTML
- CSS
- Jinja2

## 3. Main Features

### 3.1 Student Management (CRUD)

- Add new student records.
- View all student details.
- Edit student information.
- Delete student records.
- Prevent duplicate email addresses.

### 3.2 Batch Management

- Assign students to batches.
- Each student belongs to a batch.
- Maximum capacity is 20 students per batch.
- Prevent adding students to a full batch.
- Display a clear error message when a batch reaches its maximum capacity.

### 3.3 Fee Management

- Record student fee payments.
- View payment history.
- Calculate total fees paid.
- Calculate outstanding fee balances.
- Prevent payments that exceed the remaining balance.
- Prevent deleting students who have pending fees.

### 3.4 Dashboard

The dashboard displays:

- Total number of students.
- Total number of batches.
- Total fees.
- Total payments.
- Pending fees.

## 4. Business Rules

1. Every student must have a unique email address.
2. Each student must be assigned to a batch.
3. A batch can contain a maximum of 20 students.
4. The application must reject the 21st student in a full batch.
5. A student cannot be deleted if an outstanding fee balance exists.
6. A payment cannot exceed the student's remaining fee balance.
7. Dashboard statistics should reflect the database records.

## 5. Moving a Student to Another Batch When the Target Batch Is Full

A batch can contain a maximum of 20 students. If a student needs to move to another batch that already has 20 students, the transfer must not increase the batch capacity beyond the limit.

### Procedure

1. Identify the student who needs to be transferred.
2. Check the number of students currently assigned to the target batch.
3. If the target batch has fewer than 20 students, the student can be transferred after updating their batch assignment.
4. If the target batch already contains 20 students, do not transfer the student directly.
5. Check whether another existing batch has available seats.
6. If another batch has space, arrange a suitable transfer to that batch.
7. If the student must join the full target batch, create a new batch or move another student from the target batch to a different batch with available capacity.
8. Once a seat becomes available, update the student's batch assignment.
9. Verify the student count in both batches after the transfer.

### Example

| Batch | Students | Status |
|---|---:|---|
| Batch 1 | 20 | Full |
| Batch 2 | 15 | 5 seats available |

Suppose a student from Batch 2 wants to join Batch 1.

**Solution:**

- Move one student from Batch 1 to Batch 2.
- Batch 1 now contains 19 students.
- Batch 2 now contains 16 students.
- Transfer the requested student from Batch 2 to Batch 1.
- Batch 1 now contains 20 students.
- Batch 2 now contains 15 students.

Both batches remain within the maximum capacity.

**Important:** Always check the target batch capacity before and after transferring a student. Never allow a batch to exceed 20 students.

## 6. Installation and Setup

### Step 1: Open the project

Open the project folder in Visual Studio Code.

### Step 2: Create a virtual environment

```bash
python3 -m venv venv
```

### Step 3: Activate the virtual environment

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Flask application

```bash
python app.py
```

### Step 6: Open the application

Open a browser and visit:

http://127.0.0.1:5000

## 7. Database Details

The project uses SQLite as its database.

**Database file:** `tuition.db`

The database contains three main entities:

- **Batch:** Stores batch information.
- **Student:** Stores student details and batch assignments.
- **Payment:** Stores fee payment records linked to students.

## 8. Full Project Structure

```text
tuition-centre-management/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── tuition.db
│
├── instance/
│
├── __pycache__/
│
├── venv/
│
└── templates/
    │
    ├── index.html
    │
    ├── students.html
    │
    ├── edit_student.html
    │
    └── payments.html
```

### Project File Description

| File / Folder | Purpose |
|---|---|
| `app.py` | Main Flask application containing routes, database models and business logic. |
| `requirements.txt` | Contains the Python package dependencies. |
| `README.md` | Project documentation and setup instructions. |
| `tuition.db` | SQLite database storing application records. |
| `instance/` | Application instance folder. |
| `__pycache__/` | Stores Python-generated cache files. |
| `venv/` | Contains the Python virtual environment. |
| `templates/` | Contains HTML pages rendered by Flask. |
| `index.html` | Dashboard page. |
| `students.html` | Student listing and registration page. |
| `edit_student.html` | Student editing page. |
| `payments.html` | Fee payment and payment history page. |

## 9. Testing and Validation

The following functionalities and business rules were tested:

| Test Case | Expected Result |
|---|---|
| Add a student | Student added successfully. |
| Duplicate email | Duplicate email rejected. |
| Edit student | Student details updated. |
| Delete student with no pending fees | Student deleted. |
| Delete student with pending fees | Deletion rejected with an error message. |
| Add the 21st student to a batch | Addition rejected. |
| Record a valid payment | Payment recorded successfully. |
| Enter payment above remaining balance | Payment rejected. |
| Open dashboard | Statistics displayed from database records. |

## 10. Conclusion

The Green Valley Tuition Centre Management System simplifies student registration, batch allocation and fee tracking.

The application uses Flask and SQLite to manage records and enforce important business rules, helping the tuition centre maintain accurate student and payment information.