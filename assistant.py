import tkinter as tk
from tkinter import Label, Button, messagebox
from gtts import gTTS
from playsound import playsound
import os
import speech_recognition as sr
import time
import webbrowser
import requests
from itertools import cycle
from PIL import Image, ImageTk
import random

recognizer = sr.Recognizer()

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x400")

assistant_response = tk.StringVar()
assistant_response.set("Click 'Speak' to start")

colors = cycle(["red", "blue", "green", "purple"])

mic_icon = Image.open("microphone.jpg")  
mic_icon = mic_icon.resize((40, 40), Image.Resampling.LANCZOS)
mic_icon = ImageTk.PhotoImage(mic_icon)

jokes = [
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What did one ocean say to the other ocean? Nothing, they just waved."
]

def speak_animation(label):
    """Animate the label to indicate speaking."""
    current_color = next(colors)
    label.config(fg=current_color)
    root.update_idletasks()
    label.after(300, lambda: speak_animation(label))

def stop_animation(label):
    """Stop the speaking animation."""
    label.config(fg="black")
    root.update_idletasks()

def speak(text):
    """Convert text to speech using gTTS, play it, and show animation."""
    assistant_response.set(text)
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    
    # Start animation
    speak_animation(label)
    playsound(filename)
    stop_animation(label) 
    os.remove(filename)

def listen():
    """Listen to the user's input and convert it to text."""
    try:
        with sr.Microphone() as source:
            assistant_response.set("Listening...")
            root.update_idletasks()
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Request error. Check your internet connection."

def open_application(command):
    """Open a specified application or website."""
    if "browser" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening your browser")
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "notepad" in command:
        os.system("notepad")
        speak("Opening Notepad")

def get_weather():
    """Fetch the weather using an API."""
    api_key = "6ee4d000daadc89e30d210a9d1a6e1ec"
    city = "Rawalpindi"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            weather = response["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp}°C with {weather}.")
        else:
            speak(f"Sorry, I couldn't fetch the weather for {city}. Error: {response['message']}")
    except Exception as e:
        speak("An error occurred while fetching the weather.")

def tell_joke():
    """Tell a random joke."""
    joke = random.choice(jokes)
    speak(joke)

def process_command():
    """Handle commands given by the user and respond."""
    command = listen()
    assistant_response.set(f"You said: {command}")
    root.update_idletasks()
    
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "weather" in command:
        get_weather()
    elif "open" in command:
        open_application(command)
    elif "joke" in command:
        tell_joke()  # Call joke function when the user asks for a joke
    elif "stop" in command:
        speak("Goodbye!")
        root.quit()
    else:
        speak("Sorry, I didn't understand that command.")

# GUI Elements
label = Label(root, textvariable=assistant_response, font=("Helvetica", 14), wraplength=800)
label.pack(pady=50)

# Add a microphone icon
mic_label = Label(root, image=mic_icon)
mic_label.pack(pady=10)

speak_button = Button(root, text="Speak", command=process_command, font=("Sans Serif", 12))
speak_button.pack(pady=40)

root.mainloop()