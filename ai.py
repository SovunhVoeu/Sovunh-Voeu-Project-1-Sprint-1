"""
Author: Sovunh Voeu
Created: 1/29/2025
Last Edited: 3/4/2025
"""
import sqlite3
import json
import pypandoc
import google.generativeai as genai
from pathlib import Path


"""
Plans For Sprint 4:
Create the button for the resume in the secondWindow.py
Program the actual AI prompt in the ai.py file

Split this .py file into multiple functions for easier readability and debugging.
the api_model_and_response function is gonna be left alone since most of the function requirements is there.
Definitely gonna need seperate functions regarding the markdowns and requests though.

Errors:
The errors I am running into so far is that the resume and cover letter are not being generated.
It may be the main() function that is causing the issue.
"""


def gemini_setup():
    file_path = Path("YOUR_API_KEY.txt")
    api = file_path.read_text().strip()
    genai.configure(api_key=api)
    return genai.GenerativeModel("gemini-1.5-flash")


def retrieve_job_and_user_data(job_id, user_id, db_connection):
    cursor = db_connection.cursor()

    cursor.execute("SELECT title, description FROM rapidResults WHERE id = ?", (str(job_id),))
    job = cursor.fetchone()

    if job is None:
        raise ValueError(f"Job with ID {job_id} not found in the database.")

    job_title, job_description = job

    cursor.execute("SELECT name, email, phone, github, linkedin, "
                   "projects, classes, other FROM user_data WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    user_data = {
        "name": user[0], "email": user[1], "phone": user[2], "github": user[3], "linkedin": user[4],
        "projects": user[5], "classes": user[6], "other": user[7]
    }

    return {"title": job_title, "description": job_description}, user_data


def generate_markdown(model, prompt):
    response = model.generate_content(prompt)
    return response.text.strip()


def save_markdown(content, file_name):
    try:
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(content)
            print(f"The file has been successfully written to {file_name}")
    except Exception as e:
        print(f"An error occured: {e}")


def convert_markdown_to_pdf(md_file, pdf_file):
    try:
        pypandoc.convert_file(md_file, to="pdf", outputfile=pdf_file)
        print(f"The file has been successfully converted to {pdf_file}")
    except Exception as e:
        print(f"An error occured: {e}")


# LEAVE THIS FUNCTION ALONE FOR NOW AND JUST REPROGRAM EVERYTHING ELSE
def prompts(job_id, user_id, db_connection):
    model = gemini_setup()

    job, user = retrieve_job_and_user_data(job_id, user_id, db_connection)

    cover_letter_prompt = (
        f"Write a professional cover letter in markdown format for the job: {job['title']}.\n"
        f"Job Description:\n{job['description']}\n\n"
        f"Applicant Details:\n{json.dumps(user, indent=2)}"
    )

    resume_prompt = (
        f"Write a resume in markdown format tailored for the job: {job['title']}.\n"
        f"Job Description:\n{job['description']}\n\n"
        f"Applicant Details:\n{json.dumps(user, indent=2)}"
    )

    cover_letter_md = generate_markdown(model, cover_letter_prompt)
    resume_md = generate_markdown(model, resume_prompt)

    save_markdown(cover_letter_md, 'cover_letter.md')
    save_markdown(resume_md, "my_resume.md")

    convert_markdown_to_pdf('cover_letter.md', 'cover_letter.pdf')
    convert_markdown_to_pdf("my_resume.md", "my_resume.pdf")

    print("Cover letter and resume successfully created and converted to PDF.")


def get_latest_job_id(db_connection, selected_job_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT id FROM rapidResults WHERE id = ?", (selected_job_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def get_latest_user_id(db_connection, selected_user_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT id FROM user_data WHERE id = ?", (selected_user_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def example_main(selected_job_id, selected_user_id):
    db_connection = sqlite3.connect("jobs.db")

    job_id = get_latest_job_id(db_connection, selected_job_id)
    user_id = get_latest_user_id(db_connection, selected_user_id)

    prompts(job_id=job_id, user_id=user_id, db_connection=db_connection)
    db_connection.close()
