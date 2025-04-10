import requests
from bs4 import BeautifulSoup

class WebScraperX:
    def __init__(self):
        self.last_url = None
        self.last_html = None
        self.last_parsed = None

    def fetch(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.last_url = url
            self.last_html = response.text
            self.last_parsed = BeautifulSoup(response.text, "html.parser")
            return self.last_html
        except Exception as e:
            print(f"[HATA] Site alinamadi: {e}")
            return None

    def as_python(self):
        if self.last_parsed is None:
            print("[UYARI] Önce fetch() ile veri alin.")
            return None
        return self.last_parsed
