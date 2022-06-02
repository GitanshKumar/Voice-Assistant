import time
import keyboard
import tkinter as tk
from tkinter.font import Font
import threading
import assistant
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon
import sys
from plyer import notification


quited = False
path = "C:/Users/gitan/Desktop/Files/Programming/_Python/Projects/Voice Assistant/"

class Interface:
    
    def __init__(self) -> None:
        self.win = tk.Tk()
        self.win.iconphoto(False, tk.PhotoImage(file= (path + "icon.png")))
        self.win.geometry("420x320+1000+600")
        self.win.resizable(False, False)
        self.win.title("Nova")
        self.win.attributes("-topmost", True)
        self.win.protocol("WM_DELETE_WINDOW", self.terminate)

        self.font = Font(self.win, family= "Arial", size= 18)
        self.sfont = Font(self.win, family= "Arial", size= 10)
        self.stateLabel = tk.Label(self.win, text= "Initializing...", font= self.font, wraplength= 200, justify= "center", pady= 5)
        self.stateLabel.place(x = 100, y = 20)
        self.sub = tk.Label(self.win, text= "...", font= self.sfont, wraplength= 200, justify= "center", pady= 5)
        self.sub.place(x = 45, y = 100)
        self.said = tk.Label(self.win, text= "...", font= self.sfont, wraplength= 200, justify= "center", pady= 5)
        self.said.place(x = 220, y = 150)
    
    def updateState(self, text):
        self.stateLabel["text"] = text
    
    def setSub(self, text):
        self.sub["text"] = text
    
    def updateSaid(self, text):
        self.said["text"] = text
    
    def isopen(self):
        return self.win.state() == "normal"
    
    def terminate(self):
        self.win.destroy()

    def starttk(self):
        self.win.update()
        self.win.mainloop()


def notify(message, sec = 5):
    notification.notify(
        title = "Nova",
        message = message,
        app_icon = path + "icon.ico",
        timeout = sec
    )


def tray():
    global quited
    
    def quitt():
        global quited
        app.quit()
        quited = True

    app = QApplication(sys.argv)

    tray_icon = QSystemTrayIcon(QIcon(path + "icon.ico") , parent= app)
    tray_icon.setToolTip("Nova")
    tray_icon.show()

    menu = QMenu()

    exitAction = menu.addAction("Exit")
    exitAction.triggered.connect(quitt)

    tray_icon.setContextMenu(menu)

    sys.exit(app.exec_())

def createInter(temp: list):
    inter = Interface()
    temp.append(inter)
    inter.starttk()

def main():
    global quited
    temp = []
    while not quited:
        
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed("n") and keyboard.is_pressed("alt"):
            if temp != []:
                if not temp[-1].isopen():
                    print("---------------------------------")
                    continue
            threading.Timer(0, createInter, args= [temp]).start()
            time.sleep(0.1)
            nova = assistant.Assistant("Nova", "Gitansh", temp[-1])
            nova.speak("Hello " + nova.usr_name)
            while nova.run:
                said, succ = nova.get_audio()
                if succ == 1:
                    nova.understand(said.lower())
                else:
                    nova.speak("Sorry, i could not understand you, please repeat")
            
            temp[-1].updateState("Idle")
            temp[-1].setSub("...")
            temp[-1].updateSaid("...")

if __name__ == "__main__":
    notify("Service Started", 2)
    threading.Timer(0.1, main).start()
    tray()