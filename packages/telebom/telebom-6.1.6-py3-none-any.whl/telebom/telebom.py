import requests
import threading
import sys
from rich.console import Console
from rich.panel import Panel

class ReactionTelegram:
    def __init__(self, link):
        self.link = link
        self.while_loop = False
        self.thread_count = 1
        self.base_url = "http://185.158.132.66:2001/telegram-r/link="
        self.console = Console()
        if sys.platform == 'win32':
            from colorama import init
            init()

    def __getitem__(self, key):
        if key == 'while=True':
            self.while_loop = True
            return self
        elif key.startswith('threading='):
            self.thread_count = int(key.split('=')[1])
            return self
        return self

    def print_result(self, success, url):
        color = "green" if success else "red"
        status = "✓ - SUCCESS" if success else "✗ - ERROR"
        self.console.print(Panel.fit(f"[bold]URL:[/] {url}\n[bold]Status:[/] [{color}]{status}[/]",
                              title="[bold]Telegram-Reaction[/]",
                              border_style=color,
                              padding=(1, 2)))

    def send_request(self, url):
        try:
            response = requests.get(self.base_url + url, timeout=10)
            if "done" in response.text:
                self.print_result(True, url)
                return True
            self.print_result(False, url)
            return False
        except Exception:
            self.print_result(False, url)
            return False

    def process_url(self, url):
        if self.while_loop:
            while True:
                self.send_request(url)
        else:
            self.send_request(url)

    @property
    def start(self):
        if isinstance(self.link, str):
            if self.thread_count > 1:
                threads = []
                for _ in range(self.thread_count):
                    t = threading.Thread(target=self.process_url, args=(self.link,))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
            else:
                self.process_url(self.link)
        elif isinstance(self.link, list):
            if self.thread_count > 1:
                while True:
                    threads = []
                    for url in self.link:
                        for _ in range(self.thread_count):
                            t = threading.Thread(target=self.send_request, args=(url,))
                            threads.append(t)
                            t.start()
                    for t in threads:
                        t.join()
                    if not self.while_loop:
                        break
            else:
                while True:
                    for url in self.link:
                        self.send_request(url)
                    if not self.while_loop:
                        break

reaction = ReactionTelegram