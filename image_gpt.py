import tkinter as tk
from tkinter import filedialog, Scrollbar
import pytesseract
import cv2
import openai

# Replace with your OpenAI API key
openai.api_key = ""
# Enter the model you want to use
model_id = "gpt-3.5-turbo"

# function to get the image from the user
def browse_image():
    filepath = filedialog.askopenfilename()
    if filepath:
        extract_text(filepath)

#extract text from the image using open cv and OCR
def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply OCR to the pre-processed image
    extracted_text = pytesseract.image_to_string(blurred)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, extracted_text)

# Gets the response from ChatGPT
def ChatGPT_conversation(prompt):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

#Gets the text from the image and calls the ChatGPT function with the text as input
def submit_text():
    submitted_text = result_text.get(1.0, tk.END)
    response_text = ChatGPT_conversation(submitted_text)
    response.delete(1.0, tk.END)
    response.insert(tk.END, response_text)

# Create the main window
window = tk.Tk()
window.title("Chat GPT Image to Text Extractor")

# Configure the main window
window.configure(bg='#282c34')
window.geometry('800x800')

# Create and add widgets to the main window
header_frame = tk.Frame(window, bg='#282c34')
header_frame.pack(padx=10, pady=10)

title_label = tk.Label(header_frame, text="Chat GPT Image", font=("Arial", 24), fg='#61afef', bg='#282c34')
title_label.pack(pady=10)

browse_button = tk.Button(header_frame, text="Browse Image", command=browse_image, bg='#61afef', fg='black', width=15)
browse_button.pack(pady=10)

result_frame = tk.Frame(window, bg='#282c34')
result_frame.pack(padx=10, pady=10)

result_label = tk.Label(result_frame, text="Extracted Text", font=("Arial", 16), fg='#abb2bf', bg='#282c34')
result_label.pack(pady=10)

scrollbar1 = Scrollbar(result_frame)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, wrap=tk.WORD, width=80, height=20, bg='#3b4048', fg='#abb2bf', insertbackground='#61afef', yscrollcommand=scrollbar1.set)
result_text.pack(padx=10, pady=10)

scrollbar1.config(command=result_text.yview)

submit_button = tk.Button(result_frame, text="Submit", command=submit_text, bg='#61afef', fg='black', width=15)
submit_button.pack(pady=10)

response_frame = tk.Frame(window, bg='#282c34')
response_frame.pack(padx=10, pady=10)

response_label = tk.Label(response_frame, text="ChatGPT Response", font=("Arial", 16), fg='#abb2bf', bg='#282c34')
response_label.pack(pady=10)

scrollbar2 = Scrollbar(response_frame)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

response = tk.Text(response_frame, wrap=tk.WORD, width=80, height=20, bg='#3b4048', fg='#abb2bf', insertbackground='#61afef', yscrollcommand=scrollbar2.set)
response.pack(padx=10, pady=10)

scrollbar2.config(command=response.yview)

# Run the main loop
window.mainloop()
