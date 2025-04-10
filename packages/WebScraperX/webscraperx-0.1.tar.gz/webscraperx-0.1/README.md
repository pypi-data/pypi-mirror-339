# WebScraperX

Web sayfasını alır ve Python üzerinden HTML içeriğine erişmeni sağlar.

## Kurulum

```bash
pip install WebScraperX
```

## Kullanım

```python
from WebScraperX import WebScraperX

scraper = WebScraperX()
html = scraper.fetch("https://example.com")

print(html)  # tüm HTML içeriği

soup = scraper.as_python()
print(soup.title.text)  # sayfanın başlığı
```
