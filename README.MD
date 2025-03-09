Project 1 SPRINT 4:

Description:
This project opens a gui that allows the user to view 2 lists of jobs that can be selected to see the details that are
gathered from the jobs.db. There is also a second window that appears once the Open User Input Data button is clicked,
this window will all for the user information to be stored within the jobs.db under a table called user_data. At the
bottom of this page there is a button that will open a third window that will allow the user to input a 
job and user dropdown where you can click confirm job to generate a ai made resume and cover letter. The tests are in
test_ai.py my test functions are test_gemini_api_response, test_prompt_contains_job_and_user_data, and 
test_retrieve_job_user_data. The test_gemini_api_response tests the response from the gemini api. The 
test_prompt_contains_job_and_user_data tests if my prompt contains both the job and user description. While my
test_retrieve_job_user_data tests if the job and user data is retrieved from the database.

Files Used or created:
test_ai.py, main.py, ai.py, mainWindow.py, secondWindow.py, thirdWindow.py, and jobs.db

How to run this code:
To run this code open the main.py file and run it. The gui will open and inform you what the program does.

Libraries used: 
unittest.mock, json, sqlite3, pathlib, pypandoc, os, google.generativeai, sys, pytest and PyQt6


Project 1 SPRINT 3:

Description:
This project opens a gui that allows the user to view 2 lists of jobs that can be selected to see the details that are
gathered from the jobs.db. There is also a second window that appears once the Open User Input Data button is clicked,
this window will all for the user information to be stored within the jobs.db under a table called user_data. There is
also a pytest created called test_gui.py under the tests folder directory. In order to see what the test_gui.py spat out
you will need to open the user_data table in the jobs.db under the test dir since it operates separately. The functions
within the test_gui.py that are intended to cover the cases are test_job_select_return, test_job_select_return2, and
test_user_data_entry_save. The test_job_select_return cover the rapidResults table, while the test_job_select_return2
covers the rapid_jobs2 table. The test_user_data_entry_save is one long function that covers all the user input data.

Files Used or created:
test_gui.py, gui.py, and jobs.db

How to run this code:
To run this code you can just run the gui.py file regularly or click the run next to if __name__ == "__main__":.
There are more details within the gui that allows for a better navigation of the program itself.

Libraries used: 
sys, pytest and PyQt6


Project 1 SPRINT 2:

Description:
This project reads 2 JSON files that are different from one another and creates a database where data is inserted into.
The main program for this project is the db.py which holds the majority of the code. There is a tests directory that 
contains a test_data.py that runs 4 tests that uses automated testing to test the grabbing the data from a file that
does the creation and insertion of a database. You can also find test files that were produced from running the program.
If you want to get rid of them uncomment the lines of code that have if os.path.exists(test_file): os.remove(test_file) 
and the import os at the top of the file. After just rerun the program so that it may go away.

How to run this code:
You can run this code the standard way by either clicking the green arrow next to if __name__ == '__main__': or on main
itself.

Why I decided to use two separate tables:
I had decided to use two separate tables because there were too many contrasting key values and the rapidResults table
had a lot of content within the table itself.

Libraries used: 
os, sqlite3, json, and pytest


Project 1 SPRINT 1:

Before you run this program paste your API key into the YOUR_API_KEY.txt
(WARNING: MAKE SURE THAT YOU ONLY HAVE ONE LINE IN THE .TXT FOR THE API. DO NOT HAVE AN EXTRA LINE OR IT WILL NOT RUN)
The program will read your .txt file and allow you to use the AI/LLM.
In order to get started you must input the question into the prompt code line since the descriptions are hard coded.
Example: Hello, can you create a resume for me using these descriptions?

I chose this AI/LLM because it looked the simplest to me. I had no errors adding the
codes to my program and developing my program further.

Libraries used: 
os, Path, google.generativeai

The changes that I have made to settle over the prompt given over the others is I gave a more indepth job description
so that the format would look more professional.

The job description I had chose to go with was: Application Developer from the JSON
"The job description of the job I want to apply for:
Links Technology Solutions is looking for a Software Developer to join their team!
This role requires a strong foundation in .NET development with a focus on building
and maintaining robust applications within an Agile team environment.
Your Day-to-Day Design, develop, test,
and maintain multitier applications using Microsoft .NET and related technologies
Participate in daily standups Position Requirements
Microsoft .NET Framework/.NET Core C# WinForms SQL
Object-oriented design patterns Source control (Git/SVN)
HTML/CSS IIS LLBLGen (or other ORM)
'NSIS (or other Windows installers) Visual Studio
3-5 / 5-7 years minimum in Agile Development environment Other Valuable Experience
Cloud platforms (AWS/GCP) Multithreaded programming Aspose CI/CD"

The personal description I gave was:
"I am an unemployed university student who is 22 years old.
I am going to receive my Bachelors degree in Computer Science.
I have an extensive background in AI and programming.
I have a certificate in advanced Java programming and I know various languages such as Python, C#, and javascript.
I am a team player, outgoing, willing to go the extra mile, and can handle a busy work flow."
