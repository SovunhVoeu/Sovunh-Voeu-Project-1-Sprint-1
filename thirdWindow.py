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
    # QApplication,
    QMessageBox
    )
# import sys
import sqlite3
from ai import prompts


def connect_db():
    conn = sqlite3.connect('jobs.db')
    return conn


class UserSelectionWindow(QWidget):
    def __init__(self, db_path="jobs.db"):
        super().__init__()
        self.db_path = db_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select User Profiles")
        self.setGeometry(100, 500, 400, 300)

        layout = QVBoxLayout()

        self.details_label = QLabel("Select a job and user profile to generate the a AI created "
                                    "cover letter and resume. Once you click confirm wait for the files to generate, "
                                    "to check if it is finished look at the run output.")
        layout.addWidget(self.details_label)

        self.user_drop_down = QComboBox()
        self.insert_users()
        self.user_drop_down.currentIndexChanged.connect(self.show_user_info)

        self.user_info = QLabel("To see user information, select a user from the drop down.\n"
                                "To view the first user profile info, select another user profile and reselect "
                                "the first user.")

        self.select_button = QPushButton("Confirm Selected User to generate an AI Resume and Cover Letter")
        self.select_button.clicked.connect(self.user_selected)

        layout.addWidget(self.user_drop_down)
        layout.addWidget(self.user_info)
        layout.addWidget(self.select_button)

        self.conn = connect_db()
        self.cursor = self.conn.cursor()

        self.job_combo_box = QComboBox()
        self.job_combo_box.addItem("Select a job", None)
        self.cursor.execute("SELECT id, title FROM rapidResults")
        jobs = self.cursor.fetchall()
        for job in jobs:
            self.job_combo_box.addItem(job[1], job[0])
        layout.addWidget(self.job_combo_box)

        self.cursor.execute("SELECT id, name, email, phone FROM user_data")
        user_data = self.cursor.fetchall()
        self.user_combo_box = QComboBox()
        self.user_combo_box.addItem("Select a user profile")
        for user in user_data:
            self.user_combo_box.addItem(f"{user[1]} - {user[2]}", user[0])
        layout.addWidget(self.user_combo_box)

        self.setLayout(layout)

    def insert_users(self):
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
            name, email, phone, github, linkedin, projects, classes, other = (
                user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8])
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

    def user_selected(self):
        selected_job_id = self.job_combo_box.currentData()
        selected_user_id = self.user_combo_box.currentData()

        if selected_job_id is None or selected_user_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select both a job and a user.")
            return

        db_connection = sqlite3.connect("jobs.db")

        prompts(job_id=selected_job_id, user_id=selected_user_id, db_connection=db_connection)
        print("All files have been generated.")
        db_connection.close()
