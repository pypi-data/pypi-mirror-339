import os
import sys
import time
import requests
import datetime
import random
from threading import Thread
from itertools import cycle
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

class GmailGenerator:
    def __init__(self):
        self.console = Console()
        self.colors = {
            'blue': 'bright_cyan', 'red': 'red3', 
            'yellow': 'gold1', 'green': 'bright_green',
            'purple': 'bright_magenta'
        }
        self.loading = False
        self.email = None
        self.seen_messages = set()
        
    def _show_loading(self):
        frames = ["𝙻𝚘𝚍𝚒𝚗𝚐 .", "𝙻𝚘𝚍𝚒𝚗𝚐 ..", "𝙻𝚘𝚍𝚒𝚗𝚐 ..."]
        for frame in cycle(frames):
            if not self.loading:
                break
            self.console.print(frame, end="\r")
            time.sleep(0.5)
    
    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _get_ip(self):
        try:
            return requests.get('https://api64.ipify.org?format=text', timeout=5).text.strip()
        except:
            return ""
    
    def _get_current_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")
    
    def _get_current_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def _display_logo(self, email=None):
        ip = self._get_ip()
        current_time = self._get_current_time()
        current_date = self._get_current_date()
        
        logo = Text()
        logo.append("█▀▀ ", style=self.colors['blue'])
        logo.append("█▀▄▀█ ", style=self.colors['red'])
        logo.append("▄▀█ ", style=self.colors['yellow'])
        logo.append("█ ", style=self.colors['blue'])
        logo.append("█   ", style=self.colors['green'])
        logo.append("▄▄  ", style=self.colors['purple'])
        logo.append("▀█▀ ", style=self.colors['blue'])
        logo.append("█▄ █ ", style=self.colors['red'])
        logo.append("▀█▀\n", style=self.colors['green'])
        
        logo.append("█▄█ ", style=self.colors['blue'])
        logo.append("█ ▀ █ ", style=self.colors['red'])
        logo.append("█▀█ ", style=self.colors['yellow'])
        logo.append("█ ", style=self.colors['blue'])
        logo.append("█▄▄ ", style=self.colors['green'])
        logo.append("     ", style=self.colors['purple'])
        logo.append("█  ", style=self.colors['yellow'])
        logo.append("█ ▀█ ", style=self.colors['red'])
        logo.append("█", style=self.colors['green'])
        
        logo_panel = Panel.fit(logo, border_style="bright_green")
        
        info_text = Text()
        info_text.append(f"IP : {ip}\n", style=self._get_random_color())
        info_text.append(f"Time : {current_time}\n", style=self._get_random_color())
        info_text.append(f"Date : {current_date}", style=self._get_random_color())
        
        info_panel = Panel.fit(info_text, border_style="bright_green")
        
        if email:
            gmail_text = Text()
            gmail_text.append("G", style="bright_cyan")
            gmail_text.append("m", style="red3")
            gmail_text.append("a", style="gold1")
            gmail_text.append("i", style="bright_cyan")
            gmail_text.append("l", style="bright_green")
            gmail_text.append(f": {email}")
            
            email_panel = Panel(
                gmail_text,
                border_style="bright_green",
                width=len(f"Gmail : {email}") + 4,
                padding=(0, 1)
            )
            
            self.console.print(logo_panel, justify="center")
            self.console.print(info_panel, justify="center")
            self.console.print(email_panel, justify="center")
        else:
            self.console.print(logo_panel, justify="center")
            self.console.print(info_panel, justify="center")
    
    def _get_random_color(self):
        return random.choice(list(self.colors.values()))
    
    def _safe_request(self, url):
        try:
            response = requests.get(url, timeout=10)
            return response.json() if response.content else {}
        except:
            return {}
    
    def gen(self, random_gen=False):
        self.loading = True
        loading_thread = Thread(target=self._show_loading)
        loading_thread.start()
        
        try:
            data = self._safe_request("http://46.202.135.52:2002/Sawad-Gmail/v1/api/gen")
            if data and "email" in data:
                self.email = data["email"]
                while True:
                    msg_data = self._safe_request(f"http://46.202.135.52:2002/Sawad-Gmail/v1/api/message={self.email}")
                    if msg_data == {}:
                        break
                    else:
                        new_data = self._safe_request("http://46.202.135.52:2002/Sawad-Gmail/v1/api/gen")
                        if new_data and "email" in new_data:
                            self.email = new_data["email"]
            self.loading = False
            loading_thread.join()
            self._clear_screen()
            self._display_logo(self.email)
            self._check_messages()
        except Exception as e:
            self.loading = False
            loading_thread.join()
            self.console.print(f"[red]Error: {str(e)}[/]")
    
    def message(self, email):
        if email:
            self.email = email
            self._clear_screen()
            self._display_logo(self.email)
            self._check_messages()
    
    def _check_messages(self):
        while True:
            try:
                data = self._safe_request(f"http://46.202.135.52:2002/Sawad-Gmail/v1/api/message={self.email}")
                if data:
                    for key, message in data.items():
                        if isinstance(message, dict):
                            message_id = f"{message.get('from','')}-{message.get('subject','')}-{message.get('message','').split()[0] if message.get('message') else ''}"
                            if message_id not in self.seen_messages:
                                self.seen_messages.add(message_id)
                                self._display_message(message)
            except:
                pass
    
    def _display_message(self, message):
        current_date = self._get_current_date()
        color = self._get_random_color()
        table = Table(show_header=False, border_style="bright_green")
        table.add_column(style=color)
        table.add_column(style=color)
        table.add_row("From", message.get('from', ''))
        table.add_row("Subject", message.get('subject', ''))
        table.add_row("Message", message.get('message', ''))
        table.add_row("Time", message.get('time', ''))
        table.add_row("Date", current_date)
        self.console.print(Panel.fit(table, title="📧", border_style="bright_green"), justify="center")

gmail = GmailGenerator()