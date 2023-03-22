from bs4 import BeautifulSoup
import requests
import pandas as pd

class TransferScraper():

    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    def find_player_detail(self):

        all_players = []
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
                all_players.append(cols)

        final_players = [all_players[i] for i in range(len(all_players)) if i % 3 == 0]

        return final_players

    def find_badges(self):
    
        badge_list = []
        for pagenum in range(1, 5):
            URL = "https://www.transfermarkt.co.uk/premier-league/marktwerte/wettbewerb/GB1/page/" + str(pagenum)
            r = requests.get(url=URL, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find("table", class_='items')
            tbody = table.find("tbody")
            #rows = tbody.find_all("tr")
            badges = soup.find_all("td", class_="zentriert")
            for badge in badges:
                flags = badge.find_all('img')  
                if flags:  
                    first_flag = flags[0]  
                    first_badge = first_flag['title']
                    badge_list.append(first_badge)

        indexes_to_delete = [219, 218, 217, 216, 215, 164, 163, 162, 161, 160, 109, 108, 107, 106, 105, 54, 53, 52, 51, 50]
        for index in indexes_to_delete:
            del badge_list[index]

        nationality_list = [badge_list[i] for i in range(len(badge_list)) if i % 2 == 0]
        club_list = [badge_list[i] for i in range(len(badge_list)) if i % 2 == 1]

        return nationality_list, club_list
                    
    def create_pd(self, final_players, nationality_list, club_list):
    
        df = pd.DataFrame(final_players, columns=['Rank', 'null', 'null1', 'Player', 'Position', 'null3', 'Age', 'null4', 'Value'])

        df['Nationality'] = nationality_list

        df['Club'] = club_list
                

        