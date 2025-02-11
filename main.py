"""

Author: Sovunh Voeu
Date: 1/29/2025

"""

import google.generativeai as genai
from pathlib import Path


def api_model_and_response():
    file_path = Path('YOUR_API_KEY.txt')
    api = file_path.read_text()

    genai.configure(api_key=api)
    model = genai.GenerativeModel("gemini-1.5-flash")

    job_description = ('The job description of the job I want to apply for: '
                       'Links Technology Solutions is looking for a Software Developer to join their team!'
                       '\n\nThis role requires a strong foundation in .NET development with a focus on building '
                       'and maintaining robust applications within an Agile team environment.'
                       '\n\nYour Day-to-Day\n\u2022 Design, develop, test, '
                       'and maintain multitier applications using Microsoft .NET and related technologies\n\u2022 '
                       'Participate in daily standups\n\nPosition Requirements\n\u2022'
                       ' Microsoft .NET Framework/.NET Core\n\u2022 C#\n\u2022 WinForms\n\u2022 SQL\n\u2022 '
                       'Object-oriented design patterns\n\u2022 Source control (Git/SVN)\n\u2022 '
                       'HTML/CSS\n\u2022 IIS\n\u2022 LLBLGen (or other ORM)\n\u2022 '
                       'NSIS (or other Windows installers)\n\u2022 Visual Studio\n\u2022'
                       '3-5 / 5-7 years minimum in Agile Development environment\n\nOther Valuable Experience\n\u2022'
                       'Cloud platforms (AWS/GCP)\n\u2022 Multithreaded programming\n\u2022 Aspose\n\u2022 CI/CD\n\n')

    self_description = ('I am an unemployed university student who is 22 years old.'
                        'I am going to receive my Bachelors degree in Computer Science.'
                        'I have an extensive background in AI and programming.'
                        'I have a certificate in advanced Java programming and '
                        'I know various languages such as Python, C#, and javascript.'
                        'I am a team player, outgoing, willing to go the extra mile, and can handle a busy work flow.')

    # Deliver the intended prompt to the AI here
    user_input = input("Deliver the intended prompt to the AI here: "
                        "(Ex: Hello, can you create a resume for me using these descriptions?) \n")

    response = model.generate_content(user_input + self_description + job_description)
    print("\n" + response.text)

    # Create a write to file for the resume in .md or MARKDOWN
    file_name = "my_resume.md"

    try:
        with open(file_name, 'w') as file:
            file.write(str(response.text))
            print(f"The file has been successfully written to {file_name}")
    except Exception as e:
        print(f"An error occured: {e}")


if __name__ == '__main__':
    api_model_and_response()
