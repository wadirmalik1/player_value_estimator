from bs4 import BeautifulSoup
import requests

class TransferScraper():

    def __init__(self, URL: str = 'https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1'):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        r = requests.get(url=URL, headers=headers)
        self.soup = BeautifulSoup(r.content, 'html.parser')

    def find_player_detail(self):
        players_list = []
        age_list = []
        value_list = []
        nationality_list = []

        players = self.soup.find_all("td", class_="hauptlink")
        ages = self.soup.find_all("td", class_="zentriert")
        nationality = self.soup.find_all("td", class_="zentriert")
        values = self.soup.find_all("td", class_="rechts hauptlink")

        for player in players:
            players_list.append(player.text)

        i = 1
        while i < len(players_list):
            del players_list[i]
            i += 1

        for age in ages:
            age_list.append(age.text)

        new_age_list = []
        for i in range(2, len(age_list), 4):
            new_age_list.append(age_list[i])

        for nation in nationality:
            flags = nation.find_all('img')  
            if flags:  
                first_flag = flags[0]  
                first_nationality = first_flag['title']
                nationality_list.append(first_nationality)

        i = 1
        while i < len(nationality_list):
            del nationality_list[i]
            i += 1   

        for value in values:
            value_list.append(value.text)    
        