from bs4 import BeautifulSoup
import requests

class TransferScraper():

    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    def find_player_detail(self):
        for pagenum in range(1, 5):
            URL = "https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1/page/" + str(pagenum)
            r = requests.get(url=URL, headers=self.headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find("table", class_='items')
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")

            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols]
                print(cols)

        