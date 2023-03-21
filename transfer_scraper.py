from bs4 import BeautifulSoup
import requests

class TransferScraper():

    def __init__(self, URL: str = 'https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1'):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        r = requests.get(url=URL, headers=headers)
        self.soup = BeautifulSoup(r.content, 'html.parser')

    def find_player_detail(self):
        players_list = []
        age = []
        position = []
        value = []
        nationality = []

        players = self.soup.find_all("td", class_="hauptlink")

        for player in players:
            players_list.append(player.text)