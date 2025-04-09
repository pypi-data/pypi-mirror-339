from tls_client import Session
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from typing import Optional
class Logger:
    def __init__(self):
        init()
    @staticmethod
    def succ(msg):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{current_time}]{Fore.RESET} {Fore.LIGHTGREEN_EX}[+]{Fore.RESET} {msg}")
    @staticmethod
    def err(msg):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{current_time}]{Fore.RESET} {Fore.RED}[-]{Fore.RESET} {msg}")
    @staticmethod
    def warn(msg):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{current_time}]{Fore.RESET} {Fore.YELLOW}[!]{Fore.RESET} {msg}")
    @staticmethod
    def info(msg):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.LIGHTBLACK_EX}[{current_time}]{Fore.RESET} {Fore.MAGENTA}[/]{Fore.RESET} {msg}")

class Client:
    def __init__(self):
        self.session = Session(client_identifier="chrome_112", random_tls_extension_order=True)
        self.session.headers = {
    "accept": "application/json",
    "accept-language": "en-GB,en;q=0.8",
    "cache-control": "max-age=0",
    "cluster": "v2",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Not:A-Brand\";v=\"24\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version-list": "\"Chromium\";v=\"112.0.0.0\", \"Not:A-Brand\";v=\"24.0.0.0\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"10.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
    def get_emotes(self, username: str):
        while True:
            r = self.session.get(f"https://kick.com/emotes/{username}")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_leadboard(self, username: str):
        while True:
            r = self.session.get(f"https://kick.com/api/v2/channels/{username}/leaderboards")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_messages(self, user_id: int):
        while True:
            r = self.session.get(f"https://kick.com/api/v2/channels/{user_id}/messages")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_current_poll(self, username: str):
        while True:
            r = self.session.get(f"https://kick.com/api/v2/channels/{username}/polls")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_top_category(self):
        while True:
            r = self.session.get("https://kick.com/api/v1/categories/top")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_featured_streams(self, page: Optional[int] = 1):
        while True:
            r = self.session.get(f"https://kick.com/stream/livestreams/en?page={page}")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_channel(self, username: str):
        while True:
            r = self.session.get(f"https://kick.com/api/v2/channels/{username}/")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def get_chatroom(self, username: str):
        while True:
            r = self.session.get(f"https://kick.com/api/v2/channels/{username}/chatroom")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")

    def get_rules(self, username: str):
        while True:
            r = self.session.get(f"https://kick.com/api/v2/channels/{username}/chatroom/rules")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
    def send_chat(self, user_id: int, token: str, content: str):
        while True:
            self.session.headers.update({
                "authorization": "Bearer " + token
            })
            json = {
                "content": content,
                "type": "message"
            }
            r = self.session.post(f"https://kick.com/api/v2/messages/send/{user_id}", json=json)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                print(r.status_code, r.text)
    def get_clips(self):
        while True:
            r = self.session.get("https://kick.com/api/v2/clips")
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 403:
                Logger.warn("cloudflared retrying.")
                time.sleep(2)
            else:
                Logger.error(f"Uknown error {Fore.LIGHTBLACK_EX}({r.status_code}){Fore.RESET}")
