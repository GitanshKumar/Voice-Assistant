from os import remove
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import lookUp               ###### To act on tasks

######         NAMES         ######
usr_name = "gitansh"
assistant_name = "nova"

######         BROWSERS         ######
chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
opera = "C:/Program Files/Opera/launcher.exe %s"

######         SEARCH ENGINES         ######
google = "https://google.com/search?q=%s"
bing = "https://bing.com/search?q=%s"
yahoo = "https://in.search.yahoo.com/search;?p=%s"
youtube = "https://www.youtube.com/results?search_query=%s"

def speak(text):
    """
    Respond by speaking
    arguments: text:str -> Text to speak
    """
    tts = gTTS(text= text, lang= "en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound(filename)
    remove(filename)

def get_audio() -> str:
    """
    Take audio input from the user
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 4000
        audio = r.listen(source)

    try:
        print("Recognizing...")
        said = r.recognize_google(audio_data= audio, language="en-in", show_all= True)
    except Exception as e:
            print("Exception: ", e)
            raise 
    return said['alternative'][0]['transcript']         ######used to face an error


speak("Hello")
can_srch = False

######         Keep listening until termination         ######
while True:
    if can_srch:
        speak("Do you want to know more about " + sub_task)
        can_srch = False
    
    said = get_audio().lower()
    commands = said.split("and")

    if "yes" in said or "do it" in said:
        lookUp.websearch(sub_task, browser, engine)
    
    browser = chrome
    engine = google
    
    for com in commands:
        to_speak = ""
        srch = False
        opn = False

        if ("hello " + assistant_name) in com or ("hi " + assistant_name) in com:
            to_speak += " hi " + usr_name
        
        if "what is the" in com:
            task = com[com.find("what is the") + len("what is the "):].strip()
            
            if "time" in task:
                to_speak += " " + str(datetime.today().strftime("%I:%M %p"))
            elif "meaning of" in task or "meaning" in task:
                if task.find("meaning of") == -1:
                    sub_task = task[task.find("meaning") + len("meaning "):].strip()
                else:
                    sub_task = task[task.find("meaning of") + len("meaning of "):].strip()
                to_speak += " " + lookUp.get_info(sub_task)
                can_srch = True
            else:
                query_srch = task
                to_speak += " this is what i found on the internet"
                srch = True
        
        elif "tell me the" in com:
            task = com[com.find("tell me the") + len("tell me the "):].strip()
            if "time" in task:
                to_speak += " it is " + str(datetime.today().strftime("%I:%M %p"))
            elif "meaning of" in task or "meaning" in task:
                if task.find("meaning of") == -1:
                    sub_task = task[task.find("meaning") + len("meaning "):].strip()
                else:
                    sub_task = task[task.find("meaning of") + len("meaning of "):].strip()
                to_speak += " " + lookUp.get_info(sub_task)
                can_srch = True
            else:
                query_srch = task
                to_speak += " this is what i found on the internet"
        
        elif "what is" in com:
            ind = com.find("what is") + len("what is ")
            task = com[ind:]
            
            if "your name" in task:
                to_speak += " my name is " + assistant_name
            else:
                to_speak += " " + lookUp.get_info(task)
        
        if "who is" in com:
            person = com[com.find("who is") + len("who is "):].strip()
            to_speak += " " + person + " " + lookUp.get_info(person)
        
        if "search" in com:
            query_srch = com[com.find("search") + len("search "):]
            query_srch_split = query_srch.split()
            temp = " google"
            if "on" in query_srch_split:
                ind = query_srch_split.index("on")
                if query_srch_split[ind + 1] == "google":
                    engine = google
                    temp = " google"
                    query_srch = query_srch.replace("on", "").replace("google", "").strip()
                elif query_srch_split[ind + 1] == "bing":
                    engine = bing
                    temp = " bing"
                    query_srch = query_srch.replace("on", "").replace("bing", "").strip()
                elif query_srch_split[ind + 1] == "yahoo":
                    engine = yahoo
                    temp = " yahoo"
                    query_srch = query_srch.replace("on", "").replace("yahoo", "").strip()
                elif query_srch_split[ind + 1] == "youtube":
                    engine = youtube
                    temp = " youtube"
                    query_srch = query_srch.replace("on", "").replace("youtube", "").strip()
                else:
                    to_speak += " sorry cannot search on told site"
            to_speak += " searching " + query_srch + " on " + temp
            srch = True
        
        if "open" in com:
            query = com[com.find("open") + len("open "):].strip()
            to_speak += " opening " + query
            opn = True
        
        if "who is" in com:
            query = com[com.find("who is") + len("who is "):].strip()
            to_speak += " " + lookUp.get_info(query)
        
        speak(to_speak)
        if srch:
            lookUp.websearch(query_srch, browser, engine)
        if opn:
            lookUp.open(query)
        
        if "close" in com or "goodbye" in com or "bye" in com or "good bye" in com:
            speak("Goodbye " + usr_name + " have a nice day")
            break