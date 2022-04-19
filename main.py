import tweepy
import requests
import ctypes
import time 
import os
import threading
import platform
from colorama import Fore

import random
import string

ascii_text = """
  ____             _       _   __  __          _ _         _   _                  ____ _               _             
 / ___|  ___   ___(_) __ _| | |  \/  | ___  __| (_) __ _  | | | |___  ___ _ __   / ___| |__   ___  ___| | _____ _ __ 
 \___ \ / _ \ / __| |/ _` | | | |\/| |/ _ \/ _` | |/ _` | | | | / __|/ _ \ '__| | |   | '_ \ / _ \/ __| |/ / _ \ '__|
  ___) | (_) | (__| | (_| | | | |  | |  __/ (_| | | (_| | | |_| \__ \  __/ |    | |___| | | |  __/ (__|   <  __/ |   
 |____/ \___/ \___|_|\__,_|_| |_|  |_|\___|\__,_|_|\__,_|  \___/|___/\___|_|     \____|_| |_|\___|\___|_|\_\___|_|                                                                                                                                                                                     
  """

if platform.system() == "Windows":
    clear = "cls"
else:
    clear = "clear"

website = "https://www.site.com/"

class userchecker:

    def __init__(self):
        self.lock = threading.Lock()
        self.checking = True
        self.usernames = []
        self.unavailable = 0
        self.available = 0
        self.counter = 0

    def update_title(self):
        remaining = len(self.usernames) - (self.available + self.unavailable)
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Social Media User Checker | Available: {self.available} | Unavailable: {self.unavailable} | Checked: {(self.available + self.unavailable)} | Remaining: {remaining} | @Krultu"
        )
    
    def safe_print(self, arg):
        self.lock.acquire()
        print(arg)
        self.lock.release()
    
    def print_console(self, status, arg, color = Fore.LIGHTMAGENTA_EX):
        self.safe_print(f"       {Fore.WHITE}[{color}{status}{Fore.WHITE}] {arg}")
    
    def check_username(self, username, ws):
        if username.isdigit():
            self.unavailable += 1
            self.print_console("Unavailable", username)
            return
        with requests.Session() as session:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "content-type": "application/json"
            }
            r = session.head(ws + username + "/", headers=headers)

            if r.status_code == 200:
                self.unavailable += 1
                self.print_console("Unavailable", username, Fore.RED)
            elif r.status_code == 404:
                self.available += 1
                self.print_console("MAYBE Available", username, Fore.GREEN)
                with open("Available.txt", "a") as f:
                        f.write(username + "\n")
            self.update_title()
 
    def load_usernames(self):
        if not os.path.exists("usernames.txt"):
            self.print_console("Console", "File usernames.txt not found")
            time.sleep(10)
            os._exit(0)
        with open("usernames.txt", "r", encoding = "UTF-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                self.usernames.append(line)
            if not len(self.usernames):
                self.print_console("Console", "No usernames loaded in proxies.txt")
                time.sleep(10)
                os._exit(0)

    
    def main(self):
        os.system(clear)

        try:
            os.remove("Available.txt")
        except:
            print()

        try:
            os.remove("usernames.txt")
        except:
            print()

        if clear == "cls":
            ctypes.windll.kernel32.SetConsoleTitleW("Social Media User Checker | @Krultu")
        print(Fore.LIGHTMAGENTA_EX + ascii_text)
        print(Fore.LIGHTMAGENTA_EX + "// Twitter: @kruitu | Discord: Krultu#6749")

        output_file = "usernames.txt"
        smoption = int(input("\n[CONSOLE] Choose a social media \n    1 - Tiktok \nOption: "))
        if smoption == 1:
            website = "https://www.tiktok.com/@"
        # elif smoption == 2:
        #     website = "https://twitter.com/"
        else:
            os._exit(0)
        amount = int(input("\n[CONSOLE] Amount of usernames: "))
        character_amount = int(input("\n[CONSOLE] Amount of characters per username: "))
        letteronly = int(input("\n[CONSOLE] Letter only [0,1]: "))


        for i in range(amount):
            if letteronly == 1:
                generated = ("").join(random.choices(string.ascii_letters, k = character_amount))
                with open(output_file, "a") as f:
                    f.write(generated + "\n")
            else:
                generated = ("").join(random.choices(string.ascii_letters + string.digits, k = character_amount))
                with open(output_file, "a") as f:
                    f.write(generated + "\n")
        
        self.load_usernames()
        threads = 5
        
        
        def thread_starter():
            self.check_username(self.usernames[self.counter], website)
        while self.checking:
            if threading.active_count() <= threads:
                try:
                    threading.Thread(target = thread_starter).start()
                    self.counter += 1
                except:
                    pass
                if len(self.usernames) <= self.counter:
                    self.checking = None

obj = userchecker()
obj.main()

try:
    os.remove("usernames.txt")
except:
    print()


try:
    os.startfile("Available.txt")
except:
    input()
       
