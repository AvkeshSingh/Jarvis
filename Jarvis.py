import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import pyjokes
import random
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

# Email list
email_list = {
    "harsh": "234harshsingh@gmail.com",
    "john": "john@example.com",
    "jane": "jane@example.com"
}

def emailToRecipient():
    speak("Which email address would you like to send an email to?")
    for name in email_list.keys():
        speak(name)

    recipient_name = takeCommand().lower()
    if recipient_name in email_list:
        to = email_list[recipient_name]
        speak("What should I say?")
        content = takeCommand()
        sendEmail(to, content)
        speak("Email has been sent!")
    else:
        speak("Sorry, I couldn't find that email address.")

# Weather Feature
def getWeather(city):
    api_key = "your_openweathermap_api_key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        weather = data["main"]
        temperature = weather["temp"]
        description = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("City not found, please try again.")

# News Feature
def getNews():
    api_key = "your_newsapi_key"
    news_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(news_url)
    articles = response.json()["articles"]
    speak("Here are the top headlines.")
    for article in articles[:5]:
        speak(article["title"])

# Task Management
tasks = []

def addTask():
    speak("What task would you like to add?")
    task = takeCommand()
    tasks.append(task)
    speak(f"Task '{task}' added to your list.")

def showTasks():
    if tasks:
        speak("Here are your tasks.")
        for task in tasks:
            speak(task)
    else:
        speak("You have no tasks.")

# Fun Feature: Jokes and Facts
def tellJoke():
    joke = pyjokes.get_joke()
    speak(joke)

def funFact():
    facts = ["Honey never spoils.", "Bananas are berries, but strawberries are not.", "A day on Venus is longer than a year."]
    speak(random.choice(facts))

# System Control
def systemControl(command):
    if 'shutdown' in command:
        os.system("shutdown /s /t 1")
    elif 'restart' in command:
        os.system("shutdown /r /t 1")
    elif 'log off' in command:
        os.system("shutdown -l")

# Browser Search
def searchGoogle(query):
    speak('Searching Google...')
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Alarms
def setAlarm(alarm_time):
    speak(f"Alarm set for {alarm_time}.")
    while True:
        current_time = time.strftime("%H:%M:%S")
        if current_time == alarm_time:
            speak("Time to wake up!")
            break

# Calculator
def calculator(command):
    try:
        command = command.replace("calculate", "").strip()
        result = eval(command)
        speak(f"The result is {result}.")
    except:
        speak("Sorry, I couldn't calculate that.")

# Main Loop
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\234ha\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email' in query:
            emailToRecipient()

        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city = takeCommand()
            getWeather(city)

        elif 'news' in query:
            getNews()

        elif 'add task' in query:
            addTask()

        elif 'show tasks' in query:
            showTasks()

        elif 'tell me a joke' in query:
            tellJoke()

        elif 'fun fact' in query:
            funFact()

        elif 'shutdown' in query or 'restart' in query or 'log off' in query:
            systemControl(query)

        elif 'search google' in query:
            query = query.replace("search google for", "")
            searchGoogle(query)

        elif 'set alarm' in query:
            speak("What time should I set the alarm for?")
            alarm_time = takeCommand()
            setAlarm(alarm_time)

        elif 'calculate' in query:
            calculator(query)
