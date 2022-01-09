import os
import webbrowser
import threading
from wikipedia import summary

open_dict = {"chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "vscode": "C:/Users/gitan/AppData/Local/Programs/Microsoft VS Code/Code.exe",
            "whatsapp":"C:/Users/gitan/AppData/Local/WhatsApp/WhatsApp.exe",
            "blender":"C:/Program Files/Blender Foundation/Blender 2.93/blender.exe",
            "opera":"C:/Program Files/Opera/launcher.exe",
            "exlporer":"explorer",
            "notepad":"notepad",
            "msword":"C:/Program Files/Microsoft Office/root/Office16/WINWORD.exe",
            "msteams": "C:/Users/gitan/AppData/Local/Microsoft/Teams/Update.exe",
            "bin":"start shell:RecycleBinFolder",
            "obs":"C:/Program Files/obs-studio/bin/64bit/obs64.exe",
            "telegram": "C:/Users/gitan/AppData/Roaming/Telegram Desktop/Telegram.exe",
            "codeblocks":"C:/Program Files/CodeBlocks/codeblocks.exe",
            "skype":"skype",
            "youtube":"https://youtube.com",
            "wikipedia":"https://wikipedia.com"}

chrome = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
opera = "C:/Program Files/Opera/launcher.exe %s"

google = "https://google.com/search?q=%s"
bing = "https://bing.com/search?q=%s"
yahoo = "https://in.search.yahoo.com/search;?p=%s"

def websearch(query:str, browser_n:str, engine:str) -> None:
    """
    Search on web on given browser and search engine
    arguments:
    query -> To search on web
    browser_n -> browers name to search on
    engine -> search with given search engine
    """
    browser = webbrowser.get(browser_n)
    threading.Timer(0.2, browser.open_new_tab, args= [engine%query])
    

def get_info(query: str) -> str:
    """
    To get a summary of a given topic
    """
    sumry = "None"
    try:
        sumry = summary("(" + query + ")", sentences = 2)
    except Exception as e:
        print("Exception: ", e)

    return sumry

def open(query_name:str, browser = chrome) -> bool:
    try:
        to_open = open_dict[query_name]
    except KeyError:
        return 0
    if "https" in to_open:
        webbrowser.get(browser).open_new_tab(url= to_open)
    else:
        os.startfile(to_open)
    return 1

def close(app_name:str) -> bool:
    os.system("TASKKILL /F /IM " + app_name + ".exe")

if __name__ == "__main__":
    open("chrome")