import csv
import time
import pyttsx3
import speech_recognition as sr
import os
import datetime
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
           text = recognizer.recognize_google(audio)
           print(f"You said: {text}")
           return text.lower()
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        except sr.UnknownValueError:
            return None
def sr_error_handler():
    result = None
    while result is None:
        result = listen()
        if result is None:
            speak("Sorry, I didnot understand that !, Please repeat.")
    return result
def file_creation():
    if not os.path.exists('health_data.csv'):
        with open("health_data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'bp', 'heart_rate', 'oxygen_level', 'medication'])
def add_health_data():
    speak("Please say the name.")
    name = sr_error_handler()

    speak("Please say the heart rate.")
    heart_rate = sr_error_handler()

    speak("Please say the oxygen level.")
    oxygen_level = sr_error_handler()
    
    speak("Please say the blood pressure.")
    bp = sr_error_handler()

    speak("Any medication to be added? Yes or No.")
    medication = "None"
    if sr_error_handler() == "yes":
        speak("Please say the medication taken.")
        medication = sr_error_handler()

    if name and bp and heart_rate and oxygen_level and medication:
        with open("health_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, bp, heart_rate + ' bpm', oxygen_level + '%', medication])
        speak("Health data added successfully.")
    else:
        speak("Some inputs were not understood. Please try again.")
def view_health_data():
    try:
        with open("health_data.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            data_found = False
            for row in reader:
                data_found = True
                speak(" ".join(row))
            if not data_found:
                speak("No data is available in the file.")
    except FileNotFoundError:
        speak("No health data found.")
def read_rem():
    tasks = []
    with open('remainders.csv','r') as file:
        reader = csv.reader(file)
        for row in reader:
            task_name = row[0]
            reminder_time = datetime.datetime.strptime(row[1], '%d-%m-%Y %H:%M:%S')
            tasks.append((task_name, reminder_time))
    return tasks
def check_reminders(tasks):
    rep = 0
    while tasks:
        current_time = datetime.datetime.now()
        for task, reminder_time in tasks[:]:
            if current_time >= reminder_time:
                print(f"Reminder: It's time to take {task}!")
                tasks.remove((task, reminder_time))
                speak(f"Reminder: It's time to take{task}!")
                rep+=1
        time.sleep(10)
        if len(tasks) == 0: 
            speak("Todays medications are done ")
def main():
    file_creation()
    while True:
        speak("Please say a command: Add data, View data, or Exit.")
        command = sr_error_handler()
        if command:
            if "add" in command:
                add_health_data()
            elif "view" in command:
                view_health_data()
            elif "exit" in command:
                speak("Exiting the program.")
                break
            else:
                speak("Invalid command. Please try again.")               

if os.path.exists("reminders.csv"):
    tasks = read_rem()
    check_reminders(tasks)
speak("Do you want to add any data ? ")
user_input = sr_error_handler()

if "YES" in user_input.upper()  or "YUP" in user_input.upper() or "S" in user_input.upper():
     main()
else:
     check_reminders(read_rem())
