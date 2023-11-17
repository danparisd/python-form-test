import tkinter as tk
from tkinter import StringVar
import requests
import json

app = tk.Tk()

# Declare question1_var globally
question1_response = StringVar()
question2_response = StringVar()

def load_questions():
    global question1_response
    try:
        # Replace 'api_url' with something like 'https://forms.office.com/formapi/api/some_guid/users/some_guid/light/runtimeFormsWithResponses(\'some_big_char_string\')?$expand=questions($expand=choices)&$top=1'
        # make sure to escape the single ticks around the big char sting
        api_url = ''
        response = requests.get(api_url)
        data = response.json()

        # Get form title and questions
        form_title = data['form']['title']
        questions = data['form']['questions']

        # Update the app title with the form title
        app.title(form_title)

        # Clear existing widgets
        for widget in app.winfo_children():
            widget.destroy()

        # Create labels for questions
        question1_label = tk.Label(app, text=questions[0]['title'])
        question1_label.pack()

        # Parse the Choices from the questionInfo string
        question_info_1 = json.loads(questions[0]['questionInfo'])
        choices = question_info_1.get('Choices', [])
        for choice in choices:
            radiobutton = tk.Radiobutton(app, text=choice.get('Description', ''), variable=question1_response, value=choice.get('Description', ''))
            radiobutton.pack()

        question2_label = tk.Label(app, text=questions[1]['title'])
        question2_label.pack()

        # Handle text input question
        question2_entry = tk.Entry(app)
        question2_entry.pack()

    except Exception as e:
        result_label.config(text=f"Error loading questions: {str(e)}")

def submit_form():
    global question1_response, question2_response
    # Access the selected choice for the multiple-choice question
    selected_choice = question1_response.get()
    print(f"Selected choice for Question 1: {selected_choice}")

    # Access the text input for the text input question
    text_input_response = question2_response.get()
    print(f"Text input response for Question 2: {text_input_response}")

    result_label.config(text="Form submitted!")

# Load questions on startup
load_questions()

# Create a button to submit the form
submit_button = tk.Button(app, text="Submit", command=submit_form)
submit_button.pack()

# Display a label for the result
result_label = tk.Label(app, text="")
result_label.pack()

# Start the main event loop
app.mainloop()
