"""
Author: Sovunh Voeu
Created: 3/7/2025
"""
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QComboBox,
    QApplication,
    QMessageBox
    )
# import sys
import sqlite3
from ai import prompts

"""
Plans For Sprint 4:
Add more info to tell the user what does what.

Errors:
The errors I am running into so far is that it closes without saving.
"""

def connect_db():
    conn = sqlite3.connect('jobs.db')
    return conn

class UserSelectionWindow(QWidget):
    def __init__(self, db_path = "jobs.db"):
        super().__init__()
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select User Profiles")
        self.setGeometry(100, 500, 400, 300)

        layout = QVBoxLayout()

        self.user_drop_down = QComboBox()
        self.insert_users()
        self.user_drop_down.currentIndexChanged.connect(self.show_user_info)

        self.user_info = QLabel("To see user information, select a user from the drop down.")

        self.select_button = QPushButton("Confirm Selected User to generate an AI Resume and Cover Letter")
        self.select_button.clicked.connect(self.user_selected)

        layout.addWidget(self.user_drop_down)
        layout.addWidget(self.user_info)
        layout.addWidget(self.select_button)


        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        self.job_combo_box = QComboBox()
        self.job_combo_box.addItem("Select a job", None)  # Default option
        self.cursor.execute("SELECT id, title FROM rapidResults")
        jobs = self.cursor.fetchall()
        for job in jobs:
            self.job_combo_box.addItem(job[1], job[0])  # job[1] = title, job[0] = ID
        layout.addWidget(self.job_combo_box)


        self.cursor.execute("SELECT id, name, email, phone FROM user_data")  # Example query
        user_data = self.cursor.fetchall()
        self.user_combo_box = QComboBox()
        self.user_combo_box.addItem("Select a user")  # Add default instruction
        for user in user_data:
            self.user_combo_box.addItem(f"{user[1]} - {user[2]}", user[0])
        layout.addWidget(self.user_combo_box)


        self.setLayout(layout)

    def insert_users (self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_data")
        self.users = cursor.fetchall()

        conn.close()

        for user in self.users:
            self.user_drop_down.addItem(user[1], user[0])

    def show_user_info(self):
        user_id = self.user_drop_down.currentData()
        if user_id is None:
            self.user_info.setText("No user selected.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            name, email, phone, github, linkedin, projects, classes, other = user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8]
            self.user_info.setText(
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Github: {github}\n"
                f"LinkedIn: {linkedin}\n"
                f"Projects: {projects}\n"
                f"Classes: {classes}\n"
                f"Other: {other}"
            )

    #THIS IS WHERE YOU WILL TIE THE AI.py to the program
    def user_selected(self):
        # Get selected job and user ID from dropdowns
        selected_job_id = self.job_combo_box.currentData()
        selected_user_id = self.user_combo_box.currentData()

        # Ensure selections are valid
        if selected_job_id is None or selected_user_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select both a job and a user.")
            return

        # Establish database connection
        db_connection = sqlite3.connect("jobs.db")

        # Pass selected IDs to AI processing function
        prompts(job_id=selected_job_id, user_id=selected_user_id, db_connection=db_connection)

        db_connection.close()
