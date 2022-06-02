from playsound import playsound
import speech_recognition as sr
from gtts import gTTS, gTTSError
from datetime import datetime
import lookUp               ###### To act on tasks


class Assistant:
    def __init__(self, assistant_name, usr_name, interface) -> None:
        self.name = assistant_name
        self.usr_name = usr_name
        self.interface = interface
        self.state = -1
        self.can_srch = False
        self.run = True
        self.to_speak = ""
        self.chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe %s &"
        self.opera = "C:/Program Files/Opera/launcher.exe %s &"
        self.google = "https://google.com/search?q=%s"
        self.bing = "https://bing.com/search?q=%s"
        self.yahoo = "https://in.search.yahoo.com/search;?p=%s"
        self.youtube = "https://www.youtube.com/results?search_query=%s"
    
    def speak(self, text) -> str:
        """
        Respond by speaking
        arguments: text:str -> Text to speak
        """
        try:
            self.interface.updateState("Speaking...")
            tts = gTTS(text= text, lang= "en")
            filename = lookUp.os.getcwd() + "/Voice Assistant/Temp Voice/Voice.mp3"
            tts.save(filename)
            self.interface.setSub(text)
            playsound(filename)
            lookUp.os.remove(filename)
        except gTTSError:
            file = lookUp.os.getcwd() + "/Voice Assistant/Errors in Voice/Network Error.mp3"
            playsound(file)
    
    def get_audio(self) -> str:
        """
        Take audio input from the user
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.interface.updateState("Listening...")
            r.energy_threshold = 4000
            audio = r.listen(source)

        try:
            self.interface.updateState("Recognizing...")
            said = r.recognize_google(audio_data= audio, language="en-in", show_all= True)
        except Exception as e:
                print("Exception: ", e)
                raise 
        try:
            return said['alternative'][0]['transcript'], 1         ######used to face an error
        except TypeError:
            return "", 0
    
    def understand(self, said: str):
        self.interface.updateState("Working...")
        self.interface.updateSaid(said)
        commands = said.split("and")
        
        browser = self.chrome
        engine = self.google
        
        for com in commands:
            self.to_speak = ""
            srch = False
            opn = False

            if ("hello " + self.name) in com or ("hi " + self.name) in com:
                self.to_speak += " hi " + self.usr_name
            
            if "what is the" in com:
                task = com[com.find("what is the") + len("what is the "):].strip()
                
                if "time" in task:
                    self.to_speak += " " + str(datetime.today().strftime("%I:%M %p"))
                elif "meaning of" in task or "meaning" in task:
                    if task.find("meaning of") == -1:
                        sub_task = task[task.find("meaning") + len("meaning "):].strip()
                    else:
                        sub_task = task[task.find("meaning of") + len("meaning of "):].strip()
                    self.to_speak += " " + lookUp.get_info(sub_task)
                    can_srch = True
                else:
                    query_srch = task
                    self.to_speak += " this is what i found on the internet"
                    srch = True
            
            elif "tell me the" in com:
                task = com[com.find("tell me the") + len("tell me the "):].strip()
                if "time" in task:
                    self.to_speak += " it is " + str(datetime.today().strftime("%I:%M %p"))
                elif "meaning of" in task or "meaning" in task:
                    if task.find("meaning of") == -1:
                        sub_task = task[task.find("meaning") + len("meaning "):].strip()
                    else:
                        sub_task = task[task.find("meaning of") + len("meaning of "):].strip()
                    self.to_speak += " " + lookUp.get_info(sub_task)
                    can_srch = True
                else:
                    query_srch = task
                    self.to_speak += " this is what i found on the internet"
            
            elif "what is" in com:
                ind = com.find("what is") + len("what is ")
                task = com[ind:]
                
                if "your name" in task:
                    self.to_speak += " my name is " + self.name
                else:
                    self.to_speak += " " + lookUp.get_info(task)
            
            if "who is" in com:
                person = com[com.find("who is") + len("who is "):].strip()
                self.to_speak += " " + lookUp.get_info(person)
            
            if "search" in com:
                query_srch = com[com.find("search") + len("search "):]
                query_srch_split = query_srch.split()
                temp = " google"
                if "on" in query_srch_split:
                    ind = query_srch_split.index("on")
                    if query_srch_split[ind + 1] == "google":
                        engine = self.google
                        temp = " google"
                        query_srch = query_srch.replace("on", "").replace("google", "").strip()
                    elif query_srch_split[ind + 1] == "bing":
                        engine = self.bing
                        temp = " bing"
                        query_srch = query_srch.replace("on", "").replace("bing", "").strip()
                    elif query_srch_split[ind + 1] == "yahoo":
                        engine = self.yahoo
                        temp = " yahoo"
                        query_srch = query_srch.replace("on", "").replace("yahoo", "").strip()
                    elif query_srch_split[ind + 1] == "youtube":
                        engine = self.youtube
                        temp = " youtube"
                        query_srch = query_srch.replace("on", "", 1).replace("youtube", "").strip()
                    else:
                        self.to_speak += " sorry cannot search on told site"
                self.to_speak += " searching " + query_srch + " on " + temp
                srch = True
            
            if "open" in com:
                query = com[com.find("open") + len("open "):].strip()
                self.to_speak += "Trying to open " + query
                opn = True
            
            if "goodbye" in com or "bye" in com or "good bye" in com:
                self.to_speak += "Goodbye " + self.usr_name + " have a nice day"
                self.run = False

            try:
                self.speak(self.to_speak)
            except AssertionError:
                self.speak("Sorry, i could not understand you, please repeat")
            
            if srch:
                lookUp.websearch(query_srch, browser, engine)
            if opn:
                if lookUp.open(query):
                    self.speak("successfully opened")
                else:
                    self.speak("Could not find" + query)
            
        if self.can_srch:
            self.speak("Do you want to search about " + sub_task)
        if "yes" in said or "do it" in said and self.can_srch:
            lookUp.websearch(sub_task, browser, engine)
            self.can_srch = False